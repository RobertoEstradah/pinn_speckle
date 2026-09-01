# Research Journal — PINN-SIREN Speckle Óptico

### 2026-08-27 22:00 — librarian
**Phase:** Discovery
**Target:** Literatura adicional sobre PINNs para óptica/speckle/Helmholtz, para complementar el estado del arte de `Tesis_act2/`
**Score:** N/A (sin librarian-critic dispatchado aún)
**Verdict:** Encontró 10 papers candidatos nuevos. Produjo bibliografía anotada, `references.bib`, mapa de frontera y recomendación de posicionamiento. Pendiente de revisión por el usuario para decidir cuáles incorporar a la tesis/paper.
**Report:** `quality_reports/literature/pinn-speckle/annotated_bibliography.md`, `frontier_map.md`, `positioning.md`, `references.bib`

### 2026-08-27 23:15 — librarian-critic
**Phase:** Discovery
**Target:** `quality_reports/literature/pinn-speckle/` (salida del agente `librarian`)
**Score:** 74/100 (por debajo del gate de Commit >=80)
**Verdict:** Búsqueda genuinamente buena (categorización, recencia, análisis de riesgo de scooping), pero con defectos verificables: una cita ("Panagiotakopoulos et al. 2026") declarada falsamente como "ya en el bib del proyecto" (no existe en ningún .bib real), 2 entradas duplicadas re-agregadas pese a la exclusión declarada (McKay 1979, Wang et al. 2021 — ya están en `tesis/fuente_conNB03/references.bib` y `paper/fuente_conNB03/references.bib`), 2 campos de autor BibTeX con placeholders sin verificar, y 2 citas relevantes faltantes (Tancik et al. 2020 — Fourier Features, contrapunto directo a SIREN; Krishnapriyan et al. 2021 — modos de falla en PINNs, relevante al problema documentado de λ=1.0 inestable en 2D).
**Report:** Reporte completo en la respuesta del agente (no guardado a archivo aparte); ver detalle en esta entrada.

### 2026-08-27 23:40 — librarian (ronda 2, fixes)
**Phase:** Discovery
**Target:** `quality_reports/literature/pinn-speckle/` — corrección de los 6 hallazgos de la ronda 1
**Score:** N/A (creador, no se autoevalúa)
**Verdict:** Resueltos los 6 hallazgos: Panagiotakopoulos 2026 agregado correctamente como cita nueva (ya no falsamente marcado "ya en el bib"); duplicados McKay 1979 y Wang et al. 2021 eliminados; autores placeholder de zhang2025fepirbn y nair2025multiplescattering completados; agregadas Tancik et al. 2020 (Fourier Features) y Krishnapriyan et al. 2021 (modos de falla en PINN, ligada al hallazgo propio de λ=1.0 inestable); conteo de "siete" corregido.
**Report:** `quality_reports/literature/pinn-speckle/` (4 archivos actualizados)

### 2026-08-27 23:45 — librarian-critic (ronda 2)
**Phase:** Discovery
**Target:** `quality_reports/literature/pinn-speckle/` (revisión post-fix)
**Score:** 91/100 (supera el gate de Commit ≥80 y de PR ≥90)
**Verdict:** Los 6 hallazgos de la ronda 1 confirmados como resueltos (verificado independientemente por el crítico, no solo aceptado el reporte del librarian). 2 hallazgos menores nuevos: 3 entradas BibTeX incompletas (falta volumen/páginas/DOI: geetanjli2026waveguide, kazemzadeh2025digitaltwin, guo2025piganspeckle) y el frontier_map.md no menciona a Moseley 2020 ni Alkhalifah 2021 (ya citados en la tesis) en su narrativa de "qué se ha hecho", pese a ser tan cercanos al método como los 7 papers explícitamente excluidos.
**Report:** Reporte completo en la respuesta del agente; ver detalle en esta entrada.

### 2026-08-28 00:10 — Incorporación de citas (Nivel 1 y 2) a Tesis_Actual
**Phase:** Discovery → Execution (aplicado directamente, sin agente `writer`)
**Target:** `tesis/Tesis_Actual/references.bib`, `Cap2-Marcos.tex`, `Cap4-Resultados.tex`
**Score:** N/A
**Verdict:** Se incorporaron 4 de las 11 citas candidatas del `librarian` (Nivel 1: Panagiotakopoulos et al. 2026, Krishnapriyan et al. 2021; Nivel 2: Zhang et al. 2025 FE-PIRBN, Tancik et al. 2020), tras verificación independiente del rango de error de FE-PIRBN (1.40–5.82%) contra ScienceDirect/ADS antes de escribirlo en la tesis. Krishnapriyan se ligó al hallazgo propio de inestabilidad con λ=1.0; Panagiotakopoulos se contrastó explícitamente en 3 ejes (validación cualitativa vs. L², sin calibración de ω₀, fuente gaussiana vs. speckle) en la sección "Contexto en la literatura"; Zhang et al. se agregó como segunda fila en la Tabla 4.6 con el mismo framing honesto de "no comparable directamente" ya establecido para Schoder; Tancik se agregó junto a la introducción de SIREN en Cap2. Recompilado sin errores ni citas indefinidas (46 págs). Un overfull hbox introducido por la fila nueva de la tabla se corrigió acortando el texto de la celda.
**Report:** N/A — cambios directos en el LaTeX, no hay reporte de agente separado.

### 2026-08-28 00:25 — Contribución explícita en Cap1-Generalidades
**Phase:** Execution (aplicado directamente)
**Target:** `tesis/Tesis_Actual/chapters/Cap1-Generalidades.tex`, sección "Definición del problema"
**Score:** N/A
**Verdict:** Actualizado el párrafo de vacío en la literatura (antes solo mencionaba Schoder/acústica, quedaba desactualizado frente al hallazgo de Panagiotakopoulos et al. 2026, arquitectónicamente el más cercano). Se citó explícitamente a Panagiotakopoulos y se agregó un párrafo nuevo con los 3 elementos de contribución: (i) regla de calibración ω₀≈k/(2π), ausente en Sitzmann 2020 y en Panagiotakopoulos 2026; (ii) generación de speckle desde una EDP + frontera aleatoria, no ajuste a datos medidos; (iii) validación estadística contra Goodman, ausente en la literatura de PINN+Helmholtz encontrada. Sin guiones largos. Recompilado sin errores (46 págs).
**Report:** N/A — cambio directo en LaTeX.

### 2026-08-28 00:45 — Auditoria de atribucion de citas (contenido, no solo metadata)
**Phase:** Execution (verificacion directa, sin agente)
**Target:** Todos los \parencite/\textcite en Cap1-Cap4 de tesis/Tesis_Actual/
**Score:** N/A
**Verdict:** Revisados los ~55 usos de cita en el documento. Encontrados y corregidos 2 casos de mala atribucion (cita real, pero no respalda el reclamo especifico donde se usa):
1. Cap3-Modelo.tex: `\parencite{goodman2007speckle, fang2020physics}` para el criterio de speckle completamente desarrollado (sigma_phi > 2pi) -- fang2020physics es sobre diseno de metamateriales, no discute speckle. Se removio fang2020physics, se dejo solo goodman2007speckle.
2. Cap2-Marcos.tex: `\parencite{wang2021failure}` para la estrategia bifasica Adam+L-BFGS -- Wang et al. 2021 es sobre balance de gradientes/DCGD, no describe esa estrategia. Verificado en el PDF real de Cuomo et al. 2022 (`referencias_md/Cuomo_etal_2022...md` lineas 364, 369, 1111-1113) que SI describe exactamente "Adam followed by final fine-tuning with LBFGS" como practica estandar -- se cambio la cita a cuomo2022scientific. wang2021failure se reubico a Cap4 (parrafo de Krishnapriyan sobre inestabilidad de lambda), donde su contenido real (flujo de gradiente patologico) si aplica.
Resto de las ~53 citas revisadas: consistentes con lo que cada fuente realmente afirma.
**Report:** N/A -- verificacion directa, cambios en el LaTeX. Ver tambien [[feedback_citation_verification_rigor]] (memoria) -- este hallazgo confirma el patron ya documentado.

### 2026-08-28 01:15 — writer-critic
**Phase:** Execution
**Target:** `tesis/Tesis_Actual/` completo (main.tex + preliminares + Cap1-Cap4), modo standalone (categorias 4,5,6,8)
**Score:** 43/100 (round 1)
**Verdict:** Hallazgo grave verificado independientemente por mi (no solo aceptado el reporte del agente): la tabla y prosa de NB03 en Cap4 reportaban estadistico KS=0.0628 y fraccion I>2<I>=0.135, pero la figura real (estadistica_speckle_nb03.png, del mismo run: mismas epocas/tiempo/C) muestra KS=0.0487 e I>2<I>=0.1207 -- confirme visualmente leyendo la imagen. Tambien confirmada una contradiccion real: Cap3 SS "Puntos de frontera" describia NB03 con 300 pts/lado en los 4 lados, contradiciendo la descripcion correcta (256 pts, solo y=0, 3 lados libres) que aparece 3 veces en el resto del documento. Ambos corregidos. Tambien corregidos: 2 figuras huerfanas sin \ref en el texto (fig:metricas1d, fig:metricas2d), cursiva faltante en un caption, notacion $\tilde{k}$ introducida y nunca usada (removida, se aclara que k es adimensional desde su definicion). Pendiente, requiere mas trabajo: colision de simbolo phi (activacion SIREN vs fase de frontera aleatoria, ~10 ubicaciones en 4 capitulos) y titulos incrustados en las 6 figuras de resultados (ya documentado en observacion.txt desde antes, no nuevo).
**Report:** Reporte completo en la respuesta del agente; ver detalle en esta entrada.

### 2026-08-28 01:25 — Aplicacion de fixes del writer-critic
**Phase:** Execution
**Target:** `tesis/Tesis_Actual/chapters/Cap3-Modelo.tex`, `Cap4-Resultados.tex`
**Score:** N/A
**Verdict:** Aplicados 6 fixes: (1) estadistico KS corregido a 0.0487; (2) fraccion I>2<I> corregida a 0.1207 en tabla y prosa, con reencuadre honesto de la interpretacion (10.8% de diferencia relativa, explicado por correlacion espacial reduciendo el N efectivo de muestras independientes, en vez de la afirmacion previa de "consistente"); (3) contradiccion de frontera NB03 en Cap3 corregida, con nuevo \label{cap3:nb03} para la referencia cruzada; (4)(5) referencias de texto agregadas a fig:metricas1d y fig:metricas2d (antes huerfanas); (6) cursiva agregada al caption de la Tabla NB03; (7) notacion tilde-k abandonada removida. Recompilado sin errores, sin referencias indefinidas, sin guiones largos (46 paginas).
**Report:** N/A -- cambios directos en LaTeX.

### 2026-08-28 01:35 — Correccion de colision de notacion phi
**Phase:** Execution
**Target:** `tesis/Tesis_Actual/` -- Cap1-Cap4, Abstract.tex, Resumen.tex
**Score:** N/A
**Verdict:** Renombrada la fase aleatoria de frontera de phi(x) a psi(x) en las 13 ubicaciones donde aparecia (incluyendo N_phi->N_psi, sigma_phi->sigma_psi, Delta phi->Delta psi), dejando phi(z)=sin(omega_0 z) exclusivamente para la activacion SIREN. Nota: theta se descarto como alternativa porque ya esta en uso en Cap2 para los parametros entrenables de la red (N_theta, L(theta)) -- usarlo habria creado una colision nueva en vez de resolver la existente. Verificado que no queda ningun phi(x)/N_phi/sigma_phi/Delta phi en el documento y que phi(z) solo aparece en las 4 ubicaciones de la activacion SIREN. Recompilado sin errores (46 paginas), sin guiones largos.
**Report:** N/A -- cambios directos en LaTeX.

### 2026-08-28 02:00 — Justificacion del umbral L2<5%
**Phase:** Execution
**Target:** `tesis/Tesis_Actual/chapters/Cap3-Modelo.tex` (Metricas de validacion)
**Score:** N/A
**Verdict:** Agregada justificacion para el umbral L2<5%, ausente en el protocolo original (2025) y en la tesis hasta ahora -- verificado que ningun paper citado ni la tesis del director (Adan Hernandez Nolasco, ITESM 2003, revisada como precedente) justifica externamente su propio umbral de error; el director usa el mismo patron (umbral autoimpuesto, "lo recomendable", sin cita) para su propio criterio ERP<<0.001 de conservacion de energia. Redaccion revisada dos veces: se corrigio "menor al" -> "menor que el" (gramatica), y se separo la razon de fijar el umbral (no existe estandar en la literatura) de la observacion de que resulta consistente con la Tabla 4.6 (evitando implicar que la tabla causo la eleccion del numero, dado que el umbral es de 2025 y la tabla se poblo con literatura encontrada en 2026 -- desajuste cronologico que se detecto y corrigio antes de dejarlo en el texto). Recompilado sin errores (46 paginas), sin guiones largos.
**Report:** N/A -- cambio directo en LaTeX.

### 2026-08-28 03:00 — Fix de titulos incrustados: NB01 (reentrenado)
**Phase:** Execution
**Target:** `notebooks/01_pinn_helmholtz_1d_validation.ipynb` (cell-19), `results/models/nb01_helmholtz1d_gpu.pt`, `results/figures/{resultados_pinn_1d,metricas_adicionales_1d}.png`, `tesis/Tesis_Actual/chapters/Cap4-Resultados.tex`
**Score:** N/A
**Verdict:** Editados los 8 titulos incrustados de NB01 (suptitle/set_title) a etiquetas cortas de panel (A/B/C) sin cifras, via NotebookEdit. metricas_adicionales_1d.png se regenero sin reentrenar (solo requiere el checkpoint). resultados_pinn_1d.png si requirio reentrenar, porque su Panel C (curvas de perdida) necesita el historial de entrenamiento, no guardado en el checkpoint -- se reentreno NB01 completo (mismos hiperparametros/seed=42). El reentrenamiento resulto en perdida por epoca identica al log original (mismo comportamiento estocastico de GPU, no siempre determinista pero en este caso lo fue) -- L2=0.005517% (redondea igual a 0.006%, sin cambio), R2/Pearson/MSE/RMSE/MAE/error_maximo/epocas/iteraciones L-BFGS todos identicos a lo ya escrito en la tesis. Unico cambio real: tiempo total de entrenamiento 251s -> 142s (variabilidad de carga/termica de GPU, no del codigo) -- actualizado en Cap4-Resultados.tex (prosa + tabla). Bug de ruta encontrado y corregido en el proceso: get_figures_dir()/get_models_dir() dependen de cwd, hay que ejecutar scripts standalone desde notebooks/ (o pasar notebook_dir explicito) para no guardar fuera de Tesis_Maestria/. Checkpoint nb01_helmholtz1d_gpu.pt sobrescrito con los pesos nuevos (practicamente identicos a los anteriores). Recompilado sin errores (46 paginas). Pendiente: mismo tratamiento para NB02 (17 titulos) y NB03 (16 titulos).
**Report:** N/A -- cambios directos en notebook/LaTeX + scripts en scratchpad.

### 2026-08-28 03:30 — Fix de titulos incrustados: NB02 (reentrenado)
**Phase:** Execution
**Target:** `notebooks/02_pinn_helmholtz_2d_complex_field.ipynb`, `results/models/nb02_helmholtz2d_gpu.pt`, `results/figures/{resultados_pinn_2d,metricas_adicionales_2d}.png`, `tesis/Tesis_Actual/chapters/Cap4-Resultados.tex`
**Score:** N/A
**Verdict:** Editados los 17 titulos incrustados de NB02 via parche de texto crudo sobre el JSON (Read/NotebookEdit fallaron por tamano del notebook -- outputs embebidos superan el limite de tokens). NB02 se reentreno completo (mismos hiperparametros/seed=42) porque resultados_pinn_2d.png necesita el historial de perdida. El reentrenamiento fue de nuevo practicamente identico al original: mismas 8,737 epocas Adam (early stopping por paciencia), mismas 1,035 iteraciones L-BFGS, L2_real/L2_imag/L2_mean/MSE/RMSE/MAE/error_maximo/R2/Pearson todos identicos a la precision ya escrita en la tesis. Unico cambio real: tiempo total 299s -> 295s (ruido de GPU) -- actualizado en Cap4-Resultados.tex (prosa + tabla multiseed, fila SEED=42). Recompilado sin errores (46 paginas). Pendiente: mismo tratamiento para NB03 (16 titulos, el mas importante -- ahi vive el bug de KS/contraste ya corregido en el texto).
**Report:** N/A -- cambios directos en notebook/LaTeX + scripts en scratchpad.

### 2026-08-28 04:15 — Fix de titulos incrustados: NB03 (reentrenado) + hallazgo de causa raiz del bug KS/C
**Phase:** Execution
**Target:** `notebooks/03_pinn_optical_speckle_simulation.ipynb`, `results/models/nb03_speckle.pt`, `results/figures/{resultados_speckle_nb03,estadistica_speckle_nb03}.png`, `tesis/Tesis_Actual/chapters/Cap4-Resultados.tex`
**Score:** N/A
**Verdict:** Antes de reentrenar se investigo la causa raiz del bug de KS/contraste encontrado hoy con el writer-critic. Se encontraron 3 conjuntos de valores distintos para el mismo resultado: (1) texto original de la tesis: KS=0.0628, frac~0.135; (2) output guardado en la celda de estadisticas del propio notebook (ejecucion intermedia, execution_count=28): C=0.9634, KS=0.0628, frac=0.1309; (3) figura+checkpoint actuales en disco (mismo timestamp exacto entre los 3 archivos: 31 mayo 14:28): C=1.0253, KS=0.0487, frac=0.1207. El KS=0.0628 coincide exactamente entre (1) y (2) -- confirma que el texto original de la tesis se escribio copiando de una ejecucion intermedia y desactualizada del notebook, no de la ejecucion final cuyo checkpoint realmente se uso para generar la figura. Esto confirma que la correccion aplicada hoy mas temprano (ajustar el texto a los valores de la figura) fue la correcta.
Editados los 16 titulos incrustados de NB03 (parche de texto crudo, 0 advertencias). Reentrenado NB03 completo (mismos hiperparametros/seed=42, sin transfer learning de NB02 segun diseño original) -- reprodujo EXACTAMENTE los valores del checkpoint actual: C=1.0253, KS=0.0487, frac=0.1207, epocas Adam=7976/15000, iter L-BFGS=8/1000 -- confirmando que el checkpoint en disco y la correccion de hoy son consistentes y reproducibles. Unico cambio real: tiempo total 227s -> 195s (ruido de GPU) -- actualizado en Cap4-Resultados.tex tabla NB03. Limpiadas 3 celdas con outputs viejos/desactualizados en el notebook (la de estadisticas con los valores de la ejecucion intermedia, y las 2 de figuras). Recompilado sin errores (46 paginas).
**Pendiente, fuera de alcance de hoy:** el panel "RESUMEN" de estadistica_speckle_nb03.png (texto dibujado, no set_title) sigue quemando C, KS, fraccion, epocas y tiempo como pixeles -- mismo problema de fondo, no corregido en esta ronda por decision explicita (se le informo al usuario).
**Report:** N/A -- cambios directos en notebook/LaTeX + scripts en scratchpad.

### 2026-08-31 17:20 — Renombrado y actualizacion de paper/fuente_base -> paper/fuente_validacion1D2D
**Phase:** Execution
**Target:** `paper/fuente_validacion1D2D/` (renombrada desde fuente_base), CLAUDE.md, README.md
**Score:** N/A
**Verdict:** Renombrada via `git mv` (preserva historial). Actualizado CLAUDE.md y README.md (referencias a fuente_conNB03 borrada, papers_inspiracion, y el nuevo nombre). Propagados a este paper los fixes de la sesion larga que aun no habia recibido: (1) misatribucion Wang2021->Cuomo2022 para la estrategia bifasica; (2) justificacion del umbral L2<5%; (3) cita a Krishnapriyan et al. 2021 tras la discusion de ablacion lambda; (4) cita a Panagiotakopoulos et al. 2026 en el gap-statement de la introduccion (estaba desactualizado, igual que en la tesis); (5) fila de Zhang et al. 2025 FE-PIRBN en la tabla comparativa; (6) tiempos de NB01/NB02 actualizados (251->142s, 299->295s); (7) figuras NB01/NB02 actualizadas a las versiones con titulos limpios. Hallazgo adicional no anticipado: el abstract en ingles Y espanol de main.tex todavia tenian el claim enganoso "outperforming by factors of x415 and x11.2" que ya se habia removido del resto del documento en sesiones anteriores -- corregido a framing honesto de "ordenes de magnitud por debajo del umbral". 3 citas nuevas agregadas a references.bib. Recompilado sin errores (19 paginas). PDF/ZIP actualizados en paper/compilado/base/ (nombre de carpeta sin renombrar, pendiente de decision del usuario).
**Report:** N/A -- cambios directos en LaTeX.

### 2026-08-31 18:40 — Reconciliacion de tesis/fuente_base con los fixes de la sesion (el mas rezagado)
**Phase:** Execution
**Target:** `tesis/fuente_base/` (chapters/Cap1-Generalidades.tex, Cap2-Marcos.tex, Cap3-Modelo.tex, Cap4-Resultados.tex, Abstract.tex, Resumen.tex, references.bib, figures/)
**Score:** N/A
**Verdict:** Edicion mas desactualizada encontrada en la sesion. Hallazgo critico: Cap4-Resultados.tex aun contenia la cita fabricada original -- \textcite{schoder2024helmholtz} citado con "1D: 2.490%" y "2D: 1.910%" mas una columna "Factor de mejora x415/x11.2" (2.49% es real pero del caso 3D acustico de Schoder, mal etiquetado como 1D; 1.91% no tiene fuente rastreable) -- el mismo bug de integridad de citas investigado y corregido en Tesis_Actual mucho antes en la sesion, mas profundamente incrustado aqui (prosa en 2 subsecciones adicionales, ademas de la tabla). Fixes aplicados: (1) gap-statement de Cap1 actualizado con cita a Panagiotakopoulos et al. 2026; (2) Cap2: Wang2021->Cuomo2022 para la estrategia bifasica + estilo de guion "Fase 1 -- Adam"->"Fase 1 (Adam)"; (3) Cap3: agregado parrafo de justificacion del umbral L2<5%; (4) Cap4: seccion renombrada "Comparativa con el estado del arte"->"Contexto en la literatura", tabla reemplazada por version honesta de 4 filas (Schoder 3D/2.49%, Zhang 2D-EM/1.40-5.82%, PINN-SIREN 1D/0.006%, PINN-SIREN 2D/0.171%, sin columna de factor), parrafo de contraste con Panagiotakopoulos anadido, prosa de "factor de mejora x415/x11.2" en las subsecciones 1D y 2D reemplazada por referencia cruzada a la nueva seccion; (5) parrafo de Krishnapriyan et al. 2021 + Wang et al. 2021 (gradient flow pathologies) anadido tras la discusion de ablacion lambda; (6) tiempos actualizados 251->142s (NB01), 299->295s (NB02, prosa + tabla NB02 + tabla multiseed fila SEED=42); (7) 3 referencias nuevas anadidas a references.bib (Panagiotakopoulos, Krishnapriyan, Zhang); (8) figuras NB01/NB02 actualizadas a las versiones con titulos limpios. Hallazgo adicional no anticipado: Abstract.tex y Resumen.tex describian resultados de speckle (contraste C=1.0253, frontera de fase aleatoria, validacion de Goodman) que esta edicion no cubre en absoluto (fuente_base excluye NB03 por definicion) ademas de tener el mismo claim enganoso x415/x11.2 -- ambos reescritos para reflejar el alcance real (validacion 1D/2D unicamente), con el mismo framing ya aprobado por el usuario para paper/fuente_validacion1D2D. Recompilado sin errores, 0 referencias/citas indefinidas (42 paginas). No se recreo `tesis/compilado/base/` (el usuario la borro explicitamente en sesion anterior); el PDF queda solo en `tesis/fuente_base/main.pdf`.
**Report:** N/A -- cambios directos en LaTeX.
