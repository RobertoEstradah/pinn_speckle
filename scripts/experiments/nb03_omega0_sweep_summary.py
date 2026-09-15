# -*- coding: utf-8 -*-
"""Consolida el barrido de omega_0 de la formulacion modal de NB03.

Recalcula, desde los campos guardados de cada corrida, la descomposicion
exacta del error

    L2_total^2 = L2_propagante^2 + piso_evanescente^2,

que es valida porque la base modal contiene solo los modos propagantes y el
resto del espectro de la referencia es ortogonal a ella. El error propagante
es la metrica que mide al modelo; el piso es la fraccion de la referencia que
la representacion no puede expresar por construccion.

Uso:
    python scripts/experiments/nb03_omega0_sweep_summary.py
"""

from pathlib import Path
import json
import os
import sys

import numpy as np

os.environ.setdefault("MPLBACKEND", "Agg")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RESULTS = PROJECT_ROOT / "results"
K = 2.0 * np.pi
OMEGAS = (1, 5, 15, 30)
REFERENCE_SUFFIX = "_z1_corr0.10"


def main():
    reference = np.load(
        RESULTS / f"nb03_angular_spectrum_reference{REFERENCE_SUFFIX}.npz"
    )
    propagating = np.abs(reference["kx"]) <= K + 1e-12

    def project(field):
        """Componente propagante del campo, en el espacio de Fourier."""
        return np.fft.ifft(np.where(propagating, np.fft.fft(field), 0))

    norm = np.linalg.norm
    rows = []
    for omega in OMEGAS:
        suffix = f"_z1_omega{omega}"
        fields = np.load(RESULTS / f"nb03_modal_pinn_siren{suffix}.npz")
        meta = json.loads(
            (RESULTS / f"nb03_modal_pinn_siren{suffix}.json").read_text(
                encoding="utf-8"
            )
        )
        prediction = fields["field_pred"]
        target = fields["field_reference"]
        total = norm(prediction - target) / norm(target)
        floor = norm(target - project(target)) / norm(target)
        propagating_error = (
            norm(project(prediction) - project(target)) / norm(project(target))
        )
        rows.append({
            "first_omega": float(omega),
            "complex_relative_l2_total": float(total),
            "complex_relative_l2_propagating": float(propagating_error),
            "evanescent_floor": float(floor),
            "modal_residual_normalized_rmse": float(
                meta["independent_modal_residual"]["normalized_rmse"]
            ),
            "complex_coherence": float(
                meta["metrics"]["target_complex_coherence"]
            ),
            "training_seconds": float(meta["training"]["seconds"]),
            "epochs": int(meta["training"]["epochs"]),
        })

    calibrated = next(r for r in rows if r["first_omega"] == 1.0)
    worst = next(r for r in rows if r["first_omega"] == 30.0)
    output = {
        "experiment": "NB03 modal: barrido de omega_0 de la primera capa",
        "screen_seed": 42,
        "reference_suffix": REFERENCE_SUFFIX,
        "protocol": (
            "Identico en los cuatro casos: 5000 epocas Adam, lr 2e-4, 256 "
            "posiciones de z por epoca, sin refinamiento posterior. Solo "
            "cambia omega_0 de la primera capa; omega_0 interno fijo en 1."
        ),
        "decomposition_note": (
            "L2_total^2 = L2_propagante^2 + piso^2 de forma exacta: la base "
            "modal solo contiene los 41 modos propagantes y el sector "
            "evanescente de la referencia es ortogonal a ella."
        ),
        "per_omega": rows,
        "ratios": {
            "propagating_error_30_over_1": (
                worst["complex_relative_l2_propagating"]
                / calibrated["complex_relative_l2_propagating"]
            ),
            "residual_30_over_1": (
                worst["modal_residual_normalized_rmse"]
                / calibrated["modal_residual_normalized_rmse"]
            ),
        },
    }

    path = RESULTS / "nb03_modal_omega0_sweep_summary.json"
    path.write_text(
        json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    print(f"{'omega_0':>8}{'L2 total':>12}{'L2 propag.':>13}"
          f"{'piso':>10}{'residuo':>12}")
    for r in rows:
        print(f"{r['first_omega']:>8.0f}"
              f"{100*r['complex_relative_l2_total']:>11.3f}%"
              f"{100*r['complex_relative_l2_propagating']:>12.3f}%"
              f"{100*r['evanescent_floor']:>9.3f}%"
              f"{r['modal_residual_normalized_rmse']:>12.2e}")
    print(f"\nrazon del error propagante (30 / 1): "
          f"{output['ratios']['propagating_error_30_over_1']:.1f}x")
    print(f"razon del residuo (30 / 1)          : "
          f"{output['ratios']['residual_30_over_1']:.1f}x")
    print(f"\nJSON: {path}")


if __name__ == "__main__":
    main()
