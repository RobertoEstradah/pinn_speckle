"""Diagnóstico NTK del modelo validado de NB02.

Este experimento es solo diagnóstico: carga el checkpoint de NB02 y compara
el kernel tangente neuronal del término de datos con el del residuo físico.
No reentrena ni modifica NB01/NB02.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import torch


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.models import PINN_2D_SIREN  # noqa: E402
from src.utils import load_model  # noqa: E402


SEED = 42
K = 2 * np.pi
N_NTK = 80
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def latin_hypercube(n, d, seed):
    """Muestreo LHS reproducible sin añadir una dependencia de SciPy."""
    rng = np.random.default_rng(seed)
    samples = np.empty((n, d), dtype=np.float64)
    for axis in range(d):
        samples[:, axis] = (rng.permutation(n) + rng.random(n)) / n
    return samples


def flat_grad(scalar_output, params):
    grads = torch.autograd.grad(
        scalar_output, params, retain_graph=True, create_graph=False
    )
    return torch.cat([g.reshape(-1) for g in grads])


def jacobian_scalar_field(fn, points, params, n_params):
    jac = torch.zeros((len(points), n_params), dtype=torch.float32)
    for i in range(len(points)):
        point = points[i : i + 1].clone().requires_grad_(True)
        value = fn(point)
        jac[i] = flat_grad(value.squeeze(), params).detach().cpu()
    return jac


def main() -> None:
    torch.manual_seed(SEED)
    np.random.seed(SEED)

    model = PINN_2D_SIREN(hidden_dim=128, num_layers=5, omega_0=1.0).to(DEVICE)
    model = load_model(
        model,
        "nb02_helmholtz2d_gpu",
        notebook_dir=str(ROOT / "notebooks"),
        device=DEVICE,
    )
    model.eval()
    params = [p for p in model.parameters() if p.requires_grad]
    n_params = sum(p.numel() for p in params)
    print(f"Modelo NB02 cargado: {n_params:,} parametros; dispositivo={DEVICE}")

    t = np.linspace(0.0, 1.0, N_NTK // 4)
    xy_bc_np = np.vstack(
        [
            np.stack([t, np.zeros_like(t)], axis=1),
            np.stack([t, np.ones_like(t)], axis=1),
            np.stack([np.zeros_like(t), t], axis=1),
            np.stack([np.ones_like(t), t], axis=1),
        ]
    )
    xy_bc = torch.tensor(xy_bc_np, dtype=torch.float32, device=DEVICE)

    def data_fn(xy):
        return model(xy)[:, 0:1]

    jac_data = jacobian_scalar_field(data_fn, xy_bc, params, n_params)

    xy_colloc_np = latin_hypercube(N_NTK, 2, SEED)
    xy_colloc = torch.tensor(xy_colloc_np, dtype=torch.float32, device=DEVICE)

    def phys_fn(xy):
        xy = xy.clone().requires_grad_(True)
        e_real = model(xy)[:, 0:1]
        ones = torch.ones_like(e_real)
        grad = torch.autograd.grad(
            e_real, xy, grad_outputs=ones, create_graph=True
        )[0]
        fxx = torch.autograd.grad(
            grad[:, 0:1], xy, grad_outputs=ones, create_graph=True
        )[0][:, 0:1]
        fyy = torch.autograd.grad(
            grad[:, 1:2], xy, grad_outputs=ones, create_graph=True
        )[0][:, 1:2]
        return fxx + fyy + K**2 * e_real

    jac_phys = torch.zeros((N_NTK, n_params), dtype=torch.float32)
    for i in range(N_NTK):
        value = phys_fn(xy_colloc[i : i + 1])
        jac_phys[i] = flat_grad(value.squeeze(), params).detach().cpu()

    ntk_data = (jac_data @ jac_data.T).numpy()
    ntk_phys = (jac_phys @ jac_phys.T).numpy()
    eig_data = np.sort(np.linalg.eigvalsh(ntk_data))[::-1]
    eig_phys = np.sort(np.linalg.eigvalsh(ntk_phys))[::-1]

    trace_data = float(np.trace(ntk_data))
    trace_phys = float(np.trace(ntk_phys))
    result = {
        "seed": SEED,
        "device": str(DEVICE),
        "n_params": n_params,
        "N_NTK": N_NTK,
        "k": K,
        "trace_data": trace_data,
        "trace_phys": trace_phys,
        "ratio_phys_sobre_data": trace_phys / trace_data,
        "max_eig_data": float(eig_data[0]),
        "max_eig_phys": float(eig_phys[0]),
        "eig_data_top10": eig_data[:10].tolist(),
        "eig_phys_top10": eig_phys[:10].tolist(),
    }

    output = ROOT / "results" / "diagnostics" / "ntk_nb02.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    print(f"Salida: {output}")


if __name__ == "__main__":
    main()
