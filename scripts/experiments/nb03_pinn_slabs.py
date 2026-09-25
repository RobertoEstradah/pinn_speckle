# -*- coding: utf-8 -*-
"""
NB03-C - PINN-SIREN por bloques de propagacion
================================================

Este experimento mantiene la ecuacion de Helmholtz 2D de la tesis, pero evita
resolver de una sola vez el dominio completo de 20 lambda. El eje longitudinal
se divide en bloques cortos. Cada red local recibe el campo complejo y su
derivada normal en la interfaz inferior, satisface Helmholtz en el bloque y
transfiere campo/derivada a la interfaz siguiente.

La referencia de campo es NB03-A (espectro angular). No se usan valores del
campo de referencia en el interior del dominio: solo la primera condicion de
entrada radiativa se toma de la pantalla, y las interfaces posteriores se
obtienen de la PINN del bloque anterior.

La normalizacion de coordenadas es local por bloque. Las derivadas se calculan
respecto a las coordenadas fisicas x/lambda y z/lambda, aplicando la regla de
la cadena dentro de NormalizedSiren2D.
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

try:
    import torch
    import torch.nn as nn
except ModuleNotFoundError as exc:  # pragma: no cover
    raise SystemExit("Este experimento requiere PyTorch.") from exc

from src.models import PINN_2D_SIREN, Sine


SEED = int(os.environ.get("NB03_SEED", 42))
K = 2.0 * np.pi
WIDTH_LAMBDA = 20.0
DISTANCE_LAMBDA = float(os.environ.get("NB03_DISTANCE_LAMBDA", 20.0))
SLAB_WIDTH = float(os.environ.get("NB03_SLAB_WIDTH", 4.0))
N_COLLOC = int(os.environ.get("NB03_SLAB_N_COLLOC", 2500))
N_PERIODIC = int(os.environ.get("NB03_SLAB_N_PERIODIC", 256))
N_EPOCHS = int(os.environ.get("NB03_SLAB_N_EPOCHS", 1200))
LEARNING_RATE = float(os.environ.get("NB03_SLAB_LR", 1e-3))
LAMBDA_DZ = float(os.environ.get("NB03_SLAB_LAMBDA_DZ", 1.0))
LAMBDA_PERIODIC = float(os.environ.get("NB03_SLAB_LAMBDA_PERIODIC", 1.0))
LAMBDA_PHYS = float(os.environ.get("NB03_SLAB_LAMBDA_PHYS", 1.0))
PATIENCE = int(os.environ.get("NB03_SLAB_PATIENCE", 350))
BOUNDARY_PRETRAIN_EPOCHS = int(os.environ.get(
    "NB03_SLAB_BOUNDARY_PRETRAIN_EPOCHS", 0
))
PHYSICS_RAMP_EPOCHS = int(os.environ.get(
    "NB03_SLAB_PHYSICS_RAMP_EPOCHS", 0
))
ADAPTIVE_RESIDUAL = os.environ.get(
    "NB03_SLAB_ADAPTIVE_RESIDUAL", "0"
).lower() in {"1", "true", "yes"}
ADAPTIVE_INTERVAL = int(os.environ.get(
    "NB03_SLAB_ADAPTIVE_INTERVAL", 100
))
ADAPTIVE_POOL_FACTOR = int(os.environ.get(
    "NB03_SLAB_ADAPTIVE_POOL_FACTOR", 4
))
ADAPTIVE_TOP_FRACTION = float(os.environ.get(
    "NB03_SLAB_ADAPTIVE_TOP_FRACTION", 0.3
))
GRAD_CLIP_NORM = float(os.environ.get(
    "NB03_SLAB_GRAD_CLIP_NORM", 1.0
))
LBFGS_MAX_ITER = int(os.environ.get("NB03_SLAB_LBFGS_MAX_ITER", 100))
HIDDEN_DIM = int(os.environ.get("NB03_SLAB_HIDDEN_DIM", 128))
NUM_LAYERS = int(os.environ.get("NB03_SLAB_NUM_LAYERS", 5))
OMEGA_0 = float(os.environ.get("NB03_SLAB_OMEGA_0", 30.0))
INPUT_ENCODING = os.environ.get("NB03_SLAB_INPUT_ENCODING", "raw").lower()
FOURIER_MODES = int(os.environ.get("NB03_SLAB_FOURIER_MODES", 20))
USE_HARD_BOUNDARY = os.environ.get(
    "NB03_SLAB_HARD_BOUNDARY", "0"
).lower() in {"1", "true", "yes"}
OUTPUT_SUFFIX = os.environ.get("NB03_OUTPUT_SUFFIX", "")
REFERENCE_SUFFIX = os.environ.get("NB03_REFERENCE_SUFFIX", "")


def set_seed(seed):
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False


class NormalizedSiren2D(nn.Module):
    """SIREN que recibe coordenadas fisicas y normaliza cada bloque."""

    def __init__(self, z0, z1, hidden_dim=HIDDEN_DIM,
                 num_layers=NUM_LAYERS, omega_0=OMEGA_0):
        super().__init__()
        self.z0 = float(z0)
        self.z1 = float(z1)
        self.x_half = WIDTH_LAMBDA / 2.0
        self.z_half = max((self.z1 - self.z0) / 2.0, 1e-8)
        self.z_center = (self.z1 + self.z0) / 2.0
        self.net = PINN_2D_SIREN(
            hidden_dim=hidden_dim, num_layers=num_layers, omega_0=omega_0
        )

    def normalize(self, coordinates):
        x = coordinates[:, 0:1] / self.x_half
        z = (coordinates[:, 1:2] - self.z_center) / self.z_half
        return torch.cat((x, z), dim=1)

    def forward(self, coordinates):
        return self.net(self.normalize(coordinates))


class PeriodicSirenCore(nn.Module):
    """SIREN con codificación periódica de x y normalización local de z."""

    def __init__(self, z0, z1, hidden_dim=HIDDEN_DIM,
                 num_layers=NUM_LAYERS, omega_0=OMEGA_0):
        super().__init__()
        self.z0 = float(z0)
        self.z1 = float(z1)
        self.z_half = max((self.z1 - self.z0) / 2.0, 1e-8)
        self.z_center = (self.z1 + self.z0) / 2.0
        self.omega_0 = omega_0
        self.hidden_dim = hidden_dim
        layers = [nn.Linear(3, hidden_dim), Sine(omega_0=omega_0)]
        for _ in range(num_layers - 1):
            layers += [nn.Linear(hidden_dim, hidden_dim),
                       Sine(omega_0=omega_0)]
        layers.append(nn.Linear(hidden_dim, 2))
        self.net = nn.Sequential(*layers)
        self._init_weights()

    def _init_weights(self):
        with torch.no_grad():
            for index, layer in enumerate(self.net):
                if isinstance(layer, nn.Linear):
                    n_in = layer.weight.shape[1]
                    if index == 0:
                        layer.weight.uniform_(-1 / n_in, 1 / n_in)
                    else:
                        bound = np.sqrt(6 / n_in) / self.omega_0
                        layer.weight.uniform_(-bound, bound)
                    nn.init.zeros_(layer.bias)

    def forward(self, coordinates):
        x = coordinates[:, 0:1]
        z = (coordinates[:, 1:2] - self.z_center) / self.z_half
        phase = 2.0 * np.pi * x / WIDTH_LAMBDA
        features = torch.cat((torch.sin(phase), torch.cos(phase), z), dim=1)
        return self.net(features)


class FourierFeatureSiren2D(nn.Module):
    """SIREN con codificacion de modos transversales hasta |kx| <= k."""

    def __init__(self, z0, z1, hidden_dim=HIDDEN_DIM,
                 num_layers=NUM_LAYERS, omega_0=OMEGA_0,
                 n_modes=FOURIER_MODES):
        super().__init__()
        self.z0 = float(z0)
        self.z1 = float(z1)
        self.z_half = max((self.z1 - self.z0) / 2.0, 1e-8)
        self.z_center = (self.z1 + self.z0) / 2.0
        self.omega_0 = omega_0
        self.hidden_dim = hidden_dim
        self.n_modes = n_modes
        self.register_buffer(
            "mode_mask", torch.ones(n_modes, dtype=torch.float32)
        )
        input_dim = 2 * n_modes + 1
        layers = [nn.Linear(input_dim, hidden_dim), Sine(omega_0=omega_0)]
        for _ in range(num_layers - 1):
            layers += [nn.Linear(hidden_dim, hidden_dim),
                       Sine(omega_0=omega_0)]
        layers.append(nn.Linear(hidden_dim, 2))
        self.net = nn.Sequential(*layers)
        self._init_weights()

    def _init_weights(self):
        with torch.no_grad():
            for index, layer in enumerate(self.net):
                if isinstance(layer, nn.Linear):
                    n_in = layer.weight.shape[1]
                    if index == 0:
                        layer.weight.uniform_(-1 / n_in, 1 / n_in)
                    else:
                        bound = np.sqrt(6 / n_in) / self.omega_0
                        layer.weight.uniform_(-bound, bound)
                    nn.init.zeros_(layer.bias)

    def forward(self, coordinates):
        x = coordinates[:, 0:1]
        z = (coordinates[:, 1:2] - self.z_center) / self.z_half
        features = [z]
        for mode in range(1, self.n_modes + 1):
            phase = 2.0 * np.pi * mode * x / WIDTH_LAMBDA
            weight = self.mode_mask[mode - 1]
            features.extend((weight * torch.sin(phase),
                             weight * torch.cos(phase)))
        return self.net(torch.cat(features, dim=1))

    def set_active_modes(self, active_modes):
        active_modes = min(max(int(active_modes), 0), self.n_modes)
        mask = torch.zeros_like(self.mode_mask)
        mask[:active_modes] = 1.0
        self.mode_mask.copy_(mask)


class SpectralBoundary(nn.Module):
    """Interpolacion periodica diferenciable de un dato de interfaz."""

    def __init__(self, values, x_grid, kx, propagating_mask, device):
        super().__init__()
        active_kx = kx[propagating_mask]
        self.x_origin = float(x_grid[0])
        self.n_grid = int(len(x_grid))
        self.mode_indices = np.flatnonzero(propagating_mask)
        self.register_buffer(
            "kx", torch.tensor(active_kx, dtype=torch.float32, device=device)
        )
        self.register_buffer(
            "coefficients",
            torch.zeros(len(active_kx), dtype=torch.complex64, device=device)
        )
        self.set_values(values)

    def set_values(self, values):
        complex_values = values[:, 0] + 1j * values[:, 1]
        spectrum = np.fft.fft(complex_values) / self.n_grid
        coefficients = spectrum[self.mode_indices] * np.exp(
            -1j * self.kx.detach().cpu().numpy() * self.x_origin
        )
        values_tensor = torch.tensor(
            coefficients, dtype=torch.complex64,
            device=self.coefficients.device
        )
        self.coefficients.copy_(values_tensor)

    def forward(self, coordinates):
        x = coordinates[:, 0:1]
        phase = torch.exp(1j * x * self.kx.reshape(1, -1))
        values = phase @ self.coefficients.reshape(-1, 1)
        return torch.cat((values.real, values.imag), dim=1)


class HardBoundarySiren2D(nn.Module):
    """PINN por bloques con E y dE/dz exactos en la interfaz inferior."""

    def __init__(self, z0, z1, lower_field, lower_dz, x_grid, kx,
                 propagating_mask):
        super().__init__()
        self.z0 = float(z0)
        self.value_boundary = SpectralBoundary(
            lower_field, x_grid, kx, propagating_mask, torch.device("cpu")
        )
        self.dz_boundary = SpectralBoundary(
            lower_dz, x_grid, kx, propagating_mask, torch.device("cpu")
        )
        # El speckle contiene todos los modos transversales propagantes.
        # Cuando se solicita codificacion Fourier, la correccion de Cauchy
        # recibe esos modos explicitamente; la frontera sigue siendo exacta.
        if INPUT_ENCODING == "fourier":
            self.core = FourierFeatureSiren2D(z0, z1)
        else:
            self.core = PeriodicSirenCore(z0, z1)

    def forward(self, coordinates):
        value = self.value_boundary(coordinates)
        derivative = self.dz_boundary(coordinates)
        correction = self.core(coordinates)
        distance = coordinates[:, 1:2] - self.z0
        return value + distance * derivative + distance.square() * correction

    def set_boundary(self, lower_field, lower_dz):
        self.value_boundary.set_values(lower_field)
        self.dz_boundary.set_values(lower_dz)

    def set_active_modes(self, active_modes):
        if hasattr(self.core, "set_active_modes"):
            self.core.set_active_modes(active_modes)


def project_to_propagating(values, x_grid, kx, propagating_mask):
    """Elimina modos no propagantes antes de transferir una interfaz."""
    complex_values = values[:, 0] + 1j * values[:, 1]
    spectrum = np.fft.fft(complex_values)
    spectrum[~propagating_mask] = 0.0
    field = np.fft.ifft(spectrum)
    return np.column_stack((field.real, field.imag))


def component_gradient(output, coordinates, component):
    return torch.autograd.grad(
        output[:, component:component + 1], coordinates,
        grad_outputs=torch.ones_like(output[:, component:component + 1]),
        create_graph=True, retain_graph=True
    )[0]


def helmholtz_residual(model, coordinates, wave_number=K):
    coordinates = coordinates.clone().requires_grad_(True)
    output = model(coordinates)
    residuals = []
    for component in (0, 1):
        gradient = component_gradient(output, coordinates, component)
        d2x = torch.autograd.grad(
            gradient[:, 0:1], coordinates,
            grad_outputs=torch.ones_like(gradient[:, 0:1]),
            create_graph=True, retain_graph=True
        )[0][:, 0:1]
        d2z = torch.autograd.grad(
            gradient[:, 1:2], coordinates,
            grad_outputs=torch.ones_like(gradient[:, 1:2]),
            create_graph=True, retain_graph=True
        )[0][:, 1:2]
        residuals.append(
            d2x + d2z + wave_number ** 2 * output[:, component:component + 1]
        )
    return residuals[0], residuals[1]


def derivative_z(model, points):
    points = points.clone().requires_grad_(True)
    output = model(points)
    components = []
    for component in (0, 1):
        components.append(component_gradient(output, points, component)[:, 1:2])
    return output, torch.cat(components, dim=1)


def load_reference():
    path = PROJECT_ROOT / "results" / (
        f"nb03_angular_spectrum_reference{REFERENCE_SUFFIX}.npz"
    )
    if not path.exists():
        raise FileNotFoundError(
            "Ejecuta primero scripts/experiments/nb03_angular_spectrum_reference.py."
        )
    return dict(np.load(path))


def radiative_input(reference):
    x = reference["x_lambda"]
    kx = reference["kx"]
    phase = reference["phase"]
    propagating = reference["propagating_mask"].astype(bool)
    spectrum = np.fft.fft(np.exp(1j * phase))
    kz = np.zeros_like(kx, dtype=float)
    kz[propagating] = np.sqrt(K ** 2 - kx[propagating] ** 2)
    radiative_spectrum = np.where(propagating, spectrum, 0.0)
    field0 = np.fft.ifft(radiative_spectrum)
    dz0 = np.fft.ifft(1j * kz * radiative_spectrum)
    return x, field0, dz0


def points_for_slab(z0, z1, rng, x_input):
    collocation = np.column_stack((
        rng.uniform(-WIDTH_LAMBDA / 2.0, WIDTH_LAMBDA / 2.0, N_COLLOC),
        rng.uniform(z0, z1, N_COLLOC),
    ))
    z_periodic = np.linspace(z0, z1, N_PERIODIC)
    left = np.column_stack((np.full(N_PERIODIC, -WIDTH_LAMBDA / 2.0), z_periodic))
    right = np.column_stack((np.full(N_PERIODIC, WIDTH_LAMBDA / 2.0), z_periodic))
    lower = np.column_stack((
        x_input,
        np.full(len(x_input), z0),
    ))
    return {
        "collocation": collocation,
        "left": left,
        "right": right,
        "lower": lower,
    }


def to_tensors(points, lower_field, lower_dz, device):
    result = {
        key: torch.tensor(value, dtype=torch.float32, device=device)
        for key, value in points.items()
    }
    result["lower_target"] = torch.tensor(
        lower_field, dtype=torch.float32, device=device
    )
    result["lower_dz_target"] = torch.tensor(
        lower_dz, dtype=torch.float32, device=device
    )
    return result


def slab_loss(model, tensors, lambda_dz=None, lambda_periodic=None,
              lambda_phys=None, wave_number=K):
    lambda_dz = LAMBDA_DZ if lambda_dz is None else lambda_dz
    lambda_periodic = (
        LAMBDA_PERIODIC if lambda_periodic is None else lambda_periodic
    )
    lambda_phys = LAMBDA_PHYS if lambda_phys is None else lambda_phys
    lower = tensors["lower"].clone().requires_grad_(True)
    target = tensors["lower_target"]
    target_dz = tensors["lower_dz_target"]
    prediction = model(lower)
    value_loss = torch.mean((prediction - target) ** 2)

    dz_parts = []
    for component in (0, 1):
        dz_parts.append(component_gradient(prediction, lower, component)[:, 1:2])
    prediction_dz = torch.cat(dz_parts, dim=1)
    derivative_scale = max(float(wave_number), 1e-8)
    dz_loss = torch.mean(
        ((prediction_dz - target_dz) / derivative_scale) ** 2
    )

    left = tensors["left"].clone().requires_grad_(True)
    right = tensors["right"].clone().requires_grad_(True)
    left_value = model(left)
    right_value = model(right)
    periodic_value_loss = torch.mean((left_value - right_value) ** 2)
    left_dx = []
    right_dx = []
    for component in (0, 1):
        left_dx.append(component_gradient(left_value, left, component)[:, 0:1])
        right_dx.append(component_gradient(right_value, right, component)[:, 0:1])
    periodic_derivative_loss = torch.mean((
        (torch.cat(left_dx, dim=1) - torch.cat(right_dx, dim=1))
        / derivative_scale
    ) ** 2)
    periodic_loss = periodic_value_loss + periodic_derivative_loss

    residual_real, residual_imag = helmholtz_residual(
        model, tensors["collocation"], wave_number=wave_number
    )
    physics_loss = (torch.mean(residual_real ** 2) +
                    torch.mean(residual_imag ** 2)) / derivative_scale ** 4
    total = value_loss + lambda_dz * dz_loss
    total = total + lambda_periodic * periodic_loss
    total = total + lambda_phys * physics_loss
    return total, value_loss, dz_loss, periodic_loss, physics_loss


def adapt_collocation(model, tensors, rng, device):
    """Conserva puntos de alto residuo y una fraccion aleatoria de control."""
    n_points = tensors["collocation"].shape[0]
    n_candidates = max(n_points * ADAPTIVE_POOL_FACTOR, n_points)
    candidates = np.column_stack((
        rng.uniform(-WIDTH_LAMBDA / 2.0, WIDTH_LAMBDA / 2.0, n_candidates),
        rng.uniform(
            float(tensors["collocation"][:, 1].min().cpu()),
            float(tensors["collocation"][:, 1].max().cpu()),
            n_candidates,
        ),
    ))
    candidate_tensor = torch.tensor(
        candidates, dtype=torch.float32, device=device
    )
    residual_real, residual_imag = helmholtz_residual(
        model, candidate_tensor
    )
    scores = (
        residual_real.detach().cpu().numpy().ravel() ** 2
        + residual_imag.detach().cpu().numpy().ravel() ** 2
    )
    top_fraction = min(max(ADAPTIVE_TOP_FRACTION, 0.0), 1.0)
    n_top = max(1, int(top_fraction * n_points))
    top_indices = np.argpartition(scores, -n_top)[-n_top:]
    remaining = np.setdiff1d(
        np.arange(n_candidates), top_indices, assume_unique=False
    )
    random_indices = rng.choice(
        remaining, size=n_points - n_top, replace=False
    )
    selected = candidates[np.concatenate((top_indices, random_indices))]
    tensors["collocation"] = torch.tensor(
        selected, dtype=torch.float32, device=device
    )


def evaluate(model, points, device):
    tensor = torch.tensor(points, dtype=torch.float32, device=device)
    with torch.no_grad():
        return model(tensor).cpu().numpy()


def evaluate_with_dz(model, points, device):
    tensor = torch.tensor(points, dtype=torch.float32, device=device)
    value, dz = derivative_z(model, tensor)
    return value.detach().cpu().numpy(), dz.detach().cpu().numpy()


def relative_l2(predicted, reference):
    return float(np.linalg.norm(predicted - reference) /
                 max(np.linalg.norm(reference), 1e-12))


def complex_field_metrics(predicted, reference):
    """Separa error de campo, coherencia, fase y error de intensidad."""
    predicted_norm = max(np.linalg.norm(predicted), 1e-12)
    reference_norm = max(np.linalg.norm(reference), 1e-12)
    coherence = abs(np.vdot(reference, predicted)) / (
        reference_norm * predicted_norm
    )
    phase_shift = float(np.angle(np.vdot(predicted, reference)))
    phase_aligned = predicted * np.exp(1j * phase_shift)
    reference_intensity = np.abs(reference) ** 2
    predicted_intensity = np.abs(predicted) ** 2
    return {
        "target_complex_relative_l2": relative_l2(predicted, reference),
        "target_real_relative_l2": relative_l2(
            predicted.real, reference.real
        ),
        "target_imag_relative_l2": relative_l2(
            predicted.imag, reference.imag
        ),
        "target_phase_aligned_relative_l2": relative_l2(
            phase_aligned, reference
        ),
        "target_complex_coherence": float(coherence),
        "target_global_phase_shift_rad": phase_shift,
        "target_intensity_relative_l2": relative_l2(
            predicted_intensity, reference_intensity
        ),
        "target_intensity_pearson_correlation": float(np.corrcoef(
            reference_intensity, predicted_intensity
        )[0, 1]),
    }


def intensity_statistics(field):
    intensity = np.abs(field) ** 2
    mean = float(intensity.mean())
    return {
        "mean_intensity": mean,
        "std_intensity": float(intensity.std()),
        "contrast": float(intensity.std() / max(mean, 1e-12)),
    }


def main():
    set_seed(SEED)
    reference = load_reference()
    x = reference["x_lambda"]
    kx = reference["kx"]
    propagating_mask = reference["propagating_mask"].astype(bool)
    z_reference = reference["z_lambda"]
    reference_fields = reference["field_all_z"]
    target_reference_index = int(np.argmin(
        np.abs(z_reference - DISTANCE_LAMBDA)
    ))
    target_field = reference_fields[target_reference_index]
    x_input, input_field, input_dz = radiative_input(reference)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    rng = np.random.RandomState(SEED)
    field_scale = float(np.sqrt(np.mean(np.abs(input_field) ** 2)))
    input_field_scaled = input_field / field_scale
    input_dz_scaled = input_dz / field_scale

    n_slabs = int(np.ceil(DISTANCE_LAMBDA / SLAB_WIDTH))
    slab_edges = np.linspace(0.0, DISTANCE_LAMBDA, n_slabs + 1)
    predicted_fields = []
    slab_reports = []
    saved_states = []
    lower_field = np.column_stack((input_field_scaled.real,
                                   input_field_scaled.imag))
    lower_dz = np.column_stack((input_dz_scaled.real,
                                input_dz_scaled.imag))
    t_global = time.time()

    print("NB03-C: PINN-SIREN por bloques de propagacion")
    print(f"  Dispositivo: {device}")
    print(f"  Bloques: {n_slabs}; ancho: {SLAB_WIDTH:.2f} lambda")
    print(f"  Colocacion/bloque: {N_COLLOC}; periodicidad: {N_PERIODIC}")

    for slab_index in range(n_slabs):
        z0 = float(slab_edges[slab_index])
        z1 = float(slab_edges[slab_index + 1])
        if USE_HARD_BOUNDARY:
            model = HardBoundarySiren2D(
                z0, z1, lower_field, lower_dz, x_input, kx,
                propagating_mask
            ).to(device)
        elif INPUT_ENCODING == "fourier":
            model = FourierFeatureSiren2D(z0, z1).to(device)
        else:
            model = NormalizedSiren2D(z0, z1).to(device)
        points = points_for_slab(z0, z1, rng, x_input)
        tensors = to_tensors(points, lower_field, lower_dz, device)
        optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)
        history = {key: [] for key in
                   ("total", "value", "dz", "periodic", "physics")}
        if BOUNDARY_PRETRAIN_EPOCHS > 0:
            for _ in range(BOUNDARY_PRETRAIN_EPOCHS):
                optimizer.zero_grad()
                warmup_terms = slab_loss(
                    model, tensors, lambda_phys=0.0
                )
                warmup_terms[0].backward()
                optimizer.step()
        best_loss = float("inf")
        best_state = None
        no_improvement = 0
        t0 = time.time()

        for epoch in range(N_EPOCHS):
            optimizer.zero_grad()
            if PHYSICS_RAMP_EPOCHS > 0:
                ramp = min(1.0, (epoch + 1) / PHYSICS_RAMP_EPOCHS)
                physics_weight = LAMBDA_PHYS * ramp
            else:
                physics_weight = LAMBDA_PHYS
            terms = slab_loss(
                model, tensors, lambda_phys=physics_weight
            )
            terms[0].backward()
            if GRAD_CLIP_NORM > 0:
                torch.nn.utils.clip_grad_norm_(
                    model.parameters(), GRAD_CLIP_NORM
                )
            optimizer.step()
            values = [float(term.detach().cpu()) for term in terms]
            for key, value in zip(history, values):
                history[key].append(value)
            if (
                physics_weight >= LAMBDA_PHYS - 1e-12
                and values[0] < best_loss - 1e-8
            ):
                best_loss = values[0]
                best_state = copy.deepcopy(model.state_dict())
                no_improvement = 0
            else:
                no_improvement += 1
            if (
                ADAPTIVE_RESIDUAL
                and (epoch + 1) % max(1, ADAPTIVE_INTERVAL) == 0
            ):
                adapt_collocation(model, tensors, rng, device)
            if no_improvement >= PATIENCE:
                break

        if best_state is not None:
            model.load_state_dict(best_state)

        optimizer_lbfgs = torch.optim.LBFGS(
            model.parameters(), lr=1.0, max_iter=LBFGS_MAX_ITER,
            history_size=50, line_search_fn="strong_wolfe"
        )
        lbfgs_calls = [0]

        def closure():
            optimizer_lbfgs.zero_grad()
            terms = slab_loss(model, tensors)
            terms[0].backward()
            lbfgs_calls[0] += 1
            return terms[0]

        optimizer_lbfgs.step(closure)
        # En problemas de Cauchy para Helmholtz, L-BFGS puede salir del valle
        # encontrado por Adam y aumentar violentamente el residuo. Solo se
        # conserva si mejora la mejor pérdida de Adam; de lo contrario se
        # recupera el estado estable ya registrado.
        post_lbfgs_terms = slab_loss(model, tensors)
        post_lbfgs_loss = float(post_lbfgs_terms[0].detach().cpu())
        if best_state is not None and post_lbfgs_loss > best_loss:
            model.load_state_dict(best_state)
        elapsed = time.time() - t0

        # Propagacion de la interfaz para el siguiente bloque.
        upper_points = np.column_stack((x_input, np.full_like(x_input, z1)))
        upper_value, upper_dz = evaluate_with_dz(model, upper_points, device)
        lower_field = project_to_propagating(
            upper_value, x_input, kx, propagating_mask
        )
        lower_dz = project_to_propagating(
            upper_dz, x_input, kx, propagating_mask
        )
        final_terms = slab_loss(model, tensors)
        saved_states.append(model.state_dict())

        # Evaluacion solo en las filas de la referencia que caen en el bloque.
        ref_indices = np.where(
            (z_reference >= z0 - 1e-9) & (z_reference <= z1 + 1e-9)
        )[0]
        block_points = np.column_stack((
            np.tile(x_input, len(ref_indices)),
            np.repeat(z_reference[ref_indices], len(x_input)),
        ))
        block_prediction = evaluate(model, block_points, device)
        block_field = (block_prediction[:, 0] + 1j * block_prediction[:, 1]).reshape(
            len(ref_indices), len(x_input)
        ) * field_scale
        if slab_index == 0:
            predicted_fields.extend(block_field)
            predicted_indices = list(ref_indices)
        else:
            # La primera fila coincide con la interfaz ya registrada.
            predicted_fields.extend(block_field[1:])
            predicted_indices.extend(ref_indices[1:].tolist())

        slab_reports.append({
            "slab": slab_index,
            "z_lambda": [z0, z1],
            "epochs_adam": len(history["total"]),
            "lbfgs_calls": lbfgs_calls[0],
            "best_adam_loss": best_loss,
            "seconds": elapsed,
            "final_terms": {
                key: float(term.detach().cpu())
                for key, term in zip(history, final_terms)
            },
            "final_loss": float(final_terms[0].detach().cpu()),
        })
        print(f"  Bloque {slab_index + 1}/{n_slabs}: z=[{z0:.1f},{z1:.1f}], "
              f"loss={best_loss:.3e}, tiempo={elapsed:.1f}s")

    # Reordenar la salida por si el numero de puntos de referencia cambia.
    predicted_fields = np.asarray(predicted_fields)
    predicted_indices = np.asarray(predicted_indices, dtype=int)
    order = np.argsort(predicted_indices)
    predicted_fields = predicted_fields[order]
    # predicted_indices contiene indices de las filas de la referencia, no
    # coordenadas fisicas. Convertirlos a z/lambda evita comparar, por
    # ejemplo, la fila 1 (z=0.1) con el objetivo z=1.
    predicted_z = z_reference[predicted_indices[order]]
    target_index = int(np.argmin(np.abs(predicted_z - DISTANCE_LAMBDA)))
    predicted_target = predicted_fields[target_index]

    metrics = {
        **complex_field_metrics(predicted_target, target_field),
        "interface_input_rmse": float(np.sqrt(np.mean(np.abs(
            (input_field_scaled * field_scale) - input_field
        ) ** 2))),
        "reference_target_statistics": intensity_statistics(target_field),
        "pinn_target_statistics": intensity_statistics(predicted_target),
    }

    results_dir = PROJECT_ROOT / "artifacts" / "experiments" / "nb03_root_trials"
    figure_dir = results_dir / "figures"
    model_dir = results_dir / "models"
    figure_dir.mkdir(parents=True, exist_ok=True)
    model_dir.mkdir(parents=True, exist_ok=True)
    model_path = model_dir / f"nb03_speckle_slabs{OUTPUT_SUFFIX}.pt"
    torch.save({"states": saved_states, "slab_edges": slab_edges.tolist()}, model_path)

    output = {
        "experiment": "NB03-C PINN-SIREN por bloques contra referencia angular",
        "seed": SEED,
        "device": str(device),
        "domain": {
            "x_lambda": [-WIDTH_LAMBDA / 2.0, WIDTH_LAMBDA / 2.0],
            "z_lambda": [0.0, DISTANCE_LAMBDA],
            "k_normalized": K,
            "boundary_x": "periodic value and derivative",
            "boundary_z": "input field and outgoing dz derivative transferred by slabs",
        },
        "architecture": {
            "hidden_dim": HIDDEN_DIM,
            "num_layers": NUM_LAYERS,
            "omega_0": OMEGA_0,
            "coordinate_normalization": "local [-1,1] per slab",
            "input_encoding": INPUT_ENCODING,
            "fourier_modes": FOURIER_MODES if INPUT_ENCODING == "fourier" else 0,
            "hard_boundary": USE_HARD_BOUNDARY,
            "hard_boundary_ansatz": (
                "u0(x) + (z-z0) uz0(x) + (z-z0)^2 N_theta(x,z)"
                if USE_HARD_BOUNDARY else None
            ),
            "field_training_scale_rms": field_scale,
        },
        "training": {
            "n_slabs": n_slabs,
            "slab_width_lambda": SLAB_WIDTH,
            "n_colloc_per_slab": N_COLLOC,
            "n_periodic_per_slab": N_PERIODIC,
            "n_epochs_max_per_slab": N_EPOCHS,
            "lambda_dz": LAMBDA_DZ,
            "lambda_periodic": LAMBDA_PERIODIC,
            "lambda_phys": LAMBDA_PHYS,
            "boundary_pretrain_epochs": BOUNDARY_PRETRAIN_EPOCHS,
            "physics_ramp_epochs": PHYSICS_RAMP_EPOCHS,
            "adaptive_residual": ADAPTIVE_RESIDUAL,
            "adaptive_interval": ADAPTIVE_INTERVAL,
            "adaptive_pool_factor": ADAPTIVE_POOL_FACTOR,
            "adaptive_top_fraction": ADAPTIVE_TOP_FRACTION,
            "grad_clip_norm": GRAD_CLIP_NORM,
            "total_seconds": time.time() - t_global,
        },
        "slabs": slab_reports,
        "metrics": metrics,
        "status": "diagnostic; no interior reference labels used",
    }
    suffix = OUTPUT_SUFFIX
    json_path = results_dir / f"nb03_pinn_slabs_comparison{suffix}.json"
    npz_path = results_dir / f"nb03_pinn_slabs_comparison{suffix}.npz"
    png_path = figure_dir / f"nb03_pinn_slabs_comparison{suffix}.png"
    json_path.write_text(json.dumps(output, indent=2, ensure_ascii=False),
                         encoding="utf-8")
    np.savez_compressed(
        npz_path, x_lambda=x_input, z_lambda=predicted_z,
        field_pred=predicted_fields, field_reference=reference_fields,
    )

    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 3, figsize=(16, 8), constrained_layout=True)
    target_intensity = np.abs(target_field) ** 2
    predicted_intensity = np.abs(predicted_target) ** 2
    difference = np.abs(predicted_target - target_field)
    for ax, image, title in zip(
        axes[0], (target_intensity, predicted_intensity, difference),
        (f"Referencia angular: I(x,z={DISTANCE_LAMBDA:g}λ)",
         f"PINN por bloques: I(x,z={DISTANCE_LAMBDA:g}λ)",
         "|PINN - referencia|")
    ):
        image_plot = ax.imshow(image[None, :], aspect="auto", origin="lower",
                               extent=[x[0], x[-1], 0.0, 1.0], cmap="inferno")
        ax.set_title(title)
        ax.set_xlabel("x / λ")
        ax.set_yticks([])
        fig.colorbar(image_plot, ax=ax, fraction=0.046, pad=0.04)

    final_losses = [item["final_terms"]["total"] for item in slab_reports]
    axes[1, 0].plot(np.arange(1, n_slabs + 1), final_losses, "o-",
                    color="#2166ac")
    axes[1, 0].set_title("Pérdida final por bloque")
    axes[1, 0].set_xlabel("Bloque")
    axes[1, 0].set_ylabel("Loss")
    axes[1, 0].set_yscale("log")
    axes[1, 0].grid(alpha=0.25)

    axes[1, 1].plot(x, target_intensity, label="referencia", lw=1.0)
    axes[1, 1].plot(x, predicted_intensity, label="PINN", lw=1.0, alpha=0.8)
    axes[1, 1].set_title(
        f"Perfil de intensidad en z={DISTANCE_LAMBDA:g}λ"
    )
    axes[1, 1].set_xlabel("x / λ")
    axes[1, 1].set_ylabel("I")
    axes[1, 1].grid(alpha=0.25)
    axes[1, 1].legend()

    axes[1, 2].axis("off")
    axes[1, 2].text(
        0.05, 0.9,
        f"L2 complejo: {metrics['target_complex_relative_l2']:.3e}\n"
        f"Coherencia: {metrics['target_complex_coherence']:.4f}\n"
        f"C referencia: {metrics['reference_target_statistics']['contrast']:.4f}\n"
        f"C PINN: {metrics['pinn_target_statistics']['contrast']:.4f}\n"
        f"Bloques: {n_slabs}",
        transform=axes[1, 2].transAxes, va="top", fontsize=12
    )
    fig.suptitle("NB03-C - PINN-SIREN con descomposición en z", fontsize=14)
    fig.savefig(png_path, dpi=160, bbox_inches="tight")
    plt.close(fig)

    print(f"  L2 complejo en z={DISTANCE_LAMBDA:g}λ: "
          f"{metrics['target_complex_relative_l2']:.4e}")
    print(f"  Coherencia compleja: {metrics['target_complex_coherence']:.4f}")
    print(f"  Contraste C referencia/PINN: {metrics['reference_target_statistics']['contrast']:.4f} / "
          f"{metrics['pinn_target_statistics']['contrast']:.4f}")
    print(f"  JSON: {json_path}")
    print(f"  Modelo: {model_path}")


if __name__ == "__main__":
    main()
