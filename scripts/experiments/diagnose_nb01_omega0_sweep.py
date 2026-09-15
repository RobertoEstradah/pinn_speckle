"""Reproducible omega_0 ablation for NB01 without modifying the notebook.

The sweep keeps the NB01 problem fixed and changes only the SIREN frequency.
It is a diagnostic experiment, not a replacement for the validated checkpoint.
"""

from pathlib import Path
import copy
import json
import platform
import sys
import time

import numpy as np
import torch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from src.models import PINN_1D_SIREN
from src.losses import pinn_loss_1d


def run_one(omega_0, epochs, seed, threads):
    torch.set_num_threads(threads)
    torch.manual_seed(seed)
    np.random.seed(seed)
    k = 2.0 * np.pi
    x_colloc = torch.linspace(0.0, 1.0, 2000).reshape(-1, 1)
    x_bc = torch.tensor([[0.0], [0.25], [0.5], [0.75], [1.0]])
    e_bc = torch.cos(k * x_bc)
    model = PINN_1D_SIREN(hidden_dim=64, num_layers=5, omega_0=omega_0)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    best_loss = float("inf")
    best_state = None
    history = []
    t0 = time.perf_counter()
    for epoch in range(epochs):
        optimizer.zero_grad(set_to_none=True)
        loss, loss_data, loss_physics = pinn_loss_1d(
            model, x_colloc, x_bc, e_bc, k, lambda_phys=1.0
        )
        if not torch.isfinite(loss):
            return {
                "omega_0": omega_0, "status": "diverged", "epoch": epoch,
                "loss": None, "seconds": time.perf_counter() - t0,
            }
        loss.backward()
        optimizer.step()
        value = float(loss.detach())
        history.append(value)
        if value < best_loss:
            best_loss = value
            best_state = copy.deepcopy(model.state_dict())
    model.load_state_dict(best_state)
    with torch.no_grad():
        x_eval = torch.linspace(0.0, 1.0, 2001).reshape(-1, 1)
        prediction = model(x_eval).numpy().ravel()
    exact = np.cos(k * x_eval.numpy().ravel())
    l2 = np.linalg.norm(prediction - exact) / np.linalg.norm(exact)
    final_loss, final_data, final_physics = pinn_loss_1d(
        model, x_colloc, x_bc, e_bc, k, lambda_phys=1.0
    )
    return {
        "omega_0": omega_0,
        "status": "completed",
        "epochs": epochs,
        "best_total_loss": best_loss,
        "final_total_loss": float(final_loss.detach()),
        "final_data_loss": float(final_data.detach()),
        "final_physics_loss": float(final_physics.detach()),
        "l2_relative": float(l2),
        "seconds": time.perf_counter() - t0,
        "history_last": history[-1],
    }


def main():
    epochs = 3000
    seed = 42
    threads = 4
    omegas = [1.0, 5.0, 15.0, 30.0]
    results = [run_one(omega, epochs, seed, threads) for omega in omegas]
    output = {
        "experiment": "NB01 diagnostic omega_0 sweep",
        "scope": "Same NB01 problem; diagnostic only; validated notebook/checkpoint untouched",
        "problem": {
            "k": 2.0 * np.pi, "domain": [0.0, 1.0],
            "hidden_dim": 64, "num_layers": 5,
            "n_collocation": 2000, "n_boundary": 5,
            "epochs": epochs, "learning_rate": 1e-3,
            "lambda_phys": 1.0, "seed": seed,
        },
        "runtime": {
            "python": sys.version, "torch": torch.__version__,
            "numpy": np.__version__, "platform": platform.platform(),
            "threads": threads,
        },
        "results": results,
        "interpretation": (
            "The sweep tests convergence sensitivity to omega_0; it does not "
            "prove a universal calibration law and does not replace NB01."
        ),
    }
    out_dir = ROOT / "results" / "diagnostics"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "nb01_omega0_sweep.json"
    path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(json.dumps(output, indent=2))
    print(f"JSON: {path}")


if __name__ == "__main__":
    main()
