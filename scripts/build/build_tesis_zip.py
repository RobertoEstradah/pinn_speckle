# -*- coding: utf-8 -*-
"""Genera el paquete de fuentes LaTeX de la tesis para entrega u Overleaf.

Empaqueta 'tesis/Tesis_Actual/' en
'tesis/compilado/Actual/tesis_maestria_roberto_hernandez_estrada.zip',
incluyendo solo lo necesario para compilar desde cero: fuentes .tex, la
bibliografia, los archivos de formato institucional y las figuras.

Se excluyen deliberadamente el PDF compilado y todos los auxiliares de LaTeX:
el .zip es la fuente, no el resultado. El PDF se entrega por separado en la
misma carpeta.

Uso:
    python scripts/build/build_tesis_zip.py
"""

from pathlib import Path
import sys
import zipfile

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FUENTE = PROJECT_ROOT / "tesis" / "Tesis_Actual"
DESTINO = (PROJECT_ROOT / "tesis" / "compilado" / "Actual"
           / "tesis_maestria_roberto_hernandez_estrada.zip")

# Archivos de la raiz de la edicion: fuentes, formato institucional y config.
RAIZ = [
    "main.tex", "latexmkrc", "references.bib",
    "Portada.tex", "Declaracion-autoria.tex", "Cesion-derechos.tex",
    "Resumen.tex", "Abstract.tex",
    "base_azul.pdf", "base_blanca.pdf", "Oficio.pdf",
]

# Extensiones de auxiliares de LaTeX que nunca deben viajar en el paquete.
AUXILIARES = {
    ".aux", ".log", ".out", ".toc", ".lof", ".lot", ".bcf", ".bbl", ".blg",
    ".fls", ".fdb_latexmk", ".synctex.gz", ".xdv", ".bak",
}


def es_auxiliar(ruta: Path) -> bool:
    return (ruta.suffix in AUXILIARES
            or ruta.name.startswith(".")
            or "SAVE-ERROR" in ruta.name)


def main():
    if not FUENTE.is_dir():
        raise SystemExit(f"No existe la edicion fuente: {FUENTE}")

    entradas = []
    faltantes = []
    for nombre in RAIZ:
        ruta = FUENTE / nombre
        (entradas if ruta.is_file() else faltantes).append(
            (ruta, nombre) if ruta.is_file() else nombre
        )
    if faltantes:
        raise SystemExit(f"Faltan archivos de la edicion: {faltantes}")

    for sub in ("chapters", "figures"):
        carpeta = FUENTE / sub
        if not carpeta.is_dir():
            raise SystemExit(f"Falta la carpeta {sub}/ en la edicion")
        for ruta in sorted(carpeta.iterdir()):
            if ruta.is_file() and not es_auxiliar(ruta):
                entradas.append((ruta, f"{sub}/{ruta.name}"))

    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(DESTINO, "w", zipfile.ZIP_DEFLATED) as z:
        for ruta, arcname in entradas:
            z.write(ruta, arcname)

    total = sum(r.stat().st_size for r, _ in entradas)
    print(f"{len(entradas)} archivos, {total/1e6:.2f} MB sin comprimir")
    print(f"  .tex : {sum(1 for _, a in entradas if a.endswith('.tex'))}")
    print(f"  figs : {sum(1 for _, a in entradas if a.startswith('figures/'))}")
    print(f"ZIP: {DESTINO}  ({DESTINO.stat().st_size/1e6:.2f} MB)")

    # Comprobacion: el paquete debe poder compilarse, es decir contener main.tex
    # y todas las figuras que el documento referencia.
    import re
    referidas = set()
    for ruta, arc in entradas:
        if arc.endswith(".tex"):
            texto = ruta.read_text(encoding="utf-8", errors="ignore")
            referidas |= {Path(m).stem for m in
                          re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", texto)}
    incluidas = {Path(a).stem for _, a in entradas if a.startswith("figures/")}
    incluidas |= {Path(a).stem for _, a in entradas if a.endswith(".pdf")}
    huerfanas = sorted(referidas - incluidas)
    print(f"figuras referenciadas y ausentes: {huerfanas or 'ninguna'}")


if __name__ == "__main__":
    main()
