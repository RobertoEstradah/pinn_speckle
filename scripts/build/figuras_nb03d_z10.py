# -*- coding: utf-8 -*-
"""Dos figuras de Cap4 seccion sec:nb03_z10, a partir de NB03D.

    nb03d_z10_mapas.png   tres mapas (x,z): referencia, PINN y |diferencia|
                          (formato de la figura 5.5 de la tesis del director,
                          en mapa de color en vez de superficie)
    nb03d_z10_erp.png     error relativo porcentual de la energia frente a z,
                          las cinco pantallas (formula 5.25 del director)

No reentrena nada: lee los .npz ya validados y escribe PNG.
Uso:  python scripts/build/figuras_nb03d_z10.py
"""
import json
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

RAIZ = pathlib.Path(__file__).resolve().parents[2]
RESUMEN = RAIZ / "results/nb03_distance_pilot/nb03d_z10_validation/validation_summary.json"
SALIDA = RAIZ / "tesis/Tesis_Actual/figures"

# La figura va en un documento con fuente Helvetica; que el texto no desentone.
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans"],
    "font.size": 9,
    "axes.linewidth": 0.6,
    "savefig.dpi": 200,
})


def erp(campo):
    """Error relativo porcentual de la energia respecto al plano inicial.

    Es la ecuacion 5.25 de la tesis del director: E(z) = sum |U|^2 sobre la
    seccion transversal, y ERP(z) = 100 |E(0) - E(z)| / E(0).
    """
    e = (np.abs(campo) ** 2).sum(axis=1)
    return 100.0 * np.abs(e[0] - e) / e[0]


def carga():
    resumen = json.loads(RESUMEN.read_text(encoding="utf-8"))
    return [(e["screen_seed"], np.load(RAIZ / e["arrays_path"]), e)
            for e in resumen["per_screen"]]


def mapas(seed, d, meta):
    """Tres mapas (x,z) de la misma pantalla: referencia, PINN y diferencia."""
    z = d["z_lambda"]
    # El ancho del dominio es 20 lambda centrado en cero (fronteras periodicas).
    x = np.linspace(-10.0, 10.0, d["field_pred"].shape[1], endpoint=False)

    # La referencia justa es la propagante: la base modal no puede representar
    # los evanescentes por construccion, asi que compararla con el campo total
    # cargaria al PINN con un error que no es suyo.
    ref = np.abs(d["field_propagating"]) ** 2
    pin = np.abs(d["field_pred"]) ** 2
    dif = np.abs(d["field_propagating"] - d["field_pred"]) ** 2

    vmax = max(ref.max(), pin.max())
    ext = [x[0], x[-1], z[0], z[-1]]

    fig, ejes = plt.subplots(1, 3, figsize=(7.2, 4.0), constrained_layout=True)
    for ax, campo, titulo, tope, mapa in (
        (ejes[0], ref, "Referencia (espectro angular)", vmax, "inferno"),
        (ejes[1], pin, "PINN-SIREN modal", vmax, "inferno"),
        (ejes[2], dif, "$|$Diferencia$|^2$", dif.max(), "viridis"),
    ):
        im = ax.imshow(campo, origin="lower", aspect="auto", extent=ext,
                       cmap=mapa, vmin=0.0, vmax=tope)
        ax.set_title(titulo, fontsize=8.5)
        ax.set_xlabel(r"$x/\lambda$")
        # Marcar las interfaces entre los diez bloques de 1 lambda.
        for b in range(1, 10):
            ax.axhline(b, color="white", lw=0.35, alpha=0.30)
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.02)
    ejes[0].set_ylabel(r"$z/\lambda$")
    for ax in ejes[1:]:
        ax.set_yticklabels([])

    ruta = SALIDA / "nb03d_z10_mapas.png"
    fig.savefig(ruta, bbox_inches="tight")
    plt.close(fig)
    return ruta, float(dif.max()), float(vmax)


def curva_erp(datos):
    """ERP de la energia frente a z: las cinco pantallas y la referencia."""
    fig, ax = plt.subplots(figsize=(6.0, 3.4), constrained_layout=True)

    estilos = ["-", "--", "-.", ":", (0, (3, 1, 1, 1))]
    for (seed, d, _), estilo in zip(datos, estilos):
        ax.plot(d["z_lambda"], erp(d["field_pred"]), linestyle=estilo, lw=1.2,
                label=f"Pantalla {seed}")

    # La referencia sobre el mismo subespacio: conserva a precision de maquina.
    # Sirve de linea base, y demuestra que la metrica esta bien planteada.
    ref = erp(datos[0][1]["field_propagating"])
    ax.plot(datos[0][1]["z_lambda"], ref, color="0.45", lw=0.9,
            label=f"Referencia propagante (max {ref.max():.0e} %)")

    for b in range(1, 10):
        ax.axvline(b, color="0.85", lw=0.5, zorder=0)
    ax.set_xlabel(r"$z/\lambda$")
    ax.set_ylabel("Error relativo porcentual de la energía (%)")
    ax.set_xlim(0, 10)
    ax.set_ylim(bottom=0)
    ax.legend(fontsize=7.5, ncol=2, frameon=False)

    ruta = SALIDA / "nb03d_z10_erp.png"
    fig.savefig(ruta, bbox_inches="tight")
    plt.close(fig)
    return ruta


def main():
    datos = carga()
    SALIDA.mkdir(parents=True, exist_ok=True)

    seed, d, meta = datos[0]
    ruta_mapas, dmax, vmax = mapas(seed, d, meta)
    print(f"  {ruta_mapas.name}  (pantalla {seed})")
    print(f"    diferencia maxima {dmax:.3e} frente a intensidad maxima {vmax:.3e}"
          f"  ->  {100*dmax/vmax:.2f} % del pico")

    ruta_erp = curva_erp(datos)
    print(f"  {ruta_erp.name}")
    for seed, d, _ in datos:
        e = erp(d["field_pred"])
        zm = d["z_lambda"][int(e.argmax())]
        print(f"    pantalla {seed:>4}: ERP maximo {e.max():.3f} % en z={zm:.2f}, "
              f"final {e[-1]:.3f} %")

    todos = [erp(d["field_pred"]) for _, d, _ in datos]
    print(f"    ERP maximo sobre las cinco: {max(e.max() for e in todos):.3f} %")
    print(f"    ERP final medio:            {np.mean([e[-1] for e in todos]):.3f} %")


if __name__ == "__main__":
    main()
