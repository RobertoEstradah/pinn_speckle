"""
actualizar_reporte_cambios.py
=============================
Genera un reporte Markdown con las diferencias de contenido entre dos
compilados de la tesis (por defecto: tesis/compilado/conNB03 vs
tesis/compilado/actual), con la pagina exacta de cada cambio.

Uso:
    python scripts/build/actualizar_reporte_cambios.py [--base conNB03|actual]

    --base conNB03  (default) compara conNB03 (respaldo) vs
                    actual (estado actual). Uso normal.
    --base actual   compara la ultima instantanea guardada de
                    "actual" vs el estado actual -- util para ver
                    solo los cambios mas recientes dentro de la edicion
                    de trabajo, sin arrastrar todo el historial desde NB03.

Salida:
    tesis/Tesis_Actual/reporte_cambios/DD-MM-AA_reporte_cambios_roberto_hernandez_estrada.md
    (se sobrescribe si ya se genero un reporte ese mismo dia)
"""

import argparse
import difflib
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CONNB03_PDF = REPO_ROOT / "tesis/compilado/conNB03/tesis_maestria_roberto_hernandez_estrada.pdf"
ACTUAL_PDF = REPO_ROOT / "tesis/compilado/actual/tesis_maestria_roberto_hernandez_estrada.pdf"
REPORT_DIR = REPO_ROOT / "tesis/Tesis_Actual/reporte_cambios"
SNAPSHOT_FILE = REPORT_DIR / ".ultimo_snapshot_actual.txt"

MAX_CELL_LEN = 260


def extract_pages(pdf_path: Path):
    """Devuelve (lineas, pagina_de_cada_linea) usando pdftotext -layout."""
    result = subprocess.run(
        ["pdftotext", "-layout", str(pdf_path), "-"],
        capture_output=True,
    )
    text = result.stdout.decode("utf-8", errors="replace")
    pages = text.split("\f")
    lines, page_of_line = [], []
    for page_num, page_text in enumerate(pages, start=1):
        for line in page_text.split("\n"):
            lines.append(line)
            page_of_line.append(page_num)
    return lines, page_of_line


def compact_diff(old_text: str, new_text: str) -> str:
    """Extrae solo las palabras que cambiaron entre dos frases (prefijo/sufijo comun descartado)."""
    old_w, new_w = old_text.split(), new_text.split()
    i = 0
    while i < min(len(old_w), len(new_w)) and old_w[i] == new_w[i]:
        i += 1
    j = 0
    while j < min(len(old_w), len(new_w)) - i and old_w[-1 - j] == new_w[-1 - j]:
        j += 1
    old_mid = old_w[i: len(old_w) - j] if j else old_w[i:]
    new_mid = new_w[i: len(new_w) - j] if j else new_w[i:]
    old_s = " ".join(old_mid) or "(vacio)"
    new_s = " ".join(new_mid) or "(vacio)"
    return f"{old_s} -> {new_s}"


def truncate(s: str, n: int = MAX_CELL_LEN) -> str:
    s = " ".join(s.split())
    return s if len(s) <= n else s[: n - 1] + "..."


def find_changes(lines_old, pages_old, lines_new, pages_new):
    sm = difflib.SequenceMatcher(None, lines_old, lines_new, autojunk=False)
    rows = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        old_chunk = [l.strip() for l in lines_old[i1:i2] if l.strip()]
        new_chunk = [l.strip() for l in lines_new[j1:j2] if l.strip()]
        if old_chunk == new_chunk:
            continue  # reflow/whitespace, no cambio real
        if not old_chunk and not new_chunk:
            continue
        page_old = pages_old[i1] if i1 < len(pages_old) else (pages_old[-1] if pages_old else 0)
        page_new = pages_new[j1] if j1 < len(pages_new) else (pages_new[-1] if pages_new else 0)
        pagina = str(page_new) if page_old == page_new else f"{page_old}->{page_new}"
        antes = truncate(" ".join(old_chunk)) if old_chunk else "(sin contenido previo)"
        despues = truncate(" ".join(new_chunk)) if new_chunk else "(contenido eliminado)"
        correccion = compact_diff(" ".join(old_chunk), " ".join(new_chunk))
        rows.append(
            {
                "pagina": pagina,
                "pagina_sort": page_new,
                "correccion": truncate(correccion, 80),
                "antes": antes,
                "despues": despues,
            }
        )
    rows.sort(key=lambda r: r["pagina_sort"])
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", choices=["conNB03", "actual"], default="conNB03")
    args = parser.parse_args()

    if not ACTUAL_PDF.exists():
        sys.exit(f"No existe {ACTUAL_PDF} -- compila la tesis actual primero.")

    lines_new, pages_new = extract_pages(ACTUAL_PDF)

    if args.base == "actual":
        if SNAPSHOT_FILE.exists():
            old_raw = SNAPSHOT_FILE.read_text(encoding="utf-8")
            lines_old = old_raw.split("\n")
            pages_old = [1] * len(lines_old)  # snapshot plano, sin paginacion propia
            base_label = "actual (instantanea anterior)"
            usando_fallback = False
        else:
            if not CONNB03_PDF.exists():
                sys.exit("No hay instantanea previa ni conNB03 disponible para comparar.")
            lines_old, pages_old = extract_pages(CONNB03_PDF)
            base_label = "conNB03 (no habia instantanea previa de 'actual', se usa como respaldo)"
            usando_fallback = True
    else:
        if not CONNB03_PDF.exists():
            sys.exit(f"No existe {CONNB03_PDF}")
        lines_old, pages_old = extract_pages(CONNB03_PDF)
        base_label = "conNB03"
        usando_fallback = False

    rows = find_changes(lines_old, pages_old, lines_new, pages_new)

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    fecha = datetime.now().strftime("%d-%m-%y")
    fecha_larga = datetime.now().strftime("%d/%m/%Y %H:%M")
    out_path = REPORT_DIR / f"{fecha}_reporte_cambios_roberto_hernandez_estrada.md"

    lines_md = [
        "# Reporte de cambios -- Tesis Roberto Hernandez Estrada",
        "",
        f"**Fecha de generacion:** {fecha_larga}",
        f"**Comparacion:** `{base_label}` (antes)  vs.  `actual` (despues)",
        f"**Cambios detectados:** {len(rows)}",
        "",
    ]

    if not rows:
        lines_md.append("_No se detectaron diferencias de contenido entre ambas versiones._")
    else:
        lines_md.append("| Correccion | Pagina | Antes | Despues |")
        lines_md.append("|---|---|---|---|")
        for r in rows:
            lines_md.append(
                f"| {r['correccion']} | {r['pagina']} | {r['antes']} | {r['despues']} |"
            )

    out_path.write_text("\n".join(lines_md) + "\n", encoding="utf-8")

    # Actualiza la instantanea para la proxima corrida con --base actual
    SNAPSHOT_FILE.write_text("\n".join(lines_new), encoding="utf-8")

    print(f"Reporte generado: {out_path}")
    print(f"Cambios detectados: {len(rows)}")
    if usando_fallback:
        print("Nota: no habia instantanea previa de 'actual'; se uso conNB03 como base.")


if __name__ == "__main__":
    main()
