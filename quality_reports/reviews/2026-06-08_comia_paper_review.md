# Revisión: paper_comia_roberto_hernandez_estrada.zip
**Fecha:** 2026-06-08  
**Revisor:** writer-critic (modo: Comprehensive — LNCS/COMIA)  
**Archivo:** `paper/paper_comia_roberto_hernandez_estrada.zip`

---

## Puntuación Global: **86 / 100**

| Categoría | Puntos | Máx |
|-----------|--------|-----|
| 1. Estructura y formato LNCS | 18 | 20 |
| 2. Abstract y Keywords | 10 | 15 |
| 3. Contenido y evidencia | 18 | 20 |
| 4. Redacción técnica | 14 | 15 |
| 5. Calidad LaTeX | 13 | 15 |
| 6. Compilación (Verifier) | 13 | 15 |
| **TOTAL** | **86** | **100** |

**Gate:** ≥ 80 → Commit ✅ | < 90 → PR bloqueado ⚠️

---

## Verifier — PASS/FAIL por ítem

| Ítem | Estado |
|------|--------|
| `\documentclass[runningheads]{llncs}` | ✅ PASS |
| `\bibliographystyle{splncs04}` + `\bibliography{}` | ✅ PASS |
| Figuras referenciadas vs. incluidas (4/4) | ✅ PASS |
| Referencias BibTeX resueltas (13/13 claves) | ✅ PASS |
| Sin residuos biblatex (`\citep`, `\citet`) | ✅ PASS |
| `llncs.cls` + `splncs04.bst` en ZIP | ✅ PASS |
| `hyperref` penúltimo, `cleveref` último | ✅ PASS |
| Abstract word count ≥ 150 (LNCS) | ❌ FAIL — 112 palabras |
| Paquete `subcaption` sin uso en secciones | ⚠️ WARNING |
| Multi-cita con espacio `{key1, key2}` | ⚠️ WARNING |

---

## Problemas por Categoría

### Categoría 2 — Abstract y Keywords (-5 pts) **[MAYOR]**

**Problema:** El abstract en inglés tiene **112 palabras**. LNCS requiere 150–250 palabras.

**Fix concreto:** Agregar ~40 palabras expandiendo el último párrafo. Por ejemplo, ampliar la frase sobre multi-seed y añadir una oración sobre la arquitectura SIREN vs. ReLU/tanh:

```latex
% Agregar después de "13\,\% (relative)."
The SIREN architecture outperforms standard ReLU and tanh activations
by preserving second-order derivative stability throughout training,
which is critical for Helmholtz-type wave equations.
The mesh-free evaluation at $100\times100$ grid points takes
$\approx\!1.3\,\mathrm{ms}$, establishing the method as a viable
real-time surrogate for classical numerical solvers.
```

---

### Categoría 5 — Calidad LaTeX (-2 pts) **[MENOR]**

**Problema A:** `\usepackage{subcaption}` declarado en `main.tex` pero **nunca usado** en ninguna sección (0 usos de `\subfigure`, `\subcaptionbox`, etc.). Paquete muerto.

**Fix:** Eliminar la línea del preamble:
```latex
% ELIMINAR esta línea de main.tex:
\usepackage{float}        % conservar
\usepackage{subcaption}   % <- ELIMINAR, no se usa
```

**Problema B:** Multi-cita con espacio en `sections/05_conclusiones.tex` (ya conocido):
```latex
% Actual (puede fallar en algunos BibTeX):
~\cite{Cuomo2022_review, Karniadakis2021_review}.
% Corregido:
~\cite{Cuomo2022_review,Karniadakis2021_review}.
```

---

### Categoría 6 — Compilación (-2 pts) **[ADVISORY]**

**Advertencia:** `cleveref` con opción `[spanish]` y `llncs.cls` no han sido probados juntos en Overleaf pdfLaTeX. Si aparece error al compilar, cambiar:
```latex
% Opción conservadora (sin spanish):
\usepackage[nameinlink]{cleveref}
\crefname{section}{secci\'{o}n}{secciones}
% (mantener redefiniciones manuales)
```

**Advertencia:** `threeparttable` funciona con `llncs` pero genera `Package hyperref Warning: Token not allowed`. Es un warning, no un error — no bloquea compilación.

---

## Lo que está bien (no modificar)

- ✅ **Conversión de citas completa:** 17 `\citet` + 8 `\citep` convertidos a `\cite{}` sin residuos.
- ✅ **Todas las figuras incluidas:** `resultados_pinn_1d.png`, `resultados_pinn_2d.png`, `metricas_adicionales_1d.png`, `metricas_adicionales_2d.png`.
- ✅ **BibTeX limpio:** 13 claves en `.bib`, 13 claves citadas — coincidencia perfecta, sin huérfanas.
- ✅ **Caveat Schoder 3D vs 1D/2D** presente en tablenote de Tabla 4 (líneas 172–175) — correcto para tabla.
- ✅ **Running heads** configurados: título abreviado y autores abreviados.
- ✅ **Resumen bilingüe** implementado (abstract EN en `abstract`, resumen ES como `\section*{Resumen}`).
- ✅ **`\thanks{}`** corregido: ya no menciona "codirector".
- ✅ **booktabs** en todas las tablas: `\toprule`, `\midrule`, `\bottomrule`, sin `\hline`.
- ✅ **`threeparttable`** con `tablenotes` en las 3 tablas de resultados.

---

## Fixes para alcanzar 90/100 (gate PR)

| Fix | Puntos ganados | Archivo | Líneas |
|-----|---------------|---------|--------|
| Expandir abstract a ≥150 palabras | +4 | `main.tex` | ~L69–85 |
| Eliminar `\usepackage{subcaption}` | +1 | `main.tex` | ~L38 |
| Quitar espacio en multi-cita | +1 | `sections/05_conclusiones.tex` | L11 |
| **Total potencial** | **+6 → 92/100** | | |
