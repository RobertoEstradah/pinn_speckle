"""Validación reservada de NB03 en una pantalla y semilla de red nuevas.

La referencia por espectro angular solo se usa al finalizar. Adam y L-BFGS
seleccionan pesos exclusivamente mediante residuo de Helmholtz en una malla
fija que no coincide con la malla final de prueba.
"""

from __future__ import annotations

import argparse
import copy
import json
import platform
import sys
from pathlib import Path

import numpy as np
import torch


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.experiments import nb03_modal_multiseed_summary as modal_summary  # noqa: E402
from scripts.experiments import nb03_modal_pinn_siren as modal  # noqa: E402
from scripts.experiments import nb03_modal_refinement as refinement  # noqa: E402
from scripts.experiments import nb03_pinn_slabs as base  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference-suffix", default="_z1_seed31415_corr0.10")
    parser.add_argument("--screen-seed", type=int, default=31415)
    parser.add_argument("--network-seed", type=int, default=73)
    parser.add_argument("--adam-seconds", type=float, default=180.0)
    parser.add_argument("--lbfgs-seconds", type=float, default=60.0)
    parser.add_argument("--n-train", type=int, default=1024)
    parser.add_argument("--threads", type=int, default=4)
    parser.add_argument("--name", default="screen31415_net73")
    args = parser.parse_args()
    if min(args.adam_seconds, args.lbfgs_seconds) <= 0:
        parser.error("Los presupuestos de tiempo deben ser positivos.")

    torch.set_num_threads(args.threads)
    torch.manual_seed(args.network_seed)
    np.random.seed(args.network_seed)

    modal.HIDDEN_DIM, modal.NUM_LAYERS = 128, 4
    modal.FIRST_OMEGA, modal.HIDDEN_OMEGA = 30.0, 1.0

    reference_path = ROOT / "results" / (
        f"nb03_angular_spectrum_reference{args.reference_suffix}.npz"
    )
    if not reference_path.exists():
        raise FileNotFoundError(
            f"Falta la referencia reservada: {reference_path}. "
            "Genérela primero con nb03_angular_spectrum_reference.py."
        )
    reference = dict(np.load(reference_path))
    recorded_seed = int(reference.get("reference_seed", args.screen_seed))
    if recorded_seed != args.screen_seed:
        raise ValueError(
            f"La referencia contiene semilla {recorded_seed}, no {args.screen_seed}."
        )

    output_dir = ROOT / "results" / "nb03_holdout" / args.name
    output_dir.mkdir(parents=True, exist_ok=False)

    model, field_scale, kx_active = modal_summary.build_model(reference)
    model.train()

    print(
        f"Holdout NB03: pantalla={args.screen_seed}, red={args.network_seed}, "
        f"Adam={args.adam_seconds}s, L-BFGS={args.lbfgs_seconds}s",
        flush=True,
    )
    kz2_adam, adam_training = refinement.train(
        model,
        reference,
        "adam32",
        args.adam_seconds,
        args.n_train,
        learning_rate=2e-4,
        selection_interval=50,
    )
    adam_metrics, adam_arrays = refinement.evaluate(
        model, reference, field_scale, kx_active, kz2_adam
    )
    torch.save(model.state_dict(), output_dir / "adam32.pt")
    np.savez_compressed(output_dir / "adam32.npz", **adam_arrays)
    print(
        f"Adam: prop={100*adam_metrics['l2_propagating_final']:.4f}% "
        f"full={100*adam_metrics['l2_full_final']:.4f}% "
        f"res={adam_metrics['test_residual']['rmse']:.3e}",
        flush=True,
    )

    lbfgs_model = copy.deepcopy(model)
    kz2_lbfgs, lbfgs_training = refinement.train(
        lbfgs_model,
        reference,
        "lbfgs32",
        args.lbfgs_seconds,
        args.n_train,
    )
    lbfgs_metrics, lbfgs_arrays = refinement.evaluate(
        lbfgs_model, reference, field_scale, kx_active, kz2_lbfgs
    )
    torch.save(lbfgs_model.state_dict(), output_dir / "lbfgs32.pt")
    np.savez_compressed(output_dir / "lbfgs32.npz", **lbfgs_arrays)

    result = {
        "experiment": "NB03 reserved screen and network-seed validation",
        "configuration": vars(args),
        "runtime": {
            "python": sys.version,
            "torch": torch.__version__,
            "numpy": np.__version__,
            "platform": platform.platform(),
            "device": "cpu",
            "threads": torch.get_num_threads(),
        },
        "protocol": {
            "training_labels": False,
            "selection_uses_reference_field": False,
            "fixed_training_points": args.n_train,
            "fixed_selection_points": 997,
            "independent_residual_test_points": 2001,
            "field_test_planes": 201,
            "hard_cauchy": True,
            "reference": "independent angular spectrum",
        },
        "adam32": {"training": adam_training, "metrics": adam_metrics},
        "lbfgs32": {"training": lbfgs_training, "metrics": lbfgs_metrics},
        "acceptance": {
            "propagating_final_below_1pct":
                lbfgs_metrics["l2_propagating_final"] < 0.01,
            "propagating_all_201_planes_below_1pct":
                lbfgs_metrics["l2_propagating_max"] < 0.01,
            "full_final_below_5pct": lbfgs_metrics["l2_full_final"] < 0.05,
            "contrast_reference_error_below_0_05":
                lbfgs_metrics["contrast_difference"] < 0.05,
        },
    }
    (output_dir / "summary.json").write_text(
        json.dumps(result, indent=2), encoding="utf-8"
    )
    print(
        f"L-BFGS: prop={100*lbfgs_metrics['l2_propagating_final']:.4f}% "
        f"max_prop={100*lbfgs_metrics['l2_propagating_max']:.4f}% "
        f"full={100*lbfgs_metrics['l2_full_final']:.4f}% "
        f"res={lbfgs_metrics['test_residual']['rmse']:.3e}",
        flush=True,
    )
    print(f"Resultado: {output_dir}", flush=True)


if __name__ == "__main__":
    main()
