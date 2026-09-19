# -*- coding: utf-8 -*-
"""Verifica cada cifra de la seccion NB03 de Cap4 contra su archivo fuente."""
import json
import pathlib
import sys
import numpy as np

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

R = r"C:\roberto\Tesis_Maestria"
ok = fallo = 0


def chk(etiqueta, en_tesis, real, tol=5e-4):
    global ok, fallo
    if isinstance(en_tesis, str) or isinstance(real, str):
        bien = en_tesis == real
    else:
        bien = abs(en_tesis - real) <= tol * max(1.0, abs(real))
    print(f"  {'OK   ' if bien else 'FALLA'} {etiqueta:<46} tesis={str(en_tesis):<12} real={real}")
    ok, fallo = ok + bien, fallo + (not bien)


# ── consolidado omega_0 = 1 ────────────────────────────────────────────────
d = json.load(open(rf"{R}\results\nb03_modal_multiseed_z1_omega1_summary.json", encoding="utf-8"))
ag, per = d["aggregate"], {r["screen_seed"]: r for r in d["per_screen"]}

print("Tabla 'cinco pantallas':")
esperado = {42: (3.819, 0.999271, 0.9063, 0.9012, 0.0051),
            123: (2.402, 0.999712, 0.8827, 0.8821, 0.0006),
            321: (3.573, 0.999362, 0.9200, 0.9231, 0.0030),
            777: (2.947, 0.999566, 1.2246, 1.2403, 0.0157),
            2026: (3.064, 0.999531, 0.7812, 0.7841, 0.0029)}
for s, (l2, coh, cr, cp, dc) in esperado.items():
    r = per[s]
    chk(f"pantalla {s}: L2", l2, round(100 * r["complex_l2_at_z1"], 3))
    chk(f"pantalla {s}: coherencia", coh, round(r["complex_coherence_at_z1"], 6))
    chk(f"pantalla {s}: C_ref", cr, round(r["contrast_reference"], 4))
    chk(f"pantalla {s}: C_pinn", cp, round(r["contrast_pinn"], 4))
    chk(f"pantalla {s}: |dC|", dc, round(r["absolute_contrast_error"], 4))

print("\nAgregados:")
chk("L2 medio", 3.161, round(100 * ag["complex_l2_at_z1"]["mean"], 3))
chk("coherencia media", 0.999488, round(ag["complex_coherence_at_z1"]["mean"], 6))
chk("|dC| medio", 0.0055, round(ag["absolute_contrast_error"]["mean"], 4))
chk("residuo modal RMSE", 2.34e-3, round(ag["residual_normalized_rmse"]["mean"], 5), tol=5e-3)
chk("L2 propagante medio sobre z", 0.042, round(100 * ag["l2_over_z_mean_per_screen"]["mean"], 3), tol=2e-2)
chk("L2 propagante maximo sobre z", 0.084, round(100 * ag["l2_over_z_maximum_per_screen"]["mean"], 3), tol=2e-2)

# ── barrido de omega_0 modal ───────────────────────────────────────────────
print("\nBarrido de omega_0 modal:")
ref = np.load(rf"{R}\results\nb03_angular_spectrum_reference_z1_corr0.10.npz")
K = 2 * np.pi
prop = np.abs(ref["kx"]) <= K + 1e-12
P = lambda f: np.fft.ifft(np.where(prop, np.fft.fft(f), 0))
n = np.linalg.norm
esperado_w = {1: (3.819, 0.090, 3.59e-3), 5: (3.819, 0.081, 2.61e-3),
              15: (3.833, 0.329, 1.33e-2), 30: (4.962, 3.172, 5.49e-2)}
for w, (tot, pr, res) in esperado_w.items():
    z = np.load(rf"{R}\results\nb03_modal_pinn_siren_z1_omega{w}.npz")
    j = json.load(open(rf"{R}\results\nb03_modal_pinn_siren_z1_omega{w}.json", encoding="utf-8"))
    pred, r0 = z["field_pred"], z["field_reference"]
    chk(f"omega={w}: L2 total", tot, round(100 * n(pred - r0) / n(r0), 3))
    chk(f"omega={w}: L2 propagante", pr, round(100 * n(P(pred) - P(r0)) / n(P(r0)), 3))
    chk(f"omega={w}: residuo", res, round(j["independent_modal_residual"]["normalized_rmse"], 5), tol=5e-3)

# ── piso evanescente ───────────────────────────────────────────────────────
print("\nPiso evanescente por distancia:")
e0 = np.fft.fft(np.exp(1j * ref["phase"]))
kz = np.sqrt((K ** 2 - ref["kx"] ** 2).astype(complex))
for zi, esperado_piso, esperado_c in ((0.25, 25.49, 0.7968), (0.5, 12.61, 0.8283),
                                      (1.0, 3.818, 0.9063), (2.0, 0.456, 1.1595),
                                      (3.0, 0.0598, 1.2069), (5.0, 0.0011, 1.0476)):
    E = np.fft.ifft(e0 * np.exp(1j * kz * zi))
    Ep = np.fft.ifft(np.where(prop, e0, 0) * np.exp(1j * kz * zi))
    I = np.abs(E) ** 2
    chk(f"z={zi}: piso", esperado_piso, round(100 * n(E - Ep) / n(E), 4), tol=2e-2)
    chk(f"z={zi}: C referencia", esperado_c, round(I.std() / I.mean(), 4))

# ── puente NB02b ───────────────────────────────────────────────────────────
print("\nExperimento puente NB02b:")
b = json.load(open(rf"{R}\explorations\nb02b_bien_vs_mal_puesto\output\nb02b_bvp_vs_cauchy.json", encoding="utf-8"))
for caso, esperado_l2 in (("A_dirichlet_directa", 0.077), ("B_cauchy_directa", 45.14),
                          ("C_cauchy_modal", 0.155)):
    chk(f"{caso}: L2", esperado_l2, round(100 * b["cells"][caso]["l2_relative"], 3), tol=2e-2)
pB = b["cells"]["B_cauchy_directa"]["profile"]
chk("B: L2 en y=0", 0.209, round(100 * pB["l2_of_y"][0], 3), tol=2e-2)
chk("B: L2 en y=1", 73.7, round(100 * pB["l2_of_y"][-1], 1), tol=2e-2)
chk("B: evanescente maximo", 13.2, round(100 * max(pB["evanescent_energy_fraction_of_y"]), 1), tol=2e-2)

# ── arquitectura modal contra solucion exacta (tab:nb02b_arquitectura) ─────
print("\nArquitectura modal vs solucion exacta:")
a = json.load(open(rf"{R}\results\nb02b_modal_bridge\summary.json", encoding="utf-8"))
casos = {c["n_complex_modes"]: c for c in a["cases"]}
chk("omega_0 de la corrida", 1.0, a["architecture"]["first_omega"])
for modos, l2g, l2t, res, cau in ((1, 0.0149, 0.0030, 1.74e-3, 1.7e-7),
                                  (5, 0.0112, 0.0070, 1.55e-3, 6.7e-8),
                                  (41, 0.0078, 0.0073, 1.32e-3, 2.5e-8)):
    m = casos[modos]["metrics"]
    chk(f"{modos} modos: L2 global", l2g,
        round(100 * m["global_complex_relative_l2"], 4), tol=2e-2)
    chk(f"{modos} modos: L2 en z=1", l2t,
        round(100 * m["target_complex_relative_l2"], 4), tol=2e-2)
    chk(f"{modos} modos: residuo", res,
        float(f'{m["helmholtz_field_residual_normalized_rmse"]:.2e}'), tol=2e-2)
    chk(f"{modos} modos: Cauchy derivada", cau,
        float(f'{m["hard_cauchy_derivative_rmse"]:.1e}'), tol=1e-1)
    chk(f"{modos} modos: coherencia", 1.000000,
        round(m["target_complex_coherence"], 6))
    chk(f"{modos} modos: pasos", 8580, casos[modos]["cumulative_recorded_epochs"])

# ── extension analitica a 2 lambda (tab:nb02b_z2) ─────────────────────────
print("\nExtension analitica a z=2 lambda:")
z2 = json.load(open(rf"{R}\results\nb02b_modal_bridge\z_2lambda\summary.json", encoding="utf-8"))
casos2 = {c["n_complex_modes"]: c for c in z2["cases"]}
chk("z2: omega_0 de la corrida", 1.0, z2["architecture"]["first_omega"])
chk("z2: dominio z", 2.0, float(z2["physics"]["domain_z_lambda"][1]))
chk("z2: los tres aceptados", True, z2["all_cases_accepted"])
for modos, l2g, l2t, mx, coh, res in ((1, 0.210, 0.150, 0.455, 1.000000, 7.68e-3),
                                      (5, 0.334, 0.180, 0.560, 1.000000, 6.63e-3),
                                      (41, 0.195, 0.184, 0.264, 0.999999, 4.13e-3)):
    m = casos2[modos]["metrics"]
    chk(f"z2 {modos} modos: L2 global", l2g,
        round(100 * m["global_complex_relative_l2"], 3), tol=2e-2)
    chk(f"z2 {modos} modos: L2 en z=2", l2t,
        round(100 * m["target_complex_relative_l2"], 3), tol=2e-2)
    chk(f"z2 {modos} modos: maximo sobre z", mx,
        round(100 * m["max_l2_over_z"], 3), tol=2e-2)
    chk(f"z2 {modos} modos: coherencia", coh,
        round(m["target_complex_coherence"], 6))
    chk(f"z2 {modos} modos: residuo", res,
        float(f'{m["helmholtz_field_residual_normalized_rmse"]:.2e}'), tol=2e-2)

# ── epocas de la extension analitica (tab:nb02b_z2, nota) ──────────────────
chk("z2: pasos de L-BFGS de la etapa final", 90, z2["training"]["epochs_per_case"])
for modos in (1, 5, 41):
    chk(f"z2 {modos} modos: pasos acumulados", 8590,
        casos2[modos]["cumulative_recorded_epochs"])

# ── benchmark de inferencia (tab:nb03_inferencia) ──────────────────────────
print("\nBenchmark de inferencia:")
bm = json.load(open(rf"{R}\results\nb03_benchmark_inferencia.json", encoding="utf-8"))
tm = bm["timings_ms"]
for clave, media, desv, minimo in (
        ("asm_un_plano", 0.044, 0.014, 0.039),
        ("pinn_un_plano", 0.819, 0.340, 0.552),
        ("asm_101_planos", 3.246, 0.087, 3.164),
        ("pinn_101_planos", 1.845, 0.184, 1.660)):
    chk(f"{clave}: media", media, round(tm[clave]["mean"], 3), tol=2e-2)
    chk(f"{clave}: desv", desv, round(tm[clave]["std"], 3), tol=5e-2)
    chk(f"{clave}: minimo", minimo, round(tm[clave]["min"], 3), tol=2e-2)
chk("razon un plano (ASM sobre PINN)", 18.5,
    round(tm["pinn_un_plano"]["mean"] / tm["asm_un_plano"]["mean"], 1), tol=2e-2)
chk("razon 101 planos (PINN sobre ASM)", 1.76,
    round(tm["asm_101_planos"]["mean"] / tm["pinn_101_planos"]["mean"], 2), tol=2e-2)
chk("costo de entrenamiento (s)", 351.9, round(bm["training_cost_seconds"], 1))
am = bm["amortization"]["101_planos"]
chk("ahorro por evaluacion (ms)", 1.40, round(am["ahorro_ms_por_evaluacion"], 2), tol=2e-2)
chk("evaluaciones para amortizar (x1e5)", 2.5,
    round(am["evaluaciones_para_amortizar"] / 1e5, 1), tol=5e-2)

# ── validacion de speckle a 2 lambda (tab:nb03_z2, NB03B) ─────────────────
print("\nValidacion de speckle a z=2 lambda:")
nb3b = json.load(open(rf"{R}\results\nb03_distance_pilot\z2_omega1_five_120s"
                      rf"\validation_summary.json", encoding="utf-8"))
por_pantalla = {c["screen_seed"]: c for c in nb3b["per_screen"]}
chk("z2: omega_0 de la corrida", 1.0, nb3b["architecture"]["first_omega"])
chk("z2: distancia", 2.0, float(nb3b["protocol"]["distance_lambda"]))
chk("z2: segundos por pantalla", 120.0, float(nb3b["protocol"]["seconds_per_screen"]))
chk("z2: sin etiquetas de entrenamiento", False, nb3b["protocol"]["training_labels"])
esperado = ((42, 1.038, 0.932, 1.165, 0.999951, 1.1595, 1.1621),
            (123, 0.941, 0.894, 1.081, 0.999961, 1.0684, 1.0689),
            (321, 1.006, 0.893, 1.078, 0.999951, 0.9391, 0.9377),
            (777, 0.864, 0.794, 0.999, 0.999965, 1.0116, 1.0123),
            (2026, 1.117, 1.054, 1.054, 0.999960, 0.8374, 0.8369))
acum = [0.0, 0.0, 0.0, 0.0]
for semilla, full, prop, mx, coh, cref, cp in esperado:
    c = por_pantalla[semilla]
    chk(f"z2 pantalla {semilla}: L2 complejo", full,
        round(100 * c["l2_full_final"], 3), tol=2e-2)
    chk(f"z2 pantalla {semilla}: L2 propagante", prop,
        round(100 * c["l2_propagating_final"], 3), tol=2e-2)
    chk(f"z2 pantalla {semilla}: maximo sobre z", mx,
        round(100 * c["l2_propagating_max"], 3), tol=2e-2)
    chk(f"z2 pantalla {semilla}: coherencia", coh,
        round(c["coherence_full_final"], 6))
    chk(f"z2 pantalla {semilla}: C_ref", cref, round(c["contrast_reference"], 4))
    chk(f"z2 pantalla {semilla}: C_pinn", cp, round(c["contrast_pinn"], 4))
    chk(f"z2 pantalla {semilla}: seis criterios", True,
        all(c["acceptance"].values()))
    for i, k in enumerate(("l2_full_final", "l2_propagating_final",
                           "l2_propagating_max", "coherence_full_final")):
        acum[i] += c[k] / 5
for etiqueta, valor, real, esc in (("L2 complejo", 0.993, acum[0], 100),
                                   ("L2 propagante", 0.914, acum[1], 100),
                                   ("maximo sobre z", 1.075, acum[2], 100),
                                   ("coherencia", 0.999958, acum[3], 1)):
    chk(f"z2 media: {etiqueta}", valor, round(esc * real, 3 if esc == 100 else 6),
        tol=2e-2)
chk("z2: diferencia de contraste media", 0.0012,
    round(nb3b["aggregate"]["contrast_difference"]["mean"], 4), tol=5e-2)
chk("z2: residuo modal medio", 5.02e-3,
    round(nb3b["aggregate"]["residual_normalized_rmse"]["mean"], 5), tol=2e-2)

# ── multisemilla de NB02 (tab:multiseed) ───────────────────────────────────
print("\nMultisemilla NB02:")
ms = json.load(open(rf"{R}\results\multiseed_results.json", encoding="utf-8"))
for semilla, l2, epocas in ((42, 0.1707, 8737), (123, 0.0949, 9441), (777, 0.3100, 10443)):
    chk(f"multiseed {semilla}: L2", l2, ms[str(semilla)]["l2_avg"], tol=2e-2)
    chk(f"multiseed {semilla}: epocas Adam", epocas, ms[str(semilla)]["adam_epochs"])
vals = [ms[str(x)]["l2_avg"] for x in (42, 123, 777)]
media = sum(vals) / 3
desv = (sum((v - media) ** 2 for v in vals) / 3) ** 0.5
chk("multiseed: media", 0.192, round(media, 3), tol=2e-2)
chk("multiseed: desv. poblacional", 0.089, round(desv, 3), tol=2e-2)

# ── ablacion de lambda (tab:ablacion_lambda) ───────────────────────────────
print("\nAblacion de lambda:")
ab = json.load(open(rf"{R}\results\ablation_lambda.json", encoding="utf-8"))
chk("ablacion 0.01: L2", 0.163, ab["0.01"]["l2_avg"], tol=2e-2)
chk("ablacion 0.1: L2", 0.171, ab["0.1"]["l2_avg"], tol=2e-2)
chk("ablacion 1.0: no converge", False, ab["1.0"]["converged"])

# ── barrido de omega_0 de NB01 (tab:omega0_sweep) ──────────────────────────
print("\nBarrido de omega_0 (NB01):")
sw = json.load(open(rf"{R}\explorations\ntk_spectral_bias_diagnostics\output"
                    rf"\omega0_sweep.json", encoding="utf-8"))
for w, perdida in (("1.0", 0.2656), ("5.0", 0.5355), ("15.0", 0.4375), ("30.0", 0.6030)):
    chk(f"omega_0={w}: perdida final", perdida, round(sw[w]["loss_final"], 4), tol=2e-2)

# ── fraccion I>2<I> por pantalla (Cap4, seccion de Goodman) ────────────────
print("\nFraccion de pixeles con I>2<I>:")
ec = json.load(open(rf"{R}\results\nb03_estadistica_conjunto.json", encoding="utf-8"))
fp = [f["fraction_above_2mean_pinn"] for f in ec["per_screen"]]
fr = [f["fraction_above_2mean_reference"] for f in ec["per_screen"]]
chk("PINN: minimo por pantalla", 0.1309, round(min(fp), 4), tol=2e-2)
chk("PINN: maximo por pantalla", 0.1514, round(max(fp), 4), tol=2e-2)
chk("referencia: minimo por pantalla", 0.1299, round(min(fr), 4), tol=2e-2)
chk("referencia: maximo por pantalla", 0.1543, round(max(fr), 4), tol=2e-2)
chk("conjunto PINN", 0.1467, round(ec["ensemble"]["fraction_above_2mean_pinn"], 4), tol=2e-2)
chk("conjunto referencia", 0.1475,
    round(ec["ensemble"]["fraction_above_2mean_reference"], 4), tol=2e-2)
chk("valor teorico exp(-2)", 0.1353,
    round(ec["ensemble"]["expected_fraction_above_2mean"], 4), tol=2e-2)

# ── Zhang et al. (2025): verificado contra el texto completo ──────────────
# La copia local existe desde el 2026-09-17. Lo que hay que proteger ya no es
# la declaracion de alcance sino la advertencia de metrica: su ecuacion (16)
# define un error relativo en norma L1, no L2, de modo que la columna de la
# tabla comparativa no puede titularse "Error L2".
print("\nZhang et al. (2025), metrica declarada:")
CAP4 = pathlib.Path(rf"{R}\tesis\Tesis_Actual\chapters\Cap4-Resultados.tex").read_text(
    encoding="utf-8")
zhang_local = any(
    "zhang" in q.name.lower()
    for q in pathlib.Path(rf"{R}\master_supporting_docs\supporting_papers\referencias").rglob("*.pdf")
)
chk("Zhang: hay copia local", True, zhang_local)
chk("la fila lleva marca de nota", True, r"1.40--5.82\tnote{c}" in CAP4)
chk("la nota advierte que no es L2", True,
    "La métrica de esta fila no es el error $L^2$" in CAP4)
chk("la nota cita la ecuacion (16)", True, "ecuación~(16)" in CAP4)
chk("la columna no se titula 'Error L2'", False,
    r"Comparación & Error $L^2$ (\%)" in CAP4)
chk("la columna dice 'Error relativo'", True,
    r"Comparación & Error relativo (\%)" in CAP4)

# ── base modal extendida (Cap3: por que se trunca) ────────────────────────
print("\nBase modal extendida:")
be = {m: json.load(open(rf"{R}\results\nb03_base_extendida\base_extendida_m{m}.json",
                        encoding="utf-8")) for m in (20, 35)}
chk("control: modos", 41, be[20]["n_modos"])
chk("control: piso", 3.8184, round(100 * be[20]["piso_fuera_de_banda"], 4), tol=2e-2)
chk("control: error en banda", 1.98, round(100 * be[20]["l2_dentro_de_banda"], 2), tol=2e-2)
chk("extendida: modos", 71, be[35]["n_modos"])
chk("extendida: kappa maximo", 9.02, round(be[35]["kappa_maximo"], 2), tol=2e-2)
chk("extendida: piso", 0.002, round(100 * be[35]["piso_fuera_de_banda"], 3), tol=1e-1)
chk("extendida: error en banda", 24.70, round(100 * be[35]["l2_dentro_de_banda"], 2), tol=2e-2)
chk("razon de error total", 5.7,
    round(be[35]["l2_total"] / be[20]["l2_total"], 1), tol=2e-2)
chk("extendida: omega_0", 1.0, be[35]["omega_0_primera"])

# ── NB03C: propagacion hasta z=5 lambda por descomposicion (tab:nb03_z5) ──
print("\nPropagacion hasta z=5 lambda (NB03C):")
z5 = json.load(open(rf"{R}\results\nb03_distance_pilot\nb03c_z5_validation"
                    rf"\validation_summary.json", encoding="utf-8"))
p5 = {c["screen_seed"]: c for c in z5["per_screen"]}

# El metodo que la tesis describe debe ser el que el JSON declara.
met = z5["method"]
chk("z5: descomposicion en bloques", "five consecutive one-lambda slabs",
    met["domain_decomposition"])
chk("z5: Cauchy dura en cada interfaz", True, met["hard_cauchy_at_every_interface"])
chk("z5: modos propagantes", 41, met["complex_propagating_modes"])
chk("z5: sin etiquetas de entrenamiento", False, met["training_labels"])
chk("z5: planos evaluados", 201, met["field_test_planes"])
chk("z5: las cinco aceptadas", True, z5["all_screens_accepted"])

esperado = ((42, 3.083, 3.507, 4.85, 0.999601, 1.0476, 1.0547),
            (123, 2.260, 2.260, 5.00, 0.999779, 1.1210, 1.1209),
            (321, 1.856, 1.907, 4.95, 0.999854, 1.0745, 1.0685),
            (777, 2.443, 2.781, 4.30, 0.999712, 1.0148, 1.0190),
            (2026, 1.581, 1.581, 5.00, 0.999917, 0.9950, 0.9994))
for semilla, full, mx, zmx, coh, cref, cp in esperado:
    c = p5[semilla]
    chk(f"z5 pantalla {semilla}: L2 final", full,
        round(100 * c["l2_full_final"], 3), tol=2e-2)
    chk(f"z5 pantalla {semilla}: maximo propagante", mx,
        round(100 * c["l2_propagating_max"], 3), tol=2e-2)
    chk(f"z5 pantalla {semilla}: z del maximo", zmx,
        round(c["l2_propagating_max_z"], 2), tol=2e-2)
    chk(f"z5 pantalla {semilla}: coherencia", coh,
        round(c["coherence_full_final"], 6))
    chk(f"z5 pantalla {semilla}: C_ref", cref, round(c["contrast_reference"], 4))
    chk(f"z5 pantalla {semilla}: C_pinn", cp, round(c["contrast_pinn"], 4))
    chk(f"z5 pantalla {semilla}: seis criterios", True, all(c["acceptance"].values()))
    # Las interfaces deben ser CERO EXACTO, no una cantidad pequena.
    chk(f"z5 pantalla {semilla}: salto de campo", 0.0, c["interface_field_max_abs"])
    chk(f"z5 pantalla {semilla}: salto de derivada", 0.0,
        c["interface_derivative_max_abs"])

a5 = z5["aggregate"]
chk("z5 media: L2 final", 2.244, round(100 * a5["l2_full_final"]["mean"], 3), tol=2e-2)
chk("z5 media: maximo propagante", 2.407,
    round(100 * a5["l2_propagating_max"]["mean"], 3), tol=2e-2)
chk("z5 peor: maximo propagante", 3.507,
    round(100 * a5["l2_propagating_max"]["maximum"], 3), tol=2e-2)
chk("z5 media: coherencia", 0.999772,
    round(a5["coherence_full_final"]["mean"], 6))
chk("z5 media: |dC|", 0.0044, round(a5["contrast_difference"]["mean"], 4), tol=5e-2)
chk("z5 maximo: |dC|", 0.0072, round(a5["contrast_difference"]["maximum"], 4), tol=5e-2)
chk("z5 media: residuo por bloque", 1.37e-2,
    round(a5["max_slab_residual_rmse"]["mean"], 5), tol=2e-2)
chk("z5 peor: residuo por bloque", 1.79e-2,
    round(a5["max_slab_residual_rmse"]["maximum"], 5), tol=2e-2)

# ── Cap3: el parrafo que declara la formulacion no paraxial ────────────────
# Las cifras no salen de un .json sino que se recalculan aqui desde la base
# modal y la pantalla, que es la unica forma de que no se separen del dato.
_kx_todos = np.fft.fftfreq(1024, d=20.0 / 1024) * 2 * np.pi
_k = 2 * np.pi
_act = np.abs(_kx_todos) <= _k + 1e-10
_kx = _kx_todos[_act]
_kz_exacto = np.sqrt(np.maximum(_k ** 2 - _kx ** 2, 0.0))
_kz_parax = _k - _kx ** 2 / (2 * _k)
_theta = np.degrees(np.arcsin(np.clip(np.abs(_kx) / _k, 0, 1)))

chk("Cap3 no paraxial: modos de la base", 41, int(_act.sum()))
chk("Cap3 no paraxial: angulo maximo", 90.0, round(float(_theta.max()), 1))

# Desfase que introduce la paraxial por lambda, en tres angulos que cita el texto.
for grados, esperado in ((30.0, 0.056), (48.6, 0.360), (90.0, 3.142)):
    i = int(np.argmin(np.abs(_theta - grados)))
    chk(f"Cap3 no paraxial: desfase a {grados} grados", esperado,
        round(float(abs(_kz_exacto[i] - _kz_parax[i])), 3), tol=2e-2)

# El modo rasante acumula cinco vueltas de fase sobre los 10 lambda validados.
_i90 = int(np.argmax(np.abs(_kz_exacto - _kz_parax)))
chk("Cap3 no paraxial: desfase acumulado a 10 lambda", 31.4,
    round(float(abs(_kz_exacto[_i90] - _kz_parax[_i90]) * 10), 1), tol=2e-2)

# Reparto de energia de la pantalla por rango angular.
_ref = np.load(rf"{R}\results\nb03_angular_spectrum_reference_z1_corr0.10.npz")
_esp = np.fft.fft(np.exp(1j * _ref["phase"]))
_ener = np.abs(_esp[_ref["propagating_mask"].astype(bool)]) ** 2
_ener = _ener / _ener.sum()
_th = np.degrees(np.arcsin(
    np.clip(np.abs(_ref["kx"][_ref["propagating_mask"].astype(bool)]) / _k, 0, 1)))

for lo, hi, esperado in ((0, 15, 25.06), (15, 30, 16.80), (30, 45, 26.77),
                         (45, 60, 12.42), (60, 90, 12.56)):
    frac = 100 * float(((_th >= lo) & (_th < hi)).astype(float) @ _ener)
    chk(f"Cap3 energia {lo}-{hi} grados", esperado, round(frac, 2), tol=2e-2)

# Las dos cifras que sostienen el argumento.
for umbral, esperado in ((15, 74.94), (45, 31.37)):
    frac = 100 * float((_th >= umbral).astype(float) @ _ener)
    chk(f"Cap3 energia mas alla de {umbral} grados", esperado, round(frac, 2),
        tol=2e-2)

# Guarda: el texto debe seguir declarando que la formulacion NO es paraxial.
_cap3 = open(rf"{R}\tesis\Tesis_Actual\chapters\Cap3-Modelo.tex",
             encoding="utf-8").read()
chk("Cap3 declara que no es paraxial", True,
    "La formulación no es paraxial" in _cap3)
chk("Cap3 nombra el espectro angular", True,
    "carbajal2010espectro" in _cap3)

# ── NB03D: la cadena de diez bloques hasta z=10 lambda ─────────────────────
z10 = json.load(open(rf"{R}\results\nb03_distance_pilot\nb03d_z10_validation"
                     rf"\validation_summary.json", encoding="utf-8"))
p10 = {c["screen_seed"]: c for c in z10["per_screen"]}

met10 = z10["method"]
chk("z10: descomposicion en bloques", "ten consecutive one-lambda slabs",
    met10["domain_decomposition"])
chk("z10: reutiliza el tramo validado", "0<=z<=5 lambda from NB03C",
    met10["validated_prefix_reused"])
chk("z10: bloques entrenados de nuevo", "5<=z<=10 lambda",
    met10["newly_trained_slabs"])
chk("z10: Cauchy dura en cada interfaz", True,
    met10["hard_cauchy_at_every_interface"])
chk("z10: modos propagantes", 41, met10["complex_propagating_modes"])
chk("z10: sin etiquetas de entrenamiento", False, met10["training_labels"])
chk("z10: planos evaluados", 201, met10["field_test_planes"])
chk("z10: las cinco aceptadas", True, z10["all_screens_accepted"])
chk("z10: pantallas refinadas", 2, z10["aggregate"]["refined_screens"])

esperado10 = ((42, 3.288, 3.726, 6.40, 0.999485, 1.2204, 1.2189),
              (123, 2.779, 3.483, 9.70, 0.999696, 1.0105, 1.0133),
              (321, 2.312, 2.393, 9.45, 0.999852, 0.9412, 0.9316),
              (777, 2.752, 3.619, 9.75, 0.999634, 0.9080, 0.9035),
              (2026, 1.956, 1.968, 9.15, 0.999917, 0.7067, 0.7064))
for semilla, full, mx, zmx, coh, cref, cp in esperado10:
    c = p10[semilla]
    chk(f"z10 pantalla {semilla}: L2 final", full,
        round(100 * c["l2_full_final"], 3), tol=2e-2)
    chk(f"z10 pantalla {semilla}: maximo propagante", mx,
        round(100 * c["l2_propagating_max"], 3), tol=2e-2)
    chk(f"z10 pantalla {semilla}: z del maximo", zmx,
        round(c["l2_propagating_max_z"], 2), tol=2e-2)
    chk(f"z10 pantalla {semilla}: coherencia", coh,
        round(c["coherence_full_final"], 6))
    chk(f"z10 pantalla {semilla}: C_ref", cref, round(c["contrast_reference"], 4))
    chk(f"z10 pantalla {semilla}: C_pinn", cp, round(c["contrast_pinn"], 4))
    chk(f"z10 pantalla {semilla}: seis criterios", True,
        all(c["acceptance"].values()))
    # Nueve interfaces, y el salto debe ser CERO EXACTO en todas.
    chk(f"z10 pantalla {semilla}: salto de campo", 0.0,
        c["interface_field_max_abs"])
    chk(f"z10 pantalla {semilla}: salto de derivada", 0.0,
        c["interface_derivative_max_abs"])

a10 = z10["aggregate"]
chk("z10 media: L2 final", 2.617, round(100 * a10["l2_full_final"]["mean"], 3),
    tol=2e-2)
chk("z10 media: maximo propagante", 3.038,
    round(100 * a10["l2_propagating_max"]["mean"], 3), tol=2e-2)
chk("z10 peor: maximo propagante", 3.726,
    round(100 * a10["l2_propagating_max"]["maximum"], 3), tol=2e-2)
chk("z10 media: coherencia", 0.999716,
    round(a10["coherence_full_final"]["mean"], 6))
chk("z10 media: |dC|", 0.0037, round(a10["contrast_difference"]["mean"], 4),
    tol=5e-2)
chk("z10 maximo: |dC|", 0.0096, round(a10["contrast_difference"]["maximum"], 4),
    tol=5e-2)
chk("z10 media: residuo por bloque", 1.37e-2,
    round(a10["max_slab_residual_rmse"]["mean"], 5), tol=2e-2)
chk("z10 peor: residuo por bloque", 1.79e-2,
    round(a10["max_slab_residual_rmse"]["maximum"], 5), tol=2e-2)

# Guarda: NINGUN maximo debe caer en el plano final. La tesis lo afirma, y si
# una corrida futura lo cambiara, la nota al pie quedaria falsa.
chk("z10: ningun maximo en el plano final", True,
    all(c["l2_propagating_max_z"] < 9.99 for c in z10["per_screen"]))

# Guarda: el error NO se dispara al duplicar la distancia. La tesis dice que el
# incremento de 5 a 10 lambda es de 0.373 puntos porcentuales.
inc = 100 * (a10["l2_full_final"]["mean"] - a5["l2_full_final"]["mean"])
chk("z10: incremento frente a z5 (puntos)", 0.373, round(inc, 3), tol=5e-2)

# ── El ensayo de 20 lambda: NO cumple, y la tesis debe seguir diciendolo ────
z20 = json.load(open(rf"{R}\results\nb03_distance_pilot"
                     rf"\z20_screen42_net42_adaptive_slabs_v1\summary.json",
                     encoding="utf-8"))
m20 = z20["metrics"] if "metrics" in z20 else z20
chk("z20: distancia", 20.0, float(m20["distance_lambda"]))
chk("z20: L2 final", 8.743, round(100 * m20["l2_full_final"], 3), tol=2e-2)
chk("z20: maximo propagante", 11.292,
    round(100 * m20["l2_propagating_max"], 3), tol=2e-2)
chk("z20: z del maximo", 19.8, round(m20["l2_propagating_max_z"], 2), tol=2e-2)
chk("z20: coherencia", 0.996907, round(m20["coherence_full_final"], 6))
chk("z20: |dC|", 0.0178, round(m20["contrast_difference"], 4), tol=5e-2)
# Lo importante de esta corrida es que NO alcanza el criterio del 5 %.
chk("z20: excede el umbral del 5 %", True, m20["l2_full_final"] > 0.05)

# Control negativo: la extension directa de un solo dominio.
ctrl = z5["direct_single_domain_control"]
chk("control z5: pantalla", 42, ctrl["screen_seed"])
chk("control z5: omega_0", 1.0, ctrl["first_omega"])
chk("control z5: segundos", 180.0, float(ctrl["training_seconds"]))
chk("control z5: L2", 118.47, round(100 * ctrl["l2_full_final"], 2), tol=2e-2)
chk("control z5: coherencia", 0.0502, round(ctrl["coherence_full_final"], 4), tol=2e-2)
chk("control z5: no aceptado", False, ctrl["accepted"])

print("\nCap4: ERP de la energia (NB03D)")
# ── Cap4: ERP de la energia y figura de mapas de 10 lambda ────────────────
# Las cifras se recalculan desde los .npz con la formula del director, que es
# la unica forma de que el texto no se separe del dato.
_z10 = json.load(open(
    rf"{R}\results\nb03_distance_pilot\nb03d_z10_validation\validation_summary.json",
    encoding="utf-8"))


def _erp(campo):
    e = (np.abs(campo) ** 2).sum(axis=1)
    return 100.0 * np.abs(e[0] - e) / e[0]


_erp_max, _erp_fin, _erp_ref, _erp_full = [], [], [], []
for _e in _z10["per_screen"]:
    _d = np.load(rf"{R}\{_e['arrays_path']}".replace("/", "\\"))
    _p = _erp(_d["field_pred"])
    _erp_max.append(_p.max())
    _erp_fin.append(_p[-1])
    _erp_ref.append(_erp(_d["field_propagating"]).max())
    _erp_full.append(_erp(_d["field_full"]).max())

# Los cinco maximos por pantalla, en el orden en que los lista el texto.
for _seed, _esperado, _real in zip((42, 123, 321, 777, 2026),
                                   (3.347, 2.354, 2.627, 3.410, 1.666), _erp_max):
    chk(f"Cap4 ERP maximo pantalla {_seed}", _esperado, round(float(_real), 3))

chk("Cap4 ERP final medio", 1.364, round(float(np.mean(_erp_fin)), 3))

# La referencia propagante conserva a precision de maquina: es la linea base
# que hace interpretable todo lo anterior. Si dejara de cumplirse, la metrica
# no mediria al PINN sino al calculo de la referencia.
chk("Cap4 ERP referencia propagante < 1e-13", True, bool(max(_erp_ref) < 1e-13))

# El campo total NO conserva, y el texto da el rango.
chk("Cap4 ERP campo total: minimo del rango", 58.7, round(min(_erp_full), 1), tol=2e-3)
chk("Cap4 ERP campo total: maximo del rango", 65.5, round(max(_erp_full), 1), tol=2e-3)

# Los cuatro planos de la figura de perfiles transversales (pantalla 42).
_dp = np.load(
    rf"{R}\results\nb03_distance_pilot\z10_screen42_net42_adaptive_slabs_v1\adaptive_slabs_z10.npz")
for _zd, _esperado in ((0.0, 0.000), (1.0, 0.514), (5.0, 3.091), (10.0, 3.288)):
    _i = int(np.argmin(np.abs(_dp["z_lambda"] - _zd)))
    _l2 = 100 * (np.linalg.norm(_dp["field_propagating"][_i] - _dp["field_pred"][_i])
                 / np.linalg.norm(_dp["field_propagating"][_i]))
    chk(f"Cap4 perfiles: L2 en z={_zd:g} lambda", _esperado, round(float(_l2), 3))

# El plano inicial debe dar cero exacto: es la condicion de Cauchy dura, no un
# ajuste. Si dejara de serlo, la formulacion habria cambiado sin avisar.
_i0 = int(np.argmin(np.abs(_dp["z_lambda"])))
chk("Cap4 perfiles: el plano inicial es exacto", True,
    bool(np.allclose(_dp["field_propagating"][_i0], _dp["field_pred"][_i0], atol=1e-12)))

chk("Cap4 cita a Andres-Zarate et al.", True,
    "andres2019difraccion" in open(
        rf"{R}\tesis\Tesis_Actual\chapters\Cap4-Resultados.tex",
        encoding="utf-8").read())

# Pico de la diferencia frente al pico de intensidad, en la figura de mapas.
_d42 = np.load(
    rf"{R}\results\nb03_distance_pilot\z10_screen42_net42_adaptive_slabs_v1\adaptive_slabs_z10.npz")
_dif = (np.abs(_d42["field_propagating"] - _d42["field_pred"]) ** 2).max()
_pico = max((np.abs(_d42["field_propagating"]) ** 2).max(),
            (np.abs(_d42["field_pred"]) ** 2).max())
chk("Cap4 figura mapas: pico de la diferencia", 2.77, round(float(_dif) * 1e3, 2))
chk("Cap4 figura mapas: pico de intensidad", 3.88, round(float(_pico), 2))
chk("Cap4 figura mapas: diferencia como % del pico", 0.07,
    round(100 * float(_dif) / float(_pico), 2))

# Guarda: el ERP no debe presentarse como comprobacion de estabilidad.
_cap4 = open(rf"{R}\tesis\Tesis_Actual\chapters\Cap4-Resultados.tex",
             encoding="utf-8").read()
chk("Cap4 advierte que el ERP no compara con un esquema conservativo", True,
    "no debe compararse con la de un esquema conservativo" in _cap4)
chk("Cap4 cita la tesis del director", True, "hernandez2003propagacion" in _cap4)

# ── Resumen y Abstract: deben coincidir entre si y con los resultados ─────
print("\nResumen y Abstract:")
RES = pathlib.Path(rf"{R}\tesis\Tesis_Actual\Resumen.tex").read_text(encoding="utf-8")
ABS = pathlib.Path(rf"{R}\tesis\Tesis_Actual\Abstract.tex").read_text(encoding="utf-8")
for etiqueta, cifra in (("L2 1D", "0.006"), ("L2 2D", "0.171"),
                        ("L2 z=1", "3.161"), ("L2 propagante z=1", "0.042"),
                        ("contraste conjunto", "0.9489"),
                        ("contraste referencia", "0.9661"),
                        ("L2 z=2", "0.993"), ("L2 z=5", "2.244"),
                        ("maximo sobre 201 planos", "3.507"),
                        ("L2 z=10", "2.617"),
                        ("maximo en z=10", "3.726"),
                        ("el ensayo de z=20 no cumple", "8.743"),
                        ("multisemilla", "0.192")):
    chk(f"Resumen tiene {etiqueta}", True, cifra in RES)
    chk(f"Abstract tiene {etiqueta}", True, cifra in ABS)

# Ninguno debe prometer generalizacion ni omitir que 5 lambda usa otro metodo.
for nombre, t in (("Resumen", RES), ("Abstract", ABS)):
    chk(f"{nombre}: declara la descomposicion", True,
        ("descomposición del dominio" in t) or ("domain decomposition" in t))
    chk(f"{nombre}: dice pantallas conocidas", True,
        ("realizaciones de fase conocidas" in t) or ("known phase realizations" in t))
    chk(f"{nombre}: acota LHS a 1D y 2D", True,
        ("validaciones 1D y 2D" in t) or ("1D and 2D validations" in t))

print(f"\n==== {ok} verificadas, {fallo} discrepancias ====")
