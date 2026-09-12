# NB03 (speckle óptico vía PINN) — hallazgos y diagnóstico consolidado

Última actualización: 2026-09-10 (sesión de retoma, post-espectro angular).
Consolida el historial ya documentado en CLAUDE.md hasta esa fecha, la
investigación de la sesión de pausa/archivo del 2026-09-10, y la sesión de
retoma del mismo día que introdujo el espectro angular como referencia
exacta — **esta última corrige una conclusión central de las secciones
anteriores, ver "Actualización crítica" más abajo antes de leer el resto.**

## Actualización crítica (espectro angular, sesión de retoma)

Se implementó el **método de espectro angular (ASM)** — propagación libre
exacta vía FFT, sin red neuronal, validado contra un caso analítico conocido
(error ~10⁻¹⁶). Esto permitió, por primera vez, calcular una solución EXACTA
para el problema de frontera aleatoria y compararla contra el PINN. Dos
hallazgos cambian la interpretación de todo lo anterior:

1. **A la k real de NB03 (2π, dominio=1λ), el speckle de Goodman es
   físicamente imposible** — la solución EXACTA (sin PINN) tiene solo 1/256
   modos propagantes, amplitud lejana 0.06, contraste 0.83. Esto SÍ es un
   límite físico duro, confirmado independientemente del entrenamiento.
2. **Pero la conclusión "agrandar el dominio empeora la evanescencia" era
   INCORRECTA — era una falla de entrenamiento, no un límite físico.** Un
   barrido con el ASM (30 combinaciones de dominio×correlación) encontró
   varias configuraciones físicamente viables para speckle real, la mejor:
   **dominio=80λ, fase i.i.d. sin correlacionar, contraste=1.0023, KS
   p=0.4931** — casi ideal. Al recalcular contra la solución exacta el PINN
   que ya habíamos entrenado en dominio=20λ/correlación=2λ (que la sesión
   anterior interpretó como "más evanescente"), el resultado fue: **L²=99.5%
   de error** — la solución exacta ahí tiene amplitud 0.90 (casi sin atenuar),
   pero el PINN convergió a 0.0115. `L_datos` y `L_física` del PINN habían
   convergido bien (parecía "funcionar"), pero la solución encontrada no es
   la física correcta — es un mínimo espurio que satisface la pérdida en los
   puntos muestreados sin resolver la EDP real. Coincide exactamente con el
   modo de falla que describen Krishnapriyan et al. (2021), ahora demostrado
   con un número concreto en este proyecto.

**Implicación para el trabajo futuro:** el obstáculo ya no es "¿existe una
configuración física donde esto funcione?" (sí existe, confirmado) — es
"¿cómo evita el optimizador ese mínimo espurio?". Ver la sección de
direcciones pendientes, actualizada al final.

## Resumen ejecutivo (histórico, sesión de pausa — parcialmente corregido arriba)

Ninguna de las intervenciones probadas logró que la red PINN desarrolle un
campo de speckle real (propagante, con estadísticas de Goodman) a partir de
una frontera de fase aleatoria. El problema tiene al menos dos causas
distintas y confirmadas por separado — no una sola:

1. **Escalamiento del residuo con k⁴** (arreglable): a k alta, el residuo de
   Helmholtz crece como k⁴ y domina la pérdida total, colapsando la red a la
   solución trivial E≡0. Se soluciona normalizando el residuo por k².
2. ~~Frontera de fase i.i.d. es físicamente evanescente casi por definición~~
   **[CORREGIDO arriba]:** solo es un límite físico duro a la k=2π real de
   NB03. A k/dominio más grandes, la evanescencia observada en las pruebas
   de esta sección era una falla de convergencia del PINN (mínimo espurio),
   no un límite físico — el espectro angular demuestra que sí hay
   configuraciones viables (ver "Actualización crítica" arriba).

## Historial previo (documentado en CLAUDE.md antes de esta sesión)

- Con `λ_fís` fijo (0.1, el valor validado en NB02) la frontera nunca
  converge — el residuo físico domina por escala y `L_datos` queda plano en
  ~0.5 (firma de colapso a E≡0).
- Con `λ_fís` adaptativo (balance por norma de gradiente) la frontera sí
  converge (`|E|≈0.9999` en y=0), pero entonces el residuo interior deja de
  satisfacerse y las estadísticas resultantes no son speckle real.
- Rampas graduales de `λ_fís` tras el ajuste de frontera colapsan la frontera
  de nuevo ante el más mínimo incremento.
- Diagnóstico físico (`scripts/diagnose_nb03_speckle_regime.py`, archivado
  aquí): a k=2π (la k real de NB03, heredada de NB01/NB02) solo 3 de los 256
  modos de la frontera rugosa son propagantes — el resto son evanescentes,
  porque el dominio es de apenas 1 longitud de onda.
- Intento aún más antiguo de NB03 (eliminado 2026-09-10, antes de esta
  numeración): mismo problema — el criterio de contraste por sí solo dio
  falsos positivos (C≈1) sin que el campo desarrollara speckle real, porque
  el contraste es invariante de escala y no detecta que el campo es
  mayormente evanescente.

## Investigación de la sesión 2026-09-10

### Revisión de literatura
Se revisaron Panagiotakopoulos et al. (2026) y Krishnapriyan et al. (2021)
(PDFs en `master_supporting_docs/supporting_papers/referencias/`, CC BY 4.0).
- Krishnapriyan et al.: el aprendizaje curricular (subir el coeficiente de la
  PDE gradualmente, transfiriendo pesos entre etapas) funciona en su
  arquitectura tanh-MLP porque no tiene ningún hiperparámetro acoplado a la
  frecuencia. **No aplica directamente a SIREN**: ω₀ está horneado en cada
  activación, así que transferir pesos entre etapas con ω₀ distinto es
  inválido (la propia forma de la activación cambia).
- Panagiotakopoulos et al.: resuelven Helmholtz 2D con SIREN + Adam→L-BFGS,
  pero con una fuente puntual gaussiana suave (no una frontera de fase
  aleatoria) y validan solo cualitativamente. Usan un muestreo de colocación
  ~33 puntos/longitud de onda — mucho más denso que los 3,000 puntos de NB03
  a k=2π o 10λ.

### Pruebas de control (en scratchpad, no en el repo — resultados aquí)

**Control 1 — ¿es específico de la frontera de NB03?** Se replicó el setup
exacto de NB02 (onda plana suave, 4 bordes con condición Dirichlet) pero a
k=10λ (10 veces la k real de NB03) en vez de k=2π. Resultado: colapso
idéntico (L²=100%, firma E≡0). **Conclusión: el colapso NO es específico de
la frontera aleatoria de NB03 — es un problema general de escalamiento con k
que también afecta a NB02 si se lleva a k alta.**

**Fix 1 — normalización del residuo por k².** En vez de `R = ∇²E + k²E`, usar
`R_norm = R/k² = ∇²E/k² + E`. El conjunto donde R_norm=0 es idéntico (misma
solución exacta), pero la escala de violación deja de crecer con k⁴.
Resultado en el control (onda plana, k=10λ): ya no hay colapso — ambos
términos de pérdida convergen — pero aparece un segundo problema:

**Problema 2 — densidad de colocación insuficiente (aliasing espectral).**
Con 3,000 puntos LHS (~5.5 puntos/longitud de onda a k=10λ) el error L²
seguía en 97.8% incluso sin colapso. Escalando la densidad:

| N_colloc | pts/λ | L² (onda plana, control) |
|---|---|---|
| 3,000   | 5.5  | 97.79% |
| 15,000  | 12.2 | 79.04% |
| 60,000  | 24.5 | 64.13% |

Los retornos son fuertemente decrecientes (cada duplicación de densidad cuesta
~5× más tiempo de cómputo pero reduce L² cada vez menos), y `L_física`
normalizada deja de converger de forma sostenida incluso con 60,000 puntos —
sugiere que la arquitectura (SIREN 5×128, la misma de NB02) puede no tener
capacidad suficiente para un campo tan oscilatorio, o que el entrenamiento
se corta antes de que la física realmente converja.

**Aplicación a la frontera REAL de NB03 (fase aleatoria, no onda plana):**

| Configuración | L_datos final | amp_mean (esperado ~1.0 si propaga) |
|---|---|---|
| k=2π (la k real de NB03), residuo normalizado | 0.4174 — **colapso** | 0.3336 |
| k=10λ, residuo normalizado, 15,000 pts | 1.49e-6 — frontera ajusta | 0.0679 — evanescente |
| k=20λ, residuo normalizado, 60,000 pts | 4.6e-9 — frontera ajusta | 0.0314 — **más evanescente aún** |
| k=10λ, fase correlacionada (2λ, ~5 celdas), residuo normalizado | 1.5e-7 — frontera ajusta | 0.0773 — sin mejora apreciable |

**Hallazgo clave:** a la k real de NB03 (2π) la normalización no arregla el
colapso (el problema ahí no es escalamiento con k, es la evanescencia de la
mayoría de los 256 modos). Al subir k para intentar que más modos propaguen,
la frontera deja de colapsar pero el campo se vuelve **progresivamente más
evanescente**, no menos — resultado opuesto al esperado. Correlacionar la
fase (longitud de correlación de 2λ, ~5 celdas en el dominio) tampoco cambió
esto de forma apreciable, lo que sugiere que el optimizador puede tener un
sesgo hacia soluciones localizadas/decayentes independiente del contenido
espectral disponible para propagar.

## Direcciones pendientes (actualizado tras el espectro angular)

**Herramienta ya disponible para todas estas pruebas:** el espectro angular
(`explorations/angular_spectrum_reference/`) genera la solución EXACTA para
cualquier combinación de dominio/correlación en segundos — usarla SIEMPRE
antes de entrenar un PINN nuevo, para confirmar que la configuración es
físicamente viable (contraste≈1, KS p>0.05), y usarla después para medir L²
real contra el PINN, no solo `L_datos`/`L_física`.

Configuración recomendada para retomar (ya confirmada viable por el ASM):
**dominio=80λ, fase i.i.d. sin correlacionar** (contraste=1.0023, KS p=0.49).

### Actualización (sesión de retoma 2026-09-10/11): ya se probaron varias de estas

Detalle completo, con L² real contra el ASM para cada una, en
`explorations/angular_spectrum_reference/README.md`. Resumen:

- ~~Remuestrear colocación cada época~~ — **probado**: ayuda poco (99.55%→96.22%).
- ~~Múltiples semillas~~ — **probado**: seed 123 da 96.41%, casi idéntico a la 42 —
  descarta que sea un mínimo espurio dependiente de la inicialización.
- ~~Curriculum de rugosidad~~ — **probado**: empeora (99.02%), no ayuda.
- Capacidad de red en la frontera rugosa real — **aún no probado** directamente
  (solo se probó en NB01/NB02 con solución conocida).
- **Envolvente factorizada** (E=u·e^{iky}, la red predice u en vez de E) — **NUEVA,
  no estaba en esta lista original — es la que sí funcionó**: L²=35.77%, la
  mejora más grande de toda la investigación (de ~96-99% a ~36%). Ver README
  del espectro angular para el porqué (ataca el sesgo espectral directamente).
  Sigue sin cumplir el umbral de tesis (<5%); más densidad (80,000 pts) y
  recalibrar ω₀ (probado 5.0) no mejoraron más allá de esto — meseta.

### Próximas dos técnicas identificadas en literatura (2026-09-11), aún no probadas

PDFs en `master_supporting_docs/supporting_papers/referencias/`:

- **Wang, Sankaran, Perdikaris (2024), "Respecting causality is all you need
  for training physics-informed neural networks"** (`Wang_etal_2024_RespectingCausalityPINNs.pdf`,
  CMAME, DOI:10.1016/j.cma.2024.116813, CC BY-NC-SA 4.0). Propone ponderar el
  residuo por orden causal: $w_i=\exp(-\varepsilon\sum_{k<i}\mathcal{L}_r(t_k))$,
  forzando a que se resuelva la física en puntos "tempranos" antes de permitir
  que la red se despreocupe de los posteriores. Los autores confirman que
  aplica a cualquier secuencia no decreciente, no solo tiempo — **candidato
  directo: usar y (dirección de propagación desde la frontera rugosa en y=0)
  como coordenada causal**, atacando exactamente el mínimo espurio confirmado
  con el ASM (pérdida baja, solución que no se propagó correctamente desde la
  frontera conocida).
- **Wang, Wang, Perdikaris (2021), "On the eigenvector bias of Fourier feature
  networks"** (`Wang_etal_2021_EigenvectorBiasFourierFeaturePINNs.pdf`, CMAME,
  arXiv:2012.10047). Explica por qué la prueba de Fourier features de esta
  sesión explotó numéricamente: se usó una sola escala (σ=20), redundante con
  ω₀ de SIREN. La arquitectura correcta usa **varias ramas en paralelo, cada
  una con su propio σ** (ej. 1, 20, 50, 100), compartiendo la misma red
  interna, concatenadas al final — da acceso a múltiples escalas de frecuencia
  a la vez sin que ninguna domine.

**Recomendación de orden:** primero ponderación causal por y sobre la
envolvente factorizada (ataca el mecanismo de falla ya confirmado); si no
cierra la brecha, combinar con la arquitectura Fourier multi-escala corregida.

**Resultado de la ponderación causal (probado 2026-09-11):** sin mejora
(L²=36.74% vs. 35.77% de la envolvente sola), y con episodios de colapso de
`L_datos` a ~0.495 durante el entrenamiento. Hipótesis del porqué: el
remuestreo de colocación por época hace que la pérdida por franja de y
fluctúe mucho entre iteraciones, volviendo ruidosos los pesos causales.
Probar con puntos fijos quedaría pendiente.

## Segunda ronda de literatura (2026-09-11) — 4 papers nuevos descargados

PDFs en `master_supporting_docs/supporting_papers/referencias/`. Lo verificado
de cada uno (leído, no citado de memoria):

### 1. MH-PINN — restricciones duras para problemas de onda no acotados
`MHPINN_2026_HardConstrainedUnboundedWaveProblems.pdf` (arXiv:2604.19843)

**El resultado cuantitativo más fuerte encontrado.** Reporta L² de 10⁻⁴–10⁻³
para k=1–10 y **2.54×10⁻⁶ a k=20**, mientras que el PINN estándar *diverge a
0.9 (90% de error) a k=10* — exactamente el mismo modo de falla catastrófico
que documentamos nosotros. Entrenamiento: 52–79 s vs. 200–450 s del PINN
estándar.

Mecanismo: descompone la solución como `û(x) = Φ(x)·E(x)` donde
- `Φ(x) = e^{ik(|x|−R_in)}/|x|^{(d−1)/2}` — factor asintótico de campo lejano
  que codifica analíticamente la oscilación de fase (**es la misma idea que
  nuestra envolvente factorizada E=u·e^{iky}, lo que confirma que esa
  dirección era correcta**);
- `E(x) = g_D(x)/Φ(x) + d(x)·N(x)` con `d(x)` una función de distancia que se
  anula en la frontera — **la condición de frontera se cumple por
  construcción, eliminando por completo el término de pérdida de frontera.**

**Limitación explícita (citada por los autores):** el método asume un
dispersor "simplemente conexo" y no aborda Helmholtz 2D con condición en una
sola arista finita — es decir, **no es directamente aplicable a nuestra
geometría**, pero su segundo componente (frontera exacta por construcción) sí
lo es.

### 2. FBPINNs multinivel — descomposición de dominio
`Dolean_etal_2023_MultilevelDomainDecompositionFBPINNs.pdf` (arXiv:2306.05486)

Descompone el dominio en subdominios solapados (ratio δ=1.9), cada uno con una
red local pequeña (1 capa × 16 unidades), combinados por funciones ventana con
partición de unidad, en L niveles jerárquicos (J⁽ˡ⁾=2^(d(l−1)) subdominios).
Al normalizar coordenadas por subdominio, **convierte un problema de alta
frecuencia en varios de baja frecuencia**, reduciendo el sesgo espectral de
forma estructural.

**Dato clave para calibrar expectativas:** probaron Helmholtz hasta
k=2⁶π/1.6 ≈ **125.7 — exactamente nuestro k de 20λ (125.66)** — y ahí reportan
que el método "modela la frecuencia dominante y la concentricidad general pero
falla en los motivos más complejos" y "batalla para satisfacer simultáneamente
la fuente puntual y la condición de Dirichlet". O sea: **a nuestro régimen
exacto, ni siquiera un método de descomposición de dominio del estado del arte
lo resuelve por completo.** Reportan pérdida L1 normalizada, no L².

### 3. Imposición exacta de condiciones de frontera con funciones de distancia
`Sukumar_Srivastava_2021_ExactBoundaryConditionsDistanceFunctionsPINN.pdf`
(arXiv:2104.08426). Referencia clásica del enfoque de restricción dura
(funciones de distancia + interpolación transfinita, R-funciones). Solo se
verificó el resumen — el PDF completo (50 pp.) queda como respaldo.

### 4. Análisis espectral de PINNs con restricción dura
`SpectralAnalysis_2025_HardConstraintPINNsBoundaryFunctions.pdf`
(arXiv:2512.23295, CC BY 4.0). Analiza cómo la elección de las funciones de
frontera modula el espectro de la solución. **No verificado en detalle** —
descargado como respaldo por su relevancia directa al diseño del ansatz.

### Hallazgo de óptica: la fase de nuestra frontera podría ser demasiado pequeña

De la literatura de scattering de superficies rugosas, el criterio estándar
para speckle completamente desarrollado y validez de la aproximación de
Kirchhoff pide: fluctuaciones de fase gaussianas con **RMS mucho mayor que
2π rad**, autocorrelación gaussiana con **longitud de correlación > 2λ**, y
razón entre ambas < 0.05.

**Nuestra frontera no cumple el primer criterio:** el código usa
`phi_x = normalizado * π`, es decir **RMS de fase = π ≈ 3.14 rad**, por debajo
de 2π (y muy lejos de "mucho mayor que 2π"). En el caso i.i.d., φ~U(0,2π) da
un RMS aún menor (2π/√12 ≈ 1.81 rad). La longitud de correlación sí cumplía
(2λ, justo en el límite).

**Advertencia de verificación:** este criterio proviene de resúmenes de
búsqueda de fuentes de pago (Springer/ScienceDirect) que **no pude leer
completas** — debe confirmarse contra Goodman (2007), que ya está citado en la
tesis, antes de usarlo como justificación formal.
