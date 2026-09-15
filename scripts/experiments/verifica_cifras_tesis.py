# -*- coding: utf-8 -*-
"""Verifica cada cifra de la seccion NB03 de Cap4 contra su archivo fuente."""
import json
import sys
import numpy as np

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

R = r"C:\roberto\Tesis_Maestria"
ok = fallo = 0


def chk(etiqueta, en_tesis, real, tol=5e-4):
    global ok, fallo
    bien = abs(en_tesis - real) <= tol * max(1.0, abs(real))
    print(f"  {'OK   ' if bien else 'FALLA'} {etiqueta:<46} tesis={en_tesis:<12} real={real}")
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

print(f"\n==== {ok} verificadas, {fallo} discrepancias ====")
