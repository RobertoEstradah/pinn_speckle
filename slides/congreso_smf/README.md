# Cartel — Congreso Nacional de Física (SMF)

Misma investigación que la tesis, adaptada a formato póster.

| Archivo | Qué es |
|---|---|
| `cartel_pinn_siren_2d.pptx` | **El cartel.** Es el entregable; lo demás sólo explica cómo se hizo |
| `fuente/template-starter.pptx` | Plantilla intermedia sobre la que se construyó |
| `fuente/final-layout/`, `fuente/template-starter-layout/` | Geometría de las cajas y las imágenes, en JSON |
| `fuente/qa/` | Comprobación de fidelidad contra la plantilla oficial |

El script que lo armó es
[`scripts/build_slides_js/build_cartel.mjs`](../../scripts/build_slides_js/build_cartel.mjs).
Sustituye seis imágenes del cartel por las figuras de
`tesis/Tesis_Actual/figures/` y reescribe los textos.

## El script no se ejecuta hoy

Depende del runtime de presentaciones de Codex, clavado a la versión
`26.826.12353`. En esta máquina sólo está instalada la `26.909.11809`, así que
**la construcción no es reproducible tal cual**.

Se conserva como registro de cómo se hizo el cartel, no como pipeline vivo. Si
hiciera falta rehacerlo, hay tres caminos, de menos a más trabajo:

1. Editar `cartel_pinn_siren_2d.pptx` directamente en PowerPoint.
2. Ajustar `RUNTIME_VERSION` (o la variable de entorno
   `CODEX_PRESENTATIONS_VERSION`) a una versión instalada y comprobar si la API
   del runtime sigue siendo compatible.
3. Reescribir el armado con `python-pptx`, como se hizo para las diapositivas
   del coloquio en `scripts/build/add_code_slides.py`.

## Sobre `fuente/template-starter.pptx`

**No es la plantilla oficial del congreso.** La oficial está en
`master_supporting_docs/supporting_slides/congreso_smf_plantilla/` y tiene otro
hash. Ésta es una versión intermedia derivada de aquélla, y no está comprobado
que pueda regenerarse; por eso se conserva.

## Qué se descartó

El armado dejó 27.74 MB de intermedios en `tmp/smf_cartel/`: vistas previas en
PNG, el PPTX descomprimido para inspeccionarle los medios, hojas de contactos y
montajes `.webp`. Se eliminaron el 2026-09-15 por ser regenerables y no aportar
nada que el cartel final no tenga. Si se vuelve a ejecutar el script, esas
salidas van de nuevo a `tmp/`, que está en `.gitignore`.
