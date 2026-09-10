# NB03 (speckle óptico vía PINN) — hallazgos y diagnóstico consolidado

Última actualización: 2026-09-10. Consolida el historial ya documentado en
CLAUDE.md hasta esa fecha, más la investigación completa de la sesión del
2026-09-10 (revisión de literatura + pruebas de control en scratchpad).

## Resumen ejecutivo

Ninguna de las intervenciones probadas logró que la red PINN desarrolle un
campo de speckle real (propagante, con estadísticas de Goodman) a partir de
una frontera de fase aleatoria. El problema tiene al menos dos causas
distintas y confirmadas por separado — no una sola:

1. **Escalamiento del residuo con k⁴** (arreglable): a k alta, el residuo de
   Helmholtz crece como k⁴ y domina la pérdida total, colapsando la red a la
   solución trivial E≡0. Se soluciona normalizando el residuo por k².
2. **Frontera de fase i.i.d. es físicamente evanescente casi por definición**
   (no arreglable con más cómputo): una fase aleatoria muestreada punto a
   punto sin correlación espacial tiene contenido espectral de ruido blanco,
   que para cualquier k razonable es mayormente evanescente, no propagante.
   Subir k no ayuda — empeora. Correlacionar la fase con una longitud de
   correlación físicamente razonable (2λ) tampoco ayudó de forma apreciable
   en las pruebas realizadas, lo que sugiere que además existe un sesgo del
   optimizador hacia soluciones localizadas/decayentes.

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

## Direcciones no exploradas (para cuando se retome)

- Longitudes de correlación mayores (probado solo 2λ) combinadas con un
  dominio de muchas más longitudes de onda (para tener suficientes celdas de
  correlación independientes sin perder propagación) — computacionalmente
  caro, no probado por restricciones de tiempo.
- Investigar si el sesgo hacia soluciones evanescentes es del optimizador
  (Adam/L-BFGS) o de la inicialización SIREN — probar otras semillas o
  inicializaciones antes de asumir que es un límite físico duro.
- Revisar si una arquitectura con más capacidad (más capas/neuronas) cambia
  el resultado a densidad de colocación fija, en vez de asumir que el cuello
  de botella es siempre la densidad de puntos.
- Muestreo de colocación concentrado cerca de y=0 (mencionado en
  Cap4-Resultados.tex como línea pendiente, informado por Panagiotakopoulos
  et al.) — no se probó en esta sesión.
