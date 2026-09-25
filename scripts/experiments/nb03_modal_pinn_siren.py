# -*- coding: utf-8 -*-
"""NB03-E: PINN-SIREN modal para Helmholtz 2D periodico.

Se expande el campo en modos Fourier transversales y una SIREN aprende todos
los coeficientes complejos como funciones de z. La condicion de Cauchy se
impone exactamente y la perdida contiene solo la EDO modal derivada de la
ecuacion completa de Helmholtz. No se usan etiquetas interiores.
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
import torch.nn as nn
from torch.func import jvp

from scripts.experiments import nb03_pinn_slabs as base


EPOCHS = int(os.environ.get("NB03_MODAL_EPOCHS", 2500))
N_Z_TRAIN = int(os.environ.get("NB03_MODAL_N_Z_TRAIN", 256))
LEARNING_RATE = float(os.environ.get("NB03_MODAL_LR", 2e-4))
FIRST_OMEGA = float(os.environ.get("NB03_MODAL_FIRST_OMEGA", 30.0))
HIDDEN_OMEGA = float(os.environ.get("NB03_MODAL_HIDDEN_OMEGA", 1.0))
HIDDEN_DIM = int(os.environ.get("NB03_MODAL_HIDDEN_DIM", 128))
NUM_LAYERS = int(os.environ.get("NB03_MODAL_NUM_LAYERS", 4))
GRAD_CLIP = float(os.environ.get("NB03_MODAL_GRAD_CLIP", 1.0))
VALIDATION_N_Z = int(os.environ.get("NB03_MODAL_VALIDATION_N_Z", 1001))
OUTPUT_SUFFIX = os.environ.get("NB03_MODAL_OUTPUT_SUFFIX", "_z1_modal1")
RESUME_MODEL = os.environ.get("NB03_MODAL_RESUME_MODEL", "")


class SineLayer(nn.Module):
    def __init__(self, in_features, out_features, omega, first=False):
        super().__init__()
        self.linear = nn.Linear(in_features, out_features)
        self.omega = float(omega)
        with torch.no_grad():
            if first:
                bound = 1.0 / in_features
            else:
                bound = np.sqrt(6.0 / in_features) / self.omega
            self.linear.weight.uniform_(-bound, bound)
            nn.init.zeros_(self.linear.bias)

    def forward(self, values):
        return torch.sin(self.omega * self.linear(values))


class ModalSiren(nn.Module):
    def __init__(self, coefficient0, derivative0, correction_scale, distance):
        super().__init__()
        self.distance = float(distance)
        n_outputs = int(coefficient0.numel())
        layers = [SineLayer(1, HIDDEN_DIM, FIRST_OMEGA, first=True)]
        for _ in range(NUM_LAYERS - 1):
            layers.append(SineLayer(
                HIDDEN_DIM, HIDDEN_DIM, HIDDEN_OMEGA
            ))
        final = nn.Linear(HIDDEN_DIM, n_outputs)
        # Comenzar desde la prolongacion lineal impuesta por Cauchy. Una
        # salida aleatoria comun a todos los modos introduce energia espuria
        # en los coeficientes debiles antes del primer paso de optimizacion.
        nn.init.zeros_(final.weight)
        nn.init.zeros_(final.bias)
        layers.append(final)
        self.net = nn.Sequential(*layers)
        self.register_buffer("coefficient0", coefficient0.reshape(1, -1))
        self.register_buffer("derivative0", derivative0.reshape(1, -1))
        self.register_buffer(
            "correction_scale", correction_scale.reshape(1, -1)
        )

    def forward(self, z):
        normalized_z = 2.0 * z / self.distance - 1.0
        correction = self.correction_scale * self.net(normalized_z)
        return (
            self.coefficient0
            + z * self.derivative0
            + z.square() * correction
        )


def modal_residual(model, z, kz_squared):
    tangent = torch.ones_like(z)

    def first_derivative(values):
        return jvp(model, (values,), (torch.ones_like(values),))[1]

    coefficients, _ = jvp(model, (z,), (tangent,))
    _, second = jvp(first_derivative, (z,), (tangent,))
    batch = z.shape[0]
    coefficients = coefficients.reshape(batch, -1, 2)
    second = second.reshape(batch, -1, 2)
    return second + kz_squared.reshape(1, -1, 1) * coefficients


def coefficients_to_field(coefficients, x, kx_active):
    phase = np.exp(1j * np.outer(x, kx_active))
    complex_coefficients = coefficients[:, 0] + 1j * coefficients[:, 1]
    return phase @ complex_coefficients


def main():
    if abs(base.DISTANCE_LAMBDA - 1.0) > 1e-12:
        raise ValueError("Este piloto requiere NB03_DISTANCE_LAMBDA=1.")
    base.set_seed(base.SEED)
    rng = np.random.RandomState(base.SEED)
    reference = base.load_reference()
    x = reference["x_lambda"]
    kx = reference["kx"]
    active = reference["propagating_mask"].astype(bool)
    kx_active = kx[active]
    kz_squared_np = np.maximum(base.K ** 2 - kx_active ** 2, 0.0)

    field0, dz0, = base.radiative_input(reference)[1:]
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

    # Escala modal para la correccion z^2 N. Para una onda saliente, el
    # primer termino requerido por Helmholtz es -kz^2*a(0)/2; por ello se
    # usa k^2 por la amplitud de cada modo. El piso evita divisiones por cero
    # sin permitir que modos espectralmente despreciables dominen la salida.
    modal_amplitude = np.maximum(
        np.abs(coefficient0_complex),
        np.abs(derivative0_complex) / base.K,
    )
    amplitude_floor = max(float(modal_amplitude.max()) * 1e-4, 1e-8)
    modal_amplitude = np.maximum(modal_amplitude, amplitude_floor)
    correction_scale_complex = base.K ** 2 * modal_amplitude
    correction_scale = np.repeat(
        correction_scale_complex.astype(np.float32), 2
    )

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = ModalSiren(
        torch.tensor(coefficient0, device=device),
        torch.tensor(derivative0, device=device),
        torch.tensor(correction_scale, device=device),
        base.DISTANCE_LAMBDA,
    ).to(device)
    if RESUME_MODEL:
        resume_path = Path(RESUME_MODEL)
        if not resume_path.is_absolute():
            resume_path = PROJECT_ROOT / resume_path
        model.load_state_dict(torch.load(
            resume_path, map_location=device, weights_only=True
        ))
    kz_squared = torch.tensor(
        kz_squared_np, dtype=torch.float32, device=device
    )
    residual_scale = torch.tensor(
        (base.K ** 2 * modal_amplitude).astype(np.float32),
        device=device,
    ).reshape(1, -1, 1)
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
        optimizer, T_max=max(EPOCHS, 1), eta_min=LEARNING_RATE * 0.02
    )
    best_loss = float("inf")
    best_state = None
    t0 = time.time()
    print("NB03-E: PINN-SIREN modal")
    print(f"  Dispositivo: {device}; modos complejos: {len(kx_active)}")

    for epoch in range(EPOCHS):
        z = torch.tensor(
            rng.uniform(0.0, base.DISTANCE_LAMBDA, (N_Z_TRAIN, 1)),
            dtype=torch.float32, device=device
        )
        optimizer.zero_grad()
        residual = modal_residual(model, z, kz_squared)
        loss = torch.mean((residual / residual_scale).square())
        if not torch.isfinite(loss):
            raise FloatingPointError(f"Perdida no finita en epoca {epoch}.")
        loss.backward()
        if GRAD_CLIP > 0:
            torch.nn.utils.clip_grad_norm_(model.parameters(), GRAD_CLIP)
        optimizer.step()
        scheduler.step()
        value = float(loss.detach().cpu())
        if value < best_loss:
            best_loss = value
            best_state = copy.deepcopy(model.state_dict())
        if (epoch + 1) % 500 == 0:
            print(f"  Epoca {epoch + 1}/{EPOCHS}: loss={value:.3e}")

    if best_state is not None:
        model.load_state_dict(best_state)
    training_seconds = time.time() - t0

    z_validation = torch.linspace(
        0.0, base.DISTANCE_LAMBDA, VALIDATION_N_Z,
        dtype=torch.float32, device=device
    ).reshape(-1, 1)
    residual = modal_residual(model, z_validation, kz_squared)
    normalized = (
        residual / residual_scale
    ).detach().cpu().numpy()
    residual_report = {
        "n_z": VALIDATION_N_Z,
        "normalized_mse": float(np.mean(normalized ** 2)),
        "normalized_rmse": float(np.sqrt(np.mean(normalized ** 2))),
        "normalized_max_abs": float(np.max(np.abs(normalized))),
    }

    with torch.no_grad():
        coefficient_prediction = model(torch.tensor(
            [[base.DISTANCE_LAMBDA]], dtype=torch.float32, device=device
        )).cpu().numpy().reshape(-1, 2)
        coefficient_lower = model(torch.tensor(
            [[0.0]], dtype=torch.float32, device=device
        )).cpu().numpy().reshape(-1, 2)
    prediction = coefficients_to_field(
        coefficient_prediction, x, kx_active
    ) * field_scale
    reconstructed_lower = coefficients_to_field(
        coefficient_lower, x, kx_active
    ) * field_scale
    target_index = int(np.argmin(np.abs(
        reference["z_lambda"] - base.DISTANCE_LAMBDA
    )))
    target = reference["field_all_z"][target_index]
    metrics = base.complex_field_metrics(prediction, target)
    metrics["reference_target_statistics"] = base.intensity_statistics(target)
    metrics["pinn_target_statistics"] = base.intensity_statistics(prediction)
    metrics["hard_boundary_field_rmse"] = float(np.sqrt(np.mean(
        np.abs(reconstructed_lower - field0) ** 2
    )))
    contrast_reference_error = abs(
        metrics["pinn_target_statistics"]["contrast"]
        - metrics["reference_target_statistics"]["contrast"]
    )
    legacy_accepted = (
        metrics["target_complex_relative_l2"] < 0.05
        and abs(metrics["pinn_target_statistics"]["contrast"] - 1.0) < 0.1
    )
    accepted = (
        metrics["target_complex_relative_l2"] < 0.05
        and contrast_reference_error < 0.05
    )

    output = {
        "experiment": "NB03-E modal PINN-SIREN for full 2D Helmholtz",
        "seed": base.SEED,
        "reference_seed": (
            int(reference["reference_seed"])
            if "reference_seed" in reference else None
        ),
        "device": str(device),
        "representation": {
            "equation": "a_m''(z) + (k^2-kx_m^2) a_m(z) = 0",
            "field": "sum_m a_m(z) exp(i kx_m x)",
            "n_complex_modes": int(len(kx_active)),
            "hard_cauchy": "a0 + z*a0_prime + z^2*N_theta(z)",
            "interior_labels": False,
            "mode_conditioning": (
                "output scaled by k^2 times boundary modal amplitude; "
                "residual normalized by the same modal scale"
            ),
            "modal_amplitude_floor": amplitude_floor,
        },
        "architecture": {
            "hidden_dim": HIDDEN_DIM,
            "num_hidden_layers": NUM_LAYERS,
            "first_omega": FIRST_OMEGA,
            "hidden_omega": HIDDEN_OMEGA,
            "real_outputs": int(2 * len(kx_active)),
        },
        "training": {
            "epochs": EPOCHS,
            "n_z_per_epoch": N_Z_TRAIN,
            "learning_rate": LEARNING_RATE,
            "gradient_clip": GRAD_CLIP,
            "seconds": training_seconds,
            "best_training_loss": best_loss,
            "resume_model": RESUME_MODEL or None,
        },
        "independent_modal_residual": residual_report,
        "metrics": metrics,
        "acceptance": {
            "complex_l2_below_5_percent":
                metrics["target_complex_relative_l2"] < 0.05,
            "legacy_contrast_distance_from_one_below_0_1":
                abs(metrics["pinn_target_statistics"]["contrast"] - 1.0) < 0.1,
            "contrast_reference_absolute_error": contrast_reference_error,
            "contrast_reference_error_below_0_05":
                contrast_reference_error < 0.05,
            "legacy_accepted": legacy_accepted,
            "accepted": accepted,
            "criterion_note": (
                "C near one is an ensemble speckle criterion; an individual "
                "screen is judged by agreement with its reference contrast"
            ),
        },
        "status": "diagnostic spectral PINN; angular spectrum used only for evaluation",
    }

    results_dir = PROJECT_ROOT / "results"
    figures_dir = results_dir / "figures"
    models_dir = results_dir / "models"
    figures_dir.mkdir(parents=True, exist_ok=True)
    models_dir.mkdir(parents=True, exist_ok=True)
    json_path = results_dir / f"nb03_modal_pinn_siren{OUTPUT_SUFFIX}.json"
    npz_path = results_dir / f"nb03_modal_pinn_siren{OUTPUT_SUFFIX}.npz"
    model_path = models_dir / f"nb03_modal_pinn_siren{OUTPUT_SUFFIX}.pt"
    png_path = figures_dir / f"nb03_modal_pinn_siren{OUTPUT_SUFFIX}.png"
    json_path.write_text(
        json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    np.savez_compressed(
        npz_path, x_lambda=x, field_pred=prediction,
        field_reference=target, kx_active=kx_active
    )
    torch.save(model.state_dict(), model_path)

    import matplotlib.pyplot as plt
    reference_intensity = np.abs(target) ** 2
    predicted_intensity = np.abs(prediction) ** 2
    fig, axes = plt.subplots(2, 2, figsize=(12, 7), constrained_layout=True)
    axes[0, 0].plot(x, reference_intensity, label="referencia")
    axes[0, 0].plot(x, predicted_intensity, label="PINN modal", alpha=0.8)
    axes[0, 0].set_title("Intensidad en z=1 lambda")
    axes[0, 0].legend()
    axes[0, 1].plot(x, np.abs(prediction - target))
    axes[0, 1].set_title("Error absoluto del campo")
    axes[1, 0].plot(x, np.unwrap(np.angle(target)), label="referencia")
    axes[1, 0].plot(x, np.unwrap(np.angle(prediction)), label="PINN modal")
    axes[1, 0].set_title("Fase")
    axes[1, 0].legend()
    axes[1, 1].axis("off")
    axes[1, 1].text(
        0.05, 0.92,
        f"L2 complejo: {metrics['target_complex_relative_l2']:.2%}\n"
        f"Coherencia: {metrics['target_complex_coherence']:.4f}\n"
        f"C ref/PINN: "
        f"{metrics['reference_target_statistics']['contrast']:.4f} / "
        f"{metrics['pinn_target_statistics']['contrast']:.4f}\n"
        f"Residuo modal: {residual_report['normalized_rmse']:.3e}\n"
        f"Tiempo: {training_seconds:.1f} s\n"
        f"Aceptado: {'si' if accepted else 'no'}",
        va="top", fontsize=12
    )
    for axis in (axes[0, 0], axes[0, 1], axes[1, 0]):
        axis.grid(alpha=0.25)
        axis.set_xlabel("x/lambda")
    fig.suptitle("NB03-E - PINN-SIREN modal")
    fig.savefig(png_path, dpi=160, bbox_inches="tight")
    plt.close(fig)

    print(f"  L2 complejo: {metrics['target_complex_relative_l2']:.4e}")
    print(f"  Coherencia compleja: {metrics['target_complex_coherence']:.4f}")
    print(
        "  Contraste C referencia/PINN: "
        f"{metrics['reference_target_statistics']['contrast']:.4f} / "
        f"{metrics['pinn_target_statistics']['contrast']:.4f}"
    )
    print(f"  Residuo modal RMSE: {residual_report['normalized_rmse']:.4e}")
    print(f"  Tiempo: {training_seconds:.1f}s; aceptado: {accepted}")
    print(f"  JSON: {json_path}")


if __name__ == "__main__":
    main()
