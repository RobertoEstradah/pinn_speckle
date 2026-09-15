# -*- coding: utf-8 -*-
"""Benchmark de tiempo de inferencia: PINN-SIREN modal frente al espectro angular.

Cubre el alcance declarado en el Capitulo 1 --"benchmark del tiempo de
inferencia contra una referencia numerica de propagacion"--, que no requiere la
implementacion FEM.

La comparacion se plantea a igualdad de salida: ambos metodos producen el campo
complejo en z = 1 lambda sobre los mismos 1024 puntos transversales.

  - Espectro angular: FFT de la pantalla, multiplicacion por el propagador
    exp(i k_z z) y FFT inversa. Coste O(N log N) por plano.
  - PINN modal: evaluacion de la red en z, que devuelve los 41 coeficientes
    modales, y reconstruccion del campo por suma modal. Coste O(N M) en la
    reconstruccion.

Se reportan tres regimenes, porque medir solo la inferencia seria enganoso: el
modelo es especifico de cada pantalla y sus datos de Cauchy estan incorporados
a la arquitectura, de modo que cada realizacion nueva exige entrenar una red
desde cero.

Uso:
    python scripts/experiments/nb03_benchmark_inferencia.py
"""

from pathlib import Path
import json
import os
import platform
import sys
import time

import numpy as np

os.environ.setdefault("MPLBACKEND", "Agg")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

import torch

from scripts.experiments import nb03_modal_pinn_siren as modal
from scripts.experiments import nb03_modal_multiseed_summary as resumen

RESULTS = PROJECT_ROOT / "results"
REFERENCIA = "_z1_corr0.10"
MODELO = "_z1_screen42_omega1_finetune"
K = 2.0 * np.pi
N_REPS = 50
N_CALENTAMIENTO = 10
PLANOS_MULTIPLES = 101


def cronometra(funcion, n_reps=N_REPS, cuda=False):
    """Devuelve (media, desviacion, minimo) en milisegundos."""
    for _ in range(N_CALENTAMIENTO):
        funcion()
    if cuda:
        torch.cuda.synchronize()
    tiempos = []
    for _ in range(n_reps):
        if cuda:
            torch.cuda.synchronize()
        t0 = time.perf_counter()
        funcion()
        if cuda:
            torch.cuda.synchronize()
        tiempos.append((time.perf_counter() - t0) * 1000.0)
    t = np.asarray(tiempos)
    return float(t.mean()), float(t.std()), float(t.min())


def main():
    referencia = dict(np.load(RESULTS / f"nb03_angular_spectrum_reference{REFERENCIA}.npz"))
    x = referencia["x_lambda"]
    kx = referencia["kx"]
    fase = referencia["phase"]
    propagantes = referencia["propagating_mask"].astype(bool)
    n_x = len(x)

    # ── Metodo de referencia: espectro angular ──────────────────────────────
    kz = np.zeros_like(kx)
    kz[propagantes] = np.sqrt(K ** 2 - kx[propagantes] ** 2)
    campo0 = np.exp(1j * fase)

    def asm_un_plano():
        espectro = np.fft.fft(campo0)
        espectro[~propagantes] = 0.0
        return np.fft.ifft(espectro * np.exp(1j * kz * 1.0))

    def asm_todos_los_planos():
        espectro = np.fft.fft(campo0)
        espectro[~propagantes] = 0.0
        return np.stack([np.fft.ifft(espectro * np.exp(1j * kz * z))
                         for z in np.linspace(0.0, 1.0, PLANOS_MULTIPLES)])

    # ── PINN modal entrenada ────────────────────────────────────────────────
    modal.FIRST_OMEGA = 1.0
    ruta_modelo = RESULTS / "models" / f"nb03_modal_pinn_siren{MODELO}.pt"
    red, escala, kx_activos = resumen.build_model(referencia, ruta_modelo)
    dispositivo = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    red = red.to(dispositivo).eval()
    usa_cuda = dispositivo.type == "cuda"

    fase_modal = np.exp(1j * np.outer(x, kx_activos))
    z_uno = torch.tensor([[1.0]], dtype=torch.float32, device=dispositivo)
    z_todos = torch.tensor(np.linspace(0.0, 1.0, PLANOS_MULTIPLES).reshape(-1, 1),
                           dtype=torch.float32, device=dispositivo)

    def pinn_un_plano():
        with torch.no_grad():
            c = red(z_uno).cpu().numpy().reshape(-1, 2)
        return fase_modal @ (c[:, 0] + 1j * c[:, 1]) * escala

    def pinn_todos_los_planos():
        with torch.no_grad():
            c = red(z_todos).cpu().numpy().reshape(PLANOS_MULTIPLES, -1, 2)
        return ((c[..., 0] + 1j * c[..., 1]) @ fase_modal.T) * escala

    # ── Comprobacion de equivalencia antes de cronometrar ───────────────────
    a, b = asm_un_plano(), pinn_un_plano()
    error = float(np.linalg.norm(a - b) / np.linalg.norm(a))

    # ── Mediciones ──────────────────────────────────────────────────────────
    casos = {
        "asm_un_plano": cronometra(asm_un_plano),
        "pinn_un_plano": cronometra(pinn_un_plano, cuda=usa_cuda),
        "asm_101_planos": cronometra(asm_todos_los_planos, n_reps=20),
        "pinn_101_planos": cronometra(pinn_todos_los_planos, n_reps=20, cuda=usa_cuda),
    }

    # ── Costo de entrenamiento, que no puede omitirse ───────────────────────
    entrena = 0.0
    for sufijo in (f"_z1_screen42_omega1", f"_z1_screen42_omega1_finetune"):
        j = json.loads((RESULTS / f"nb03_modal_pinn_siren{sufijo}.json").read_text(encoding="utf-8"))
        entrena += j["training"]["seconds"]

    salida = {
        "experiment": "NB03: tiempo de inferencia frente al espectro angular",
        "scope_note": (
            "Cubre el alcance del Capitulo 1 de comparar contra una referencia "
            "numerica de propagacion. No sustituye al benchmark FEM (NB04), que "
            "sigue pendiente."
        ),
        "fairness_note": (
            "Ambos metodos producen el mismo campo complejo en z=1 lambda sobre "
            f"{n_x} puntos transversales; la discrepancia entre ambas salidas es "
            f"de {100*error:.4f} % relativo."
        ),
        "environment": {
            "device": str(dispositivo),
            "gpu": torch.cuda.get_device_name(0) if usa_cuda else None,
            "torch": torch.__version__,
            "numpy": np.__version__,
            "platform": platform.platform(),
        },
        "problem": {
            "n_transverse_points": int(n_x),
            "n_propagating_modes": int(propagantes.sum()),
            "distance_lambda": 1.0,
            "n_planes_multi": PLANOS_MULTIPLES,
        },
        "equivalence_relative_l2": error,
        "timings_ms": {k: {"mean": v[0], "std": v[1], "min": v[2]}
                       for k, v in casos.items()},
        "speedup_inference_only": {
            "un_plano_asm_sobre_pinn": casos["asm_un_plano"][0] / casos["pinn_un_plano"][0],
            "101_planos_asm_sobre_pinn": casos["asm_101_planos"][0] / casos["pinn_101_planos"][0],
        },
        "training_cost_seconds": entrena,
        "amortization_note": (
            "El modelo es especifico de su pantalla: los datos de Cauchy estan "
            "incorporados a la arquitectura, de modo que cada realizacion nueva "
            "exige entrenar desde cero. El costo de entrenamiento debe incluirse "
            "en cualquier comparacion por pantalla nueva."
        ),
        "amortization": {
            "un_plano": {
                "pinn_gana": casos["asm_un_plano"][0] < casos["pinn_un_plano"][0],
                "ahorro_ms_por_evaluacion":
                    casos["asm_un_plano"][0] - casos["pinn_un_plano"][0],
                "evaluaciones_para_amortizar": None,
            },
            "101_planos": {
                "pinn_gana": casos["asm_101_planos"][0] > casos["pinn_101_planos"][0],
                "ahorro_ms_por_evaluacion":
                    casos["asm_101_planos"][0] - casos["pinn_101_planos"][0],
                "evaluaciones_para_amortizar": (
                    entrena * 1000.0
                    / (casos["asm_101_planos"][0] - casos["pinn_101_planos"][0])
                    if casos["asm_101_planos"][0] > casos["pinn_101_planos"][0]
                    else None),
            },
        },
    }

    ruta = RESULTS / "nb03_benchmark_inferencia.json"
    ruta.write_text(json.dumps(salida, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Dispositivo: {dispositivo}"
          + (f" ({torch.cuda.get_device_name(0)})" if usa_cuda else ""))
    print(f"Equivalencia de salida: {100*error:.4f} % de error relativo\n")
    print(f"{'caso':<22}{'media (ms)':>12}{'desv':>9}{'min':>9}")
    for nombre, (m, s, mn) in casos.items():
        print(f"{nombre:<22}{m:>12.4f}{s:>9.4f}{mn:>9.4f}")
    print()
    r1 = salida["speedup_inference_only"]["un_plano_asm_sobre_pinn"]
    r2 = salida["speedup_inference_only"]["101_planos_asm_sobre_pinn"]
    print(f"Razon ASM/PINN, un plano   : {r1:.2f}x  "
          f"({'PINN mas rapida' if r1 > 1 else 'ASM mas rapido'})")
    print(f"Razon ASM/PINN, 101 planos : {r2:.2f}x  "
          f"({'PINN mas rapida' if r2 > 1 else 'ASM mas rapido'})")
    print(f"\nCosto de entrenamiento por pantalla: {entrena:.1f} s")
    amo = salida["amortization"]["101_planos"]["evaluaciones_para_amortizar"]
    if amo:
        print(f"Evaluaciones de 101 planos, sobre LA MISMA pantalla, necesarias")
        print(f"  para amortizar ese entrenamiento : {amo:,.0f}")
    print(f"\nJSON: {ruta}")


if __name__ == "__main__":
    main()
