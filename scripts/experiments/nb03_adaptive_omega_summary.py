"""Consolida la confirmación predefinida de frecuencia adaptativa de NB03."""

from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np

os.environ.setdefault("MPLBACKEND", "Agg")


ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "results" / "nb03_holdout"
CASES = {
    73: RESULTS / "screen31415_net73_adaptiveomega_lbfgs180" / "summary.json",
    101: RESULTS / "screen31415_net101_adaptiveomega_lbfgs180" / "summary.json",
    211: RESULTS / "screen31415_net211_adaptiveomega_lbfgs180" / "summary.json",
}


def aggregate(values):
    values = np.asarray(values, dtype=float)
    return {
        "mean": float(values.mean()),
        "median": float(np.median(values)),
        "std_population": float(values.std()),
        "minimum": float(values.min()),
        "maximum": float(values.max()),
    }


def main() -> None:
    rows = []
    for seed, path in CASES.items():
        data = json.loads(path.read_text(encoding="utf-8"))
        metrics = data["lbfgs32"]["metrics"]
        row = {
            "network_seed": seed,
            "source": str(path),
            "l2_propagating_final": metrics["l2_propagating_final"],
            "l2_propagating_max": metrics["l2_propagating_max"],
            "l2_full_final": metrics["l2_full_final"],
            "residual_rmse": metrics["test_residual"]["rmse"],
            "coherence_full_final": metrics["coherence_full_final"],
            "contrast_difference": metrics["contrast_difference"],
            "adaptive_scale_final": data["activation_scale"]["after_lbfgs"],
        }
        row["primary_full_l2_pass"] = row["l2_full_final"] < 0.05
        row["propagating_final_pass"] = row["l2_propagating_final"] < 0.01
        row["propagating_interval_pass"] = row["l2_propagating_max"] < 0.01
        row["contrast_pass"] = row["contrast_difference"] < 0.05
        row["all_predefined_metrics_pass"] = all(
            row[key]
            for key in (
                "primary_full_l2_pass",
                "propagating_final_pass",
                "propagating_interval_pass",
                "contrast_pass",
            )
        )
        rows.append(row)

    primary_count = sum(row["primary_full_l2_pass"] for row in rows)
    output = {
        "experiment": "NB03 adaptive-frequency pre-registered confirmation",
        "screen_seed": 31415,
        "network_seeds": list(CASES),
        "pre_registered_confirmation_rule": "at least 2 of 3 seeds with full final L2 < 5%",
        "primary_pass_count": primary_count,
        "primary_confirmed": primary_count >= 2,
        "all_metrics_pass_count": sum(
            row["all_predefined_metrics_pass"] for row in rows
        ),
        "cases": rows,
        "aggregate": {
            key: aggregate([row[key] for row in rows])
            for key in (
                "l2_propagating_final",
                "l2_propagating_max",
                "l2_full_final",
                "residual_rmse",
                "coherence_full_final",
                "contrast_difference",
                "adaptive_scale_final",
            )
        },
        "interpretation": (
            "The pre-registered primary rule is met, but one catastrophic "
            "initialization remains and only one seed passes every stricter "
            "propagating-field criterion. The method is promising but not "
            "initialization-robust enough for unconditional replacement."
        ),
    }
    path = RESULTS / "adaptiveomega_multiseed_summary.json"
    path.write_text(json.dumps(output, indent=2), encoding="utf-8")

    import matplotlib.pyplot as plt

    seeds = [row["network_seed"] for row in rows]
    full_pct = [100 * row["l2_full_final"] for row in rows]
    residuals = [row["residual_rmse"] for row in rows]
    colors = ["#2a9d8f" if row["primary_full_l2_pass"] else "#e76f51" for row in rows]
    fig, axes = plt.subplots(1, 2, figsize=(9.5, 4.2), constrained_layout=True)
    axes[0].bar([str(seed) for seed in seeds], full_pct, color=colors)
    axes[0].axhline(5.0, color="black", linestyle="--", linewidth=1, label="umbral 5 %")
    axes[0].set(yscale="log", xlabel="semilla neuronal", ylabel="L2 completo final (%)")
    axes[0].legend()
    axes[1].bar([str(seed) for seed in seeds], residuals, color=colors)
    axes[1].set(yscale="log", xlabel="semilla neuronal", ylabel="residuo RMSE normalizado")
    for axis in axes:
        axis.grid(axis="y", alpha=0.25)
    fig.suptitle("NB03 - frecuencia SIREN adaptativa, pantalla reservada 31415")
    fig.savefig(RESULTS / "adaptiveomega_multiseed.png", dpi=180)
    plt.close(fig)
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
