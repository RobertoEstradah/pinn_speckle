# -*- coding: utf-8 -*-
"""Validación fundamental de la EDO modal utilizada en NB02B y NB03.

Se conserva exactamente la arquitectura ``ModalSiren`` de NB03, pero se
estudia un único modo transversal con solución cerrada conocida. Se entrenan
tres problemas de Cauchy independientes:

1. base coseno;
2. base seno;
3. combinación compleja general de ambas bases.

La referencia analítica no participa en el entrenamiento. La función de
pérdida usa únicamente el residuo ``a'' + kz**2 a``. Las condiciones de
Cauchy se satisfacen exactamente mediante la transformación dura de salida.
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
# La frecuencia debe fijarse antes de importar la arquitectura de NB03.
os.environ.setdefault("NB03_MODAL_FIRST_OMEGA", "1")
os.environ.setdefault("NB03_MODAL_HIDDEN_OMEGA", "1")

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

import torch
from torch.func import jvp

from scripts.experiments import nb03_modal_pinn_siren as nb03


K = 2.0 * np.pi
KX = 0.6 * K
KZ = 0.8 * K
DISTANCE_LAMBDA = float(os.environ.get("NB02B_BASIS_DISTANCE_LAMBDA", 1.0))
SEED = int(os.environ.get("NB02B_BASIS_SEED", 2026))
N_Z_TRAIN = int(os.environ.get("NB02B_BASIS_N_Z_TRAIN", 512))
N_Z_EVAL = int(os.environ.get("NB02B_BASIS_N_Z_EVAL", 1001))
N_X_EVAL = int(os.environ.get("NB02B_BASIS_N_X_EVAL", 256))
LBFGS_STAGES = int(os.environ.get("NB02B_BASIS_LBFGS_STAGES", 80))
LBFGS_INNER = int(os.environ.get("NB02B_BASIS_LBFGS_INNER", 20))
OUTPUT_DIR = Path(os.environ.get(
    "NB02B_BASIS_OUTPUT_DIR",
    str(PROJECT_ROOT / "results" / "nb02b_modal_basis"),
)).resolve()


CASES = {
    "cosine": {
        "label": "Base coseno",
        "C": 1.0 + 0.0j,
        "D": 0.0 + 0.0j,
    },
    "sine": {
        "label": "Base seno",
        "C": 0.0 + 0.0j,
        "D": 1.0 + 0.0j,
    },
    "general": {
        "label": "Combinación compleja general",
        "C": 0.6 + 0.2j,
        "D": -0.3 + 0.7j,
    },
}


def set_seed(seed: int) -> None:
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def complex_to_channels(value: complex) -> np.ndarray:
    return np.asarray([value.real, value.imag], dtype=np.float32)


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
    denominator = np.linalg.norm(prediction_flat) * np.linalg.norm(reference_flat)
    if denominator == 0:
        return float("nan")
    return float(abs(np.vdot(reference_flat, prediction_flat)) / denominator)


def masked_phase_mae(
    prediction: np.ndarray,
    reference: np.ndarray,
    relative_threshold: float = 1e-8,
) -> float:
    amplitude = np.abs(reference)
    threshold = relative_threshold * max(float(amplitude.max()), 1.0)
    mask = amplitude > threshold
    if not np.any(mask):
        return float("nan")
    phase_difference = np.angle(prediction[mask] * np.conj(reference[mask]))
    return float(np.mean(np.abs(phase_difference)))


def exact_coefficient(z: np.ndarray, C: complex, D: complex) -> np.ndarray:
    return C * np.cos(KZ * z) + D * np.sin(KZ * z)


def reconstruct_field(coefficient: np.ndarray, x: np.ndarray) -> np.ndarray:
    transverse_phase = np.exp(1j * KX * x)
    return coefficient.reshape(-1, 1) * transverse_phase.reshape(1, -1)


def build_model(C: complex, D: complex, device: torch.device) -> torch.nn.Module:
    coefficient0 = complex_to_channels(C)
    derivative0 = complex_to_channels(KZ * D)
    modal_amplitude = max(abs(C), abs(D), 1.0)
    correction_scale = np.full(2, K**2 * modal_amplitude, dtype=np.float32)
    return nb03.ModalSiren(
        torch.tensor(coefficient0, device=device),
        torch.tensor(derivative0, device=device),
        torch.tensor(correction_scale, device=device),
        DISTANCE_LAMBDA,
    ).to(device)


def evaluate_case(
    model: torch.nn.Module,
    C: complex,
    D: complex,
    device: torch.device,
) -> tuple[dict, dict[str, np.ndarray]]:
    z = np.linspace(0.0, DISTANCE_LAMBDA, N_Z_EVAL)
    x = np.linspace(-1.0, 1.0, N_X_EVAL, endpoint=False)
    z_tensor = torch.tensor(z, dtype=torch.float32, device=device).reshape(-1, 1)
    kz_squared = torch.tensor([KZ**2], dtype=torch.float32, device=device)

    with torch.no_grad():
        channels = model(z_tensor).cpu().numpy().reshape(N_Z_EVAL, 1, 2)
    coefficient_prediction = channels_to_complex(channels[:, 0, :])
    coefficient_reference = exact_coefficient(z, C, D)
    field_prediction = reconstruct_field(coefficient_prediction, x)
    field_reference = reconstruct_field(coefficient_reference, x)

    residual_channels = nb03.modal_residual(
        model, z_tensor, kz_squared
    ).detach().cpu().numpy().reshape(N_Z_EVAL, 1, 2)
    residual = channels_to_complex(residual_channels[:, 0, :])
    residual_scale = KZ**2 * max(
        float(np.sqrt(np.mean(np.abs(coefficient_reference) ** 2))), 1e-12
    )

    zero = torch.zeros((1, 1), dtype=torch.float32, device=device)
    tangent = torch.ones_like(zero)
    coefficient_zero, derivative_zero = jvp(model, (zero,), (tangent,))
    coefficient_zero = channels_to_complex(
        coefficient_zero.detach().cpu().numpy().reshape(1, 2)
    )[0]
    derivative_zero = channels_to_complex(
        derivative_zero.detach().cpu().numpy().reshape(1, 2)
    )[0]

    per_z_l2 = np.abs(coefficient_prediction - coefficient_reference) / np.maximum(
        np.abs(coefficient_reference), 1e-12
    )
    intensity_prediction = np.abs(field_prediction) ** 2
    intensity_reference = np.abs(field_reference) ** 2
    metrics = {
        "coefficient_relative_l2": relative_l2(
            coefficient_prediction, coefficient_reference
        ),
        "global_complex_relative_l2": relative_l2(
            field_prediction, field_reference
        ),
        "target_complex_relative_l2": relative_l2(
            field_prediction[-1], field_reference[-1]
        ),
        "global_complex_coherence": coherence(
            field_prediction, field_reference
        ),
        "target_complex_coherence": coherence(
            field_prediction[-1], field_reference[-1]
        ),
        "global_intensity_relative_l2": relative_l2(
            intensity_prediction, intensity_reference
        ),
        "target_intensity_relative_l2": relative_l2(
            intensity_prediction[-1], intensity_reference[-1]
        ),
        "global_phase_mae_rad": masked_phase_mae(
            field_prediction, field_reference
        ),
        "target_phase_mae_rad": masked_phase_mae(
            field_prediction[-1], field_reference[-1]
        ),
        "helmholtz_modal_residual_normalized_rmse": float(
            np.sqrt(np.mean(np.abs(residual / residual_scale) ** 2))
        ),
        "helmholtz_modal_residual_normalized_max_abs": float(
            np.max(np.abs(residual / residual_scale))
        ),
        "hard_cauchy_coefficient_abs_error": float(abs(coefficient_zero - C)),
        "hard_cauchy_derivative_abs_error": float(
            abs(derivative_zero - KZ * D)
        ),
    }
    arrays = {
        "x_lambda": x,
        "z_lambda": z,
        "coefficient_prediction": coefficient_prediction,
        "coefficient_reference": coefficient_reference,
        "field_prediction": field_prediction,
        "field_reference": field_reference,
        "residual": residual,
        "pointwise_relative_error": per_z_l2,
    }
    return metrics, arrays


def train_case(
    case_name: str,
    case: dict,
    device: torch.device,
) -> tuple[dict, dict[str, np.ndarray], dict]:
    case_seed = SEED + list(CASES).index(case_name)
    set_seed(case_seed)
    C = complex(case["C"])
    D = complex(case["D"])
    model = build_model(C, D, device)
    kz_squared = torch.tensor([KZ**2], dtype=torch.float32, device=device)
    amplitude_scale = max(abs(C), abs(D), 1.0)
    residual_scale = torch.tensor(
        [[[KZ**2 * amplitude_scale]]], dtype=torch.float32, device=device
    )
    z_train = torch.tensor(
        (np.arange(N_Z_TRAIN) + 0.5) / N_Z_TRAIN * DISTANCE_LAMBDA,
        dtype=torch.float32,
        device=device,
    ).reshape(-1, 1)
    optimizer = torch.optim.LBFGS(
        model.parameters(),
        lr=1.0,
        max_iter=LBFGS_INNER,
        max_eval=LBFGS_INNER + 5,
        history_size=100,
        tolerance_grad=1e-10,
        tolerance_change=1e-12,
        line_search_fn="strong_wolfe",
    )
    best_loss = float("inf")
    best_state = None
    loss_history: list[float] = []
    started = time.time()

    print(f"Caso: {case['label']}")
    for stage in range(LBFGS_STAGES):
        def closure():
            optimizer.zero_grad(set_to_none=True)
            residual = nb03.modal_residual(model, z_train, kz_squared)
            loss = torch.mean((residual / residual_scale).square())
            if not torch.isfinite(loss):
                raise FloatingPointError(
                    f"Pérdida no finita en {case_name}, etapa {stage}."
                )
            loss.backward()
            return loss

        optimizer.step(closure)
        residual = nb03.modal_residual(model, z_train, kz_squared)
        loss = torch.mean((residual / residual_scale).square())
        value = float(loss.detach().cpu())
        loss_history.append(value)
        if value < best_loss:
            best_loss = value
            best_state = copy.deepcopy(model.state_dict())
        if (stage + 1) % max(LBFGS_STAGES // 4, 1) == 0:
            print(f"  etapa {stage + 1:3d}/{LBFGS_STAGES}: loss={value:.3e}")

    if best_state is not None:
        model.load_state_dict(best_state)
    training_seconds = time.time() - started
    metrics, arrays = evaluate_case(model, C, D, device)
    arrays["loss_history"] = np.asarray(loss_history)

    acceptance = {
        "coefficient_l2_below_5_percent": (
            metrics["coefficient_relative_l2"] < 0.05
        ),
        "target_complex_l2_below_5_percent": (
            metrics["target_complex_relative_l2"] < 0.05
        ),
        "global_coherence_above_0_90": (
            metrics["global_complex_coherence"] > 0.90
        ),
        "normalized_residual_rmse_below_0_05": (
            metrics["helmholtz_modal_residual_normalized_rmse"] < 0.05
        ),
        "hard_cauchy_coefficient_below_1e_5": (
            metrics["hard_cauchy_coefficient_abs_error"] < 1e-5
        ),
        "hard_cauchy_derivative_below_1e_5": (
            metrics["hard_cauchy_derivative_abs_error"] < 1e-5
        ),
    }
    acceptance["accepted"] = all(acceptance.values())
    report = {
        "case": case_name,
        "label": case["label"],
        "C": {"real": C.real, "imag": C.imag},
        "D": {"real": D.real, "imag": D.imag},
        "initial_coefficient": {"real": C.real, "imag": C.imag},
        "initial_derivative": {
            "real": (KZ * D).real,
            "imag": (KZ * D).imag,
        },
        "training_seconds": training_seconds,
        "best_training_loss": best_loss,
        "metrics": metrics,
        "acceptance": acceptance,
    }
    return report, arrays, model.state_dict()


def save_case(
    case_name: str,
    arrays: dict[str, np.ndarray],
    state_dict: dict,
) -> None:
    models_dir = OUTPUT_DIR / "models"
    models_dir.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(OUTPUT_DIR / f"{case_name}.npz", **arrays)
    torch.save(state_dict, models_dir / f"{case_name}.pt")


def make_figures(reports: list[dict], arrays_by_case: dict[str, dict]) -> None:
    import matplotlib.pyplot as plt

    # La corrida canonica deja sus figuras con las de los demas notebooks.
    if OUTPUT_DIR == (PROJECT_ROOT / "results" / "nb02b_modal_basis").resolve():
        figures_dir = PROJECT_ROOT / "results" / "figures"
    else:
        figures_dir = OUTPUT_DIR / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)
    for report in reports:
        case_name = report["case"]
        arrays = arrays_by_case[case_name]
        z = arrays["z_lambda"]
        predicted = arrays["coefficient_prediction"]
        reference = arrays["coefficient_reference"]
        residual = arrays["residual"]
        history = arrays["loss_history"]

        figure, axes = plt.subplots(2, 2, figsize=(12, 8), constrained_layout=True)
        axes[0, 0].plot(z, reference.real, label="Re exacta")
        axes[0, 0].plot(z, predicted.real, "--", label="Re PINN")
        axes[0, 0].plot(z, reference.imag, label="Im exacta")
        axes[0, 0].plot(z, predicted.imag, "--", label="Im PINN")
        axes[0, 0].set_title(r"Coeficiente modal $a_m(\tilde z)$")
        axes[0, 0].set_xlabel(r"$\tilde z=z/\lambda$")
        axes[0, 0].legend(ncol=2)

        axes[0, 1].semilogy(
            z, np.maximum(np.abs(predicted - reference), 1e-14)
        )
        axes[0, 1].set_title("Error absoluto del coeficiente")
        axes[0, 1].set_xlabel(r"$\tilde z$")
        axes[0, 1].set_ylabel(r"$|a_{m,\theta}-a_m|$")

        axes[1, 0].semilogy(z, np.maximum(np.abs(residual), 1e-14))
        axes[1, 0].set_title("Residuo de la EDO modal")
        axes[1, 0].set_xlabel(r"$\tilde z$")
        axes[1, 0].set_ylabel(r"$|a_m''+k_{z,m}^2a_m|$")

        axes[1, 1].semilogy(np.maximum(history, 1e-14))
        axes[1, 1].set_title("Pérdida física")
        axes[1, 1].set_xlabel("Etapa L-BFGS")
        axes[1, 1].set_ylabel("MSE residual normalizado")
        axes[1, 1].grid(alpha=0.25)
        figure.suptitle(f"NB02B: {report['label']}")
        figure.savefig(
            figures_dir / f"nb02b_basis_{case_name}.png", dpi=160, bbox_inches="tight"
        )
        plt.close(figure)

    figure, axis = plt.subplots(figsize=(9, 5), constrained_layout=True)
    names = [item["label"] for item in reports]
    l2_values = [
        100.0 * item["metrics"]["coefficient_relative_l2"] for item in reports
    ]
    residual_values = [
        item["metrics"]["helmholtz_modal_residual_normalized_rmse"]
        for item in reports
    ]
    positions = np.arange(len(names))
    width = 0.36
    axis.bar(positions - width / 2, l2_values, width, label=r"$L^2$ coeficiente (%)")
    axis.bar(
        positions + width / 2,
        100.0 * np.asarray(residual_values),
        width,
        label="Residuo normalizado (%)",
    )
    axis.axhline(5.0, color="tab:red", linestyle=":", label="Umbral 5 %")
    axis.set_xticks(positions, names)
    axis.set_ylabel("Porcentaje")
    axis.set_title("Validación de la base modal fundamental")
    axis.legend()
    axis.grid(axis="y", alpha=0.25)
    figure.savefig(
        figures_dir / "nb02b_basis_summary.png", dpi=160, bbox_inches="tight"
    )
    plt.close(figure)


def main() -> None:
    if not np.isclose(KX**2 + KZ**2, K**2):
        raise RuntimeError("La relación de dispersión modal no se satisface.")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("NB02B: validación de la base modal fundamental")
    print(f"Dispositivo: {device}")
    print(f"kx={KX:.8f}; kz={KZ:.8f}; k={K:.8f}")

    reports = []
    arrays_by_case = {}
    for case_name, case in CASES.items():
        report, arrays, state_dict = train_case(case_name, case, device)
        reports.append(report)
        arrays_by_case[case_name] = arrays
        save_case(case_name, arrays, state_dict)

    make_figures(reports, arrays_by_case)
    summary = {
        "experiment": "NB02B modal fundamental basis validation",
        "equation": "a_m''(z) + kz_m^2 a_m(z) = 0",
        "training_uses_interior_labels": False,
        "normalization": {
            "x_tilde": "x/lambda",
            "z_tilde": "z/lambda",
            "k_tilde": "2*pi",
        },
        "dispersion": {
            "k": K,
            "kx": KX,
            "kz": KZ,
            "kx_squared_plus_kz_squared": KX**2 + KZ**2,
        },
        "architecture": {
            "class": "ModalSiren",
            "first_omega": nb03.FIRST_OMEGA,
            "hidden_omega": nb03.HIDDEN_OMEGA,
            "hidden_dim": nb03.HIDDEN_DIM,
            "num_layers": nb03.NUM_LAYERS,
            "hard_cauchy": "a(0)+z*a'(0)+z^2*N_theta(z)",
        },
        "training": {
            "optimizer": "L-BFGS",
            "stages": LBFGS_STAGES,
            "inner_iterations": LBFGS_INNER,
            "n_z_train": N_Z_TRAIN,
            "device": str(device),
        },
        "cases": reports,
        "all_cases_accepted": all(
            item["acceptance"]["accepted"] for item in reports
        ),
    }
    with (OUTPUT_DIR / "summary.json").open("w", encoding="utf-8") as stream:
        json.dump(summary, stream, indent=2, ensure_ascii=False)

    print("Resumen:")
    for report in reports:
        metrics = report["metrics"]
        print(
            f"  {report['case']}: "
            f"L2={100.0 * metrics['coefficient_relative_l2']:.6f} %, "
            f"C={metrics['global_complex_coherence']:.9f}, "
            f"R={metrics['helmholtz_modal_residual_normalized_rmse']:.3e}, "
            f"aceptado={report['acceptance']['accepted']}"
        )
    print(f"Todos aceptados: {summary['all_cases_accepted']}")
    print(f"Resultados: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
