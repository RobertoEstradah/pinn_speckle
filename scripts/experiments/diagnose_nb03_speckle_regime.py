# -*- coding: utf-8 -*-
"""
diagnose_nb03_speckle_regime.py — Diagnostico del regimen fisico de NB03
========================================================================
Proyecto : Simulacion Acelerada de Speckle Optico mediante PINNs
Autor    : Roberto Hernandez Estrada
Director : Dr. Jose Adan Hernandez Nolasco — UJAT

Motivacion
----------
El campo entrenado en NB03 quedo en |E| <= 0.05 pese a imponer |E| = 1 en la
frontera y = 0, y la perdida de datos se estanco en 0.5 (el valor exacto de
E == 0) durante toda la corrida. Este script determina si eso es un fallo de
entrenamiento o una consecuencia del planteamiento fisico.

Metodo
------
Se resuelve el mismo problema de contorno por espectro angular, que es la
solucion exacta del semiespacio con ondas salientes:

    E(x, y) = F^-1{ A(k_x) exp(i k_y y) },   k_y = sqrt(k^2 - k_x^2)

Los modos con |k_x| > k tienen k_y imaginario: son evanescentes y decaen en
una fraccion de longitud de onda sin entrar al dominio. La fraccion de la
frontera que realmente propaga es lo que determina el campo interior.

Salida: results/nb03_speckle_regime.json
"""
import json
from pathlib import Path

import numpy as np

SEED = 42
N_PHI = 256          # puntos de fase en y=0, igual que CONFIG de NB03
N_EVAL = 100         # malla de evaluacion, igual que CONFIG de NB03
K_NB03 = 2 * np.pi   # dominio = 1 longitud de onda


def campo_referencia(k, n_phi=N_PHI, n_eval=N_EVAL, seed=SEED, corr_len=None):
    """Solucion exacta por espectro angular con la frontera rugosa de NB03.

    corr_len : longitud de correlacion de la rugosidad, en unidades del
               dominio. None reproduce NB03 (fases independientes punto a
               punto, es decir ruido blanco espacial).

    Devuelve (E, n_modos_propagantes, fraccion_de_energia_que_propaga).
    """
    rng = np.random.RandomState(seed)
    phi = rng.uniform(0, 2 * np.pi, n_phi)

    dx = 1.0 / (n_phi - 1)
    kx = 2 * np.pi * np.fft.fftfreq(n_phi, d=dx)

    if corr_len is not None:
        sigma_f = 1.0 / corr_len
        phi = np.real(np.fft.ifft(np.fft.fft(phi) * np.exp(-(kx ** 2) / (2 * sigma_f ** 2))))
        phi = (phi - phi.mean()) / phi.std() * (2 * np.pi / np.sqrt(12))

    amp = np.fft.fft(np.exp(1j * phi)) / n_phi
    propaga = np.abs(kx) <= k
    ky = np.where(propaga,
                  np.sqrt(np.maximum(k ** 2 - kx ** 2, 0)),
                  1j * np.sqrt(np.maximum(kx ** 2 - k ** 2, 0)))

    idx = np.round(np.linspace(0, 1, n_eval) * (n_phi - 1)).astype(int)
    E = np.stack([np.fft.ifft(amp * np.exp(1j * ky * y) * n_phi)[idx]
                  for y in np.linspace(0, 1, n_eval)])

    energia = np.sum(np.abs(amp[propaga]) ** 2) / np.sum(np.abs(amp) ** 2)
    return E, int(propaga.sum()), float(energia)


def contraste(E, excluir_frontera=True):
    """C = sigma_I / <I>. La fila y=0 es un dato impuesto, no campo propagado:
    incluirla mete un valor atipico (I = 1 contra I ~ 0.005 en el interior)."""
    I = np.abs(E[1:] if excluir_frontera else E) ** 2
    return float(I.std() / I.mean()), float(I.mean())


def main():
    out = {}

    # ── 1. El regimen de NB03 tal como esta ───────────────────────────────
    E, n_prop, e_frac = campo_referencia(K_NB03)
    C_int, I_int = contraste(E)
    C_full, _ = contraste(E, excluir_frontera=False)
    dx = 1.0 / (N_PHI - 1)
    out["nb03_tal_como_esta"] = {
        "k": K_NB03,
        "dominio_en_lambdas": 1.0,
        "n_phi": N_PHI,
        "long_correlacion_rugosidad_en_lambdas": dx,
        "kx_nyquist": float(2 * np.pi * np.fft.fftfreq(N_PHI, d=dx).max()),
        "modos_propagantes": n_prop,
        "modos_totales": N_PHI,
        "fraccion_energia_propagante": e_frac,
        "max_abs_E": float(np.abs(E).max()),
        "I_media_interior": I_int,
        "contraste_interior": C_int,
        "contraste_malla_completa": C_full,
        "nota": ("Solo 3 de 256 modos propagan; el 99.5 % de la energia de la "
                 "frontera es evanescente y decae antes de entrar al dominio. "
                 "El campo interior es la superposicion de 3 ondas planas, que "
                 "produce interferencia suave, no speckle."),
    }

    # ── 2. Cuantas longitudes de onda hace falta ──────────────────────────
    barrido_k = []
    for n_lambda in (1, 2, 5, 10, 20, 50, 100):
        E, n_prop, e_frac = campo_referencia(2 * np.pi * n_lambda)
        C, I_m = contraste(E)
        barrido_k.append({
            "dominio_en_lambdas": n_lambda,
            "k": 2 * np.pi * n_lambda,
            "modos_propagantes": n_prop,
            "fraccion_energia_propagante": e_frac,
            "contraste": C,
            "I_media": I_m,
        })
    out["barrido_tamano_dominio"] = barrido_k

    # ── 3. Rugosidad con correlacion finita, dominio de 20 lambda ─────────
    barrido_corr = []
    for cl in (None, 1 / 256, 1 / 64, 1 / 20, 1 / 10, 1 / 5):
        E, n_prop, e_frac = campo_referencia(2 * np.pi * 20, corr_len=cl)
        C, I_m = contraste(E)
        barrido_corr.append({
            "long_correlacion": "independiente" if cl is None else cl,
            "fraccion_energia_propagante": e_frac,
            "contraste": C,
        })
    out["barrido_correlacion_rugosidad"] = barrido_corr

    out["conclusion"] = (
        "El campo bajo de NB03 no es un fallo de optimizacion sino la solucion "
        "correcta de un problema mal escalado. Con k = 2*pi el dominio mide una "
        "longitud de onda y solo caben 3 modos transversales propagantes, muy por "
        "debajo de lo que el teorema del limite central exige para speckle "
        "completamente desarrollado. Se necesita un dominio de al menos 20 lambda "
        "(k >= 125.7) para que la solucion exacta alcance C ~ 1."
    )

    destino = Path(__file__).resolve().parents[2] / "results" / "nb03_speckle_regime.json"
    destino.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")

    r = out["nb03_tal_como_esta"]
    print("NB03 tal como esta planteado:")
    print(f"  modos propagantes            : {r['modos_propagantes']} de {r['modos_totales']}")
    print(f"  energia que entra al dominio : {100 * r['fraccion_energia_propagante']:.3f} %")
    print(f"  contraste de la sol. exacta  : {r['contraste_interior']:.4f}  (speckle = 1.0)")
    print()
    print("Tamano de dominio necesario:")
    for b in barrido_k:
        print(f"  {b['dominio_en_lambdas']:>3} lambda : "
              f"{b['modos_propagantes']:>3} modos, "
              f"{100 * b['fraccion_energia_propagante']:5.2f} % energia, "
              f"C = {b['contraste']:.4f}")
    print()
    print(f"Guardado en: {destino}")


if __name__ == "__main__":
    main()
