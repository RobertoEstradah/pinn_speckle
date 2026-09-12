# -*- coding: utf-8 -*-
"""NB03-D: curriculum espectral/frecuencial para Cauchy dura en z=1 lambda.

La red conserva 20 modos Fourier y transfiere sus pesos entre cuatro problemas
fisicamente consistentes. En cada etapa se filtra la pantalla a |kx| <= k_s,
se recalcula dE/dz con k_s y se usa el mismo k_s en Helmholtz. La ultima etapa
corresponde exactamente al problema objetivo k=2*pi.
"""

from pathlib import Path
import copy
import json
import os
import sys
import time

import numpy as np

os.environ.setdefault("MPLBACKEND", "Agg")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

import torch

from scripts.experiments import nb03_pinn_slabs as base


MODE_STAGES = [int(value) for value in os.environ.get(
    "NB03_CURRICULUM_MODE_STAGES", "5,10,15,20"
).split(",")]
K_SCALES = [float(value) for value in os.environ.get(
    "NB03_CURRICULUM_K_SCALES", "0.25,0.5,0.75,1.0"
).split(",")]
EPOCHS_PER_STAGE = int(os.environ.get(
    "NB03_CURRICULUM_EPOCHS_PER_STAGE", 200
))
RESAMPLE_INTERVAL = int(os.environ.get(
    "NB03_CURRICULUM_RESAMPLE_INTERVAL", 25
))
VALIDATION_NX = int(os.environ.get("NB03_CURRICULUM_VALIDATION_NX", 256))
VALIDATION_NZ = int(os.environ.get("NB03_CURRICULUM_VALIDATION_NZ", 41))
OUTPUT_SUFFIX = os.environ.get(
    "NB03_CURRICULUM_OUTPUT_SUFFIX", "_z1_frequency_curriculum1"
)
RESUME_MODEL_PATH = os.environ.get("NB03_CURRICULUM_RESUME_MODEL", "")


def radiative_input_for_k(reference, wave_number):
    x = reference["x_lambda"]
    kx = reference["kx"]
    spectrum = np.fft.fft(np.exp(1j * reference["phase"]))
    propagating = np.abs(kx) <= wave_number + 1e-10
    kz = np.zeros_like(kx, dtype=float)
    kz[propagating] = np.sqrt(np.maximum(
        wave_number ** 2 - kx[propagating] ** 2, 0.0
    ))
    radiative_spectrum = np.where(propagating, spectrum, 0.0)
    field = np.fft.ifft(radiative_spectrum)
    derivative = np.fft.ifft(1j * kz * radiative_spectrum)
    return field, derivative, propagating


def two_component(values):
    return np.column_stack((values.real, values.imag)).astype(np.float32)


def replace_collocation(tensors, z0, z1, rng, device):
    points = np.column_stack((
        rng.uniform(-base.WIDTH_LAMBDA / 2.0,
                    base.WIDTH_LAMBDA / 2.0, base.N_COLLOC),
        rng.uniform(z0, z1, base.N_COLLOC),
    ))
    tensors["collocation"] = torch.tensor(
        points, dtype=torch.float32, device=device
    )


def independent_residual(model, wave_number, device):
    x = np.linspace(-base.WIDTH_LAMBDA / 2.0,
                    base.WIDTH_LAMBDA / 2.0, VALIDATION_NX,
                    endpoint=False)
    z = np.linspace(0.0, base.DISTANCE_LAMBDA, VALIDATION_NZ)
    grid = np.column_stack((np.tile(x, len(z)), np.repeat(z, len(x))))
    sum_squared = 0.0
    maximum = 0.0
    count = 0
    for start in range(0, len(grid), 512):
        points = torch.tensor(
            grid[start:start + 512], dtype=torch.float32, device=device
        )
        real, imag = base.helmholtz_residual(
            model, points, wave_number=wave_number
        )
        normalized = (
            real.detach().cpu().numpy().ravel() ** 2
            + imag.detach().cpu().numpy().ravel() ** 2
        ) / wave_number ** 4
        sum_squared += float(normalized.sum())
        maximum = max(maximum, float(np.sqrt(normalized.max())))
        count += len(normalized)
    mean_squared = sum_squared / max(count, 1)
    return {
        "grid_shape": [VALIDATION_NZ, VALIDATION_NX],
        "normalized_mse": mean_squared,
        "normalized_rmse": float(np.sqrt(mean_squared)),
        "normalized_max_abs": maximum,
    }


def main():
    if len(MODE_STAGES) != len(K_SCALES) or not MODE_STAGES:
        raise ValueError("MODE_STAGES y K_SCALES deben tener igual longitud.")
    if abs(K_SCALES[-1] - 1.0) > 1e-12:
        raise ValueError("La ultima etapa debe usar k/k_final=1.")
    if abs(base.DISTANCE_LAMBDA - 1.0) > 1e-12:
        raise ValueError("Este piloto controlado requiere NB03_DISTANCE_LAMBDA=1.")
    if not base.USE_HARD_BOUNDARY or base.INPUT_ENCODING != "fourier":
        raise ValueError("Activa hard boundary y Fourier para este curriculum.")

    base.set_seed(base.SEED)
    rng = np.random.RandomState(base.SEED)
    reference = base.load_reference()
    x = reference["x_lambda"]
    kx = reference["kx"]
    full_mask = reference["propagating_mask"].astype(bool)
    z_reference = reference["z_lambda"]
    target_index = int(np.argmin(
        np.abs(z_reference - base.DISTANCE_LAMBDA)
    ))
    target = reference["field_all_z"][target_index]

    full_field, full_dz, _ = radiative_input_for_k(reference, base.K)
    field_scale = float(np.sqrt(np.mean(np.abs(full_field) ** 2)))
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    first_k = base.K * K_SCALES[0]
    first_field, first_dz, _ = radiative_input_for_k(reference, first_k)
    first_field_scaled = two_component(first_field / field_scale)
    first_dz_scaled = two_component(first_dz / field_scale)
    model = base.HardBoundarySiren2D(
        0.0, base.DISTANCE_LAMBDA,
        first_field_scaled, first_dz_scaled,
        x, kx, full_mask
    ).to(device)
    if RESUME_MODEL_PATH:
        checkpoint = torch.load(
            RESUME_MODEL_PATH, map_location=device, weights_only=False
        )
        model.load_state_dict(checkpoint["model_state"])

    points = base.points_for_slab(
        0.0, base.DISTANCE_LAMBDA, rng, x
    )
    tensors = base.to_tensors(
        points, first_field_scaled, first_dz_scaled, device
    )
    stage_reports = []
    t_global = time.time()

    print("NB03-D: curriculum espectral y de frecuencia")
    stage_plan = list(zip(MODE_STAGES, K_SCALES))
    if RESUME_MODEL_PATH:
        stage_plan = [stage_plan[-1]]
        print(f"  Reanudado desde: {RESUME_MODEL_PATH}")
    print(f"  Dispositivo: {device}; etapas ejecutadas: {len(stage_plan)}")
    print(f"  Colocacion por epoca: {base.N_COLLOC}")

    for stage_index, (active_modes, k_scale) in enumerate(
        stage_plan, start=1
    ):
        wave_number = base.K * k_scale
        stage_field, stage_dz, stage_mask = radiative_input_for_k(
            reference, wave_number
        )
        stage_field_scaled = two_component(stage_field / field_scale)
        stage_dz_scaled = two_component(stage_dz / field_scale)
        model.set_boundary(stage_field_scaled, stage_dz_scaled)
        model.set_active_modes(active_modes)
        tensors["lower_target"] = torch.tensor(
            stage_field_scaled, dtype=torch.float32, device=device
        )
        tensors["lower_dz_target"] = torch.tensor(
            stage_dz_scaled, dtype=torch.float32, device=device
        )

        optimizer = torch.optim.Adam(
            model.parameters(), lr=base.LEARNING_RATE
        )
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
            optimizer, T_max=max(EPOCHS_PER_STAGE, 1),
            eta_min=base.LEARNING_RATE * 0.05
        )
        best_loss = float("inf")
        best_state = None
        t_stage = time.time()
        for epoch in range(EPOCHS_PER_STAGE):
            if RESAMPLE_INTERVAL > 0 and epoch > 0 and (
                epoch % RESAMPLE_INTERVAL == 0
            ):
                replace_collocation(
                    tensors, 0.0, base.DISTANCE_LAMBDA, rng, device
                )
            optimizer.zero_grad()
            terms = base.slab_loss(
                model, tensors, wave_number=wave_number
            )
            if not torch.isfinite(terms[0]):
                raise FloatingPointError(
                    f"Perdida no finita en etapa {stage_index}, epoca {epoch}."
                )
            terms[0].backward()
            if base.GRAD_CLIP_NORM > 0:
                torch.nn.utils.clip_grad_norm_(
                    model.parameters(), base.GRAD_CLIP_NORM
                )
            optimizer.step()
            scheduler.step()
            loss_value = float(terms[0].detach().cpu())
            if loss_value < best_loss:
                best_loss = loss_value
                best_state = copy.deepcopy(model.state_dict())

        if best_state is not None:
            model.load_state_dict(best_state)
        final_terms = base.slab_loss(
            model, tensors, wave_number=wave_number
        )
        report = {
            "stage": stage_index,
            "active_modes": active_modes,
            "k_scale": k_scale,
            "wave_number": wave_number,
            "propagating_mode_count": int(stage_mask.sum()),
            "epochs": EPOCHS_PER_STAGE,
            "best_loss": best_loss,
            "final_loss_on_last_batch": float(final_terms[0].detach().cpu()),
            "final_physics_loss_on_last_batch": float(
                final_terms[4].detach().cpu()
            ),
            "seconds": time.time() - t_stage,
        }
        stage_reports.append(report)
        print(
            f"  Etapa {stage_index}: modos={active_modes}, "
            f"k/kf={k_scale:.2f}, loss={best_loss:.3e}, "
            f"tiempo={report['seconds']:.1f}s"
        )

    # Refinamiento final, conservado solo si mejora sobre el mismo lote.
    before_state = copy.deepcopy(model.state_dict())
    before_loss = float(base.slab_loss(
        model, tensors, wave_number=base.K
    )[0].detach().cpu())
    lbfgs_calls = 0
    if base.LBFGS_MAX_ITER > 0:
        optimizer_lbfgs = torch.optim.LBFGS(
            model.parameters(), lr=0.5,
            max_iter=base.LBFGS_MAX_ITER,
            history_size=50, line_search_fn="strong_wolfe"
        )

        def closure():
            nonlocal lbfgs_calls
            optimizer_lbfgs.zero_grad()
            loss = base.slab_loss(
                model, tensors, wave_number=base.K
            )[0]
            loss.backward()
            lbfgs_calls += 1
            return loss

        optimizer_lbfgs.step(closure)
        after_loss = float(base.slab_loss(
            model, tensors, wave_number=base.K
        )[0].detach().cpu())
        if not np.isfinite(after_loss) or after_loss > before_loss:
            model.load_state_dict(before_state)

    target_points = np.column_stack((
        x, np.full_like(x, base.DISTANCE_LAMBDA)
    ))
    prediction_components = base.evaluate(model, target_points, device)
    prediction = (
        prediction_components[:, 0] + 1j * prediction_components[:, 1]
    ) * field_scale
    metrics = base.complex_field_metrics(prediction, target)
    metrics["reference_target_statistics"] = base.intensity_statistics(target)
    metrics["pinn_target_statistics"] = base.intensity_statistics(prediction)

    lower_points = np.column_stack((x, np.zeros_like(x)))
    lower_value, lower_dz = base.evaluate_with_dz(
        model, lower_points, device
    )
    expected_value = two_component(full_field / field_scale)
    expected_dz = two_component(full_dz / field_scale)
    metrics["hard_boundary_value_rmse"] = float(np.sqrt(np.mean(
        (lower_value - expected_value) ** 2
    )))
    metrics["hard_boundary_dz_rmse"] = float(np.sqrt(np.mean(
        (lower_dz - expected_dz) ** 2
    )))
    residual_validation = independent_residual(model, base.K, device)
    elapsed = time.time() - t_global

    accepted = (
        metrics["target_complex_relative_l2"] < 0.05
        and abs(metrics["pinn_target_statistics"]["contrast"] - 1.0) < 0.1
    )
    output = {
        "experiment": "NB03-D hard-Cauchy SIREN/Fourier frequency curriculum",
        "seed": base.SEED,
        "device": str(device),
        "domain": {
            "x_lambda": [-base.WIDTH_LAMBDA / 2.0,
                         base.WIDTH_LAMBDA / 2.0],
            "z_lambda": [0.0, base.DISTANCE_LAMBDA],
            "final_wave_number": base.K,
        },
        "architecture": {
            "hidden_dim": base.HIDDEN_DIM,
            "num_layers": base.NUM_LAYERS,
            "omega_0": base.OMEGA_0,
            "fourier_modes_max": base.FOURIER_MODES,
            "hard_boundary_ansatz":
                "u0+(z-z0)uz0+(z-z0)^2*N_theta",
        },
        "training": {
            "mode_stages": MODE_STAGES,
            "k_scales": K_SCALES,
            "epochs_per_stage": EPOCHS_PER_STAGE,
            "n_collocation_per_epoch": base.N_COLLOC,
            "resample_interval": RESAMPLE_INTERVAL,
            "learning_rate": base.LEARNING_RATE,
            "gradient_clip_norm": base.GRAD_CLIP_NORM,
            "lbfgs_calls": lbfgs_calls,
            "total_seconds": elapsed,
            "resumed_from": RESUME_MODEL_PATH or None,
        },
        "stages": stage_reports,
        "independent_residual": residual_validation,
        "metrics": metrics,
        "acceptance": {
            "complex_l2_below_5_percent":
                metrics["target_complex_relative_l2"] < 0.05,
            "contrast_distance_from_one_below_0_1":
                abs(metrics["pinn_target_statistics"]["contrast"] - 1.0) < 0.1,
            "accepted": accepted,
        },
        "status": "diagnostic; no interior angular-spectrum labels used",
    }

    results_dir = PROJECT_ROOT / "results"
    figures_dir = results_dir / "figures"
    models_dir = results_dir / "models"
    figures_dir.mkdir(parents=True, exist_ok=True)
    models_dir.mkdir(parents=True, exist_ok=True)
    json_path = results_dir / f"nb03_frequency_curriculum{OUTPUT_SUFFIX}.json"
    npz_path = results_dir / f"nb03_frequency_curriculum{OUTPUT_SUFFIX}.npz"
    model_path = models_dir / f"nb03_frequency_curriculum{OUTPUT_SUFFIX}.pt"
    png_path = figures_dir / f"nb03_frequency_curriculum{OUTPUT_SUFFIX}.png"
    json_path.write_text(
        json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    np.savez_compressed(
        npz_path, x_lambda=x, field_pred=prediction,
        field_reference=target
    )
    torch.save({
        "model_state": model.state_dict(),
        "mode_stages": MODE_STAGES,
        "k_scales": K_SCALES,
    }, model_path)

    import matplotlib.pyplot as plt
    reference_intensity = np.abs(target) ** 2
    predicted_intensity = np.abs(prediction) ** 2
    fig, axes = plt.subplots(2, 2, figsize=(12, 7), constrained_layout=True)
    axes[0, 0].plot(x, reference_intensity, label="referencia")
    axes[0, 0].plot(x, predicted_intensity, label="PINN", alpha=0.8)
    axes[0, 0].set_title("Intensidad en z=1 lambda")
    axes[0, 0].legend()
    axes[0, 1].plot(x, np.abs(prediction - target))
    axes[0, 1].set_title("Error absoluto del campo")
    axes[1, 0].plot(
        [item["stage"] for item in stage_reports],
        [item["final_physics_loss_on_last_batch"] for item in stage_reports],
        "o-"
    )
    axes[1, 0].set_yscale("log")
    axes[1, 0].set_title("Residuo por etapa")
    axes[1, 0].set_xlabel("Etapa")
    axes[1, 1].axis("off")
    axes[1, 1].text(
        0.05, 0.92,
        f"L2 complejo: {metrics['target_complex_relative_l2']:.2%}\n"
        f"Coherencia: {metrics['target_complex_coherence']:.4f}\n"
        f"C ref/PINN: "
        f"{metrics['reference_target_statistics']['contrast']:.4f} / "
        f"{metrics['pinn_target_statistics']['contrast']:.4f}\n"
        f"Residuo independiente: "
        f"{residual_validation['normalized_rmse']:.3e}\n"
        f"Tiempo: {elapsed:.1f} s\n"
        f"Aceptado: {'si' if accepted else 'no'}",
        va="top", fontsize=12
    )
    for axis in (axes[0, 0], axes[0, 1], axes[1, 0]):
        axis.grid(alpha=0.25)
    axes[0, 0].set_xlabel("x/lambda")
    axes[0, 1].set_xlabel("x/lambda")
    fig.suptitle("NB03-D - Curriculum espectral/frecuencial")
    fig.savefig(png_path, dpi=160, bbox_inches="tight")
    plt.close(fig)

    print(f"  L2 complejo: {metrics['target_complex_relative_l2']:.4e}")
    print(f"  Coherencia compleja: {metrics['target_complex_coherence']:.4f}")
    print(
        "  Contraste C referencia/PINN: "
        f"{metrics['reference_target_statistics']['contrast']:.4f} / "
        f"{metrics['pinn_target_statistics']['contrast']:.4f}"
    )
    print(
        "  Residuo independiente RMSE: "
        f"{residual_validation['normalized_rmse']:.4e}"
    )
    print(f"  Tiempo total: {elapsed:.1f}s; aceptado: {accepted}")
    print(f"  JSON: {json_path}")


if __name__ == "__main__":
    main()
