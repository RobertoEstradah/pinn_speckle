"""Continúa y evalúa un checkpoint reservado de NB03 sin etiquetas de campo."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import torch


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.experiments import nb03_modal_multiseed_summary as modal_summary  # noqa: E402
from scripts.experiments import nb03_modal_pinn_siren as modal  # noqa: E402
from scripts.experiments import nb03_modal_refinement as refinement  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference-suffix", default="_z1_seed31415_corr0.10")
    parser.add_argument("--input-model", required=True)
    parser.add_argument("--screen-seed", type=int, default=31415)
    parser.add_argument("--network-seed", type=int, default=73)
    parser.add_argument("--arm", choices=["adam32", "lbfgs32", "lbfgs64"], default="lbfgs32")
    parser.add_argument("--seconds", type=float, default=180.0)
    parser.add_argument("--learning-rate", type=float, default=None)
    parser.add_argument("--n-train", type=int, default=1024)
    parser.add_argument("--selection-interval", type=int, default=10)
    parser.add_argument("--threads", type=int, default=4)
    parser.add_argument("--name", required=True)
    args = parser.parse_args()

    torch.set_num_threads(args.threads)
    torch.manual_seed(args.network_seed)
    np.random.seed(args.network_seed)
    modal.HIDDEN_DIM, modal.NUM_LAYERS = 128, 4
    modal.FIRST_OMEGA, modal.HIDDEN_OMEGA = 30.0, 1.0

    reference_path = ROOT / "results" / (
        f"nb03_angular_spectrum_reference{args.reference_suffix}.npz"
    )
    input_model = Path(args.input_model)
    if not input_model.is_absolute():
        input_model = ROOT / input_model
    if not reference_path.exists() or not input_model.exists():
        raise FileNotFoundError("No se encontró la referencia o el checkpoint de entrada.")

    reference = dict(np.load(reference_path))
    recorded_seed = int(reference.get("reference_seed", args.screen_seed))
    if recorded_seed != args.screen_seed:
        raise ValueError("La semilla declarada no coincide con la referencia.")

    model, field_scale, kx_active = modal_summary.build_model(reference, input_model)
    if args.arm.endswith("64"):
        model = model.to(dtype=torch.float64)
    active = reference["propagating_mask"].astype(bool)
    dtype = next(model.parameters()).dtype
    kz2_before = torch.tensor(
        np.maximum((2 * np.pi) ** 2 - reference["kx"][active] ** 2, 0),
        dtype=dtype,
    )
    baseline_metrics, baseline_arrays = refinement.evaluate(
        model, reference, field_scale, kx_active, kz2_before
    )

    kz2_after, training = refinement.train(
        model,
        reference,
        args.arm,
        args.seconds,
        args.n_train,
        learning_rate=args.learning_rate,
        selection_interval=args.selection_interval,
    )
    final_metrics, final_arrays = refinement.evaluate(
        model, reference, field_scale, kx_active, kz2_after
    )

    output_dir = ROOT / "results" / "nb03_holdout" / args.name
    output_dir.mkdir(parents=True, exist_ok=False)
    torch.save(model.state_dict(), output_dir / f"{args.arm}.pt")
    np.savez_compressed(output_dir / "baseline.npz", **baseline_arrays)
    np.savez_compressed(output_dir / f"{args.arm}.npz", **final_arrays)
    result = {
        "experiment": "NB03 holdout checkpoint continuation",
        "configuration": vars(args),
        "input_model": str(input_model),
        "protocol": {
            "training_labels": False,
            "selection_uses_reference_field": False,
            "fixed_training_points": args.n_train,
            "fixed_selection_points": 997,
            "independent_residual_test_points": 2001,
            "field_test_planes": 201,
        },
        "baseline": baseline_metrics,
        "training": training,
        "final": final_metrics,
        "acceptance": {
            "propagating_final_below_1pct": final_metrics["l2_propagating_final"] < 0.01,
            "propagating_all_201_planes_below_1pct": final_metrics["l2_propagating_max"] < 0.01,
            "full_final_below_5pct": final_metrics["l2_full_final"] < 0.05,
            "contrast_reference_error_below_0_05": final_metrics["contrast_difference"] < 0.05,
        },
    }
    (output_dir / "summary.json").write_text(
        json.dumps(result, indent=2), encoding="utf-8"
    )
    print(
        f"Antes: prop={100*baseline_metrics['l2_propagating_final']:.4f}% "
        f"full={100*baseline_metrics['l2_full_final']:.4f}%",
        flush=True,
    )
    print(
        f"Después: prop={100*final_metrics['l2_propagating_final']:.4f}% "
        f"max_prop={100*final_metrics['l2_propagating_max']:.4f}% "
        f"full={100*final_metrics['l2_full_final']:.4f}% "
        f"res={final_metrics['test_residual']['rmse']:.3e}",
        flush=True,
    )
    print(f"Resultado: {output_dir}", flush=True)


if __name__ == "__main__":
    main()
