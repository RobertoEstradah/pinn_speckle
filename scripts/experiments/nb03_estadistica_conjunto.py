# -*- coding: utf-8 -*-
"""Estadistica de conjunto de NB03: contraste y bondad de ajuste.

El criterio de speckle completamente desarrollado de Goodman es una propiedad
del conjunto de realizaciones, no de una pantalla individual. Este script reune
las cinco pantallas validadas y calcula el contraste del conjunto para el campo
de la PINN y para su referencia, junto con el test de Kolmogorov-Smirnov en
ambos niveles.

Persiste el resultado para que las cifras de conjunto citadas en la tesis
tengan artefacto propio.

Uso:
    python scripts/experiments/nb03_estadistica_conjunto.py
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
PANTALLAS = (42, 123, 321, 777, 2026)


def ks_exponencial(intensidad):
    """KS contra la exponencial de media ajustada, con la aproximacion de
    Stephens para el p-valor. Misma convencion que la referencia fisica."""
    x = np.sort(np.asarray(intensidad, dtype=float))
    n = x.size
    media = x.mean()
    teorica = 1.0 - np.exp(-x / media)
    empirica_sup = np.arange(1, n + 1) / n
    empirica_inf = np.arange(0, n) / n
    d = float(np.max(np.maximum(empirica_sup - teorica, teorica - empirica_inf)))
    # Stephens (1974) para exponencial con media estimada.
    modificado = (d - 0.2 / n) * (np.sqrt(n) + 0.26 + 0.5 / np.sqrt(n))
    p = float(np.exp(-(modificado ** 2) * 2.0))
    return d, min(max(p, 0.0), 1.0)


def contraste(intensidad):
    i = np.asarray(intensidad, dtype=float)
    return float(i.std() / i.mean())


def main():
    pinn, referencia, filas = [], [], []
    for semilla in PANTALLAS:
        suf = ("_z1_screen42_omega1_finetune" if semilla == 42
               else f"_z1_screen{semilla}_omega1_finetune")
        datos = np.load(RESULTS / f"nb03_modal_pinn_siren{suf}.npz")
        i_pinn = np.abs(datos["field_pred"]) ** 2
        i_ref = np.abs(datos["field_reference"]) ** 2
        pinn.append(i_pinn)
        referencia.append(i_ref)
        filas.append({
            "screen_seed": semilla,
            "contrast_pinn": contraste(i_pinn),
            "contrast_reference": contraste(i_ref),
            "absolute_contrast_error": abs(contraste(i_pinn) - contraste(i_ref)),
            "goodman_absolute_pass": abs(contraste(i_pinn) - 1.0) < 0.1,
            "n_samples": int(i_pinn.size),
        })

    i_pinn = np.concatenate(pinn)
    i_ref = np.concatenate(referencia)
    d_pinn, p_pinn = ks_exponencial(i_pinn)
    d_ref, p_ref = ks_exponencial(i_ref)

    salida = {
        "experiment": "NB03: estadistica de conjunto sobre las cinco pantallas",
        "note": (
            "El conjunto lo forman las cinco realizaciones de fase validadas en "
            "z=1 lambda. No es comparable en tamano con el conjunto de 64 "
            "realizaciones de cada referencia individual, que se reporta aparte "
            "en los JSON de espectro angular."
        ),
        "screen_seeds": list(PANTALLAS),
        "n_realizations": len(PANTALLAS),
        "n_samples_total": int(i_pinn.size),
        "ensemble": {
            "contrast_pinn": contraste(i_pinn),
            "contrast_reference": contraste(i_ref),
            "goodman_absolute_deviation_pinn": abs(contraste(i_pinn) - 1.0),
            "goodman_absolute_pass_pinn": abs(contraste(i_pinn) - 1.0) < 0.1,
            "ks_statistic_pinn": d_pinn,
            "ks_pvalue_pinn": p_pinn,
            "ks_statistic_reference": d_ref,
            "ks_pvalue_reference": p_ref,
            "fraction_above_2mean_pinn": float(np.mean(i_pinn > 2 * i_pinn.mean())),
            "fraction_above_2mean_reference": float(np.mean(i_ref > 2 * i_ref.mean())),
            "expected_fraction_above_2mean": float(np.exp(-2.0)),
        },
        "per_screen": filas,
        "individual_goodman_pass_count": sum(f["goodman_absolute_pass"] for f in filas),
    }

    ruta = RESULTS / "nb03_estadistica_conjunto.json"
    ruta.write_text(json.dumps(salida, indent=2, ensure_ascii=False), encoding="utf-8")

    e = salida["ensemble"]
    print(f"conjunto de {len(PANTALLAS)} pantallas, {i_pinn.size} muestras")
    print(f"  contraste PINN       : {e['contrast_pinn']:.4f}  "
          f"|C-1| = {e['goodman_absolute_deviation_pinn']:.4f}  "
          f"{'cumple' if e['goodman_absolute_pass_pinn'] else 'NO cumple'}")
    print(f"  contraste referencia : {e['contrast_reference']:.4f}")
    print(f"  KS PINN       : D={e['ks_statistic_pinn']:.5f}  p={e['ks_pvalue_pinn']:.3e}")
    print(f"  KS referencia : D={e['ks_statistic_reference']:.5f}  p={e['ks_pvalue_reference']:.3e}")
    print(f"  fraccion I>2<I>: PINN {e['fraction_above_2mean_pinn']:.4f}  "
          f"ref {e['fraction_above_2mean_reference']:.4f}  "
          f"teorico {e['expected_fraction_above_2mean']:.4f}")
    print(f"  criterio absoluto individual: "
          f"{salida['individual_goodman_pass_count']}/{len(PANTALLAS)}")
    print(f"JSON: {ruta}")


if __name__ == "__main__":
    main()
