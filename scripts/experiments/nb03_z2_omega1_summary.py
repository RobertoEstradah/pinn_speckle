"""Consolida la validación NB03 a z=2 lambda con omega_0=1.

El script no entrena ni selecciona modelos con el campo de referencia. Lee la
corrida multirrealización ya terminada, verifica su configuración y produce un
resumen portátil con los criterios científicos declarados para NB03B.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
RUN_DIR = (
    ROOT / "results" / "nb03_distance_pilot" /
    "z2_omega1_five_120s"
)
RAW_SUMMARY = RUN_DIR / "summary.json"
OUTPUT = RUN_DIR / "validation_summary.json"
EXPECTED_SEEDS = (42, 123, 321, 777, 2026)


def relative_path(value: str) -> str:
    path = Path(value)
    if path.is_absolute():
        try:
            return path.relative_to(ROOT).as_posix()
        except ValueError:
            marker = "results"
            parts = list(path.parts)
            if marker in parts:
                return Path(*parts[parts.index(marker):]).as_posix()
    return path.as_posix()


def main() -> None:
    report = json.loads(RAW_SUMMARY.read_text(encoding="utf-8"))
    config = report["configuration"]
    if not np.isclose(config["distances"], [2.0]).all():
        raise ValueError("La corrida no corresponde únicamente a z=2 lambda.")
    if not np.isclose(config["first_omega"], 1.0):
        raise ValueError("La corrida no usa omega_0=1.")
    if not np.isclose(config["hidden_omega"], 1.0):
        raise ValueError("La frecuencia interna no es 1.")
    if config["source_variant"] != "omega1":
        raise ValueError("Los checkpoints de origen no son la variante omega1.")
    if tuple(config["seeds"]) != EXPECTED_SEEDS:
        raise ValueError("Las cinco pantallas esperadas no están presentes.")

    rows = []
    for case in report["cases"]:
        entry = case["distances"]["z2"]
        metric = entry["metrics"]
        acceptance = {
            "l2_full_final_below_5pct": metric["l2_full_final"] < 0.05,
            "coherence_above_0_99": metric["coherence_full_final"] > 0.99,
            "intensity_correlation_above_0_99": (
                metric["intensity_correlation_full_final"] > 0.99
            ),
            "contrast_difference_below_0_05": (
                metric["contrast_difference"] < 0.05
            ),
            "l2_propagating_all_planes_below_5pct": (
                metric["l2_propagating_max"] < 0.05
            ),
            "hard_cauchy_below_1e_6": (
                metric["cauchy_field_max_abs"] < 1e-6 and
                metric["cauchy_derivative_max_abs"] < 1e-6
            ),
        }
        rows.append({
            "screen_seed": case["seed"],
            "reference_path": relative_path(case["reference_path"]),
            "source_model": relative_path(case["source_model"]),
            "training_seconds": entry["training"]["seconds"],
            "l2_full_final": metric["l2_full_final"],
            "l2_propagating_final": metric["l2_propagating_final"],
            "l2_propagating_max": metric["l2_propagating_max"],
            "coherence_full_final": metric["coherence_full_final"],
            "intensity_correlation_full_final": (
                metric["intensity_correlation_full_final"]
            ),
            "contrast_reference": metric["contrast_full"],
            "contrast_pinn": metric["contrast_pinn"],
            "contrast_difference": metric["contrast_difference"],
            "residual_normalized_rmse": metric["test_residual"]["rmse"],
            "cauchy_field_max_abs": metric["cauchy_field_max_abs"],
            "cauchy_derivative_max_abs": metric["cauchy_derivative_max_abs"],
            "acceptance": acceptance,
            "accepted": all(acceptance.values()),
        })

    def aggregate(key: str) -> dict[str, float]:
        values = np.asarray([row[key] for row in rows], dtype=float)
        return {
            "mean": float(values.mean()),
            "std_population": float(values.std()),
            "minimum": float(values.min()),
            "maximum": float(values.max()),
        }

    output = {
        "experiment": "NB03B random-speckle validation at z=2 lambda",
        "coordinate_system": "Cartesian (x,z)",
        "equation": "Normalized homogeneous Helmholtz equation",
        "architecture": {
            "model": "modal PINN-SIREN with hard Cauchy conditions",
            "first_omega": config["first_omega"],
            "hidden_omega": config["hidden_omega"],
            "hidden_layers": 4,
            "hidden_width": 128,
            "complex_propagating_modes": 41,
        },
        "protocol": {
            "distance_lambda": 2.0,
            "screen_seeds": list(EXPECTED_SEEDS),
            "seconds_per_screen": config["seconds"],
            "training_labels": False,
            "selection_uses_reference_field": False,
            "independent_reference": "angular spectrum",
            "field_test_planes": 201,
            "source_summary": RAW_SUMMARY.relative_to(ROOT).as_posix(),
        },
        "per_screen": rows,
        "aggregate": {
            "l2_full_final": aggregate("l2_full_final"),
            "l2_propagating_final": aggregate("l2_propagating_final"),
            "l2_propagating_max": aggregate("l2_propagating_max"),
            "coherence_full_final": aggregate("coherence_full_final"),
            "intensity_correlation_full_final": aggregate(
                "intensity_correlation_full_final"
            ),
            "contrast_difference": aggregate("contrast_difference"),
            "residual_normalized_rmse": aggregate(
                "residual_normalized_rmse"
            ),
            "accepted_screens": sum(row["accepted"] for row in rows),
            "total_screens": len(rows),
        },
        "all_screens_accepted": all(row["accepted"] for row in rows),
        "scope_limitation": (
            "Validates five known random phase screens at z=2 lambda; it does "
            "not prove arbitrary-distance or unseen-screen generalization."
        ),
    }
    OUTPUT.write_text(
        json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"Resumen: {OUTPUT}")
    print(
        f"Aceptadas: {output['aggregate']['accepted_screens']}/"
        f"{output['aggregate']['total_screens']}"
    )
    print(
        "L2 completo medio: "
        f"{100 * output['aggregate']['l2_full_final']['mean']:.4f}%"
    )


if __name__ == "__main__":
    main()
