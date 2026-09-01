#!/usr/bin/env bash
# actualizar-reporte-cambios.sh
# Recompila tesis/Tesis_actualizada, refresca tesis/compilado/actualizada,
# y genera el reporte de cambios en tesis/Tesis_actualizada/reporte_cambios/.
#
# Uso:
#   bash scripts/build/actualizar-reporte-cambios.sh
#   bash scripts/build/actualizar-reporte-cambios.sh --base actualizada
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
ACT_DIR="$REPO_ROOT/tesis/Tesis_actualizada"
COMP_DIR="$REPO_ROOT/tesis/compilado/actualizada"
PDF_NAME="tesis_maestria_roberto_hernandez_estrada.pdf"
ZIP_NAME="tesis_maestria_roberto_hernandez_estrada.zip"

echo "==> Compilando tesis/Tesis_actualizada/main.tex ..."
( cd "$ACT_DIR" && latexmk -interaction=nonstopmode -g main.tex )

echo "==> Actualizando tesis/compilado/actualizada/ ..."
mkdir -p "$COMP_DIR"
cp "$ACT_DIR/main.pdf" "$COMP_DIR/$PDF_NAME"
( cd "$ACT_DIR" && zip -r -X -q "$COMP_DIR/$ZIP_NAME" \
    Abstract.tex Resumen.tex Portada.tex Declaracion-autoria.tex Cesion-derechos.tex \
    main.tex latexmkrc references.bib base_azul.pdf base_blanca.pdf Oficio.pdf \
    chapters figures -x "*.aux" )

echo "==> Generando reporte de cambios ..."
python "$REPO_ROOT/scripts/build/actualizar_reporte_cambios.py" "$@"
