---
name: actualiza-documentos
description: >
  Regenera los entregables de la tesis en cascada — tesis, artículo y, si se pide,
  la adaptación a la plantilla de un venue. Cada etapa compila, verifica sus cifras
  contra los resultados, y sólo entonces deja pasar a la siguiente. Usar cuando el
  usuario diga "actualiza los documentos", "regenera la tesis", "recompila todo",
  "actualiza el paper", o invoque `/actualiza-documentos`. NO hace commit ni push.
argument-hint: "[etapa inicial: tesis | paper | plantilla] — sin argumento empieza en tesis"
allowed-tools: Read,Grep,Glob,Bash,AskUserQuestion,SendUserFile
---

# Actualiza documentos

Tres etapas encadenadas. **El orden no es una preferencia, es una dependencia:**
la tesis es el documento base, el artículo deriva de ella, y la plantilla deriva
del artículo. Una cifra que cambia arriba invalida lo de abajo.

```
[1] TESIS ──► compila ──► verifica 369 cifras ──► PDF + ZIP
     │                         └── ¿falla? PARA
     ▼
[2] ARTÍCULO ──► compila ──► PDF        (no tiene verificador propio)
     │              └── ¿errores de LaTeX? PARA
     ▼
[3] PLANTILLA ──► compila ──► verifica 39 contra la tesis ──► PDF + ZIP
                                └── ¿falla? PARA
```

**Dónde vive cada verificador.** `verifica_cifras_tesis.py` lee la tesis.
`verifica_paper_vs_tesis.py` lee las **tres ediciones de plantilla** --CyS
español, CyS inglés y COMIA--, no `fuente_validacion1D2D`, así que **pertenece a
la etapa 3**. Son 13 comprobaciones por edición, 39 en total.

La edición `fuente_validacion1D2D` **no tiene verificador**: para ella, la única
comprobación es que LaTeX compile sin errores. COMIA tampoco lo tenía hasta el
18/09/2026, y en ocho días acumuló siete afirmaciones falsas que nadie vio --el
título con «acelerada», el 13 % obsoleto llamado «variance», y un reclamo de
sustituir a FEM en tiempo real. **Una edición sin verificador se pudre en
silencio.**

---

## Reglas que no se negocian

1. **Nunca hacer commit ni push.** Al terminar se reporta qué quedó modificado y
   se deja la decisión al autor. Regla del proyecto, no de esta skill.
2. **Si un verificador no termina en `0 discrepancias`, parar en seco.** No pasar
   a la etapa siguiente. Reportar exactamente qué cifra no cuadra y esperar.
   Propagar un número equivocado a la plantilla es el peor resultado posible.
3. **Donde el paper y la tesis discrepen, se corrige el paper.** Nunca al revés.
   Es la regla que implementa `verifica_paper_vs_tesis.py` en su propia salida.
4. **No tocar la capa computacional.** Ni `notebooks/`, ni `src/`, ni `results/`,
   ni `scripts/experiments/`. Esta skill compila y verifica; no reentrena nada.
5. **Cap1 (Generalidades) no se modifica** sin consultarlo con el Dr. Adán.

---

## Argumento de entrada

| Invocación | Empieza en |
|---|---|
| `/actualiza-documentos` | Etapa 1 (tesis) |
| `/actualiza-documentos tesis` | Etapa 1 |
| `/actualiza-documentos paper` | Etapa 2 |
| `/actualiza-documentos plantilla` | Etapa 3 |

Al saltar etapas, **avisar** de que las anteriores no se revalidaron: el PDF que
hay en disco puede ser de un estado anterior.

---

## Etapa 1 — Tesis

Preguntar con `AskUserQuestion`, cabecera `Tesis`:

| # | Opción | Ruta |
|---|---|---|
| 1 | **Completa** — Cap1 a Cap4, speckle en 1λ, 2λ, 5λ y 10λ | `tesis/Tesis_Actual/` |
| 2 | **Hasta 2D** — sin resultados de speckle | `tesis/fuente_base/` |
| 3 | **Otra / saltar esta etapa** | preguntar cuál |

Las dos existen ya en disco; no hay que construir nada para la opción 2.

**Las dos ediciones llevan títulos distintos, y es correcto que así sea.**
`Tesis_Actual` valida speckle y se titula «Simulación del speckle óptico
mediante Redes Neuronales Informadas por Física: formulación modal de
Helmholtz». `fuente_base` **no tiene resultados de speckle** --su Cap4 lista
NB03 como pendiente-- y se titula por el alcance que sí entrega: «Validación de
Redes Neuronales Informadas por Física con activación sinusoidal para la
ecuación de Helmholtz 1D y 2D con campo complejo», el mismo del paper. No
unificarlos: cada uno promete lo que cumple.

`fuente_base` son **42 páginas** y no genera ZIP.

### Qué ejecutar

```bash
cd tesis/<edicion> && latexmk main.tex
```

Comprobar en el log:

- `0` líneas que empiecen por `!`
- `0` coincidencias de `Citation .* undefined` o `Reference .* undefined`
- que salga `Output written on main.pdf (N pages)`

**Cuidado con el primer `latexmk` tras un `latexmk -C`:** las pasadas
intermedias muestran citas sin resolver que la pasada final sí resuelve.
Comprobar el estado *final*, volviendo a correr `latexmk` si hace falta.

Luego el verificador, que es el que manda:

```bash
python scripts/experiments/verifica_cifras_tesis.py
```

Debe terminar en `369 verificadas, 0 discrepancias`. Si no, **parar** y decir qué
cifra falló, en qué archivo y contra qué `.json` se comparó.

El verificador lleva además **guardas de afirmación**, que no comparan cifras
sino comprueban que el texto siga diciendo lo que el dato sostiene: que ningún
máximo de $10\lambda$ caiga en el plano final, que el incremento de $5$ a
$10\lambda$ siga siendo $0.373$ puntos, y que la corrida de $20\lambda$ siga
excediendo el $5\%$. Si una falla, el problema está en el texto, no en la cifra.

### Entregables

Sólo para la edición `Tesis_Actual`:

```bash
cp tesis/Tesis_Actual/main.pdf tesis/compilado/Actual/tesis_maestria_roberto_hernandez_estrada.pdf
python scripts/build/build_tesis_zip.py
```

El ZIP lleva fuentes, `references.bib`, los archivos de formato institucional y
`figures/`. **No lleva el PDF ni auxiliares de LaTeX.** El script comprueba que no
falte ninguna figura referenciada; si avisa de una que falta, parar.

---

## Etapa 2 — Artículo

Preguntar, cabecera `Artículo`:

| # | Opción | Estado |
|---|---|---|
| 1 | **Validación 1D y 2D** — el alcance vigente | `paper/fuente_validacion1D2D/` |
| 2 | **Con speckle** | **No existe en disco** |
| 3 | **Otra / saltar esta etapa** | preguntar cuál |

### Si eligen la opción 2

`paper/fuente_conNB03/` se eliminó el 28/08/2026. **No recrearla en silencio.**
Decir esto y pedir confirmación explícita:

> Esa edición no existe. Está en el commit `3489f4c` y habría que recuperarla,
> pero fue escrita antes de NB03B y NB03C, así que sus cifras de speckle están
> desactualizadas: no conocía ni el 0.993 % de 2λ ni el 2.244 % de 5λ.
> ¿La recupero de todos modos?

Si dicen que sí: `git show 3489f4c` para localizarla, restaurarla, y **avisar de
que su contenido necesita revisión manual** antes de darla por buena.

### Qué ejecutar

```bash
cd paper/fuente_validacion1D2D && latexmk main.tex
```

Esta edición usa **XeLaTeX**, así que el log dice `Output written on main.xdv`,
no `main.pdf`. Buscar el conteo de páginas ahí. Son **20 páginas**; las 9 que
menciona `CLAUDE.md` son la versión CyS, que es otra cosa.

**No hay verificador para esta edición.** El único criterio es que compile con
0 errores y 0 referencias sin resolver.

### Entregable, con su nombre exacto

```bash
cp paper/fuente_validacion1D2D/main.pdf \
   paper/compilado/fuente_validacion1D2D/paper_maestria_roberto_hernandez_estrada.pdf
```

**Nunca dejar un `main.pdf` en `paper/compilado/`.** Cada carpeta tiene su
nombre propio; copiar con el nombre de origen ensucia el directorio de
entregables.

| Destino | Nombre del PDF |
|---|---|
| `paper/compilado/fuente_validacion1D2D/` | `paper_maestria_roberto_hernandez_estrada.pdf` |
| `paper/compilado/CyS/es/` | `paper_maestria_cys_es_roberto_hernandez_estrada.pdf` |
| `paper/compilado/CyS/en/` | `paper_maestria_cys_en_roberto_hernandez_estrada.pdf` |

Los `.zip` de esas carpetas se regeneran con `build_paper_zips.py` --ver la
etapa 3--. Tras recompilar cualquier edición, **regenerar también su ZIP**: si no,
queda desfasado respecto a su PDF.

---

## Etapa 3 — Plantilla

Preguntar primero si quieren adaptarlo. Cabecera `Plantilla`:

| # | Opción | Estado |
|---|---|---|
| 1 | **CyS** (español e inglés) | Adaptada y activa — la revista decidida con el director |
| 2 | **COMIA** (LNCS/Springer) | Adaptada y activa |
| 3 | **Otra / ninguna** | preguntar cuál |

Las cinco restantes están en blanco, cada una con su `README.md` documentando
indexación, costo y periodicidad: `CLEI`, `InteligenciaArtificial_IBERAMIA`,
`IJCOPI`, `RevistaColombianaComputacion`, `RevistaMatematica_UCR`. Adaptar una de
esas es trabajo de redacción, no de compilación — **no intentarlo dentro de esta
skill**; decirlo y parar.

### CyS

Dos idiomas, cada uno con su `main.tex`, su `cys.cls` y su `cys.bst`:

```bash
cd paper/papers_plantillas/CyS/fuente/es && latexmk main.tex
cd paper/papers_plantillas/CyS/fuente/en && latexmk main.tex
```

Ambas carpetas llevan un `latexmkrc` con `$pdf_mode = 1;` y `$bibtex_use = 2;`.
**Si falta, `latexmk` arranca en modo DVI y muere en la primera figura** — ver
errores conocidos. Se añadió el 18/09/2026 tras ese fallo. La clase `cys` usa
BibTeX clásico, no biber.

Luego el verificador, que es el que manda en esta etapa:

```bash
python scripts/experiments/verifica_paper_vs_tesis.py
```

Lee **ambos idiomas** en una sola pasada, así que basta con correrlo una vez
después de tocar cualquiera de los dos. Debe terminar en
`39 verificadas, 0 discrepancias` --13 por cada una de las tres ediciones: CyS
espanol, CyS ingles y COMIA--. Si falla, **parar** — y recordar que lo que
se corrige es el paper, no la tesis.

Copiar los PDF a `paper/compilado/CyS/{es,en}/` con los nombres de la tabla de
la etapa 2.

### COMIA

```bash
cd paper/papers_plantillas/COMIA/fuente && latexmk main.tex
```

Salida a `paper/compilado/COMIA/`, con el nombre de la tabla de la etapa 2.
Lleva su propio `latexmkrc` desde el 18/09/2026, por el mismo fallo de DVI que
tenía CyS.

**No usar `build_comia_paper.py`.** Es andamiaje de un solo uso que generaba
`main.tex` desde una plantilla embebida; ejecutarlo destruiría las correcciones
hechas a mano. El propio script se niega a correr y lo explica.

### Los ZIP de las ediciones del paper

```bash
python scripts/build/build_paper_zips.py          # las cuatro
python scripts/build/build_paper_zips.py COMIA    # sólo una
```

Empaqueta `validacion1D2D`, `CyS_es`, `CyS_en` y `COMIA`. Comprueba, como el de
la tesis, que no falte ninguna figura referenciada, y falla si falta alguna.

---

## Informe final

Una tabla, no prosa:

| Etapa | Edición | Páginas | Verificador | Entregable |
|---|---|---|---|---|
| Tesis | Tesis_Actual | 81 | 369/369 | PDF + ZIP |
| Artículo | fuente_validacion1D2D | 20 | (no tiene) | PDF + ZIP |
| Plantilla | CyS es + en | 9 + 9 | 39/39 | 2 PDF + 2 ZIP |

Después:

- **Archivos modificados** — la salida literal de `git status --short`.
- **Qué NO entra en el commit** — si se tocó `CLAUDE.md`, decir que está
  gitignorado y que el cambio es local.
- **Propuesta de commit** — la lista exacta de archivos, sin ejecutarlo.

Enviar los PDF generados con `SendUserFile` para que se puedan abrir desde otro
dispositivo.

---

## Errores conocidos

| Síntoma | Causa y salida |
|---|---|
| `Cannot determine size of graphic ... (no BoundingBox)` y `Emergency stop` | La carpeta no tiene `latexmkrc`, así que `latexmk` usa modo **DVI**, que no puede incrustar PNG. Añadir `$pdf_mode = 1;`. Pasó en las dos carpetas de CyS el 18/09/2026 |
| Citas sin resolver tras `latexmk -C` | Pasadas intermedias. Volver a correr `latexmk` y mirar el estado final |
| El log no dice `Output written on main.pdf` | La edición usa XeLaTeX y escribe `main.xdv`, o bien todo estaba al día y no recompiló. Comprobar la fecha del PDF frente a la de los `.tex` |
| `main.pdf` aparece como modificado sin querer | Es un artefacto rastreado; se regenera al compilar. Si no era el objetivo, `git checkout -- tesis/Tesis_Actual/main.pdf` |
| El verificador falla en una cifra de 2λ | La fuente oficial es `results/nb03_distance_pilot/z2_omega1_five_120s/validation_summary.json` (ω₀=1, 120 s, 0.993 %, 5/5). `z2_cinco_uniforme_180s/` es histórica y da 4.257 % |
| `build_tesis_zip.py` avisa de una figura que falta | Parar. Significa que el `.tex` referencia algo que no está en `figures/` |
| Una cifra nueva de la tesis no está verificada | Añadirla a `verifica_cifras_tesis.py`. Es lo único que impide que texto y resultados se separen |
