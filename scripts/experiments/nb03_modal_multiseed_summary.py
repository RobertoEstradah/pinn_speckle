# -*- coding: utf-8 -*-
"""Consolida y verifica la validacion multisemilla de NB03 en z=1 lambda."""

from pathlib import Path
import json
import os
import sys

import numpy as np
import torch

os.environ.setdefault("MPLBACKEND", "Agg")

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.experiments import nb03_modal_pinn_siren as modal
from scripts.experiments import nb03_pinn_slabs as base


CASES = (
    (42, "_z1_corr0.10", "_z1_modal_scaled1", "_z1_modal_scaled1_finetune"),
    (123, "_z1_seed123_corr0.10", "_z1_screen123_scaled1", "_z1_screen123_scaled1_finetune"),
    (321, "_z1_seed321_corr0.10", "_z1_screen321_scaled1", "_z1_screen321_scaled1_finetune"),
    (777, "_z1_seed777_corr0.10", "_z1_screen777_scaled1", "_z1_screen777_scaled1_finetune"),
    (2026, "_z1_seed2026_corr0.10", "_z1_screen2026_scaled1", "_z1_screen2026_scaled1_finetune"),
)


def build_model(reference, model_path):
    x = reference["x_lambda"]
    kx = reference["kx"]
    active = reference["propagating_mask"].astype(bool)
    kx_active = kx[active]
    _, field0, dz0 = base.radiative_input(reference)
    field_scale = float(np.sqrt(np.mean(np.abs(field0) ** 2)))
    spectrum0 = np.fft.fft(field0 / field_scale) / len(x)
    spectrum_dz0 = np.fft.fft(dz0 / field_scale) / len(x)
    physical_phase = np.exp(-1j * kx_active * float(x[0]))
    coefficient0_complex = spectrum0[active] * physical_phase
    derivative0_complex = spectrum_dz0[active] * physical_phase
    coefficient0 = np.column_stack((
        coefficient0_complex.real, coefficient0_complex.imag
    )).astype(np.float32).reshape(-1)
    derivative0 = np.column_stack((
        derivative0_complex.real, derivative0_complex.imag
    )).astype(np.float32).reshape(-1)
    modal_amplitude = np.maximum(
        np.abs(coefficient0_complex),
        np.abs(derivative0_complex) / base.K,
    )
    floor = max(float(modal_amplitude.max()) * 1e-4, 1e-8)
    modal_amplitude = np.maximum(modal_amplitude, floor)
    correction_scale = np.repeat(
        (base.K ** 2 * modal_amplitude).astype(np.float32), 2
    )
    model = modal.ModalSiren(
        torch.tensor(coefficient0),
        torch.tensor(derivative0),
        torch.tensor(correction_scale),
        1.0,
    )
    model.load_state_dict(torch.load(
        model_path, map_location="cpu", weights_only=True
    ))
    model.eval()
    return model, field_scale, kx_active


def radiative_reference(reference):
    kx = reference["kx"]
    active = reference["propagating_mask"].astype(bool)
    spectrum = np.fft.fft(np.exp(1j * reference["phase"]))
    spectrum[~active] = 0.0
    kz = np.zeros_like(kx)
    kz[active] = np.sqrt(base.K ** 2 - kx[active] ** 2)
    return np.asarray([
        np.fft.ifft(spectrum * np.exp(1j * kz * z))
        for z in reference["z_lambda"]
    ])


def predict_all_z(model, field_scale, x, kx_active, z_values):
    with torch.no_grad():
        coefficients = model(torch.tensor(
            z_values.reshape(-1, 1), dtype=torch.float32
        )).numpy().reshape(len(z_values), -1, 2)
    phase = np.exp(1j * np.outer(x, kx_active))
    complex_coefficients = coefficients[..., 0] + 1j * coefficients[..., 1]
    return (complex_coefficients @ phase.T) * field_scale


def summary_stats(values):
    values = np.asarray(values, dtype=float)
    return {
        "mean": float(values.mean()),
        "std_population": float(values.std()),
        "minimum": float(values.min()),
        "maximum": float(values.max()),
    }


def main():
    results_dir = PROJECT_ROOT / "results"
    rows = []
    l2_curves = []
    z_common = None
    for screen_seed, reference_suffix, initial_suffix, final_suffix in CASES:
        reference_path = results_dir / (
            f"nb03_angular_spectrum_reference{reference_suffix}.npz"
        )
        final_json_path = results_dir / (
            f"nb03_modal_pinn_siren{final_suffix}.json"
        )
        initial_json_path = results_dir / (
            f"nb03_modal_pinn_siren{initial_suffix}.json"
        )
        model_path = results_dir / "models" / (
            f"nb03_modal_pinn_siren{final_suffix}.pt"
        )
        reference = dict(np.load(reference_path))
        final = json.loads(final_json_path.read_text(encoding="utf-8"))
        initial = json.loads(initial_json_path.read_text(encoding="utf-8"))
        model, field_scale, kx_active = build_model(reference, model_path)
        z_values = reference["z_lambda"].astype(float)
        prediction = predict_all_z(
            model, field_scale, reference["x_lambda"], kx_active, z_values
        )
        target = radiative_reference(reference)
        l2_z = np.linalg.norm(prediction - target, axis=1) / np.maximum(
            np.linalg.norm(target, axis=1), 1e-12
        )
        l2_curves.append(l2_z)
        z_common = z_values

        metrics = final["metrics"]
        c_ref = metrics["reference_target_statistics"]["contrast"]
        c_pred = metrics["pinn_target_statistics"]["contrast"]
        l2_final = metrics["target_complex_relative_l2"]
        contrast_error = abs(c_pred - c_ref)
        legacy_pass = l2_final < 0.05 and abs(c_pred - 1.0) < 0.1
        fidelity_pass = l2_final < 0.05 and contrast_error < 0.05
        rows.append({
            "screen_seed": screen_seed,
            "complex_l2_at_z1": l2_final,
            "complex_coherence_at_z1": metrics["target_complex_coherence"],
            "intensity_correlation_at_z1": metrics[
                "target_intensity_pearson_correlation"
            ],
            "contrast_reference": c_ref,
            "contrast_pinn": c_pred,
            "absolute_contrast_error": contrast_error,
            "residual_normalized_rmse": final[
                "independent_modal_residual"
            ]["normalized_rmse"],
            "l2_over_z_mean": float(l2_z.mean()),
            "l2_over_z_maximum": float(l2_z.max()),
            "training_seconds_initial": initial["training"]["seconds"],
            "training_seconds_finetune": final["training"]["seconds"],
            "legacy_absolute_contrast_pass": legacy_pass,
            "reference_fidelity_pass": fidelity_pass,
        })

    l2_curves = np.asarray(l2_curves)
    output = {
        "experiment": "NB03 modal PINN-SIREN five-screen validation at z=1 lambda",
        "network_seed_fixed": 42,
        "screen_seeds": [row["screen_seed"] for row in rows],
        "protocol": {
            "initial_epochs": 5000,
            "finetune_epochs": 3000,
            "initial_learning_rate": 2e-4,
            "finetune_learning_rate": 5e-5,
            "n_z_per_epoch": 256,
            "n_propagating_modes": 41,
            "interior_labels": False,
        },
        "criteria": {
            "legacy": "L2 < 0.05 and abs(C_pinn-1) < 0.1",
            "reference_fidelity": (
                "L2 < 0.05 and abs(C_pinn-C_reference) < 0.05"
            ),
            "statistical_note": (
                "C near 1 is assessed on an ensemble; an individual finite "
                "screen is assessed by agreement with its reference contrast"
            ),
        },
        "per_screen": rows,
        "aggregate": {
            "complex_l2_at_z1": summary_stats([
                row["complex_l2_at_z1"] for row in rows
            ]),
            "complex_coherence_at_z1": summary_stats([
                row["complex_coherence_at_z1"] for row in rows
            ]),
            "absolute_contrast_error": summary_stats([
                row["absolute_contrast_error"] for row in rows
            ]),
            "residual_normalized_rmse": summary_stats([
                row["residual_normalized_rmse"] for row in rows
            ]),
            "l2_over_z_mean_per_screen": summary_stats([
                row["l2_over_z_mean"] for row in rows
            ]),
            "l2_over_z_maximum_per_screen": summary_stats([
                row["l2_over_z_maximum"] for row in rows
            ]),
            "legacy_pass_count": sum(
                row["legacy_absolute_contrast_pass"] for row in rows
            ),
            "reference_fidelity_pass_count": sum(
                row["reference_fidelity_pass"] for row in rows
            ),
            "total_screens": len(rows),
        },
    }
    json_path = results_dir / "nb03_modal_multiseed_z1_summary.json"
    json_path.write_text(
        json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    np.savez_compressed(
        results_dir / "nb03_modal_multiseed_z1_l2_curves.npz",
        z_lambda=z_common,
        screen_seeds=np.asarray(output["screen_seeds"]),
        l2_curves=l2_curves,
    )

    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(9, 5.5), constrained_layout=True)
    for row, curve in zip(rows, l2_curves):
        ax.plot(z_common, 100.0 * curve, alpha=0.65,
                label=f"semilla {row['screen_seed']}")
    ax.plot(z_common, 100.0 * l2_curves.mean(axis=0), color="black",
            linewidth=2.4, label="promedio")
    ax.axhline(5.0, color="tab:red", linestyle="--", label="umbral 5 %")
    ax.set_xlabel("z/lambda")
    ax.set_ylabel("L2 complejo (%)")
    ax.set_title("NB03: error a lo largo de la propagacion")
    ax.grid(alpha=0.25)
    ax.legend(ncol=2)
    figure_path = results_dir / "figures" / "nb03_modal_multiseed_z1_l2.png"
    fig.savefig(figure_path, dpi=170, bbox_inches="tight")
    plt.close(fig)

    print(json.dumps(output["aggregate"], indent=2, ensure_ascii=False))
    print(f"JSON: {json_path}")
    print(f"PNG: {figure_path}")


if __name__ == "__main__":
    main()
