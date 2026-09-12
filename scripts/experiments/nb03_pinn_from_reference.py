# -*- coding: utf-8 -*-
"""
NB03-B — PINN 2D contra la referencia de espectro angular
===========================================================

Entrena una PINN SIREN para el mismo problema que NB03-A. NB01 y NB02 no se
modifican. Las coordenadas están expresadas en lambda_laser:

    x/lambda in [-10, 10],  z/lambda in [0, 20],  k = 2*pi.

La condición inicial usa la parte radiativa (modos propagantes) de la pantalla
de fase. Además de U(x,0), se impone dU/dz en z=0, calculada de forma
independiente por espectro angular; esto selecciona la propagación saliente y
evita tratar los bordes laterales como paredes. En x se imponen periodicidad de
valor y periodicidad de derivada.

Salidas:
    results/models/nb03_speckle_reference.pt
    results/nb03_pinn_reference_comparison.json
    results/nb03_pinn_reference_comparison.npz
    results/figures/nb03_pinn_reference_comparison.png
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
except ModuleNotFoundError as exc:  # pragma: no cover - mensaje operativo
    raise SystemExit(
        "Este experimento requiere PyTorch. Instala el entorno declarado en "
        "environment.yml y vuelve a ejecutar el script."
    ) from exc

from src.models import PINN_2D_SIREN


SEED = 42
K = 2.0 * np.pi
WIDTH_LAMBDA = 20.0
DISTANCE_LAMBDA = 20.0
N_COLLOC = int(os.environ.get("NB03_N_COLLOC", 8000))
N_PERIODIC = int(os.environ.get("NB03_N_PERIODIC", 512))
N_EPOCHS = int(os.environ.get("NB03_N_EPOCHS", 5000))
LEARNING_RATE = 1e-3
LAMBDA_PHYS = 0.1
LAMBDA_NEUMANN = 0.2
LAMBDA_PERIODIC = 1.0
LAMBDA_ANCHOR = float(os.environ.get("NB03_LAMBDA_ANCHOR", 1.0))
USE_ANCHORS = os.environ.get("NB03_USE_ANCHORS", "0").lower() in {"1", "true", "yes"}
ANCHOR_X_STRIDE = int(os.environ.get("NB03_ANCHOR_X_STRIDE", 16))
ANCHOR_Z_STRIDE = int(os.environ.get("NB03_ANCHOR_Z_STRIDE", 4))
ANCHOR_Z_START = int(os.environ.get("NB03_ANCHOR_Z_START", 10))
PATIENCE = int(os.environ.get("NB03_PATIENCE", 800))
CURRICULUM_EPOCHS = int(os.environ.get("NB03_CURRICULUM_EPOCHS", 1000))
LBFGS_MAX_ITER = int(os.environ.get("NB03_LBFGS_MAX_ITER", 300))
LBFGS_HISTORY = 50
HIDDEN_DIM = int(os.environ.get("NB03_HIDDEN_DIM", 128))
NUM_LAYERS = int(os.environ.get("NB03_NUM_LAYERS", 5))
OMEGA_0 = float(os.environ.get("NB03_OMEGA_0", 1.0))
OUTPUT_SUFFIX = os.environ.get("NB03_OUTPUT_SUFFIX", "")


def set_seed(seed):
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False


def component_gradient(output, coordinates, component):
    """Gradiente de una salida respecto a (x,z), conservando el grafo."""
    return torch.autograd.grad(
        output[:, component:component + 1], coordinates,
        grad_outputs=torch.ones_like(output[:, component:component + 1]),
        create_graph=True, retain_graph=True
    )[0]


def helmholtz_residual(model, coordinates, k):
    """Residuo complejo de Helmholtz en puntos de colocación."""
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
        residuals.append(d2x + d2z + float(k) ** 2 * output[:, component:component + 1])
    return residuals[0], residuals[1], output


def launch_data(reference):
    """Construye la condición radiativa en z=0 desde la pantalla de fase."""
    x = reference["x_lambda"]
    kx = reference["kx"]
    phase = reference["phase"]
    propagating = reference["propagating_mask"].astype(bool)

    screen_spectrum = np.fft.fft(np.exp(1j * phase))
    kz = np.sqrt(np.maximum(K ** 2 - kx[propagating] ** 2, 0.0))
    radiative_spectrum = np.zeros_like(screen_spectrum, dtype=complex)
    radiative_spectrum[propagating] = screen_spectrum[propagating]
    field0 = np.fft.ifft(radiative_spectrum)
    derivative0 = np.fft.ifft(
        radiative_spectrum * (1j * np.where(propagating,
                                             np.sqrt(np.maximum(K ** 2 - kx ** 2, 0.0)),
                                             0.0))
    )
    return x, field0, derivative0, int(propagating.sum())


def make_training_data(reference, rng):
    x, field0, derivative0, n_propagating = launch_data(reference)
    z_periodic = np.linspace(0.0, DISTANCE_LAMBDA, N_PERIODIC)
    left = np.column_stack((np.full(N_PERIODIC, -WIDTH_LAMBDA / 2.0), z_periodic))
    right = np.column_stack((np.full(N_PERIODIC, WIDTH_LAMBDA / 2.0), z_periodic))
    colloc = np.column_stack((
        rng.uniform(-WIDTH_LAMBDA / 2.0, WIDTH_LAMBDA / 2.0, N_COLLOC),
        rng.uniform(0.0, DISTANCE_LAMBDA, N_COLLOC),
    ))
    data = {
        "x_input": x[:, None],
        "input_points": np.column_stack((x, np.zeros_like(x))),
        "input_target": np.column_stack((field0.real, field0.imag)),
        "input_dz_target": np.column_stack((derivative0.real, derivative0.imag)),
        "left": left,
        "right": right,
        "collocation": colloc,
        "n_propagating": n_propagating,
    }
    if USE_ANCHORS:
        z_reference = reference["z_lambda"]
        field_reference = reference["field_all_z"]
        anchor_x_index = np.arange(0, len(x), ANCHOR_X_STRIDE)
        # z=0 de field_all_z es la pantalla completa; la PINN recibe solo su
        # parte radiativa. Comenzar en z>=1 lambda mantiene consistencia entre
        # la referencia de entrenamiento y la condición inicial radiativa.
        anchor_z_index = np.arange(ANCHOR_Z_START, len(z_reference), ANCHOR_Z_STRIDE)
        anchor_x, anchor_z = np.meshgrid(x[anchor_x_index],
                                         z_reference[anchor_z_index])
        anchor_field = field_reference[np.ix_(anchor_z_index, anchor_x_index)]
        data["anchors"] = np.column_stack((anchor_x.ravel(), anchor_z.ravel()))
        data["anchor_target"] = np.column_stack((
            anchor_field.real.ravel(), anchor_field.imag.ravel()
        ))
    return data


def loss_terms(model, tensors, lambda_phys=LAMBDA_PHYS,
               lambda_neumann=LAMBDA_NEUMANN):
    input_points = tensors["input_points"].clone().requires_grad_(True)
    input_target = tensors["input_target"]
    input_dz_target = tensors["input_dz_target"]
    left = tensors["left"]
    right = tensors["right"]
    collocation = tensors["collocation"]

    pred_input = model(input_points)
    loss_dirichlet = torch.mean((pred_input - input_target) ** 2)

    dz_pred = []
    for component in (0, 1):
        gradient = component_gradient(pred_input, input_points, component)
        dz_pred.append(gradient[:, 1:2])
    pred_dz = torch.cat(dz_pred, dim=1)
    # Se normaliza la derivada por k para que la condición saliente tenga una
    # magnitud comparable a la condición de valor.
    loss_neumann = torch.mean(((pred_dz - input_dz_target) / K) ** 2)

    left_points = left.clone().requires_grad_(True)
    right_points = right.clone().requires_grad_(True)
    pred_left = model(left_points)
    pred_right = model(right_points)
    loss_periodic_value = torch.mean((pred_left - pred_right) ** 2)

    dx_left = []
    dx_right = []
    for component in (0, 1):
        dx_left.append(component_gradient(pred_left, left_points, component)[:, 0:1])
        dx_right.append(component_gradient(pred_right, right_points, component)[:, 0:1])
    loss_periodic_derivative = torch.mean(
        ((torch.cat(dx_left, dim=1) - torch.cat(dx_right, dim=1)) / K) ** 2
    )
    loss_periodic = loss_periodic_value + loss_periodic_derivative

    res_real, res_imag, _ = helmholtz_residual(model, collocation, K)
    # El residuo bruto escala aproximadamente con k^2; dividir por k^4 hace
    # comparable el peso de la física entre configuraciones de frecuencia.
    loss_physics = (
        torch.mean(res_real ** 2) + torch.mean(res_imag ** 2)
    ) / K ** 4

    if "anchors" in tensors:
        pred_anchor = model(tensors["anchors"])
        loss_anchor = torch.mean((pred_anchor - tensors["anchor_target"]) ** 2)
    else:
        loss_anchor = torch.zeros((), dtype=loss_physics.dtype,
                                  device=loss_physics.device)

    total = (
        loss_dirichlet
        + lambda_neumann * loss_neumann
        + LAMBDA_PERIODIC * loss_periodic
        + lambda_phys * loss_physics
        + LAMBDA_ANCHOR * loss_anchor
    )
    return total, loss_dirichlet, loss_neumann, loss_periodic, loss_physics, loss_anchor


def as_tensors(data, device):
    return {
        key: torch.tensor(value, dtype=torch.float32, device=device)
        for key, value in data.items()
        if key != "n_propagating" and key != "x_input"
    }


def evaluate_model(model, points, device, chunk_size=32768):
    predictions = []
    for start in range(0, len(points), chunk_size):
        batch = torch.tensor(points[start:start + chunk_size], dtype=torch.float32,
                             device=device)
        with torch.no_grad():
            predictions.append(model(batch).cpu().numpy())
    return np.concatenate(predictions, axis=0)


def relative_l2(predicted, reference):
    return float(np.linalg.norm(predicted - reference) / np.linalg.norm(reference))


def intensity_statistics(field):
    intensity = np.abs(field) ** 2
    mean = float(intensity.mean())
    return {
        "mean_intensity": mean,
        "std_intensity": float(intensity.std()),
        "contrast": float(intensity.std() / mean),
    }


def main():
    set_seed(SEED)
    project_root = PROJECT_ROOT
    results_dir = project_root / "results"
    figure_dir = results_dir / "figures"
    model_dir = results_dir / "models"
    figure_dir.mkdir(parents=True, exist_ok=True)
    model_dir.mkdir(parents=True, exist_ok=True)
    matplotlib_cache = results_dir / ".matplotlib_cache"
    matplotlib_cache.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("MPLCONFIGDIR", str(matplotlib_cache))

    reference_path = results_dir / "nb03_angular_spectrum_reference.npz"
    if not reference_path.exists():
        raise FileNotFoundError(
            "Falta NB03-A. Ejecuta primero nb03_angular_spectrum_reference.py."
        )
    reference = dict(np.load(reference_path))
    target_field = reference["field_target"]
    x = reference["x_lambda"]
    z = reference["z_lambda"]

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    rng = np.random.RandomState(SEED)
    data = make_training_data(reference, rng)
    # La pantalla radiativa es la parte propagante de exp(i*phi), por lo que
    # su amplitud RMS es menor que uno al eliminar los modos evanescentes.
    # Normalizar durante el entrenamiento evita que el optimizador favorezca la
    # solución casi nula; la escala se conserva para reportar el campo físico.
    field_scale = float(np.sqrt(np.mean(np.sum(data["input_target"] ** 2, axis=1))))
    data["input_target"] = data["input_target"] / field_scale
    data["input_dz_target"] = data["input_dz_target"] / field_scale
    tensors = as_tensors(data, device)
    model = PINN_2D_SIREN(
        hidden_dim=HIDDEN_DIM, num_layers=NUM_LAYERS, omega_0=OMEGA_0
    ).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)

    history = {"total": [], "dirichlet": [], "neumann": [], "periodic": [],
               "physics": [], "anchor": []}
    best_loss = float("inf")
    best_state = None
    no_improvement = 0
    t0 = time.time()
    epoch_final = N_EPOCHS

    print("NB03-B: entrenamiento PINN contra referencia angular")
    print(f"  Dispositivo: {device}")
    print(f"  Dominio: {WIDTH_LAMBDA:.0f}λ × {DISTANCE_LAMBDA:.0f}λ; k={K:.6f}")
    print(f"  Modos propagantes: {data['n_propagating']}")
    print(f"  Colocación: {N_COLLOC}; periodicidad: {N_PERIODIC} por lado")

    for epoch in range(N_EPOCHS):
        optimizer.zero_grad()
        curriculum = min(1.0, (epoch + 1) / max(1, CURRICULUM_EPOCHS))
        terms = loss_terms(
            model, tensors,
            lambda_phys=LAMBDA_PHYS * curriculum,
            lambda_neumann=LAMBDA_NEUMANN * curriculum,
        )
        terms[0].backward()
        optimizer.step()

        values = [float(term.detach().cpu()) for term in terms]
        for key, value in zip(history, values):
            history[key].append(value)
        current = values[0]
        if current < best_loss - 1e-8:
            best_loss = current
            best_state = copy.deepcopy(model.state_dict())
            no_improvement = 0
        else:
            no_improvement += 1
        if (epoch + 1) % 500 == 0:
            print(f"  Adam {epoch + 1:5d}: total={current:.3e}, physics={values[4]:.3e}, "
                  f"anchor={values[5]:.3e}")
        if no_improvement >= PATIENCE:
            epoch_final = epoch + 1
            break

    if best_state is not None:
        model.load_state_dict(best_state)
    adam_seconds = time.time() - t0

    # L-BFGS usa los mismos puntos para hacer comparable la corrida.
    lbfgs_history = {key: [] for key in history}
    lbfgs_calls = [0]
    optimizer_lbfgs = torch.optim.LBFGS(
        model.parameters(), lr=1.0, max_iter=LBFGS_MAX_ITER,
        history_size=LBFGS_HISTORY, line_search_fn="strong_wolfe"
    )

    def closure():
        optimizer_lbfgs.zero_grad()
        terms = loss_terms(model, tensors)
        terms[0].backward()
        values = [float(term.detach().cpu()) for term in terms]
        for key, value in zip(lbfgs_history, values):
            lbfgs_history[key].append(value)
        lbfgs_calls[0] += 1
        return terms[0]

    t1 = time.time()
    optimizer_lbfgs.step(closure)
    lbfgs_seconds = time.time() - t1

    # Evaluación en la misma malla de referencia.
    xx, zz = np.meshgrid(x, z)
    eval_points = np.column_stack((xx.ravel(), zz.ravel()))
    pred = evaluate_model(model, eval_points, device)
    pred_field = (pred[:, 0] + 1j * pred[:, 1]).reshape(len(z), len(x))
    pred_target = pred_field[-1] * field_scale

    input_pred = evaluate_model(model, data["input_points"], device) * field_scale
    input_target_physical = data["input_target"] * field_scale
    metrics = {
        "target_complex_relative_l2": relative_l2(pred_target, target_field),
        "target_real_relative_l2": relative_l2(pred_target.real, target_field.real),
        "target_imag_relative_l2": relative_l2(pred_target.imag, target_field.imag),
        "input_boundary_rmse": float(np.sqrt(np.mean(np.abs(
            input_pred - input_target_physical
        ) ** 2))),
        "reference_target_statistics": intensity_statistics(target_field),
        "pinn_target_statistics": intensity_statistics(pred_target),
    }

    model_path = model_dir / f"nb03_speckle_reference{OUTPUT_SUFFIX}.pt"
    torch.save(model.state_dict(), model_path)
    output = {
        "experiment": "NB03-B PINN against angular-spectrum reference",
        "seed": SEED,
        "device": str(device),
        "domain": {
            "x_lambda": [-WIDTH_LAMBDA / 2.0, WIDTH_LAMBDA / 2.0],
            "z_lambda": [0.0, DISTANCE_LAMBDA],
            "k_normalized": K,
            "boundary_x": "periodic value and derivative",
            "boundary_z0": "radiative field and outgoing dz derivative",
        },
        "architecture": {
            "hidden_dim": HIDDEN_DIM,
            "num_layers": NUM_LAYERS,
            "omega_0": OMEGA_0,
            "parameters": int(sum(parameter.numel() for parameter in model.parameters())),
            "field_training_scale_rms": field_scale,
        },
        "training": {
            "n_colloc": N_COLLOC,
            "n_periodic": N_PERIODIC,
            "n_epochs_max": N_EPOCHS,
            "adam_epochs": epoch_final,
            "lbfgs_calls": lbfgs_calls[0],
            "lambda_phys": LAMBDA_PHYS,
            "lambda_neumann": LAMBDA_NEUMANN,
            "lambda_periodic": LAMBDA_PERIODIC,
            "lambda_anchor": LAMBDA_ANCHOR,
            "use_reference_anchors": USE_ANCHORS,
            "n_anchors": int(len(data.get("anchors", []))),
            "anchor_z_start_index": ANCHOR_Z_START,
            "curriculum_epochs": CURRICULUM_EPOCHS,
            "best_adam_loss": best_loss,
            "adam_seconds": adam_seconds,
            "lbfgs_seconds": lbfgs_seconds,
        },
        "metrics": metrics,
        "status": "reference comparison completed; inspect metrics before thesis integration",
    }
    comparison_json = results_dir / f"nb03_pinn_reference_comparison{OUTPUT_SUFFIX}.json"
    comparison_npz = results_dir / f"nb03_pinn_reference_comparison{OUTPUT_SUFFIX}.npz"
    comparison_png = figure_dir / f"nb03_pinn_reference_comparison{OUTPUT_SUFFIX}.png"
    comparison_json.write_text(
        json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    np.savez_compressed(
        comparison_npz,
        x_lambda=x, z_lambda=z, field_pred=pred_field * field_scale,
        field_reference=reference["field_all_z"],
    )

    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 3, figsize=(16, 8), constrained_layout=True)
    target_intensity = np.abs(target_field) ** 2
    predicted_intensity = np.abs(pred_target) ** 2
    difference = np.abs(pred_target - target_field)
    for ax, image, title in zip(
        axes[0], (target_intensity, predicted_intensity, difference),
        ("Referencia angular: I(x,z=20λ)", "PINN: I(x,z=20λ)", "|PINN - referencia|")
    ):
        plot = ax.imshow(image[None, :], aspect="auto", origin="lower",
                         extent=[x[0], x[-1], 0.0, 1.0], cmap="inferno")
        ax.set_title(title)
        ax.set_xlabel("x / λ")
        ax.set_yticks([])
        fig.colorbar(plot, ax=ax, fraction=0.046, pad=0.04)

    axes[1, 0].semilogy(history["total"], label="total")
    axes[1, 0].semilogy(history["physics"], label="física")
    axes[1, 0].set_title("Pérdidas Adam")
    axes[1, 0].set_xlabel("Época")
    axes[1, 0].set_ylabel("Loss")
    axes[1, 0].grid(alpha=0.25)
    axes[1, 0].legend()

    axes[1, 1].plot(x, target_intensity, label="referencia", lw=1.0)
    axes[1, 1].plot(x, predicted_intensity, label="PINN", lw=1.0, alpha=0.8)
    axes[1, 1].set_title("Perfil de intensidad en z=20λ")
    axes[1, 1].set_xlabel("x / λ")
    axes[1, 1].set_ylabel("I")
    axes[1, 1].grid(alpha=0.25)
    axes[1, 1].legend()

    axes[1, 2].axis("off")
    axes[1, 2].text(
        0.05, 0.9,
        f"L2 complejo: {metrics['target_complex_relative_l2']:.3e}\n"
        f"C referencia: {metrics['reference_target_statistics']['contrast']:.4f}\n"
        f"C PINN: {metrics['pinn_target_statistics']['contrast']:.4f}\n"
        f"RMSE frontera: {metrics['input_boundary_rmse']:.3e}",
        transform=axes[1, 2].transAxes, va="top", fontsize=12
    )
    fig.suptitle("NB03-B — PINN frente a referencia física", fontsize=14)
    fig.savefig(comparison_png,
                dpi=160, bbox_inches="tight")
    plt.close(fig)

    print(f"  Tiempo Adam: {adam_seconds:.1f} s; L-BFGS: {lbfgs_seconds:.1f} s")
    print(f"  L2 complejo en z=20λ: {metrics['target_complex_relative_l2']:.4e}")
    print(f"  C referencia/PINN: {metrics['reference_target_statistics']['contrast']:.4f} / "
          f"{metrics['pinn_target_statistics']['contrast']:.4f}")
    print(f"  JSON: {comparison_json}")
    print(f"  Modelo: {model_path}")


if __name__ == "__main__":
    main()
