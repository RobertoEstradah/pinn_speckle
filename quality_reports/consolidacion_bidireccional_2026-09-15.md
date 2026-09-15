# Consolidación bidireccional y actualización de la tesis

**Fecha:** 2026-09-15
**Destino:** `C:\roberto\Tesis_Maestria` (proyecto principal)
**Fuente adicional:** `C:\roberto\Tesis_Maestria - codex` (proyecto alternativo, sólo lectura)

Este documento registra la auditoría, las decisiones de consolidación y los
cambios aplicados a la tesis, con su evidencia asociada. No se eliminó ningún
archivo del proyecto principal.

---

## Fase 1 — Inventario comparado

| | Principal | Alternativo |
|---|---:|---:|
| Archivos | 937 | 1 062 |
| Tamaño | 472.3 MB | 1 104.0 MB |

| Relación | Cantidad |
|---|---:|
| Sólo en el principal | 191 |
| Sólo en el alternativo | 316 |
| En ambos, idénticos | 710 |
| En ambos, contenido distinto | 36 |

Comparación por hash MD5 de contenido, no por nombre ni fecha. Inventario
completo en `.inventario_fase1.json`.

### Duplicados detectados

Preexistentes en **ambos** proyectos, no introducidos por esta consolidación:

- `referencias/Krishnapriyan_etal_2021_...pdf` == `referencias/NB03/Krishnapriyan_etal_2021_...pdf`
- `referencias/Panagiotakopoulos_etal_2026_...pdf` == `referencias/NB03/Panagiotakopoulos_etal_2026_...pdf`
- `tesis/fuente_base/{base_azul,base_blanca,Oficio}.pdf` == `tesis/Tesis_Actual/{...}.pdf`

**Decisión:** no se eliminan. Los tres últimos son plantillas institucionales
que cada edición de la tesis necesita en su propio directorio para compilar; los
dos primeros son copias temáticas deliberadas. Eliminar cualquiera rompería una
compilación o una organización existente, y el beneficio es nulo.

### Incorporado desde el alternativo

| Recurso | Cantidad | Justificación |
|---|---:|---|
| PDFs científicos nuevos | 7 | Contenido ausente del principal (verificado por hash) |
| Scripts de experimentos | 13 | Producen los resultados de extensión de distancia y los diagnósticos |
| Documentos de metodología | 5 | Registro de la escalera de distancias y la validación por bloques |
| Resultados de experimentos | 3 carpetas | `nb03_distance_pilot`, `nb03_holdout`, `nb03_refinement` |
| Reportes de revisión | 2 | `quality_reports/reviews/` |
| `referencias_candidatas.bib` | 1 | Bibliografía candidata de NB03 |

PDFs nuevos: `Cai_Xu_2020_MscaleDNN`, `Costabal_etal_2024_DeltaPINNs`,
`Jagtap_Karniadakis_2020_AdaptiveActivationPINNs`,
`Rathore_etal_2024_PINN_LossLandscape`, `Wang_etal_2023_ExpertsGuideTrainingPINNs`,
`Wang_etal_2024_PirateNets`, `Born_Wolf_1999_Principles_of_Optics_Legal_Preview`.

De los 14 PDFs que aparecían como «sólo en el alternativo» por ruta, sólo 7 eran
nuevos por contenido: los otros 7 son los mismos archivos ubicados en
`referencias/NB03/` en lugar de `referencias/`.

### Conservado del principal (no existe en el alternativo)

- 4 papers de literatura descargados y evaluados en esta sesión
  (`referencias/optica_y_bien_puesto/`) con su documento de evaluación.
- `explorations/nb02b_bien_vs_mal_puesto/`, `explorations/angular_spectrum_reference/`,
  `explorations/ntk_spectral_bias_diagnostics/`, `explorations/architecture_ablation_4layers/`.
- Los resultados con `omega_0 = 1` de las cinco pantallas.
- `archive/nb03_speckle_pausado/` con el diagnóstico histórico.

### Decisión sobre el volumen de evidencia importada

Las tres carpetas de resultados importadas pesan 573 MB, de los cuales 551 MB
son campos `.npz` y 19 MB pesos `.pt`. **Decisión:** se conservan íntegras en
disco como evidencia y se excluyen del control de versiones sólo los binarios
pesados; las métricas (`.json`), figuras (`.png`) y documentación (`.md`) de esas
mismas carpetas —58 archivos, 2.5 MB— sí quedan rastreadas, que es lo que la
tesis cita. Los binarios son regenerables con los scripts importados.

---

## Fase 1b — Comparación de la tesis

Resultado: **el proyecto principal está por delante del alternativo en todos los
archivos de la tesis.** Detalle:

| Archivo | Diferencias reales | Decisión |
|---|---:|---|
| `Abstract.tex` | 0 | Sin acción (sólo terminador de línea) |
| `Resumen.tex` | 0 | Sin acción |
| `references.bib` | 1 espacio de sangría | Sin acción |
| `Cap2-Marcos.tex` | 47 líneas | **Conservar el principal**: contiene el párrafo de Krishnapriyan, la comparación con Zhang (FE-PIRBN) y el posicionamiento frente a Panagiotakopoulos, ausentes en el alternativo |
| `Cap3-Modelo.tex` | 33 líneas | **Rechazar el cambio del alternativo** (ver abajo) |
| `Cap4-Resultados.tex` | 99 líneas | **Conservar el principal**: es un superconjunto estricto; el alternativo no aporta ninguna línea |

### Conflicto resuelto: hiperparámetros de NB03 en Cap3

El `Cap3-Modelo.tex` del alternativo extiende la tabla de hiperparámetros para
declarar que NB03 comparte los de NB02: tasa de aprendizaje $10^{-3}$, 15 000
épocas Adam, paciencia 800, L-BFGS 1 000 iteraciones y $\lambda_\text{fís}=0.1$.

**Esa afirmación es falsa para la formulación modal validada**, que usa tasas de
$2\times10^{-4}$ y $5\times10^{-5}$, 5 000 + 3 000 épocas, **no emplea L-BFGS**
y **no tiene término de datos**, por lo que no existe $\lambda_\text{fís}$.
Evidencia: `scripts/experiments/nb03_modal_pinn_siren.py` y
`results/nb03_modal_multiseed_z1_omega1_summary.json` (bloque `protocol`).

**Decisión:** rechazado. En su lugar se escribió una descripción metodológica
correcta de la formulación modal en Cap3 (ver Fase 4).

---

## Fase 2 — Notebooks

Los cuatro notebooks activos del principal proceden del alternativo y ya habían
sido consolidados. Verificaciones de reproducibilidad aplicadas:

### Defecto corregido: dependencia implícita en NB01

`01_validacion_helmholtz_1d_normalizada.ipynb` usaba `helmholtz_residual_1d(...)`
en la celda de evaluación **sin haberla importado**. Las salidas almacenadas
procedían de una sesión en la que ese nombre existía en el espacio de nombres,
de modo que el notebook no era reproducible desde cero: al ejecutarlo limpio
fallaba con `NameError`.

**Corrección:** se añadió a los imports de la celda 2:
`from src.losses import pinn_loss_1d, helmholtz_residual_1d`.
Comprobado que NB02 y NB03 no presentan el mismo defecto.

### Defecto corregido: salidas obsoletas en NB03

`03_simulacion_speckle_2d_pinn_siren_modal.ipynb` declaraba `omega_0 = 30` y
reportaba $L^2 = 3.542\%$, valores superados por la calibración verificada.
Se actualizó a `omega_0 = 1`, se reapuntó al consolidado correspondiente, se
añadió una sección con el barrido de $\omega_0$ y se **reejecutó completo**
(0 celdas sin ejecutar, 0 errores).

### Notebook incompleto, documentado y no utilizado

`02b_validacion_puente_arquitectura_modal_nb03.ipynb` está vacío: 7 de 7 celdas
sin ejecutar, 11 KB, sin salidas. Los resultados asociados en
`results/nb02b_modal_bridge/` son una prueba de humo de 3 épocas y 0.2 s, con
$L^2 = 416\%$ y `accepted: false`.

**Decisión:** no se utiliza como evidencia. El experimento equivalente, completo
y ejecutado, es `explorations/nb02b_bien_vs_mal_puesto/`, que es el que se cita
en la tesis. El notebook vacío se conserva sin modificar a petición del autor.

---

## Fase 3 — Reportes

### Discrepancia detectada: tabla de $z=2\lambda$ mezcla dos presupuestos

`results/nb03_distance_pilot/README.md` presenta una tabla de cinco pantallas a
$z=2\lambda$ con media $L^2 = 1.887\%$ y afirma que «las cinco pantallas cumplen
$L^2<5\%$ tanto al final como en el máximo».

Contrastado contra los JSON:

| Pantalla | README | `z2_five_120s` (120 s) | `z2_seeds42_123_180s` (180 s) |
|---:|---:|---:|---:|
| 42 | 0.887 % | **4.718 %** | 0.887 % |
| 123 | 1.318 % | **4.457 %** | 1.318 % |
| 321 | 3.108 % | 3.108 % | — |
| 777 | 2.411 % | 2.411 % | — |
| 2026 | 1.710 % | 1.710 % | — |

La tabla del README **combina dos corridas con presupuestos de cómputo
distintos** (180 s para las pantallas 42 y 123, 120 s para las otras tres) y
promedia sobre esa mezcla. Con presupuesto uniforme de 120 s, el máximo
propagante de las pantallas 42 y 123 es de 6.999 % y 6.692 %, **por encima del
umbral del 5 %**.

**Decisión:** el valor 1.887 % no se incorpora a la tesis. Se relanzó la corrida
con presupuesto uniforme de 180 s para las cinco pantallas
(`results/nb03_distance_pilot/z2_cinco_uniforme_180s/`) y se reporta ese
resultado homogéneo.

### Verificación sin discrepancia

`results/nb03_distance_pilot/adaptive_slabs_multiseed_summary.json` coincide con
su documentación y **declara sus propias limitaciones**:
`independent_phase_screens_pending: true` y
`goodman_absolute_rule_at_z5_pass: false`, con la razón explícita de que la
referencia misma tiene $C = 1.146$ en $z = 5\lambda$. El resultado de
$z = 5\lambda$ corresponde a **una sola pantalla** (31415) con dos semillas de
red, no a una validación multipantalla.

---

## Fase 4 — Cambios aplicados a la tesis

### Generalidades: NO MODIFICADAS

`chapters/Cap1-Generalidades.tex` **no fue modificado**. Se verifica por hash y
por `git diff`. Esto incluye título, preguntas de investigación, hipótesis,
objetivo general, objetivos específicos, justificación, alcances y limitaciones.

### `chapters/Cap4-Resultados.tex`

| Sección | Estado anterior | Estado nuevo | Motivo | Evidencia |
|---|---|---|---|---|
| `\section{NB03}` completa | 49 líneas, `[Sección en progreso]`, dominio $[0,20]$, $\ell_\phi=0.5\lambda$, bloques de $4\lambda$, resultados no convergentes | 324 líneas con 7 subsecciones y 5 tablas | La sección describía una configuración abandonada y declaraba que el experimento no converge | `results/nb03_modal_multiseed_z1_omega1_summary.json` y JSON de referencia |
| Tabla resumen de experimentos | NB03-B/C «En progreso» | NB03-B «Completo, $L^2=3.161\%$» | El experimento está completo y verificado | ídem |
| Contraste de NB03-A | $C=0.9732$ (config. de $20\lambda$) | $C=0.9661$ (media de conjunto de las 5 pantallas a $1\lambda$) | Coherencia con la configuración vigente | `nb03_angular_spectrum_reference_z1*.json` |
| Tabla comparativa | 4 filas | 5 filas, con nota sobre la naturaleza semianalítica de la referencia | Incorporar NB03 sin sugerir comparabilidad directa | — |

Respaldo de la sección obsoleta: `chapters/.Cap4-NB03-obsoleta.bak`.

### `chapters/Cap3-Modelo.tex`

| Cambio | Motivo | Evidencia |
|---|---|---|
| $\ell_\phi: 0.5\lambda \rightarrow 0.10\lambda$ | El valor declarado no correspondía al utilizado | `nb03_angular_spectrum_reference_z1_corr0.10.json` |
| Sustituido el párrafo de «bloques cortos» por la reducción modal, la Cauchy dura y el escalamiento por modo | La descripción no correspondía al método ejecutado en $z=1\lambda$ | `scripts/experiments/nb03_modal_pinn_siren.py` |
| Nueva subsección de métricas de NB03 | No existía descripción de las métricas del experimento | `nb03_modal_multiseed_summary.py` |
| Nombres de los notebooks | Referenciaban archivos ya reemplazados | — |

### `references.bib`

Dos entradas nuevas, ambas **verificadas abriendo el PDF local** (Fase 7).

---

## Fase 7 — Fuentes verificadas

Se abrió cada documento y se comprobó que el contenido citado aparece en él.

| Cita | Documento local | Verificación | Afirmación respaldada | Ubicación en la tesis |
|---|---|---|---|---|
| `nguyen2016truncation` | `optica_y_bien_puesto/Nguyen_etal_2014_TruncacionCauchyHelmholtz.pdf` | Abstract, p. 1: «we rigorously investigate the truncation method for the Cauchy problem of Helmholtz equations... regularization of several types of ill-posed problems... error estimates in L2-norm». arXiv:1408.1932v3, 11 Mar 2016. Autores y afiliaciones comprobados | El truncamiento a modos propagantes es la regularización del problema de Cauchy, no una simplificación | Cap3 §Reducción modal; Cap4 §Formulación modal adoptada |
| `sukumar2022exact` | `referencias/Sukumar_Srivastava_2021_ExactBoundaryConditionsDistanceFunctionsPINN.pdf` | Abstract, p. 1: «a new approach based on distance fields to exactly impose boundary conditions in physics-informed deep neural networks... the trial function is taken as φ(x) multiplied by the PINN approximation». arXiv:2104.08426v2, 7 Nov 2021 | Imponer la frontera en la función de prueba en lugar de penalizarla | Cap3 §Condición de Cauchy dura; Cap4 §Formulación modal adoptada |

Documentos verificados como legibles y con metadatos correctos, disponibles para
uso futuro pero **no citados todavía**: `Cai_Xu_2020_MscaleDNN` (arXiv:1910.11710),
`Jagtap_Karniadakis_2020_AdaptiveActivationPINNs` (arXiv:1906.01170),
`Wang_etal_2023_ExpertsGuideTrainingPINNs` (arXiv:2308.08468),
`Born_Wolf_1999_Principles_of_Optics_Legal_Preview` (vista previa autorizada de
99 páginas, con `_SOURCE.md` documentando origen, edición y DOI).

---

## Pendientes y decisiones humanas

Ver la sección correspondiente del informe final.

---

## Fase 6 — Auditoría independiente de consistencia

Se dispachó un agente auditor con la instrucción de verificar cada valor
numérico de Cap3 y Cap4 contra los archivos de resultados, sin permiso para
editar. Revisó ~150 afirmaciones. Resultado y acciones:

### Discrepancias confirmadas y corregidas

| # | Hallazgo | Acción |
|---|---|---|
| B1 | «máximo de 12.3 %» en la fracción evanescente del caso B; el máximo real es 13.206 % (el 12.3 % es el valor en ỹ=0.75, no el máximo) | Corregido a 13.2 % en Cap4 y en el README de la exploración |
| B3 | «el error de las condiciones de Cauchy es exactamente nulo» en dos lugares; el valor registrado es 1.28e-08 en RMSE | Reformulado: nulo por construcción algebraica, 1.28e-08 por aritmética en float32 |
| D3 | `eq:loss_nb03` en Cap3 definía una pérdida con tres pesos (λ_z, λ_p, λ_f), contradiciendo la afirmación —85 líneas antes en el mismo capítulo— de que NB03 no tiene pesos que calibrar | Ecuación sustituida por el residuo modal normalizado, sin pesos |
| D1 | Ω₀₃ = [−10,10]×[0,20] en Cap3 vs [−10,10]×[0,1] en Cap4 | Cap3 ahora distingue dominio objetivo de dominio validado |
| D2 | Cap3 asignaba 5 capas a NB03; el JSON registra 4 | Corregido |
| D4 | Cap3 declaraba entrada (x,z) para NB03; la red modal recibe z̃ escalar | Corregido |
| D5 | Cap3 presentaba ω₀ de NB03 como hiperparámetro calibrable por bloque | Corregido: ω₀=1 por la regla, con contraste experimental |
| D7 | «40.99 % de la energía espectral» presentado como propiedad general; es de la pantalla 42 | Acotado, con el rango real de las cinco (34.55 %–41.28 %) |
| D8 | Los p-valores KS se presentaban en un párrafo sobre el modelo; son de la referencia | Atribución explícita añadida |
| — | Párrafo corrupto preexistente («duplican el / contribución del término físico», con sangría de `tablenotes` arrastrada). Presente también en la copia alternativa | Reparado con la frase que documenta `CLAUDE.md` («duplican el peso efectivo») |

### Afirmaciones sin respaldo persistido, corregidas

| # | Hallazgo | Acción |
|---|---|---|
| C1 | La columna «L² propagante» del barrido modal (0.090/0.081/0.329/3.172 %) sólo existía como texto; ningún JSON la contenía | Creado `scripts/experiments/nb03_omega0_sweep_summary.py`, que la recalcula desde los campos guardados y la persiste en `results/nb03_modal_omega0_sweep_summary.json`. La tabla ahora cita esa fuente |
| C2 | «residuo hasta ~10⁻¹⁴» no está guardado en ningún artefacto | Reemplazado por la cifra que sí está persistida (error máximo de frontera 9e-08) más una afirmación cualitativa |
| C3 | «error relativo de 5.6×10⁻¹⁶» sólo se imprimía por consola | Reemplazado por «del orden de la precisión de máquina (~10⁻¹⁶)», que es lo que el README respalda |
| C9 | La ablación de 4 vs 5 capas existía en `explorations/` sin citarse en ningún capítulo | Incorporada como subsección con tabla en Cap4 |

### Conflicto de datos resuelto

**C8 — dos barridos de ω₀ de NB01 con resultados incompatibles.**
`explorations/ntk_spectral_bias_diagnostics/output/omega0_sweep.json` (GPU) da
ω₀=1 como mejor; `results/diagnostics/nb01_omega0_sweep.json` (importado del
proyecto alternativo; **CPU**, torch 2.14.0+cpu, Python 3.12) da ω₀=5 como
mejor, tanto en pérdida como en L². Ambos declaran el mismo protocolo.

No se descartó ninguno. La afirmación de la tesis —que ω₀=1 supera a *los tres*
valores descalibrados— **no se sostiene** al incluir ω₀=5, y el barrido modal de
NB03 lo confirma de forma independiente (0.090 % para ω₀=1 frente a 0.081 %
para ω₀=5, es decir, indistinguibles). Cap4 se reescribió para afirmar sólo lo
que las tres corridas sostienen de forma consistente: la degradación es clara y
reproducible para ω₀ ≥ 15, y ω₀=1 y ω₀=5 quedan próximos entre sí.

### Falso positivo

**B4 — tamaño de grano transversal.** El auditor obtuvo 0.3844λ frente al
0.378λ de la tesis. Recalculado con el estimador declarado (FWHM de la
autocorrelación de intensidad con interpolación lineal) se obtiene **0.3778λ**,
que redondea al valor de la tesis. La diferencia proviene del estimador, no del
dato. Sin cambio.

### Verificación final

`scripts/experiments/verifica_cifras_tesis.py` comprueba 61 valores de la
sección NB03 contra sus archivos fuente: **61 verificadas, 0 discrepancias.**

---

## Fase 3b — Resultado de la corrida uniforme a $z=2\lambda$

Se relanzó el piloto de extensión de distancia con presupuesto **uniforme de
180 s** para las cinco pantallas (`z2_cinco_uniforme_180s`), para sustituir la
tabla del README que mezclaba dos presupuestos.

| Pantalla | L² propagante | L² completo | Máximo propagante | Piso | \|ΔC\| | Acepta |
|---:|---:|---:|---:|---:|---:|:--:|
| 42 | 1.690 % | 1.750 % | 2.499 % | 0.456 % | 0.0013 | sí |
| 123 | 6.144 % | **6.151 %** | 7.373 % | 0.292 % | 0.0166 | **no** |
| 321 | 8.069 % | **8.082 %** | 10.010 % | 0.462 % | 0.0118 | **no** |
| 777 | 4.178 % | 4.192 % | 5.651 % | 0.340 % | 0.0062 | sí |
| 2026 | 1.047 % | 1.111 % | 1.722 % | 0.371 % | 0.0014 | sí |
| **Media** | **4.226 %** | **4.257 %** | **5.451 %** | 0.384 % | | **3/5** |

**Conclusión: la extensión a $z=2\lambda$ no está validada.** Dos de las cinco
pantallas superan el umbral del 5 % en el error final y tres lo superan en el
máximo sobre los planos evaluados. La media del máximo propagante (5.451 %)
está por encima del umbral.

**Observación adicional que agrava el diagnóstico:** el resultado no mejora de
forma monótona con el presupuesto de cómputo. La pantalla 321 pasa de 3.108 %
con 120 s a 8.069 % con 180 s, y la 123 de 4.457 % a 6.144 %. Un refinamiento
que empeora al dársele más tiempo indica que el procedimiento no está
convergiendo de forma estable en ese régimen, no que le falte presupuesto.

**Decisión:** ningún resultado de $z=2\lambda$ se incorpora a la tesis. El
capítulo de resultados reporta exclusivamente $\tilde z=1\lambda$, que sí está
verificado en las cinco pantallas y reproducido desde cero en este equipo. La
evidencia de $2\lambda$ y $5\lambda$ queda en `results/` como material de
trabajo futuro, con esta advertencia asociada.

Esto invalida también, por extensión, la lectura optimista de
`docs/NB03_escalera_distancias.md`, que declara $2\lambda$ como «validada en
cinco pantallas». Esa afirmación descansa en la tabla mezclada del README.

---

## Verificación de la ruta de entrenamiento de NB03

El notebook `03_simulacion_speckle_2d_pinn_siren_modal.ipynb` trae el
entrenamiento desactivado por diseño (`RUN_TRAINING = False`), de modo que su
ejecución habitual sólo carga y analiza los resultados validados. Esa ruta de
análisis quedaba verificada, pero la de entrenamiento no.

Se ejecutó una vez con `RUN_TRAINING = True`, escribiendo en los sufijos
`_z1_nuevo_*` que no sobrescriben ningún artefacto validado. Resultado de la
réplica independiente frente al modelo validado de la pantalla 42:

| Métrica | Réplica nueva | Validado | Diferencia |
|---|---:|---:|---:|
| L² complejo | 0.038187 | 0.038187 | 0 |
| Coherencia compleja | 0.999271 | 0.999271 | 0 |
| Contraste de la PINN | 0.901197 | 0.901197 | 0 |
| Residuo modal RMSE | 0.002318 | 0.002318 | 0 |

Un entrenamiento independiente desde cero (5 000 épocas Adam + 3 000 de
refinamiento, $\omega_0=1$) alcanza exactamente el mismo punto en las cuatro
métricas. **El pipeline de NB03 es determinista** bajo la semilla fijada y
`cudnn.deterministic`. Evidencia:
`results/nb03_modal_pinn_siren_z1_nuevo_finetune.json`.

Tras la comprobación se restauró `RUN_TRAINING = False` y se reejecutó el
notebook, para que el código y las salidas almacenadas vuelvan a corresponder
--el mismo tipo de incoherencia que se corrigió en la Fase 2--.
