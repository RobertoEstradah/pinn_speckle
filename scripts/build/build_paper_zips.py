# -*- coding: utf-8 -*-
"""Genera los paquetes de fuentes LaTeX de las ediciones del paper.

Empaqueta cada edicion viva en su carpeta de 'paper/compilado/', incluyendo
solo lo necesario para compilar desde cero: fuentes .tex, la bibliografia, los
archivos de clase y estilo del venue, y las figuras.

Se excluyen deliberadamente el PDF compilado y todos los auxiliares de LaTeX:
el .zip es la fuente, no el resultado. El PDF se entrega por separado en la
misma carpeta.

Sustituye a 'build_comia_paper.py', que NO regeneraba el ZIP: era andamiaje de
un solo uso que generaba main.tex desde una plantilla embebida. Reejecutarlo
hoy destruiria las correcciones hechas a mano sobre COMIA.

Uso:
    python scripts/build/build_paper_zips.py            # todas las ediciones
    python scripts/build/build_paper_zips.py CyS_es     # solo una
"""

from pathlib import Path
import re
import sys
import zipfile

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

RAIZ_PROYECTO = Path(__file__).resolve().parents[2]
PAPER = RAIZ_PROYECTO / "paper"

# Cada edicion: de donde sale, a donde va, y que archivos sueltos de la raiz
# hacen falta ademas de main.tex, latexmkrc y references.bib.
EDICIONES = {
    "validacion1D2D": {
        "fuente": PAPER / "fuente_validacion1D2D",
        "destino": (PAPER / "compilado" / "fuente_validacion1D2D"
                    / "paper_maestria_roberto_hernandez_estrada.zip"),
        "extra": [],
    },
    "CyS_es": {
        "fuente": PAPER / "papers_plantillas" / "CyS" / "fuente" / "es",
        "destino": (PAPER / "compilado" / "CyS" / "es"
                    / "paper_maestria_cys_es_roberto_hernandez_estrada.zip"),
        "extra": ["cys.cls", "cys.bst"],
    },
    "CyS_en": {
        "fuente": PAPER / "papers_plantillas" / "CyS" / "fuente" / "en",
        "destino": (PAPER / "compilado" / "CyS" / "en"
                    / "paper_maestria_cys_en_roberto_hernandez_estrada.zip"),
        "extra": ["cys.cls", "cys.bst"],
    },
    "COMIA": {
        "fuente": PAPER / "papers_plantillas" / "COMIA" / "fuente",
        "destino": (PAPER / "compilado" / "COMIA"
                    / "paper_maestria_comia_roberto_hernandez_estrada.zip"),
        "extra": ["llncs.cls", "splncs04.bst"],
    },
}

COMUNES = ["main.tex", "latexmkrc", "references.bib"]

AUXILIARES = {
    ".aux", ".log", ".out", ".toc", ".lof", ".lot", ".bcf", ".bbl", ".blg",
    ".fls", ".fdb_latexmk", ".synctex.gz", ".xdv", ".dvi", ".bak", ".pdf",
}


def es_auxiliar(ruta: Path) -> bool:
    return (ruta.suffix in AUXILIARES
            or ruta.name.startswith(".")
            or ruta.name.endswith(".run.xml"))


def empaqueta(nombre: str, cfg: dict) -> bool:
    fuente, destino = cfg["fuente"], cfg["destino"]
    if not fuente.is_dir():
        print(f"{nombre}: NO existe la edicion en {fuente}")
        return False

    entradas, faltantes = [], []
    for archivo in COMUNES + cfg["extra"]:
        ruta = fuente / archivo
        if ruta.is_file():
            entradas.append((ruta, archivo))
        else:
            faltantes.append(archivo)
    if faltantes:
        print(f"{nombre}: FALTAN archivos de la edicion: {faltantes}")
        return False

    for sub in ("sections", "figures"):
        carpeta = fuente / sub
        if not carpeta.is_dir():
            print(f"{nombre}: falta la carpeta {sub}/")
            return False
        for ruta in sorted(carpeta.iterdir()):
            if ruta.is_file() and not es_auxiliar(ruta):
                entradas.append((ruta, f"{sub}/{ruta.name}"))

    destino.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as z:
        for ruta, arcname in entradas:
            z.write(ruta, arcname)

    # El paquete debe poder compilarse: comprobar que no falte ninguna figura
    # que el documento referencia. Es la misma guarda que build_tesis_zip.py.
    referidas = set()
    for ruta, arc in entradas:
        if arc.endswith(".tex"):
            texto = ruta.read_text(encoding="utf-8", errors="ignore")
            referidas |= {
                Path(m).stem for m in re.findall(
                    r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", texto)
            }
    incluidas = {Path(a).stem for _, a in entradas if a.startswith("figures/")}
    huerfanas = sorted(referidas - incluidas)

    total = sum(r.stat().st_size for r, _ in entradas)
    tex = sum(1 for _, a in entradas if a.endswith(".tex"))
    figs = sum(1 for _, a in entradas if a.startswith("figures/"))
    print(f"{nombre}: {len(entradas)} archivos ({tex} .tex, {figs} figs), "
          f"{total/1e6:.2f} MB sin comprimir -> "
          f"{destino.stat().st_size/1e6:.2f} MB")
    print(f"  {destino.relative_to(RAIZ_PROYECTO)}")
    if huerfanas:
        print(f"  FIGURAS REFERENCIADAS Y AUSENTES: {huerfanas}")
        return False
    return True


def main():
    pedidas = sys.argv[1:] or list(EDICIONES)
    desconocidas = [p for p in pedidas if p not in EDICIONES]
    if desconocidas:
        raise SystemExit(
            f"Edicion desconocida: {desconocidas}. "
            f"Validas: {', '.join(EDICIONES)}")

    fallos = [n for n in pedidas if not empaqueta(n, EDICIONES[n])]
    if fallos:
        raise SystemExit(f"\nFALLARON: {', '.join(fallos)}")
    print(f"\n{len(pedidas)} ediciones empaquetadas, 0 figuras ausentes")


if __name__ == "__main__":
    main()
