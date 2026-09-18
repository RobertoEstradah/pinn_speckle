# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

**Título:** Simulación del speckle óptico mediante Redes Neuronales Informadas por
Física: formulación modal de Helmholtz
*(aprobado por el director el 2026-09-18; antes decía «Simulación acelerada… con
activación sinusoidal». Se retiró «acelerada» porque NB04 sigue pendiente, y se
añadió la formulación modal, que es lo que distingue el trabajo entregado del que
prometía el protocolo.)*
**Grado:** Maestro en Ciencias de la Computación — UJAT (matrícula 252H21004)
**Director:** Dr. José Adán Hernández Nolasco
**Coasesor:** Dr. Noel Zacarías Morales (añadido el 2026-09-18)
**Comité coloquio:** Dr. Pablo Pancardo García (Sin. 1) | Dr. Óscar Alberto Chávez Bosquez (Sin. 2) | Dr. Miguel Antonio Wister Ovando (Sin. 3) | Moderador: Otoniel Sánchez Marín
**Pregunta de investigación:** ¿Puede una PINN-SIREN simular speckle óptico con L² < 5% y contraste C ≈ 1?
**Rama:** main

---

## Dos repositorios, y cuál es el principal

| Ruta | Papel |
|---|---|
| `C:\roberto\Tesis_Maestria - codex` | **Principal.** Aquí se hacen los notebooks, los scripts y los experimentos |
| `C:\roberto\Tesis_Maestria` (este) | **Derivado.** Aquí se redacta la tesis y el paper, con el material de soporte |

El flujo va en una sola dirección: **codex produce → se sincroniza aquí → aquí se
verifica y se redacta**. La capa computacional tiene que estar presente en este
repositorio no como respaldo, sino para que los verificadores puedan abrir los
`.json` y contrastar cada cifra del texto contra su fuente.

**Un experimento o notebook nuevo se crea en codex, no aquí.** A este repositorio
sólo llega el producto: figuras, métricas y texto.

Consecuencia a recordar: varios archivos de `results/` registran rutas absolutas
hacia codex como modelo de partida. No es un defecto --es la trazabilidad del
flujo-- pero significa que **este repositorio no se basta solo para reproducir
esos resultados**. Importa si algún día hace falta un paquete de replicación
autocontenido.

**No subir nada a GitHub sin que el autor lo pida explícitamente.** Commitear en
local está bien; `git push` sólo cuando él lo diga.

---

## Marco Metodológico

**Física:** Ecuación de Helmholtz 2D escalar, dominio adimensional [0,1]², laser diodo rojo (λ=638 nm, k=2π)
**Arquitectura:** SIREN (Sitzmann et al., 2020) — activación sin(ω₀·x), inicialización especial para derivadas de 2.º orden
**Optimización:** Adam (exploración global) → L-BFGS strong Wolfe (ajuste fino)
**Muestreo:** Latin Hypercube Sampling (LHS) para puntos de colocación interiores

### Hiperparámetros por notebook (verificados en archivos)

**NB01 y NB02: métricas congeladas, notebooks reescritos (2026-09-15).** Las métricas se
verificaron línea por línea contra `Cap4-Resultados.tex` (L², MSE, RMSE, MAE, error máximo,
R², Pearson, épocas Adam, iteraciones L-BFGS, tiempo total) y contra
`results/multiseed_results.json` / `results/ablation_lambda.json`: coinciden exactamente.

El 2026-09-15 los notebooks se reemplazaron por versiones *normalizadas*
(`01_validacion_helmholtz_1d_normalizada.ipynb`, `02_validacion_helmholtz_2d_normalizada.ipynb`),
que hacen explícita la adimensionalización `x̃ = x_físico/λ` → `k̃ = k_real·λ = 2π` y añaden
métricas conjuntas de campo complejo. **Los números no cambiaron** (0.006% y 0.171%, mismas
épocas y tiempos). Los notebooks anteriores siguen recuperables en git (commit `972bde6`).

**Sigue vigente: no alterar las métricas ni los capítulos de la tesis que las reportan.**
Lo que cambió es la exposición, no el resultado.

| Parámetro | NB01 (1D) — FINAL | NB02 (2D) — FINAL |
|-----------|-----------|-----------|
| Arquitectura | SIREN 5×64, 16 833 params | SIREN 5×128, 66 690 params |
| ω₀ | 1.0 | 1.0 |
| λ_phys | **1.0** | **0.1** |
| N_colloc | 2 000 uniforme | 3 000 LHS |
| N_boundary | 5 pts (0,0.25,0.5,0.75,1) | 300 por borde → 1 200 total |
| Paciencia | umbral L_total < 1e-4 | 800 épocas |
| L-BFGS max_iter/history | 500/50 | 1 000/100 |
| SEED | 42 | 42 |

**Diferencia clave NB01 vs NB02:** en 2D los dos residuos (real + imag) duplican el peso efectivo de la
física → λ=1.0 explota en float32; λ=0.1 es la configuración estable.

**NB03 (speckle óptico por PINN): ACTIVO — formulación modal validada (2026-09-15).**
Se retomó y funciona. La formulación colocada directa se abandonó tras demostrarse que el
problema estaba mal planteado (ver tabla anti-errores); la formulación vigente es **modal**:

- Fronteras laterales periódicas → serie de Fourier exacta en x, y Helmholtz 2D se separa
  en 41 EDOs desacopladas `aₘ'' + (k²−kxₘ²)aₘ = 0`. Sólo los modos propagantes entran en la
  base: es el truncamiento espectral, la regularización canónica del problema de Cauchy para
  Helmholtz (Nguyen et al. 2014, en `referencias/optica_y_bien_puesto/`).
- **Condición de Cauchy dura** `aₘ(z) = aₘ(0) + z·aₘ'(0) + z²·N_θ(z)`: fija valor y derivada
  en z=0 por construcción, lo que restaura la unicidad. No hay término de datos, así que
  **no hay λ_phys que balancear** en NB03.
- Escalamiento por modo `escala_m = k²·max(|aₘ(0)|, |aₘ'(0)|/k, piso)`.
- Arquitectura SIREN 4×128, entrada escalar z̃, 82 salidas reales, **ω₀ = 1** (regla de NB01).
- Optimización: Adam 5 000 épocas (lr 2e-4) + refinamiento 3 000 (lr 5e-5). Sin L-BFGS.

Resultados en z = 1λ, cinco pantallas independientes, reentrenadas y verificadas:

| Métrica | Valor |
|---|---|
| L² complejo medio | **3.161 ± 0.497 %** (5/5 por debajo del 5%) |
| Piso evanescente de la referencia | 3.160 ± 0.497 % |
| L² propagante medio sobre z | **0.042 %** (máximo 0.084 %) |
| Residuo modal RMSE | 0.00234 |
| Coherencia compleja | 0.99949 |
| Error de contraste vs su referencia | ≤ 0.0157 |

El L² total está **dominado por el piso evanescente**, que la base modal no puede representar
por construcción; la métrica que mide al PINN es la propagante. El piso depende de la
distancia (25.5% a 0.25λ, 3.82% a 1λ, 0.46% a 2λ, 0.001% a 5λ): **z = 1λ es campo cercano
estricto y la peor distancia posible para validar.**

Diagnósticos y material previo archivados en `archive/nb03_speckle_pausado/`; siguen siendo
válidos como registro de lo descartado.

---

## Arquitectura del Código

### Paquete `src/`

Módulos reutilizables extraídos de los notebooks para uso en NB03+:

| Módulo | Clases / Funciones | Descripción |
|--------|-------------------|-------------|
| `src/models.py` | `PINN_1D_SIREN`, `PINN_2D_SIREN`, `Sine` | Arquitecturas SIREN con inicialización de Sitzmann et al. |
| `src/losses.py` | `pinn_loss_1d`, `pinn_loss_2d`, `helmholtz_residual_*` | Pérdidas PINN: L_datos + λ·L_física |
| `src/training.py` | `train_adam_lbfgs` | Loop híbrido Adam (early stopping) → L-BFGS (strong Wolfe) |
| `src/utils.py` | `l2_rel`, `get_figures_dir`, `get_models_dir`, `save_model`, `load_model` | Métrica L² relativa y paths a `results/` |

**Importación estándar desde notebooks:**
```python
from src.models import PINN_1D_SIREN, PINN_2D_SIREN
from src.losses import pinn_loss_1d, pinn_loss_2d
from src.training import train_adam_lbfgs
from src.utils import l2_rel, get_figures_dir, save_model
```

**Nota:** NB01 y NB02 tienen el loop de entrenamiento inline por legibilidad pedagógica. `src/training.py` es la referencia documentada para NB03+.

### Notebooks

Los **seis** notebooks activos viven en `notebooks/`. Los tres anteriores
(`01_pinn_helmholtz_1d_validation`, `02_pinn_helmholtz_2d_complex_field`,
`03_pinn_optical_speckle_simulation`) se reemplazaron el 2026-09-15 y quedan
recuperables desde el commit `972bde6`.

| Notebook | Propósito | Salida clave |
|----------|-----------|--------------|
| `notebooks/01_validacion_helmholtz_1d_normalizada.ipynb` | Validación 1D con adimensionalización explícita — referencia analítica cos(2πx̃) | L²=0.006%, R²=1.000 |
| `notebooks/02_validacion_helmholtz_2d_normalizada.ipynb` | Campo complejo 2D (E_real, E_imag), LHS, dominio 1×1 λ = 0.638×0.638 µm | L²_avg=0.171% |
| `notebooks/02b_validacion_puente_arquitectura_modal_nb03.ipynb` | Puente: valida la `ModalSiren` de NB03 contra solución analítica exacta, sin etiquetas interiores, con 1, 5 y 41 modos | **Ejecutado, 7/7, ω₀=1.** L² global 0.0149 / 0.0112 / **0.0078 %**; Cauchy dura a ~1e-9; 3/3 aceptados. Reportado en Cap4 §`sec:nb02b_arquitectura` |
| `notebooks/03_simulacion_speckle_2d_pinn_siren_modal.ipynb` | Speckle por PINN-SIREN modal de **dominio único**, 5 pantallas, ω₀=1, en z=1λ | L²=3.161%, propagante 0.042%, 5/5 aceptadas |
| `notebooks/03b_validacion_speckle_2d_z2lambda.ipynb` | Speckle en **z=2λ**, mismo dominio único, partiendo del punto de control de 1λ | L² medio **0.993 %**, 5/5 aceptadas. Cap4 §`sec:nb03_extension` |
| `notebooks/03c_validacion_speckle_2d_z5lambda.ipynb` | Speckle hasta **z=5λ** por **descomposición** en cinco bloques de 1λ, con escala sinusoidal adaptativa | L² final medio **2.244 %**, máximo 3.507 % sobre 201 planos, 5/5 aceptadas. Cap4 §`sec:nb03_z5` |
| `notebooks/v1_exploracion_cpu/` | Línea base CPU pre-GPU (archivados — solo referencia histórica) | NB01 v1: L²≈0.009%, NB02 v1: L²≈0.222%, ×4.3 más lento |

**Ejecutar el `03`, `03b` y `03c` sólo carga y analiza** (`RUN_TRAINING = False`). Para
entrenar una réplica hay que ponerlo en `True`; usa sufijos `_z1_nuevo_*` para no
sobrescribir los modelos validados.

**Tres distancias, DOS procedimientos distintos.** No deben enunciarse como uno solo:

| Distancia | Procedimiento | L² | Notebook |
|---|---|---|---|
| z=1λ | Dominio único, una red por pantalla | 3.161 % | `03` |
| z=2λ | Dominio único, reanudando desde 1λ | 0.993 % | `03b` |
| z=5λ | **Cinco redes locales de 1λ** acopladas por Cauchy dura, con **escala sinusoidal aprendida por bloque** | 2.244 % | `03c` |

NB03C **no usa ω₀=1**: su implementación adaptativa tiene frecuencias base de
**30 en la primera capa y 1 en las internas**, multiplicadas por una escala
aprendida. Las escalas observadas bajan de 1.00 en el primer bloque a ~0.30 en
los siguientes — comportamiento empírico de optimización, **no** una reducción
física de la frecuencia modal: en medio homogéneo `k_z,m` es constante.

NB03C trae además un **control negativo**: una sola red sobre `[0,5λ]`, pantalla
42, 180 s en CPU, da L²=118.47 % y coherencia 0.0502. No es ablación
equivalente --difieren arquitectura, presupuesto y hardware--, así que sólo
autoriza a decir que *bajo los protocolos evaluados* la extensión global directa
no alcanzó los criterios.

**Los presupuestos de NB03C no son uniformes:** pantallas 42 y 123 con protocolo
v2 (pesos transferidos), y 321, 777 y 2026 con refinamiento residual v3.

**NB04 (aparcado por decisión del autor el 2026-09-17):** Benchmark PINN vs
FEM/FEniCSx. Es el único hueco que queda en las hipótesis: sin él, H(ii) (factor
$S = T_{FEM}/T_{PINN} > 1$) no tiene respuesta, **Cap5 no puede escribirse**, y
la referencia de NB03 no puede llamarse *independiente* — el espectro angular es
**semianalítico**, porque propaga cada modo como la solución cerrada de la misma
EDO que la red minimiza.

Tres cosas que conviene saber antes de retomarlo:

1. **FEniCSx no corre en Windows nativo.** Necesita WSL2 o Docker, no instalados.
   Es el primer paso y bloquea todo lo demás.
2. **Cap1:133 condiciona la comparación FEM a fronteras absorbentes**, mientras
   NB03 usa **periódicas**. Hay que resolverlo con el director antes de
   implementar, o el notebook se reescribe después.
3. **El resultado sería probablemente negativo.** El espectro angular ya resultó
   18.5× más rápido que la PINN para un plano, y el entrenamiento cuesta 351.9 s
   por pantalla. Cap4 ya reubicó la contribución en precisión y planteamiento,
   así que eso no invalida la tesis — pero sí afecta a la palabra «acelerada» del
   título, pendiente con el director.

### Flujo de resultados

```
notebooks/ → autodiferenciación PyTorch → resultados en results/figures/, results/models/
scripts/experiments/run_*.py → resultados en results/*.json (multiseed, ablación λ)
src/ → importado por notebooks y scripts/
```

**Outputs de experimentos:**
- `results/multiseed_results.json` — seeds {42, 123, 777}, medidas en la misma sesión: L²_avg = 0.192 ± 0.089%
- `results/ablation_lambda.json` — λ=0.01→0.163%, λ=0.1→0.171%, λ=1.0→crash CUDA (sin valor de L²)
- `results/figures/` — figuras PNG de todos los notebooks y experimentos
- `results/models/` — pesos `.pt` (gitignored)
- `results/nb03_angular_spectrum_reference_z1*.npz` — referencias ASM por pantalla (fase, campo, espectro). Regeneran **bit a bit idénticas**: verificado en las 5 semillas
- `results/nb03_modal_multiseed_z1_summary.json` — consolidado de las 5 pantallas con ω₀=30 (histórico)
- `results/nb03_modal_multiseed_z1_omega1_summary.json` — **consolidado vigente**, ω₀=1
- `results/nb03_modal_pinn_siren_z1_*.npz` — campo predicho y de referencia por corrida
- `results/nb02b_modal_bridge/summary.json` — puente modal contra solución analítica (1, 5 y 41 modos). Los `.npz` están gitignorados; se regeneran con `FORCE_RETRAIN=True` en el notebook 02b, unos 20 min

**Evidencia importada de la copia paralela (2026-09-15).** Tres carpetas con los
experimentos de extensión de distancia y validación reservada:

| Carpeta | Contenido | Alcance real |
|---|---|---|
| `results/nb03_distance_pilot/` | Pilotos a z=2λ y z=5λ, bloques adaptativos | 2λ validado en 5 pantallas; **5λ sólo en 1 pantalla (31415) con 2 semillas** |
| `results/nb03_holdout/` | Pantalla reservada 31415, enfoque cartesiano | No alcanzó L²<5% a 1λ (6.45%) |
| `results/nb03_refinement/` | Checkpoints L-BFGS float32 que alimentan los pilotos | — |

Los `.npz` y `.pt` de esas carpetas (≈570 MB) están **gitignorados**: se conservan
en disco como evidencia y son regenerables con los scripts. Las métricas `.json`,
figuras y documentación sí se rastrean.

**Cifra vigente para $z=2\lambda$:** usar
`results/nb03_distance_pilot/z2_omega1_five_120s/validation_summary.json`.
Corresponde a $\omega_0=1$, presupuesto uniforme de 120 s por pantalla, error
$L^2$ final medio de 0.993 % y 5/5 pantallas aceptadas. La carpeta
`z2_cinco_uniforme_180s/` pertenece a una configuración histórica y no debe
usarse como fuente del resultado oficial de NB03B.

El consolidado se genera con `NB03_SUMMARY_VARIANT` (`""` = ω₀=30, `"_omega1"` = ω₀=1):
```bash
NB03_SUMMARY_VARIANT=_omega1 python scripts/experiments/nb03_modal_multiseed_summary.py
```

### Directorios adicionales

- `explorations/` — sandbox para prototipos; umbral de calidad reducido (60/100). Graduar a `notebooks/` requiere 80/100. Ver `explorations/README.md`.
  - `nb02b_bien_vs_mal_puesto/` — **experimento puente**: misma solución analítica, tres planteamientos. Dirichlet directa 0.077% · Cauchy directa 45.14% · Cauchy modal 0.155%, con datos idénticos en las dos últimas. Sostiene por qué NB03 cambió de formulación
  - `angular_spectrum_reference/` — validación del ASM (5.6e-16) y las 9 rutas descartadas de la formulación directa
  - `ntk_spectral_bias_diagnostics/` — traza NTK física/datos = 858× y barrido de ω₀ de NB01
  - `architecture_ablation_4layers/` — 4 vs 5 capas: 5 gana en 1D (0.006% vs 0.0133%) y en 2D (0.171% vs 0.2279%)
- `data/raw/` / `data/cleaned/` — datos de entrada si aplica
- `quality_reports/reviews/` — reportes de revisión con scores
- `master_supporting_docs/` — NO modificar; documentos de referencia para el coloquio
- `docs/` — documentos de referencia sueltos (propuestas, ruta de tesis, lista de revistas)
- `slides/` — presentaciones PPTX (`segundo coloquio/` para el coloquio, `smf/` para el cartel del congreso SMF)
- `paper/papers_plantillas/` — plantillas de revistas/congresos candidatos para adaptar el contenido de `paper/fuente_validacion1D2D/`, organizadas por venue, cada una con `fuente/` (LaTeX/Word editable). Flujo: se toma el contenido de `fuente_validacion1D2D/`, se ajusta a la plantilla del venue elegido, y el resultado compilado va a `paper/compilado/`. **`CyS/` y `COMIA/` ya están adaptadas y activas.** `CyS/fuente/{es,en}/` es la
edición vigente --la revista que se decidió con el director-- con el paper completo
en ambos idiomas, 9 páginas cada uno, y salida en `paper/compilado/CyS/{es,en}/`;
`COMIA/` está en formato LNCS/Springer. `RevistaMatematica_UCR/`, `CLEI/`,
`InteligenciaArtificial_IBERAMIA/`, `RevistaColombianaComputacion/` e `IJCOPI/`
siguen en blanco, cada una con `README.md` documentando indexación, costo y
periodicidad.

**El alcance del paper es la validación 1D y 2D**, por decisión del autor: el
speckle aparece sólo como trabajo futuro. Su título dice eso desde el 17/09; antes
prometía «simulación acelerada de speckle óptico», que el paper no entrega.

### Ediciones de `paper/` y `tesis/`

**`tesis/`** — 2 ediciones:

| Carpeta | Contenido | Uso |
|---------|-----------|-----|
| `Tesis_Actual/` | Copia de trabajo activa y principal, creada el 27/08/2026 como `Tesis_act2` (sucesora de `Tesis_actualizada/`, borrada), renombrada a `Tesis_Actual` el mismo día | Aquí se aplican todos los cambios nuevos a la tesis |
| `fuente_base/` | Sin la sección de resultados de speckle | Sin modificar |

`tesis/fuente_conNB03/` (el respaldo con NB03) se eliminó el 28/08/2026 — `tesis/` ya tiene su propio respaldo real en el historial de git (commit `1fd2a13`), así que dejó de ser necesaria una copia en disco aparte.

Flujo de compilación de `Tesis_Actual/`: editar en `tesis/Tesis_Actual/`,
compilar con `latexmk`, y copiar el PDF resultante a
`tesis/compilado/Actual/tesis_maestria_roberto_hernandez_estrada.pdf`,
sobrescribiendo siempre la versión anterior, sin conservar historial.

**Estado al 2026-09-17:** 78 páginas, 0 errores de LaTeX, 0 referencias sin
resolver, 28 de 28 citas usadas. Capítulos 1 a 4; **no hay Cap5**, que depende de
NB04.

**Antes de dar por buena cualquier cifra de la tesis, correr:**

```bash
python scripts/experiments/verifica_cifras_tesis.py
```

Compara **292 cifras** del texto contra los `.json` y `.npz` que las generaron y
debe terminar en `0 discrepancias`. **Al añadir una cifra nueva a la tesis,
añadirla también ahí**: es lo único que impide que el texto y los resultados se
separen.

Lleva además guardas que no son cifras sino afirmaciones que deben permanecer:
que la corrida de NB02B usara ω₀=1, que los saltos de interfaz de NB03C sean
cero exacto, y que la nota de Zhang siga advirtiendo que su métrica no es $L^2$.

Y hay un **segundo verificador**, un nivel más arriba en la cadena:

```bash
python scripts/experiments/verifica_paper_vs_tesis.py
```

Compara las **tres ediciones vivas del paper** --CyS espanol, CyS ingles y
COMIA-- contra la tesis: **39 comprobaciones**, 13 por edicion. La
regla que implementa está escrita en su propia salida: *donde el paper y la tesis
discrepen, se corrige el paper*. La cadena completa es
**codex produce → la tesis verifica → el paper deriva**.

**Qué capítulos se pueden tocar.** Cap2, Cap3 y Cap4 sí. **Cap1
(Generalidades) NO se modifica sin consultarlo antes con el Dr. Adán** —
instrucción explícita del autor, incluso para corregir afirmaciones que el
código contradice. Hay cuatro puntos abiertos ahí, más la palabra «acelerada»
del título, esperando esa conversación.

### Secciones de Cap4 sobre NB03 y el puente

| Etiqueta | Contenido |
|---|---|
| `sec:nb03_diagnostico` | Por qué se abandonó la formulación colocada directa |
| `sec:nb02b_puente` | Puente de buen planteamiento: Dirichlet 0.077% · Cauchy directa 45.14% · Cauchy modal 0.155%. Fuente: `explorations/nb02b_bien_vs_mal_puesto/` |
| `sec:nb02b_arquitectura` | **Añadida el 2026-09-15.** La `ModalSiren` de NB03 contra solución exacta, 1/5/41 modos. Fuente: `results/nb02b_modal_bridge/summary.json` |
| `sec:nb03_config` | Formulación modal adoptada |
| `sec:nb03_omega` | Barrido de ω₀ sobre speckle (contraste controlado) |
| `sec:nb03_resultados_z1` | Las cinco pantallas en z=1λ, L²=3.161% |
| `sec:nb03_piso` | Descomposición L²_total² = L²_propagante² + piso² |
| `sec:nb03_inferencia` | Benchmark de tiempo: sin ganancia frente al espectro angular |

**Cuidado al comparar cifras entre secciones.** El 0.0078% de
`sec:nb02b_arquitectura` **no compite** con el 3.161% de
`sec:nb03_resultados_z1`: el primero mide un campo propagante puro, sin piso
evanescente, y acota el error de la arquitectura; el segundo está dominado por
el piso de la pantalla aleatoria. La sección lo dice explícitamente, y conviene
no deshacer esa aclaración.

**`tesis/compilado/Actual/` contiene exactamente dos archivos**, ambos con el
nombre `tesis_maestria_roberto_hernandez_estrada`:

| Archivo | Qué es | Cómo se genera |
|---|---|---|
| `.pdf` | Documento compilado, para leer y entregar | `latexmk` en `tesis/Tesis_Actual/`, luego copiar |
| `.zip` | Fuentes LaTeX completas, para Overleaf o entrega | `python scripts/build/build_tesis_zip.py` |

El `.zip` lleva fuentes `.tex`, `references.bib`, los archivos de formato
institucional (`Portada`, `base_azul`, `base_blanca`, `Oficio`, `latexmkrc`) y
`figures/`. **No lleva el PDF compilado ni auxiliares de LaTeX**: es la fuente,
no el resultado. El script verifica que no falte ninguna figura referenciada.

No dejar ahí `main.pdf` ni respaldos con fecha: el historial de git ya conserva
cualquier estado anterior. Se limpió el 2026-09-15 (se retiraron `main.pdf`, un
respaldo del 10/09 y un `.zip` desactualizado del 27/08, y se regeneró el `.zip`
desde el estado vigente).

**`paper/`** — 1 edición activa:

| Carpeta | Contenido | Uso |
|---------|-----------|-----|
| `fuente_validacion1D2D/` | Valida SIREN en Helmholtz 1D y 2D (NB01+NB02); el speckle se menciona solo como trabajo futuro planificado, no como resultado. Renombrada desde `fuente_base/` el 31/08/2026 | Edición activa del paper |

`paper/fuente_conNB03/` (la edición con la sección completa de speckle) se eliminó el 28/08/2026, mismo motivo que en `tesis/` — respaldo real ya en git (commit `3489f4c`). El PDF/ZIP ya compilados de esa edición se eliminaron el 01/09/2026 (commit `b7c1b41`) por el mismo motivo — recuperable desde el commit `3489f4c` si hace falta.

`paper/papers_plantillas/COMIA/` es la edición adaptada al formato LNCS/Springer del congreso COMIA — ver la sección de `paper/papers_plantillas/` arriba. Su salida compilada vive en `paper/compilado/COMIA/`, separada de `paper/compilado/fuente_validacion1D2D/` (antes `base/`, renombrada el 01/09/2026 para que coincida con su fuente).

---

## Convenciones y Entorno

**Entorno:** `environment.yml` ya declara lo que realmente se usa — Python 3.14, PyTorch 2.11,
CUDA 12.8, GPU NVIDIA RTX 5050. **En la práctica se corre con el Python del sistema, sin conda**;
el entorno `pinn_speckle` no está instalado en esta máquina. El `.yml` sirve como especificación
reproducible para terceros, no como el entorno en uso.

**VRAM:** la RTX 5050 tiene 8 GB. N_colloc ≥ 90 000 la satura (~7.9/8.1 GiB) y el entrenamiento
se vuelve extremadamente lento; mantenerse en 60–80 k.
**Crear entorno:** `conda env create -f environment.yml`
**FEniCSx (NB04):** solo disponible en WSL2 Ubuntu o Docker en Windows
**Tests:** no hay suite automatizada (`pytest`/lint no configurados) — la verificación es manual, corriendo notebooks/scripts y revisando `results/`

```bash
# Notebooks
jupyter lab notebooks/

# Paper — validación 1D/2D, sin speckle (única edición activa)
cd paper/fuente_validacion1D2D && latexmk main.tex

# Tesis UJAT (biblatex APA, helvet font — formato UJAT, NO working-paper)
# Copia de trabajo activa — todos los cambios nuevos van aquí
cd tesis/Tesis_Actual && latexmk main.tex

# Tesis UJAT, edición sin speckle
cd tesis/fuente_base && latexmk main.tex

# Paper COMIA (LNCS/Springer)
cd paper/papers_plantillas/COMIA/fuente && latexmk main.tex

# ZIP de fuentes de las ediciones del paper (validacion1D2D, CyS_es, CyS_en, COMIA)
python scripts/build/build_paper_zips.py
# build_comia_paper.py es andamiaje historico: NO ejecutarlo, destruiria ediciones

# Experimentos
python scripts/experiments/run_ablation_lambda.py
python scripts/experiments/run_multiseed.py
python scripts/experiments/run_seed777.py
python scripts/experiments/measure_inference.py

# Verificar que las cifras de la tesis coinciden con los resultados (292 checks)
python scripts/experiments/verifica_cifras_tesis.py

# Verificar que el paper no contradiga a la tesis: CyS es, CyS en y COMIA (39 checks)
python scripts/experiments/verifica_paper_vs_tesis.py

# NB03: extension de distancia y validacion reservada (importados 2026-09-15)
python scripts/experiments/nb03_distance_pilot.py --seeds 42 123 321 777 2026 --distances 2 --seconds 180 --name mi_corrida
python scripts/experiments/nb03_adaptive_slabs.py      # encadenamiento por bloques
python scripts/experiments/nb03_holdout_validation.py  # pantalla reservada

# Slides — reconstruir slide_new.pptx desde cero (copia base + agrega 2 slides de código en pos 13,14)
python scripts/build/add_code_slides.py
python scripts/build/extract_pptx.py   # extraer texto para inspección
python scripts/build/verify_slides.py  # verificar orden y títulos

```

**Rutas:** outputs finales → `slides/coloquio_segundo_semestre/`, `tesis/compilado/{fuente_base,Actual}/`, `paper/compilado/{fuente_validacion1D2D,COMIA,CyS}/` |
resultados crudos → `results/` | modelos → `results/models/` (gitignored) | referencias → `master_supporting_docs/` (NO modificar) |
scripts de entrenamiento/medición → `scripts/experiments/` | scripts de generación de entregables → `scripts/build/` (Python) y `scripts/build_slides_js/` (Node)

**Slides — archivos clave:**
- `slides/coloquio_segundo_semestre/presentacion_mcc_roberto_hernandez_estrada.pptx` — presentación oficial del coloquio (33 slides), la que se usó en el coloquio real
- `slides/congreso_smf/cartel_pinn_siren_2d.pptx` — cartel para el congreso SMF. Su `README.md` documenta que el script que lo armó, `scripts/build_slides_js/build_cartel.mjs`, **no se ejecuta hoy**: depende de un runtime de Codex clavado a una versión que ya no está instalada
- `slides/slide_new.pptx` — versión con slides de código añadidas; **no existe en disco actualmente**, regenerar con `python scripts/build/add_code_slides.py` si se necesita
- `slides/guion_latex/` y `slides/compilado/guion.zip` — eliminados el 01/09/2026, ya no se usan (respaldo en git, commit `1fee2ba`, si hace falta recuperarlos)

**Coloquio:** Slot 10:30–11:15 h | Presentación ≤ 20 min | Tiempo real ≈ 16:35 min (margen 3:25 min)

---

## Problemas Resueltos (Memoria Anti-Errores)

| Problema | Solución documentada |
|----------|----------------------|
| ω₀=30 explota gradientes con k≈2π | Calibrar ω₀=1.0 — regla: ω₀ ≈ k/(2π) (`notebooks/01`) |
| BCs simétricas E(0)=E(1)=1 colapsan a constante | Agregar puntos intermedios conocidos (`notebooks/01`) |
| λ=1.0 en 2D → CUDA crash float32 | Dos residuos duplican física → usar λ=0.1 en 2D+ (`results/ablation_lambda.json`) |
| LR scheduler mata L-BFGS (7/1000 iter) | Nunca usar scheduler antes de L-BFGS — Adam sin scheduler (`notebooks/02`) |
| Transfer learning entre soluciones con física distinta → sesgo | Al extender NB02 a una frontera nueva, inicializar desde cero — pesos calibrados para onda plana entran en conflicto con un campo que varía libremente |
| E=0 en bordes libres con frontera aleatoria → colapso | Sin condición Dirichlet en los bordes libres, el optimizador puede converger a la solución trivial si la frontera activa no logra imponerse (ver diagnóstico de escala en `archive/nb03_speckle_pausado/scripts/diagnose_nb03_speckle_regime.py`) |
| `RGBColor` no es int en python-pptx 1.0.2 | `hex6(rgb)`: desempacar `r,g,b = rgb` en lugar de `int(rgb)` (`scripts/`) |
| `slide_new.pptx` no persiste entre sesiones | Regenerar con `python scripts/build/add_code_slides.py` |
| Columnas `p{}` dentro de tcolorbox → crash LaTeX | Usar `lll` o `llll` sin `p{ancho}` ni `@{}` en tabular dentro de tcolorbox |
| ω₀ **no vive en el `state_dict`** | Es un atributo fijado al construir `SineLayer`. Reconstruir una red con ω₀=30 y cargarle pesos entrenados con ω₀=1 da una función distinta, **sin error visible** y con métricas silenciosamente erróneas. Fijar `modal.FIRST_OMEGA` antes de instanciar (`scripts/experiments/nb03_modal_multiseed_summary.py`) |
| La regla de ω₀ **también aplica a NB03** | ω₀=30 (valor de Sitzmann para imágenes) degrada el error propagante 35×. La entrada es z̃ normalizada y cada modo oscila ≤1 vez en el dominio → ω₀=1. Barrido en `explorations/ntk_spectral_bias_diagnostics/` y en la celda 16 del `notebooks/03` |
| Residuo bajo **no** acredita solución correcta | La formulación directa de NB03 cumplía Helmholtz a 1e-14 y la frontera exactamente, con 92.75% de error: sin condición de radiación el problema admite infinitas soluciones. Validar contra una referencia, nunca sólo por el residuo |
| k² igual a un autovalor de Dirichlet → BVP singular | En [0,1]² los autovalores son π²(m²+n²). Elegir k²=20π² (=4+16) volvió singular el caso de control de NB02b y dio 58.8% de error sin culpa del método. Verificar no-resonancia antes de entrenar (`check_not_resonant()` en `explorations/nb02b_bien_vs_mal_puesto/`). NB02 está a salvo: k²=4π² y 4 no es suma de dos cuadrados con m,n≥1 |
| Escalar k² sin normalizar el residuo → colapso a E≡0 | El término físico crece como O(k⁴) frente a datos O(1), y E≡0 satisface la ecuación homogénea. Usar el residuo normalizado `∇²E/k² + E` |
| z=1λ es la peor distancia para validar NB03 | Campo cercano estricto: 3.82% de la energía es evanescente e irrepresentable por la base modal, y el speckle aún no madura (C=0.906). El piso cae a 0.46% en 2λ y 0.001% en 5λ |
| **La continuidad exacta no implica valores exactos** | En NB03C el salto de campo y derivada entre bloques es cero algebraico, pero eso sólo garantiza que la *solución aproximada* sea continua. Lo que un bloque entrega al siguiente es su propia aproximación, de modo que el error se transfiere y puede propagarse aguas abajo. No atribuir todo el error al ajuste dentro de cada subdominio |
| **Un control que cambia varias variables a la vez no es una ablación** | El control de dominio único a 5λ difiere de NB03C en arquitectura, escala sinusoidal, presupuesto y hardware. Autoriza a decir «bajo los protocolos evaluados, A no alcanzó el criterio y B sí», nunca «B es necesario» |
| **Verificar la métrica de una cita, no sólo su valor** | El rango de Zhang et al. (2025) era correcto, pero su ecuación (16) define el error en norma L1 mientras `tab:comparativa` lo ponía bajo «Error L²». El resumen sólo dice «relative error»: la discrepancia era invisible sin el texto completo. Al comparar cifras de varios trabajos, comprobar en cada fuente cómo define su error |
| **Editar LaTeX con scripts: sólo cadenas crudas y la herramienta Write** | Un heredoc convierte `\\textbf` en tabulador y `\\ref` en retorno de carro, rompiendo la compilación sin aviso. Ocurrió dos veces el 17/09. Escribir el script con Write, todo en `r"""..."""`, y compilar exigiendo 0 errores después de cada edición |
| Importar un módulo **hereda su ω₀ por defecto**, no el que usa el experimento | `nb03_modal_pinn_siren` trae `FIRST_OMEGA=30.0` (valor de Sitzmann para imágenes); NB03 lo sobrescribe a 1 por variable de entorno. NB02B lo importaba sin fijarlo y validó durante toda una corrida la variante de ω₀=30: L² global 1.637% frente a **0.0078%** con ω₀=1, unas 210 veces peor. Fijar `os.environ['NB03_MODAL_FIRST_OMEGA']` **antes** del `import`, y comprobar en el análisis que `summary.json` y el notebook coinciden (la celda 10 del 02b lleva ese `assert`) |

---

## Referencia Rápida de Skills

| Skill | Uso |
|-------|-----|
| `/analyze` | Análisis de extremo a extremo |
| `/write [sección]` | Redacta secciones del paper |
| `/review [archivo]` | Revisión de calidad (paper, código, peer) |
| `/talk` | Presentaciones Beamer / Quarto |
| `/tools compile` | Compilar LaTeX |
| `/checkpoint` | Handoff de sesión: memoria + journal |
