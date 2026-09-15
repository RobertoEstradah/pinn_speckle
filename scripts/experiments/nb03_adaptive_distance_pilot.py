"""Extiende a distancias mayores un checkpoint NB03 de frecuencia adaptativa."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import torch


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.experiments import nb03_adaptive_omega_holdout as adaptive  # noqa: E402
from scripts.experiments import nb03_distance_pilot as distance_tools  # noqa: E402
from scripts.experiments import nb03_modal_multiseed_summary as modal_summary  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference-suffix", default="_z1_seed31415_corr0.10")
    parser.add_argument("--source-model", required=True)
    parser.add_argument("--screen-seed", type=int, default=31415)
    parser.add_argument("--network-seed", type=int, default=73)
    parser.add_argument("--distance", type=float, default=5.0)
    parser.add_argument("--seconds", type=float, default=180.0)
    parser.add_argument("--n-train", type=int, default=1024)
    parser.add_argument("--threads", type=int, default=4)
    parser.add_argument("--slope-multiplier", type=float, default=10.0)
    parser.add_argument("--name", required=True)
    args = parser.parse_args()
    if args.distance <= 2 or min(args.seconds, args.slope_multiplier) <= 0:
        parser.error("La distancia debe ser mayor que 2 lambda y los demás valores positivos.")

    torch.set_num_threads(args.threads)
    torch.manual_seed(args.network_seed)
    np.random.seed(args.network_seed)

    reference_path = ROOT / "results" / (
        f"nb03_angular_spectrum_reference{args.reference_suffix}.npz"
    )
    source_model = Path(args.source_model)
    if not source_model.is_absolute():
        source_model = ROOT / source_model
    reference = dict(np.load(reference_path))
    recorded_seed = int(reference.get("reference_seed", args.screen_seed))
    if recorded_seed != args.screen_seed:
        raise ValueError("La semilla declarada no coincide con la referencia.")

    shell, field_scale, kx_active = modal_summary.build_model(reference)
    model = adaptive.AdaptiveOmegaModalSiren(
        shell.coefficient0.detach().flatten(),
        shell.derivative0.detach().flatten(),
        shell.correction_scale.detach().flatten(),
        args.distance,
        slope_multiplier=args.slope_multiplier,
    )
    model.load_state_dict(torch.load(
        source_model, map_location="cpu", weights_only=True
    ))
    initial_scale = float(model.adaptive_scale.detach())

    kz2, training = distance_tools.train(
        model,
        reference,
        args.distance,
        args.seconds,
        args.n_train,
        args.screen_seed,
    )
    metrics, arrays = distance_tools.evaluate(
        model,
        reference,
        field_scale,
        kx_active,
        args.distance,
        kz2,
    )
    z_test = torch.tensor(
        np.linspace(0.0, args.distance, 2001), dtype=torch.float32
    ).reshape(-1, 1)
    metrics["test_residual"] = distance_tools.residual_score(model, z_test, kz2)
    final_scale = float(model.adaptive_scale.detach())

    output_dir = ROOT / "results" / "nb03_distance_pilot" / args.name
    output_dir.mkdir(parents=True, exist_ok=False)
    torch.save(model.state_dict(), output_dir / f"adaptive_z{args.distance:g}.pt")
    np.savez_compressed(output_dir / f"adaptive_z{args.distance:g}.npz", **arrays)
    output = {
        "experiment": "NB03 adaptive-frequency direct distance extension",
        "configuration": vars(args),
        "source_model": str(source_model),
        "protocol": {
            "training_labels": False,
            "selection_uses_reference_field": False,
            "hard_cauchy_at_z0": True,
            "reference": "angular spectrum used only for final evaluation",
            "fixed_training_points": args.n_train,
            "fixed_selection_points": 997,
            "independent_residual_test_points": 2001,
            "field_test_planes": 201,
        },
        "activation_scale": {"initial": initial_scale, "final": final_scale},
        "training": training,
        "metrics": metrics,
        "acceptance": {
            "full_final_below_5pct": metrics["l2_full_final"] < 0.05,
            "propagating_final_below_5pct": metrics["l2_propagating_final"] < 0.05,
            "propagating_all_201_planes_below_5pct": metrics["l2_propagating_max"] < 0.05,
            "contrast_reference_error_below_0_05": metrics["contrast_difference"] < 0.05,
        },
    }
    (output_dir / "summary.json").write_text(
        json.dumps(output, indent=2), encoding="utf-8"
    )
    print(
        f"z={args.distance:g} lambda: prop={100*metrics['l2_propagating_final']:.4f}% "
        f"max_prop={100*metrics['l2_propagating_max']:.4f}% "
        f"full={100*metrics['l2_full_final']:.4f}% "
        f"res={metrics['test_residual']['rmse']:.3e} "
        f"scale={final_scale:.5f}",
        flush=True,
    )
    print(f"Resultado: {output_dir}", flush=True)


if __name__ == "__main__":
    main()
