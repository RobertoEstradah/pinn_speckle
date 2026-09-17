"""Consolida la validacion NB03C de speckle 2D hasta z=5 lambda."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = ROOT / "results" / "nb03_distance_pilot" / "nb03c_z5_validation"
OUTPUT = OUTPUT_DIR / "validation_summary.json"
DIRECT_PILOT = (
    ROOT / "results" / "nb03_distance_pilot" /
    "z5_omega1_screen42_pilot180" / "summary.json"
)
CASES = {
    42: "z5_screen42_net42_adaptive_slabs_v2",
    123: "z5_screen123_net42_adaptive_slabs_v2",
    321: "z5_screen321_net42_adaptive_slabs_v3_refine",
    777: "z5_screen777_net42_adaptive_slabs_v3_refine",
    2026: "z5_screen2026_net42_adaptive_slabs_v3_refine",
}


def portable(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def stats(rows: list[dict], key: str) -> dict[str, float]:
    values = np.asarray([row[key] for row in rows], dtype=float)
    return {
        "mean": float(values.mean()),
        "std_population": float(values.std()),
        "minimum": float(values.min()),
        "maximum": float(values.max()),
    }


def continuity_max(blocks: list[dict]) -> tuple[float, float]:
    field = []
    derivative = []
    for block in blocks:
        interface = block.get("interface_after_training")
        if not interface:
            continue
        field.append(float(interface["field_max_abs"]))
        derivative.append(float(interface["derivative_max_abs"]))
    return max(field, default=0.0), max(derivative, default=0.0)


def main() -> None:
    rows = []
    for seed, name in CASES.items():
        run_dir = ROOT / "results" / "nb03_distance_pilot" / name
        summary_path = run_dir / "summary.json"
        report = json.loads(summary_path.read_text(encoding="utf-8"))
        config = report["configuration"]
        protocol = report["protocol"]
        metrics = report["metrics"]
        if int(config["screen_seed"]) != seed:
            raise ValueError(f"La corrida {name} no corresponde a la pantalla {seed}.")
        if int(config["target_distance"]) != 5:
            raise ValueError(f"La corrida {name} no termina en 5 lambda.")
        if protocol["training_labels"]:
            raise ValueError(f"La corrida {name} utilizo etiquetas interiores.")
        if protocol["selection_uses_reference_field"]:
            raise ValueError(f"La corrida {name} selecciono con la referencia.")
        if not protocol["hard_cauchy_each_interface"]:
            raise ValueError(f"La corrida {name} no impuso Cauchy duro.")
        field_jump, derivative_jump = continuity_max(report["blocks"])
        residuals = metrics["slab_residuals"]
        max_slab_residual = max(float(item["rmse"]) for item in residuals)
        acceptance = {
            "l2_full_final_below_5pct": metrics["l2_full_final"] < 0.05,
            "l2_propagating_all_planes_below_5pct": (
                metrics["l2_propagating_max"] < 0.05
            ),
            "coherence_above_0_99": metrics["coherence_full_final"] > 0.99,
            "intensity_correlation_above_0_99": (
                metrics["intensity_correlation_full_final"] > 0.99
            ),
            "contrast_difference_below_0_05": (
                metrics["contrast_difference"] < 0.05
            ),
            "hard_interface_continuity_below_1e_6": (
                field_jump < 1e-6 and derivative_jump < 1e-6
            ),
        }
        rows.append({
            "screen_seed": seed,
            "run_directory": portable(run_dir),
            "summary_path": portable(summary_path),
            "arrays_path": portable(run_dir / "adaptive_slabs_z5.npz"),
            "method": report["experiment"],
            "l2_full_final": metrics["l2_full_final"],
            "l2_propagating_final": metrics["l2_propagating_final"],
            "l2_propagating_max": metrics["l2_propagating_max"],
            "l2_propagating_max_z": metrics["l2_propagating_max_z"],
            "coherence_full_final": metrics["coherence_full_final"],
            "intensity_correlation_full_final": (
                metrics["intensity_correlation_full_final"]
            ),
            "contrast_reference": metrics["contrast_full"],
            "contrast_pinn": metrics["contrast_pinn"],
            "contrast_difference": metrics["contrast_difference"],
            "max_slab_residual_rmse": max_slab_residual,
            "interface_field_max_abs": field_jump,
            "interface_derivative_max_abs": derivative_jump,
            "acceptance": acceptance,
            "accepted": all(acceptance.values()),
        })

    direct_report = json.loads(DIRECT_PILOT.read_text(encoding="utf-8"))
    direct_metrics = direct_report["cases"][0]["distances"]["z5"]["metrics"]
    output = {
        "experiment": "NB03C random-speckle validation through z=5 lambda",
        "coordinate_system": "Cartesian (x,z)",
        "equation": "Normalized homogeneous Helmholtz equation",
        "method": {
            "model": "modal PINN-SIREN with adaptive sinusoidal scale",
            "domain_decomposition": "five consecutive one-lambda slabs",
            "hard_cauchy_at_every_interface": True,
            "complex_propagating_modes": 41,
            "training_labels": False,
            "selection_uses_reference_field": False,
            "independent_reference": "angular spectrum after training",
            "field_test_planes": 201,
        },
        "direct_single_domain_control": {
            "path": portable(DIRECT_PILOT),
            "screen_seed": 42,
            "first_omega": 1.0,
            "training_seconds": direct_report["configuration"]["seconds"],
            "l2_full_final": direct_metrics["l2_full_final"],
            "l2_propagating_max": direct_metrics["l2_propagating_max"],
            "coherence_full_final": direct_metrics["coherence_full_final"],
            "accepted": False,
            "interpretation": (
                "La extension directa de un solo dominio falla; el resultado "
                "aceptado requiere continuacion por subdominios."
            ),
        },
        "per_screen": rows,
        "aggregate": {
            "l2_full_final": stats(rows, "l2_full_final"),
            "l2_propagating_final": stats(rows, "l2_propagating_final"),
            "l2_propagating_max": stats(rows, "l2_propagating_max"),
            "coherence_full_final": stats(rows, "coherence_full_final"),
            "intensity_correlation_full_final": stats(
                rows, "intensity_correlation_full_final"
            ),
            "contrast_difference": stats(rows, "contrast_difference"),
            "max_slab_residual_rmse": stats(rows, "max_slab_residual_rmse"),
            "accepted_screens": sum(row["accepted"] for row in rows),
            "total_screens": len(rows),
        },
        "all_screens_accepted": all(row["accepted"] for row in rows),
        "scope_limitation": (
            "Valida cinco pantallas conocidas en 0<=z<=5 lambda mediante "
            "cinco PINN-SIREN locales; no demuestra generalizacion a una "
            "pantalla no vista ni equivale a una sola PINN global."
        ),
    }
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
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
    print(
        "Peor maximo propagante: "
        f"{100 * output['aggregate']['l2_propagating_max']['maximum']:.4f}%"
    )


if __name__ == "__main__":
    main()
