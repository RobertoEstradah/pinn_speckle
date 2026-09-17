# -*- coding: utf-8 -*-
"""Figura del patron de speckle: PINN modal frente a la referencia.

La tesis reporta el speckle con metricas pero nunca lo muestra. Esta figura
genera el mapa de intensidad sobre (x, z) para las dos, mas el perfil en el
plano de validacion z=1 lambda.

Uso:
    python scripts/experiments/nb03_figura_speckle.py
"""

from pathlib import Path
import os
import sys

import numpy as np

os.environ.setdefault("MPLBACKEND", "Agg")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

# omega_0 antes de importar: no vive en el state_dict.
os.environ.setdefault("NB03_MODAL_FIRST_OMEGA", "1")
os.environ.setdefault("NB03_MODAL_HIDDEN_OMEGA", "1")
os.environ.setdefault("NB03_DISTANCE_LAMBDA", "1")
# La referencia validada de NB03 es la de correlacion 0.10 lambda.
# El defecto del modulo es 0.50, que da OTRA pantalla y otro piso.
os.environ.setdefault("NB03_REFERENCE_SUFFIX", "_z1_corr0.10")

import matplotlib.pyplot as plt  # noqa: E402
import torch  # noqa: E402

from scripts.experiments import nb03_modal_pinn_siren as modal  # noqa: E402
from scripts.experiments import nb03_pinn_slabs as base  # noqa: E402

PANTALLA = 42
MODELO = "nb03_modal_pinn_siren_z1_screen42_omega1_finetune.pt"
N_Z = 201


def main():
    modal.FIRST_OMEGA = 1.0
    modal.HIDDEN_OMEGA = 1.0

    base.set_seed(base.SEED)
    referencia = base.load_reference()
    x = referencia["x_lambda"]
    kx = referencia["kx"]
    activos = referencia["propagating_mask"].astype(bool)
    kx_act = kx[activos]

    # ── referencia: espectro angular completo sobre la rejilla de z ─────────
    espectro = np.fft.fft(np.exp(1j * referencia["phase"]))
    kz = np.sqrt((base.K ** 2 - kx ** 2).astype(complex))
    z = np.linspace(0.0, base.DISTANCE_LAMBDA, N_Z)
    campo_ref = np.stack([
        np.fft.ifft(espectro * np.exp(1j * kz * zi)) for zi in z
    ])

    # ── PINN: se reconstruye el modelo y se evalua en la misma rejilla ──────
    campo0, dz0 = base.radiative_input(referencia)[1:]
    escala = float(np.sqrt(np.mean(np.abs(campo0) ** 2)))
    esp0 = np.fft.fft(campo0 / escala) / len(x)
    esp_dz0 = np.fft.fft(dz0 / escala) / len(x)
    fase = np.exp(-1j * kx_act * float(x[0]))
    a0 = esp0[activos] * fase
    da0 = esp_dz0[activos] * fase
    coef0 = np.column_stack((a0.real, a0.imag)).astype(np.float32).reshape(-1)
    der0 = np.column_stack((da0.real, da0.imag)).astype(np.float32).reshape(-1)
    amp = np.maximum(np.abs(a0), np.abs(da0) / base.K)
    amp = np.maximum(amp, max(float(amp.max()) * 1e-4, 1e-8))
    escala_corr = np.repeat((base.K ** 2 * amp).astype(np.float32), 2)

    dispositivo = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    red = modal.ModalSiren(
        torch.tensor(coef0, device=dispositivo),
        torch.tensor(der0, device=dispositivo),
        torch.tensor(escala_corr, device=dispositivo),
        base.DISTANCE_LAMBDA,
    ).to(dispositivo)
    red.load_state_dict(torch.load(
        PROJECT_ROOT / "results" / "models" / MODELO,
        map_location=dispositivo, weights_only=True,
    ))
    red.eval()
    with torch.no_grad():
        zt = torch.tensor(z.reshape(-1, 1), dtype=torch.float32, device=dispositivo)
        coef = red(zt).cpu().numpy().reshape(len(z), -1, 2) * escala
    campo_pinn = np.stack([
        modal.coefficients_to_field(coef[i], x, kx_act) for i in range(len(z))
    ])

    i_ref = np.abs(campo_ref) ** 2
    i_pinn = np.abs(campo_pinn) ** 2
    vmax = float(max(i_ref.max(), i_pinn.max()))

    # ── figura ──────────────────────────────────────────────────────────────
    fig = plt.figure(figsize=(11.0, 6.9))
    ejes = fig.subplot_mosaic([["ref", "pinn"], ["perfil", "perfil"]],
                              height_ratios=[1.35, 1.0],
                              gridspec_kw={"hspace": 0.42, "wspace": 0.12})

    for clave, campo, titulo in (("ref", i_ref, "Referencia (espectro angular)"),
                                 ("pinn", i_pinn, "PINN-SIREN modal")):
        ax = ejes[clave]
        im = ax.imshow(campo, origin="lower", aspect="auto", cmap="inferno",
                       vmin=0.0, vmax=vmax,
                       extent=[x[0], x[-1], z[0], z[-1]])
        ax.set_xlabel(r"$x/\lambda$")
        ax.set_title(titulo, fontsize=11)
        ax.axhline(1.0, color="white", lw=0.8, ls="--", alpha=0.7)
    ejes["ref"].set_ylabel(r"$z/\lambda$")
    fig.colorbar(im, ax=[ejes["ref"], ejes["pinn"]], label=r"$|E|^2$",
                 fraction=0.035, pad=0.02)

    ax = ejes["perfil"]
    ax.plot(x, i_ref[-1], color="0.25", lw=1.4, label="Referencia")
    ax.plot(x, i_pinn[-1], color="tab:red", lw=1.0, ls="--", label="PINN-SIREN")
    ax.set_xlabel(r"$x/\lambda$")
    ax.set_ylabel(r"$|E|^2$")
    ax.set_xlim(x[0], x[-1])
    ax.legend(loc="upper right", fontsize=9, framealpha=0.9)
    ax.set_title(r"Perfil de intensidad en el plano de validación $z=1\lambda$",
                 fontsize=10)

    destino = PROJECT_ROOT / "results" / "figures" / "nb03_speckle_campo_z1.png"
    fig.savefig(destino, dpi=170, bbox_inches="tight")
    plt.close(fig)

    n = np.linalg.norm
    print(f"pantalla {PANTALLA}")
    print(f"  L2 del campo en z=1 lambda : "
          f"{100 * n(campo_pinn[-1] - campo_ref[-1]) / n(campo_ref[-1]):.3f} %")
    print(f"  contraste referencia       : {i_ref[-1].std() / i_ref[-1].mean():.4f}")
    print(f"  contraste PINN             : {i_pinn[-1].std() / i_pinn[-1].mean():.4f}")
    print(f"  figura: {destino}")


if __name__ == "__main__":
    main()
