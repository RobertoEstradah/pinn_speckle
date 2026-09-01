# Revisión Comprensiva — paper/main.tex
**Fecha:** 2026-05-31  
**Archivo:** `paper/main.tex` + secciones 01–05  
**Modo:** Comprensivo (.tex auto-detect) → writer-critic + strategist-critic + Verifier  
**Puntaje agregado:** **85 / 100** — APRUEBA gate de commit (≥ 80), NO aprueba gate de PR (≥ 90)

---

## PASS 1 — VERIFIER (Puntaje: 90/100)

### ✅ PASS — Invariantes críticos

| Invariante | Resultado |
|------------|-----------|
| INV-3: Sin `\hline` | ✅ 0 ocurrencias |
| INV-1: Todas las tablas con `threeparttable` + notas | ✅ 4/4 tablas |
| INV-5: Abstract ≤ 150 palabras | ✅ ES=143, EN=148 |
| INV-10: `hyperref` antes de `cleveref` | ✅ posición 1885 < 2466 |
| INV-11: Números consistentes | ✅ 0.006%, 0.171%, 1.0253, ×415, ×11.2 coinciden en tablas y texto |
| Integridad bibliográfica | ✅ 13 claves citadas, todas definidas en `.bib` |
| Keywords (ES + EN) | ✅ Presentes |
| Paquetes requeridos | ✅ `microtype`, `biblatex`, `biber`, `doublespacing`, `fancyhdr`, `booktabs`, `threeparttable` |

### ❌ FAIL — Problemas detectados

| Problema | Archivo | Línea | Severidad |
|----------|---------|-------|-----------|
| Naked `\ref{sec:conclusiones}` — debe usar `\cref` | `04_resultados.tex` | 148 | **MINOR** (−5) |
| 0 figuras en el paper | (ningún `\begin{figure}`) | — | **ADVISORY** (−5) |

**Detalle naked \ref:**
```latex
% 04_resultados.tex:148 — ACTUAL (incorrecto)
La incorporación de esta condición es parte del trabajo futuro (§\,\ref{sec:conclusiones}).

% CORRECTO
La incorporación de esta condición es parte del trabajo futuro (\cref{sec:conclusiones}).
```

**Observación sobre figuras:**  
Un paper de física computacional sin figuras es atípico. Las tablas cubren las métricas numéricas, pero falta visualización de: curvas de convergencia de la pérdida, comparación PINN vs solución analítica, patrón de speckle 2D, e histograma de intensidades. No es un invariante bloqueante, pero reducirá el impacto del artículo significativamente.

**Entradas `.bib` definidas pero no citadas (6 huérfanas):**  
`Cai2021_PINNreview`, `Daw2023_rPINN`, `Haghighat2021_SciANN`, `Lagaris1998_NNdiff`, `Lu2021_DeepXDE`, `Maiocchetti2025_PINN`  
→ Limpiar `references.bib` o incorporar al texto.

---

## PASS 2 — WRITER-CRITIC (Puntaje: 87/100)

### Categoría 1: Estructura y flujo (90/100)

**Bien:**
- Orden estándar Intro → Marco Teórico → Metodología → Resultados → Conclusiones ✅
- Road map en el último párrafo de la Introducción ✅
- Cada subsección tiene título y label ✅
- Las conclusiones numeran los hallazgos de forma clara ✅

**Debilidades:**
- La Introducción (6 bloques) es algo corta para un paper que compite contra FEM. Se podría reforzar la importancia del benchmark NB04 pendiente.
- La sección de Trabajo Futuro usa `subsection*` (sin número). Dado que es parte de las Conclusiones, esto es aceptable.

### Categoría 2: Alineación claims-evidencia (85/100)

**Bien:**
- Todas las métricas en texto tienen su tabla de respaldo ✅
- El fallo del test KS se explica honestamente con dos causas (potencia estadística, ausencia de condición de Sommerfeld) ✅
- La justificación de λ_phys=0.1 es explícita y correcta ✅
- "por casi tres órdenes de magnitud" → 5%/0.006% = 833× ≈ 2.9 OOM — correcto ✅

**Debilidades:**
- **Claim de velocidad sin respaldo cuantitativo**: La Introducción afirma "el modelo evalúa nuevas configuraciones en *microsegundos*" (línea 29). Este dato no aparece en la sección de Resultados. Si la inferencia real es en microsegundos es una ventaja enorme; si no se ha medido, la afirmación debe removerse o calificarse como "subcientésimas de segundo" o similar. **(−5)**
- **Contribución LHS no demostrada**: Se afirma que LHS redujo el error en regiones de baja densidad vs mallas cartesianas equivalentes, pero no se presenta una tabla comparativa LHS vs malla uniforme. Es un hallazgo clave que quedó sin validar cuantitativamente.

### Categoría 3: Calidad de escritura (88/100)

**Bien:**
- Español técnico correcto y consistente ✅
- Terminología uniforme ("speckle completamente desarrollado", "libre de malla") ✅
- Ecuaciones numeradas y referenciadas con `\cref` (salvo una excepción) ✅

**Debilidades:**
- "reduciendo drásticamente el costo de almacenamiento" (§3.1, línea 52) — "drásticamente" es vago en un paper técnico. Cuantificar o calificar.
- La comparación "superando al estado del arte en ×415 y ×11.2" se basa en un único paper (Schoder 2024). Un revisor puede objetar que un paper no es suficiente para establecer un SOTA. Se recomienda agregar una frase de calificación: "respecto al único trabajo de referencia disponible para Helmholtz con PINNs".

### Categoría 4: Formato LaTeX (94/100)

**Bien:**
- Todas las tablas: `booktabs` + `threeparttable` + notas ✅
- Paquetes en orden correcto ✅
- `\cref{}` usado consistentemente (except una) ✅
- Biblatex/biber configurado correctamente ✅

**Falla:**
- 1 naked `\ref{sec:conclusiones}` en `04_resultados.tex:148` → −3
- Sin figuras (INV-2 advisory) → −3

### Categoría 5: Compilación (no ejecutable — análisis estático)

- 40 labels definidas, 9 referencias `\cref` — todas resolvibles ✅
- 13 claves BibTeX usadas — todas definidas en `.bib` ✅
- Sin comandos LaTeX aparentemente erróneos ✅
- **Nota:** Compilación real (pdflatex + biber + pdflatex + pdflatex) no ejecutada por ausencia de instalación TeX en entorno.

---

## PASS 3 — STRATEGIST-CRITIC / VALIDACIÓN METODOLÓGICA (Puntaje: 78/100)

*(Adaptado al paradigma de física computacional: validación numérica en lugar de identificación causal.)*

### Fase 1: Diseño y estimando (85/100)

**Bien:**
- La pregunta de investigación está clara: ¿puede PINN-SIREN simular speckle con L2 < 5%? ✅
- Los tres niveles de validación (1D analítico → 2D analítico → speckle estadístico) forman una cadena de validación progresiva correcta ✅
- La elección ω₀=1.0 está justificada en §3.2 (dominio [0,1]² con k=2π) ✅
- La decomposición E=E_real + iE_imag está correctamente fundamentada en §2.1 ✅

**Debilidad menor:**
- La hipótesis incluye S = T_FEM/T_PINN > 1 como componente explícita, pero NB04 está pendiente. La hipótesis central queda parcialmente sin validar en este paper.

### Fase 2: Validez de la comparación principal (72/100)

**Problema principal — comparación inter-dimensional:**  
El paper compara su error L2 en Helmholtz 1D/2D con el error L2 de Schoder (2024) en Helmholtz **3D**. Esta comparación es problemática porque:
1. Un problema 3D tiene mayor capacidad expresiva requerida y mayor dificultad numérica
2. Schoder valida contra FEM en un dominio físico, este paper valida contra solución analítica
3. Las condiciones de frontera difieren (Schoder: dominio físico; este trabajo: plana / fase aleatoria)

El factor ×415 es probable que se deba en parte a esta diferencia de complejidad, no solo a la mejora arquitectural (SIREN vs PINNs convencionales). El paper debería incluir un párrafo de caveat explícito en la sección comparativa.

**Recomendación:**  
Agregar en §4.4 (Comparativa): "Nota: Schoder & Kraxberger (2024) abordan Helmholtz 3D; la comparación es indicativa de la mejora arquitectural (SIREN vs tanh/ReLU) pero no controla por diferencias en dimensionalidad ni en dominio físico."

### Fase 3: Reproducibilidad e inferencia (80/100)

**Bien:**
- SEED=42 fijo, GPU especificado ✅
- Hiperparámetros completamente reportados (Adam lr, épocas, L-BFGS max iter, historial 100) ✅

**Debilidades:**
- Una sola semilla — sin estimación de varianza de los resultados
- Sin ablación sobre λ_phys (se justifica 0.1 pero no se muestran alternativas cuantitativas)
- Sin ablación sobre ω₀ (se justifica 1.0 pero no se evalúan otras opciones)
- Sin ablación sobre N_c = 3,000 puntos de colocación vs alternativas

Estos son habituales en papers de ML para físicas, pero un revisor metodológico los pedirá.

### Fase 4: Completitud del trabajo (75/100)

| Item | Estado |
|------|--------|
| Validación contra solución analítica (1D, 2D) | ✅ Completo |
| Validación estadística del speckle | ✅ Completo |
| Benchmark FEM (S = T_FEM/T_PINN) | ❌ PENDIENTE |
| Figuras de visualización | ❌ AUSENTES |
| Ablación de hiperparámetros | ❌ AUSENTE |
| Comparación LHS vs malla uniforme (cuantitativa) | ❌ AUSENTE |
| Estimación de varianza (múltiples semillas) | ❌ AUSENTE |

---

## RESUMEN EJECUTIVO

### Puntajes por componente

| Componente | Puntaje | Peso |
|------------|---------|------|
| Verifier | 90/100 | 20% |
| Writer-critic | 87/100 | 40% |
| Strategist-critic (metodología) | 78/100 | 40% |
| **AGREGADO** | **84/100** | |

### Decisión: APRUEBA commit gate (≥ 80) — NO aprueba PR gate (≥ 90)

---

## LISTA DE CORRECCIONES

### Bloqueantes para PR (score ≥ 90)

1. **[EASY]** Reemplazar naked `\ref{sec:conclusiones}` por `\cref{sec:conclusiones}` en `04_resultados.tex:148`
2. **[MEDIUM]** Agregar caveat en §4.4 sobre la comparación 1D/2D vs 3D de Schoder (2024)
3. **[EASY]** Quitar o calificar la afirmación de "microsegundos" de inferencia (Intro línea 29) — o agregar medición en NB03
4. **[EASY]** Limpiar las 6 entradas huérfanas de `references.bib`

### Recomendadas (elevan impacto, no bloqueantes)

5. **[HIGH IMPACT]** Agregar figuras: curva de pérdida de entrenamiento, comparación PINN vs analítica (1D y 2D), patrón de speckle 2D, histograma de intensidades con exponencial teórica
6. **[MEDIUM]** Agregar tabla de ablación: λ_phys ∈ {0.01, 0.1, 1.0} vs error L2 para NB02
7. **[MEDIUM]** Completar NB04 (FEM benchmark) y agregar el Speed-up Factor en Resultados — esto valida la hipótesis principal
8. **[LOW]** Cuantificar "drásticamente" en la reducción de costo de almacenamiento (§3.1)
9. **[LOW]** Correr con 3 semillas distintas y reportar media ± std de L2 en la tabla de resultados

---

## CORRECCIÓN INMEDIATA SUGERIDA

El único fix bloqueante para el gate de commit es el naked `\ref`. Aplicar ahora:

**`04_resultados.tex:148`** — cambiar:
```latex
La incorporación de esta condición es parte del trabajo futuro (§\,\ref{sec:conclusiones}).
```
por:
```latex
La incorporación de esta condición es parte del trabajo futuro (véase \cref{sec:conclusiones}).
```
