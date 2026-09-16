# -*- coding: utf-8 -*-
"""NB02B: validacion analitica de la arquitectura modal usada por NB03.

El experimento conserva la arquitectura ``ModalSiren`` de NB03 y sustituye la
pantalla aleatoria por una superposicion de ondas planas cuya solucion exacta
es conocida. De esta forma se pueden separar los errores de arquitectura de
los asociados al espectro aleatorio del speckle.

No se emplean etiquetas interiores durante el entrenamiento. La solucion
analitica se reserva exclusivamente para la evaluacion posterior.
"""

from __future__ import annotations

import copy
import json
import os
from pathlib import Path
import sys
import time

import numpy as np

os.environ.setdefault("MPLBACKEND", "Agg")

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

import torch
from torch.func import jvp

from scripts.experiments import nb03_modal_pinn_siren as nb03


K = 2.0 * np.pi
WIDTH_LAMBDA = float(os.environ.get("NB02B_WIDTH_LAMBDA", 20.0))
DISTANCE_LAMBDA = float(os.environ.get("NB02B_DISTANCE_LAMBDA", 1.0))
SEED = int(os.environ.get("NB02B_SEED", 2026))
EPOCHS = int(os.environ.get("NB02B_EPOCHS", 2500))
N_Z_TRAIN = int(os.environ.get("NB02B_N_Z_TRAIN", 256))
N_Z_EVAL = int(os.environ.get("NB02B_N_Z_EVAL", 301))
N_X_EVAL = int(os.environ.get("NB02B_N_X_EVAL", 512))
LEARNING_RATE = float(os.environ.get("NB02B_LR", 2e-4))
GRAD_CLIP = float(os.environ.get("NB02B_GRAD_CLIP", 1.0))
OPTIMIZER_NAME = os.environ.get("NB02B_OPTIMIZER", "adam").strip().lower()
LBFGS_INNER_ITER = int(os.environ.get("NB02B_LBFGS_INNER_ITER", 20))
CASE_COUNTS = tuple(
    int(value.strip())
    for value in os.environ.get("NB02B_CASE_COUNTS", "1,5,41").split(",")
    if value.strip()
)
OUTPUT_DIR = PROJECT_ROOT / "results" / "nb02b_modal_bridge"
RESUME_EXISTING = os.environ.get("NB02B_RESUME_EXISTING", "0") == "1"


def set_seed(seed: int) -> None:
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def symmetric_mode_indices(count: int) -> np.ndarray:
    """Return an odd number of Fourier indices symmetric around zero."""
    if count < 1 or count % 2 == 0:
        raise ValueError("Cada caso debe usar un numero impar positivo de modos.")
    half = count // 2
    indices = np.arange(-half, half + 1, dtype=int)
    maximum_propagating_index = int(round(WIDTH_LAMBDA))
    if np.max(np.abs(indices)) > maximum_propagating_index:
        raise ValueError(
            f"{count} modos exceden el intervalo propagante para "
            f"L={WIDTH_LAMBDA:g} lambda."
        )
    return indices


def make_initial_modes(count: int) -> dict[str, np.ndarray]:
    """Build deterministic complex amplitudes and outgoing derivatives."""
    indices = symmetric_mode_indices(count)
    kx = 2.0 * np.pi * indices / WIDTH_LAMBDA
    kz_squared = np.maximum(K**2 - kx**2, 0.0)
    kz = np.sqrt(kz_squared)

    if count == 1:
        amplitudes = np.ones(1, dtype=np.complex128)
    else:
        rng = np.random.RandomState(SEED + count)
        sigma = max(float(np.max(np.abs(indices))) / 2.5, 1.0)
        envelope = np.exp(-0.5 * (indices / sigma) ** 2)
        phases = rng.uniform(-np.pi, np.pi, count)
        amplitudes = envelope * np.exp(1j * phases)
        amplitudes /= np.sqrt(np.sum(np.abs(amplitudes) ** 2))

    derivatives = 1j * kz * amplitudes
    return {
        "indices": indices,
        "kx": kx,
        "kz": kz,
        "kz_squared": kz_squared,
        "amplitudes": amplitudes,
        "derivatives": derivatives,
    }


def complex_to_real_channels(values: np.ndarray) -> np.ndarray:
    return np.column_stack((values.real, values.imag)).astype(np.float32).reshape(-1)


def channels_to_complex(values: np.ndarray) -> np.ndarray:
    values = np.asarray(values)
    return values[..., 0] + 1j * values[..., 1]


def relative_l2(prediction: np.ndarray, reference: np.ndarray) -> float:
    denominator = np.linalg.norm(reference.ravel())
    if denominator == 0:
        return float("nan")
    return float(np.linalg.norm((prediction - reference).ravel()) / denominator)


def coherence(prediction: np.ndarray, reference: np.ndarray) -> float:
    prediction_flat = prediction.ravel()
    reference_flat = reference.ravel()
    denominator = (
        np.linalg.norm(prediction_flat) * np.linalg.norm(reference_flat)
    )
    if denominator == 0:
        return float("nan")
    return float(abs(np.vdot(reference_flat, prediction_flat)) / denominator)


def circular_phase_mae(prediction: np.ndarray, reference: np.ndarray) -> float:
    difference = np.angle(prediction * np.conj(reference))
    return float(np.mean(np.abs(difference)))


def reconstruct_field(
    coefficients: np.ndarray, x: np.ndarray, kx: np.ndarray
) -> np.ndarray:
    phase = np.exp(1j * np.outer(x, kx))
    return coefficients @ phase.T


def exact_coefficients(
    z: np.ndarray, amplitudes: np.ndarray, kz: np.ndarray
) -> np.ndarray:
    return amplitudes.reshape(1, -1) * np.exp(
        1j * np.outer(z, kz)
    )


def evaluate_case(
    model: torch.nn.Module,
    mode_data: dict[str, np.ndarray],
    device: torch.device,
) -> tuple[dict, dict[str, np.ndarray]]:
    x = np.linspace(
        -WIDTH_LAMBDA / 2.0,
        WIDTH_LAMBDA / 2.0,
        N_X_EVAL,
        endpoint=False,
    )
    z = np.linspace(0.0, DISTANCE_LAMBDA, N_Z_EVAL)
    z_tensor = torch.tensor(z, dtype=torch.float32, device=device).reshape(-1, 1)
    kz_squared_tensor = torch.tensor(
        mode_data["kz_squared"], dtype=torch.float32, device=device
    )

    with torch.no_grad():
        coefficient_channels = model(z_tensor).cpu().numpy().reshape(
            N_Z_EVAL, -1, 2
        )
    coefficient_prediction = channels_to_complex(coefficient_channels)
    coefficient_reference = exact_coefficients(
        z, mode_data["amplitudes"], mode_data["kz"]
    )
    field_prediction = reconstruct_field(
        coefficient_prediction, x, mode_data["kx"]
    )
    field_reference = reconstruct_field(
        coefficient_reference, x, mode_data["kx"]
    )

    residual_channels = nb03.modal_residual(
        model, z_tensor, kz_squared_tensor
    ).detach().cpu().numpy()
    residual_complex = channels_to_complex(residual_channels)
    residual_field = reconstruct_field(
        residual_complex, x, mode_data["kx"]
    )
    field_scale = K**2 * np.sqrt(np.mean(np.abs(field_reference) ** 2))

    zero = torch.zeros((1, 1), dtype=torch.float32, device=device)
    tangent = torch.ones_like(zero)
    coefficient_zero, derivative_zero = jvp(model, (zero,), (tangent,))
    coefficient_zero = channels_to_complex(
        coefficient_zero.detach().cpu().numpy().reshape(-1, 2)
    )
    derivative_zero = channels_to_complex(
        derivative_zero.detach().cpu().numpy().reshape(-1, 2)
    )

    per_z_l2 = np.asarray([
        relative_l2(field_prediction[index], field_reference[index])
        for index in range(N_Z_EVAL)
    ])
    target_prediction = field_prediction[-1]
    target_reference = field_reference[-1]
    intensity_prediction = np.abs(field_prediction) ** 2
    intensity_reference = np.abs(field_reference) ** 2

    metrics = {
        "global_complex_relative_l2": relative_l2(
            field_prediction, field_reference
        ),
        "target_complex_relative_l2": relative_l2(
            target_prediction, target_reference
        ),
        "global_complex_coherence": coherence(
            field_prediction, field_reference
        ),
        "target_complex_coherence": coherence(
            target_prediction, target_reference
        ),
        "global_intensity_relative_l2": relative_l2(
            intensity_prediction, intensity_reference
        ),
        "target_intensity_relative_l2": relative_l2(
            intensity_prediction[-1], intensity_reference[-1]
        ),
        "global_phase_mae_rad": circular_phase_mae(
            field_prediction, field_reference
        ),
        "target_phase_mae_rad": circular_phase_mae(
            target_prediction, target_reference
        ),
        "max_l2_over_z": float(np.max(per_z_l2)),
        "helmholtz_field_residual_normalized_rmse": float(
            np.sqrt(np.mean(np.abs(residual_field / field_scale) ** 2))
        ),
        "helmholtz_field_residual_normalized_max_abs": float(
            np.max(np.abs(residual_field / field_scale))
        ),
        "hard_cauchy_coefficient_rmse": float(np.sqrt(np.mean(
            np.abs(coefficient_zero - mode_data["amplitudes"]) ** 2
        ))),
        "hard_cauchy_derivative_rmse": float(np.sqrt(np.mean(
            np.abs(derivative_zero - mode_data["derivatives"]) ** 2
        ))),
    }
    arrays = {
        "x_lambda": x,
        "z_lambda": z,
        "field_prediction": field_prediction,
        "field_reference": field_reference,
        "coefficient_prediction": coefficient_prediction,
        "coefficient_reference": coefficient_reference,
        "per_z_l2": per_z_l2,
        "mode_indices": mode_data["indices"],
        "kx": mode_data["kx"],
        "kz": mode_data["kz"],
    }
    return metrics, arrays


def train_case(count: int, device: torch.device) -> tuple[dict, dict[str, np.ndarray], dict]:
    set_seed(SEED + count)
    rng = np.random.RandomState(SEED + 1000 + count)
    mode_data = make_initial_modes(count)
    amplitude = np.abs(mode_data["amplitudes"])
    amplitude_floor = max(float(np.max(amplitude)) * 1e-3, 1e-8)
    modal_scale = np.maximum(amplitude, amplitude_floor)
    correction_scale = np.repeat((K**2 * modal_scale).astype(np.float32), 2)

    model = nb03.ModalSiren(
        torch.tensor(
            complex_to_real_channels(mode_data["amplitudes"]), device=device
        ),
        torch.tensor(
            complex_to_real_channels(mode_data["derivatives"]), device=device
        ),
        torch.tensor(correction_scale, device=device),
        DISTANCE_LAMBDA,
    ).to(device)
    model_path = OUTPUT_DIR / "models" / f"case_{count:02d}_modes.pt"
    resumed_from = None
    previous_history = np.asarray([], dtype=float)
    if RESUME_EXISTING and model_path.exists():
        model.load_state_dict(torch.load(
            model_path, map_location=device, weights_only=True
        ))
        resumed_from = str(model_path)
        previous_npz = OUTPUT_DIR / f"case_{count:02d}_modes.npz"
        if previous_npz.exists():
            with np.load(previous_npz) as stored:
                if "loss_history" in stored:
                    previous_history = stored["loss_history"].copy()
    kz_squared = torch.tensor(
        mode_data["kz_squared"], dtype=torch.float32, device=device
    )
    residual_scale = torch.tensor(
        (K**2 * modal_scale).astype(np.float32), device=device
    ).reshape(1, -1, 1)
    if OPTIMIZER_NAME == "adam":
        optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
            optimizer,
            T_max=max(EPOCHS, 1),
            eta_min=LEARNING_RATE * 0.02,
        )
        fixed_z = None
    elif OPTIMIZER_NAME == "lbfgs":
        optimizer = torch.optim.LBFGS(
            model.parameters(),
            lr=1.0,
            max_iter=LBFGS_INNER_ITER,
            max_eval=LBFGS_INNER_ITER + 5,
            history_size=100,
            tolerance_grad=1e-10,
            tolerance_change=1e-12,
            line_search_fn="strong_wolfe",
        )
        scheduler = None
        fixed_z = torch.tensor(
            (np.arange(N_Z_TRAIN) + 0.5) / N_Z_TRAIN * DISTANCE_LAMBDA,
            dtype=torch.float32,
            device=device,
        ).reshape(-1, 1)
    else:
        raise ValueError("NB02B_OPTIMIZER debe ser 'adam' o 'lbfgs'.")
    best_loss = float("inf")
    best_state = None
    loss_history = []
    started = time.time()

    print(f"Caso controlado: {count} modo(s) complejos")
    for epoch in range(EPOCHS):
        if OPTIMIZER_NAME == "adam":
            z = torch.tensor(
                rng.uniform(0.0, DISTANCE_LAMBDA, (N_Z_TRAIN, 1)),
                dtype=torch.float32,
                device=device,
            )
            optimizer.zero_grad()
            residual = nb03.modal_residual(model, z, kz_squared)
            loss = torch.mean((residual / residual_scale).square())
            if not torch.isfinite(loss):
                raise FloatingPointError(
                    f"Perdida no finita para {count} modos en epoca {epoch}."
                )
            loss.backward()
            if GRAD_CLIP > 0:
                torch.nn.utils.clip_grad_norm_(model.parameters(), GRAD_CLIP)
            optimizer.step()
            scheduler.step()
        else:
            def closure():
                optimizer.zero_grad(set_to_none=True)
                residual_value = nb03.modal_residual(
                    model, fixed_z, kz_squared
                )
                objective = torch.mean(
                    (residual_value / residual_scale).square()
                )
                if not torch.isfinite(objective):
                    raise FloatingPointError(
                        f"Perdida no finita para {count} modos en paso {epoch}."
                    )
                objective.backward()
                return objective

            optimizer.step(closure)
            residual = nb03.modal_residual(model, fixed_z, kz_squared)
            loss = torch.mean((residual / residual_scale).square())

        value = float(loss.detach().cpu())
        loss_history.append(value)
        if value < best_loss:
            best_loss = value
            best_state = copy.deepcopy(model.state_dict())
        if (epoch + 1) % max(EPOCHS // 5, 1) == 0:
            print(f"  epoca {epoch + 1:5d}/{EPOCHS}: loss={value:.3e}")

    if best_state is not None:
        model.load_state_dict(best_state)
    training_seconds = time.time() - started
    metrics, arrays = evaluate_case(model, mode_data, device)
    arrays["loss_history"] = np.concatenate((
        previous_history, np.asarray(loss_history)
    ))

    accepted = (
        metrics["global_complex_relative_l2"] < 0.05
        and metrics["target_complex_relative_l2"] < 0.05
        and metrics["target_complex_coherence"] > 0.90
        and metrics["helmholtz_field_residual_normalized_rmse"] < 0.05
    )
    report = {
        "n_complex_modes": count,
        "mode_indices": mode_data["indices"].tolist(),
        "training_seconds": training_seconds,
        "stage_epochs": EPOCHS,
        "cumulative_recorded_epochs": int(arrays["loss_history"].size),
        "resumed_from": resumed_from,
        "optimizer": OPTIMIZER_NAME,
        "best_training_loss": best_loss,
        "metrics": metrics,
        "acceptance": {
            "global_complex_l2_below_5_percent": (
                metrics["global_complex_relative_l2"] < 0.05
            ),
            "target_complex_l2_below_5_percent": (
                metrics["target_complex_relative_l2"] < 0.05
            ),
            "target_coherence_above_0_90": (
                metrics["target_complex_coherence"] > 0.90
            ),
            "normalized_residual_rmse_below_0_05": (
                metrics["helmholtz_field_residual_normalized_rmse"] < 0.05
            ),
            "accepted": accepted,
        },
    }
    return report, arrays, model.state_dict()


def save_case(count: int, arrays: dict[str, np.ndarray], state_dict: dict) -> None:
    models_dir = OUTPUT_DIR / "models"
    models_dir.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(OUTPUT_DIR / f"case_{count:02d}_modes.npz", **arrays)
    torch.save(state_dict, models_dir / f"case_{count:02d}_modes.pt")


def make_figures(reports: list[dict], arrays_by_count: dict[int, dict]) -> None:
    import matplotlib.pyplot as plt

    figures_dir = OUTPUT_DIR / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)
    for report in reports:
        count = report["n_complex_modes"]
        arrays = arrays_by_count[count]
        x = arrays["x_lambda"]
        z = arrays["z_lambda"]
        predicted = arrays["field_prediction"]
        reference = arrays["field_reference"]
        per_z_l2 = arrays["per_z_l2"]
        history = arrays["loss_history"]

        fig, axes = plt.subplots(2, 2, figsize=(12, 8), constrained_layout=True)
        axes[0, 0].plot(x, np.abs(reference[-1]) ** 2, label="analitica")
        axes[0, 0].plot(
            x, np.abs(predicted[-1]) ** 2, "--", label="PINN-SIREN"
        )
        axes[0, 0].set_title(r"Intensidad en $\tilde z=1$")
        axes[0, 0].set_xlabel(r"$\tilde x=x/\lambda$")
        axes[0, 0].set_ylabel(r"$I=|E|^2$")
        axes[0, 0].legend()

        axes[0, 1].semilogy(z, np.maximum(per_z_l2, 1e-12))
        axes[0, 1].axhline(0.05, color="tab:red", linestyle=":", label="5 %")
        axes[0, 1].set_title(r"Error complejo a lo largo de $\tilde z$")
        axes[0, 1].set_xlabel(r"$\tilde z=z/\lambda$")
        axes[0, 1].set_ylabel(r"Error relativo $L^2$")
        axes[0, 1].legend()

        image = axes[1, 0].imshow(
            np.abs(predicted) ** 2,
            aspect="auto",
            origin="lower",
            extent=[x[0], x[-1], z[0], z[-1]],
            cmap="magma",
        )
        axes[1, 0].set_title("Propagacion predicha")
        axes[1, 0].set_xlabel(r"$\tilde x$")
        axes[1, 0].set_ylabel(r"$\tilde z$")
        fig.colorbar(image, ax=axes[1, 0], label=r"$|E_\theta|^2$")

        axes[1, 1].semilogy(np.maximum(history, 1e-14))
        axes[1, 1].set_title("Perdida fisica durante entrenamiento")
        axes[1, 1].set_xlabel("Epoca")
        axes[1, 1].set_ylabel("MSE residual modal normalizado")
        axes[1, 1].grid(alpha=0.25)
        fig.suptitle(
            f"NB02B - validacion analitica con {count} modo(s) complejos"
        )
        fig.savefig(
            figures_dir / f"case_{count:02d}_modes.png",
            dpi=160,
            bbox_inches="tight",
        )
        plt.close(fig)

    counts = [item["n_complex_modes"] for item in reports]
    global_l2 = [
        item["metrics"]["global_complex_relative_l2"] for item in reports
    ]
    target_l2 = [
        item["metrics"]["target_complex_relative_l2"] for item in reports
    ]
    residual = [
        item["metrics"]["helmholtz_field_residual_normalized_rmse"]
        for item in reports
    ]
    fig, axis = plt.subplots(figsize=(8, 5), constrained_layout=True)
    axis.semilogy(counts, global_l2, "o-", label="L2 global")
    axis.semilogy(counts, target_l2, "s-", label="L2 en z=1")
    axis.semilogy(counts, residual, "^-", label="residuo Helmholtz")
    axis.axhline(0.05, color="tab:red", linestyle=":", label="umbral 5 %")
    axis.set_xticks(counts)
    axis.set_xlabel("Numero de modos complejos")
    axis.set_ylabel("Metrica relativa")
    axis.set_title("Escalamiento controlado de la arquitectura de NB03")
    axis.grid(alpha=0.25)
    axis.legend()
    fig.savefig(
        figures_dir / "summary_modes.png", dpi=160, bbox_inches="tight"
    )
    plt.close(fig)


def main() -> None:
    if not CASE_COUNTS:
        raise ValueError("NB02B_CASE_COUNTS no contiene casos.")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("NB02B - validacion analitica de la arquitectura modal de NB03")
    print(f"Dispositivo: {device}")
    print(
        "Arquitectura reutilizada: "
        f"{nb03.NUM_LAYERS}x{nb03.HIDDEN_DIM}, "
        f"omega primera={nb03.FIRST_OMEGA:g}, "
        f"omega interna={nb03.HIDDEN_OMEGA:g}"
    )
    print(f"Casos: {CASE_COUNTS}; epocas por caso: {EPOCHS}")

    reports = []
    arrays_by_count = {}
    for count in CASE_COUNTS:
        report, arrays, state_dict = train_case(count, device)
        reports.append(report)
        arrays_by_count[count] = arrays
        save_case(count, arrays, state_dict)
        print(
            f"  resultado {count:2d}: "
            f"L2 global={report['metrics']['global_complex_relative_l2']:.3%}, "
            f"L2 z=1={report['metrics']['target_complex_relative_l2']:.3%}, "
            f"coherencia={report['metrics']['target_complex_coherence']:.6f}, "
            f"aceptado={report['acceptance']['accepted']}"
        )

    make_figures(reports, arrays_by_count)
    summary = {
        "experiment": "NB02B analytic bridge for NB03 modal PINN-SIREN",
        "purpose": (
            "Validar la arquitectura exacta de NB03 con soluciones complejas "
            "multimodales conocidas antes de usar una pantalla aleatoria."
        ),
        "physics": {
            "coordinates": "Cartesian normalized (x_tilde, z_tilde)",
            "equation": "d2E/dx2 + d2E/dz2 + (2*pi)^2 E = 0",
            "domain_x_lambda": [-WIDTH_LAMBDA / 2.0, WIDTH_LAMBDA / 2.0],
            "domain_z_lambda": [0.0, DISTANCE_LAMBDA],
            "exact_field": "sum_m A_m exp(i*(kx_m*x+kz_m*z))",
            "interior_training_labels": 0,
            "hard_cauchy": "a_m(0), a_m'(0)=i*kz_m*a_m(0)",
        },
        "architecture": {
            "source": "scripts/experiments/nb03_modal_pinn_siren.py",
            "hidden_dim": nb03.HIDDEN_DIM,
            "num_hidden_layers": nb03.NUM_LAYERS,
            "first_omega": nb03.FIRST_OMEGA,
            "hidden_omega": nb03.HIDDEN_OMEGA,
        },
        "training": {
            "seed": SEED,
            "epochs_per_case": EPOCHS,
            "n_z_per_epoch": N_Z_TRAIN,
            "learning_rate": LEARNING_RATE,
            "gradient_clip": GRAD_CLIP,
            "optimizer": (
                "Adam with cosine annealing"
                if OPTIMIZER_NAME == "adam"
                else f"L-BFGS strong Wolfe; {LBFGS_INNER_ITER} inner iterations"
            ),
            "resume_existing_checkpoints": RESUME_EXISTING,
        },
        "acceptance_criteria": {
            "global_complex_relative_l2": "< 0.05",
            "target_complex_relative_l2": "< 0.05",
            "target_complex_coherence": "> 0.90",
            "normalized_helmholtz_residual_rmse": "< 0.05",
        },
        "cases": reports,
        "all_cases_accepted": all(
            item["acceptance"]["accepted"] for item in reports
        ),
    }
    summary_path = OUTPUT_DIR / "summary.json"
    summary_path.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"Resumen: {summary_path}")


if __name__ == "__main__":
    main()
