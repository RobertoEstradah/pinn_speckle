"""Validación multidireccional de Helmholtz 2D para NB02.

Extiende la onda plana compleja original (+kx,+ky) a las cuatro combinaciones
de signos de un vector de onda con |kx|=|ky|=k/sqrt(2). Cada caso adicional
usa una PINN-SIREN independiente con la misma configuración de NB02.

El caso (+,+) reutiliza el checkpoint canónico ya validado cuando está
disponible. Los otros casos se entrenan desde la misma semilla para que la
comparación sea controlada.
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import qmc
import torch


PROJECT_ROOT = Path(__file__).resolve().parents[2]

import sys

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.losses import helmholtz_residual_2d, pinn_loss_2d
from src.models import PINN_2D_SIREN


CONFIG = {
    "k": 2 * np.pi,
    "N_colloc": 3000,
    "N_boundary_per_edge": 300,
    "hidden_dim": 128,
    "num_layers": 5,
    "omega_0": 1.0,
    "n_epochs": 15000,
    "lr": 1e-3,
    "physics_weight": 0.1,
    "patience": 800,
    "lbfgs_max_iter": 1000,
    "lbfgs_history": 100,
    "seed": 42,
    "l2_threshold": 0.05,
    "N_eval": 100,
}

DIRECTIONS = {
    "pp": {"sign_x": 1, "sign_y": 1, "label": "(+kx,+ky), 45°"},
    "pm": {"sign_x": 1, "sign_y": -1, "label": "(+kx,-ky), -45°"},
    "mp": {"sign_x": -1, "sign_y": 1, "label": "(-kx,+ky), 135°"},
    "mm": {"sign_x": -1, "sign_y": -1, "label": "(-kx,-ky), -135°"},
}


def set_seed(seed: int) -> None:
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def build_sampling(device: torch.device):
    sampler = qmc.LatinHypercube(d=2, seed=CONFIG["seed"])
    lhs_pts = sampler.random(n=CONFIG["N_colloc"])
    xy_colloc = torch.tensor(lhs_pts, dtype=torch.float32, device=device)

    n_b = CONFIG["N_boundary_per_edge"]
    t = np.linspace(0, 1, n_b)
    bottom = np.stack([t, np.zeros(n_b)], axis=1)
    top = np.stack([t, np.ones(n_b)], axis=1)
    left = np.stack([np.zeros(n_b), t], axis=1)
    right = np.stack([np.ones(n_b), t], axis=1)
    xy_boundary_np = np.vstack([bottom, top, left, right])
    xy_boundary = torch.tensor(
        xy_boundary_np, dtype=torch.float32, device=device
    )
    return xy_colloc, xy_boundary_np, xy_boundary


def boundary_values(
    xy_boundary_np: np.ndarray,
    sign_x: int,
    sign_y: int,
    device: torch.device,
) -> torch.Tensor:
    k_axis = CONFIG["k"] / np.sqrt(2)
    phase = (
        sign_x * k_axis * xy_boundary_np[:, 0]
        + sign_y * k_axis * xy_boundary_np[:, 1]
    )
    values = np.stack([np.cos(phase), np.sin(phase)], axis=1)
    return torch.tensor(values, dtype=torch.float32, device=device)


def new_model(device: torch.device) -> PINN_2D_SIREN:
    set_seed(CONFIG["seed"])
    return PINN_2D_SIREN(
        hidden_dim=CONFIG["hidden_dim"],
        num_layers=CONFIG["num_layers"],
        omega_0=CONFIG["omega_0"],
    ).to(device)


def train_direction(
    direction_key: str,
    model: PINN_2D_SIREN,
    xy_colloc: torch.Tensor,
    xy_boundary: torch.Tensor,
    field_boundary: torch.Tensor,
) -> dict:
    optimizer = torch.optim.Adam(model.parameters(), lr=CONFIG["lr"])
    patience = CONFIG["patience"]
    min_delta = 1e-7
    best_loss = float("inf")
    best_state = None
    without_improvement = 0
    epoch_final = CONFIG["n_epochs"]

    print(f"\n[{direction_key}] Entrenamiento Adam")
    t0_adam = time.time()
    for epoch in range(CONFIG["n_epochs"]):
        optimizer.zero_grad()
        loss, loss_data, loss_physics = pinn_loss_2d(
            model,
            xy_colloc,
            xy_boundary,
            field_boundary,
            k=CONFIG["k"],
            lambda_phys=CONFIG["physics_weight"],
        )
        loss.backward()
        optimizer.step()

        current = loss.item()
        if current < best_loss - min_delta:
            best_loss = current
            best_state = {
                name: value.detach().clone()
                for name, value in model.state_dict().items()
            }
            without_improvement = 0
        else:
            without_improvement += 1

        if (epoch + 1) % 1000 == 0:
            elapsed = time.time() - t0_adam
            print(
                f"  época {epoch + 1:5d} | total={current:.3e} | "
                f"datos={loss_data.item():.3e} | física={loss_physics.item():.3e} | "
                f"mejor={best_loss:.3e} | {elapsed:.1f} s"
            )

        if without_improvement >= patience:
            epoch_final = epoch + 1
            if best_state is not None:
                model.load_state_dict(best_state)
            print(f"  early stopping en época {epoch_final}")
            break

    adam_seconds = time.time() - t0_adam

    optimizer_lbfgs = torch.optim.LBFGS(
        model.parameters(),
        lr=1.0,
        max_iter=CONFIG["lbfgs_max_iter"],
        history_size=CONFIG["lbfgs_history"],
        line_search_fn="strong_wolfe",
    )
    lbfgs_evaluations = [0]
    t0_lbfgs = time.time()

    def closure():
        optimizer_lbfgs.zero_grad()
        loss, _, _ = pinn_loss_2d(
            model,
            xy_colloc,
            xy_boundary,
            field_boundary,
            k=CONFIG["k"],
            lambda_phys=CONFIG["physics_weight"],
        )
        loss.backward()
        lbfgs_evaluations[0] += 1
        if lbfgs_evaluations[0] % 100 == 0:
            print(
                f"  [{direction_key}] L-BFGS {lbfgs_evaluations[0]:4d} | "
                f"total={loss.item():.3e}"
            )
        return loss

    optimizer_lbfgs.step(closure)
    lbfgs_seconds = time.time() - t0_lbfgs

    return {
        "training_source": "independent_cold_start",
        "adam_epochs": int(epoch_final),
        "best_adam_loss": float(best_loss),
        "adam_seconds": float(adam_seconds),
        "lbfgs_evaluations": int(lbfgs_evaluations[0]),
        "lbfgs_seconds": float(lbfgs_seconds),
        "training_seconds": float(adam_seconds + lbfgs_seconds),
    }


def evaluate_direction(
    model: PINN_2D_SIREN,
    sign_x: int,
    sign_y: int,
    device: torch.device,
) -> tuple[dict, dict[str, np.ndarray]]:
    n_eval = CONFIG["N_eval"]
    axis = np.linspace(0, 1, n_eval)
    xx, yy = np.meshgrid(axis, axis)
    xy_np = np.stack([xx.ravel(), yy.ravel()], axis=1)
    xy = torch.tensor(xy_np, dtype=torch.float32, device=device)

    model.eval()
    with torch.no_grad():
        output = model(xy).cpu().numpy()

    real_pred = output[:, 0].reshape(n_eval, n_eval)
    imag_pred = output[:, 1].reshape(n_eval, n_eval)
    k_axis = CONFIG["k"] / np.sqrt(2)
    phase_exact = sign_x * k_axis * xx + sign_y * k_axis * yy
    real_exact = np.cos(phase_exact)
    imag_exact = np.sin(phase_exact)
    complex_pred = real_pred + 1j * imag_pred
    complex_exact = real_exact + 1j * imag_exact

    l2_real = np.linalg.norm(real_pred - real_exact) / np.linalg.norm(real_exact)
    l2_imag = np.linalg.norm(imag_pred - imag_exact) / np.linalg.norm(imag_exact)
    l2_complex = (
        np.linalg.norm(complex_pred - complex_exact)
        / np.linalg.norm(complex_exact)
    )
    intensity_pred = np.abs(complex_pred) ** 2
    intensity_exact = np.ones_like(intensity_pred)
    l2_intensity = (
        np.linalg.norm(intensity_pred - intensity_exact)
        / np.linalg.norm(intensity_exact)
    )
    phase_error = np.angle(complex_pred * np.conj(complex_exact))
    phase_rmse = np.sqrt(np.mean(phase_error**2))

    residual_real_parts = []
    residual_imag_parts = []
    for start in range(0, len(xy_np), 1024):
        batch = torch.tensor(
            xy_np[start : start + 1024],
            dtype=torch.float32,
            device=device,
        )
        residual_real, residual_imag, _, _ = helmholtz_residual_2d(
            model, batch, CONFIG["k"]
        )
        residual_real_parts.append(
            residual_real.detach().cpu().numpy().ravel()
        )
        residual_imag_parts.append(
            residual_imag.detach().cpu().numpy().ravel()
        )

    residual_real = np.concatenate(residual_real_parts)
    residual_imag = np.concatenate(residual_imag_parts)
    residual_rms = np.sqrt(
        np.mean(residual_real**2 + residual_imag**2)
    )
    residual_relative = residual_rms / (CONFIG["k"] ** 2)

    metrics = {
        "l2_real_percent": float(100 * l2_real),
        "l2_imag_percent": float(100 * l2_imag),
        "l2_complex_percent": float(100 * l2_complex),
        "l2_intensity_percent": float(100 * l2_intensity),
        "phase_rmse_rad": float(phase_rmse),
        "residual_rms_complex": float(residual_rms),
        "residual_relative_complex": float(residual_relative),
        "accepted_l2_below_5_percent": bool(
            l2_complex < CONFIG["l2_threshold"]
        ),
    }
    arrays = {
        "real_exact": real_exact,
        "real_pred": real_pred,
        "real_error": np.abs(real_pred - real_exact),
    }
    return metrics, arrays


def save_comparison_figure(
    direction_arrays: dict[str, dict[str, np.ndarray]],
    output_path: Path,
) -> None:
    fig, axes = plt.subplots(4, 3, figsize=(13, 16), constrained_layout=True)
    for row, (key, definition) in enumerate(DIRECTIONS.items()):
        arrays = direction_arrays[key]
        vmin = min(arrays["real_exact"].min(), arrays["real_pred"].min())
        vmax = max(arrays["real_exact"].max(), arrays["real_pred"].max())
        axes[row, 0].imshow(
            arrays["real_exact"],
            origin="lower",
            extent=[0, 1, 0, 1],
            cmap="RdBu_r",
            vmin=vmin,
            vmax=vmax,
        )
        axes[row, 1].imshow(
            arrays["real_pred"],
            origin="lower",
            extent=[0, 1, 0, 1],
            cmap="RdBu_r",
            vmin=vmin,
            vmax=vmax,
        )
        image_error = axes[row, 2].imshow(
            arrays["real_error"],
            origin="lower",
            extent=[0, 1, 0, 1],
            cmap="magma",
        )
        axes[row, 0].set_ylabel(
            f"{definition['label']}\nỹ", fontsize=10
        )
        for column in range(3):
            axes[row, column].set_xlabel("x̃")
        fig.colorbar(image_error, ax=axes[row, 2], fraction=0.046)

    axes[0, 0].set_title("Referencia: parte real")
    axes[0, 1].set_title("PINN-SIREN: parte real")
    axes[0, 2].set_title("Error absoluto")
    fig.suptitle(
        "NB02: validación multidireccional de Helmholtz 2D",
        fontsize=15,
    )
    fig.savefig(output_path, dpi=160, bbox_inches="tight")
    plt.close(fig)


def run(reuse_existing: bool = True) -> dict:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    set_seed(CONFIG["seed"])

    results_dir = PROJECT_ROOT / "results" / "nb02_multidirectional"
    models_dir = results_dir / "models"
    arrays_dir = results_dir / "arrays"
    figures_dir = PROJECT_ROOT / "results" / "figures"
    for directory in (results_dir, models_dir, arrays_dir, figures_dir):
        directory.mkdir(parents=True, exist_ok=True)

    xy_colloc, xy_boundary_np, xy_boundary = build_sampling(device)
    summary = {
        "problem": "Helmholtz 2D normalized multidirectional validation",
        "equation": "E_xx + E_yy + (2*pi)^2 E = 0",
        "domain": "[0,1]^2",
        "device": str(device),
        "configuration": CONFIG,
        "directions": {},
        "scope_note": (
            "Four controlled plane-wave directions for one fixed magnitude "
            "|kx|=|ky|=k/sqrt(2); not a complete basis of all 2D solutions."
        ),
    }
    direction_arrays = {}

    base_checkpoint = (
        PROJECT_ROOT / "results" / "models" / "nb02_helmholtz2d_gpu.pt"
    )

    for key, definition in DIRECTIONS.items():
        checkpoint = models_dir / f"nb02_direction_{key}.pt"
        metrics_path = results_dir / f"direction_{key}.json"
        model = new_model(device)

        if key == "pp" and base_checkpoint.exists():
            model.load_state_dict(
                torch.load(
                    base_checkpoint,
                    map_location=device,
                    weights_only=True,
                )
            )
            training = {
                "training_source": "canonical_nb02_checkpoint",
                "checkpoint": str(base_checkpoint),
                "training_seconds": None,
            }
            torch.save(model.state_dict(), checkpoint)
            print(f"[{key}] checkpoint canónico NB02 reutilizado")
        elif reuse_existing and checkpoint.exists() and metrics_path.exists():
            model.load_state_dict(
                torch.load(
                    checkpoint,
                    map_location=device,
                    weights_only=True,
                )
            )
            previous = json.loads(metrics_path.read_text(encoding="utf-8"))
            training = previous["training"]
            print(f"[{key}] resultado existente reutilizado")
        else:
            field_boundary = boundary_values(
                xy_boundary_np,
                definition["sign_x"],
                definition["sign_y"],
                device,
            )
            training = train_direction(
                key,
                model,
                xy_colloc,
                xy_boundary,
                field_boundary,
            )
            torch.save(model.state_dict(), checkpoint)

        metrics, arrays = evaluate_direction(
            model,
            definition["sign_x"],
            definition["sign_y"],
            device,
        )
        direction_entry = {
            **definition,
            "kx_normalized": float(
                definition["sign_x"] * CONFIG["k"] / np.sqrt(2)
            ),
            "ky_normalized": float(
                definition["sign_y"] * CONFIG["k"] / np.sqrt(2)
            ),
            "training": training,
            "metrics": metrics,
            "checkpoint": str(checkpoint),
        }
        summary["directions"][key] = direction_entry
        direction_arrays[key] = arrays
        np.savez_compressed(arrays_dir / f"direction_{key}.npz", **arrays)
        metrics_path.write_text(
            json.dumps(direction_entry, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        (results_dir / "validation_summary.partial.json").write_text(
            json.dumps(summary, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        print(
            f"[{key}] L2 complejo={metrics['l2_complex_percent']:.6f}% | "
            f"aceptada={metrics['accepted_l2_below_5_percent']}"
        )
        del model
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    accepted = [
        entry["metrics"]["accepted_l2_below_5_percent"]
        for entry in summary["directions"].values()
    ]
    l2_values = [
        entry["metrics"]["l2_complex_percent"]
        for entry in summary["directions"].values()
    ]
    summary["aggregate"] = {
        "accepted_count": int(sum(accepted)),
        "total_count": len(accepted),
        "all_directions_accepted": bool(all(accepted)),
        "mean_l2_complex_percent": float(np.mean(l2_values)),
        "worst_l2_complex_percent": float(np.max(l2_values)),
        "criterion": "L2 complex < 5% for every direction",
    }

    figure_path = figures_dir / "nb02_multidirectional_validation.png"
    save_comparison_figure(direction_arrays, figure_path)
    summary["figure"] = str(figure_path)
    summary_path = results_dir / "validation_summary.json"
    summary_path.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"\nResumen: {summary_path}")
    print(f"Figura : {figure_path}")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--no-reuse",
        action="store_true",
        help="Reentrena también los casos direccionales ya existentes.",
    )
    args = parser.parse_args()
    run(reuse_existing=not args.no_reuse)


if __name__ == "__main__":
    main()
