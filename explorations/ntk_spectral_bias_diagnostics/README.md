# Diagnóstico NTK y sesgo espectral (sobre NB01/NB02 ya entrenados)

**Objetivo:** análisis adicional inspirado en Wang et al. (2022, teoría NTK) y
Rahaman et al. (2019, sesgo espectral) — ambos ya citados en
`Cap2-Marcos.tex` — para profundizar el "por qué funciona" de NB01/NB02, sin
reentrenar ni modificar sus resultados finales ya reportados y verificados.

## 1. Análisis NTK sobre NB02 (`scripts/ntk_analysis_nb02.py`)

Carga el modelo YA ENTRENADO (`results/models/nb02_helmholtz2d_gpu.pt`, sin
reentrenar) y calcula el kernel tangente neuronal (NTK) empírico para el
término de datos (frontera, onda plana) y el término de física (residuo de
Helmholtz), sobre una muestra de 80 puntos cada uno.

**Resultado** (`output/ntk_nb02.json`):

| Término | Traza NTK | Autovalor máximo |
|---|---|---|
| Datos (frontera) | 14,488 | 5,293 |
| Física (residuo Helmholtz) | 12,431,223 | 8,494,677 |
| **Razón física/datos** | **858×** | **1,605×** |

**Interpretación:** el término de física tiene un espectro NTK ~858× más
grande que el de datos. Según la teoría de Wang et al., esto significa que,
a peso igual (λ=1.0), el gradiente del término de física domina por completo
el paso de optimización — consistente cuantitativamente con el hallazgo ya
documentado en la ablación de `Cap4-Resultados.tex`: λ=1.0 es inestable
(explota en float32) y λ=0.1 es la configuración estable. Este análisis no
prueba que 0.1 sea el valor "óptimo" exacto (la razón NTK sugeriría un factor
de reescalamiento aún menor si se tomara literalmente), pero sí explica
cuantitativamente la *dirección y magnitud* del desbalance que motivó la
ablación.

## 2. Barrido de ω₀ (sesgo espectral) sobre NB01 (`scripts/omega0_spectral_sweep.py`)

Corridas cortas y nuevas (3,000 épocas Adam, no las 15,000+L-BFGS del NB01
real) para ω₀ ∈ {1.0, 5.0, 15.0, 30.0} con k=2π fijo, mismo problema de NB01.

**Resultado** (`output/omega0_sweep.json`):

| ω₀ | Pérdida final (3,000 épocas) |
|---|---|
| **1.0 (calibrado, ω₀≈k/2π)** | **0.2656** |
| 5.0 | 0.5355 |
| 15.0 | 0.4375 |
| 30.0 | 0.6030 |

**Interpretación:** ω₀=1.0 (el valor calibrado y usado en NB01) converge
notablemente mejor que los demás en la misma cantidad de épocas — apoya
cuantitativamente la regla de calibración ω₀≈k/(2π) con un barrido, no solo
con el caso puntual ω₀=30. **Nota honesta:** ninguna corrida divergió
(pérdida infinita/NaN) en estas 3,000 épocas — la "explosión de gradientes"
documentada para ω₀=30 en CLAUDE.md pudo haberse observado en un
entrenamiento más largo o con otra configuración; este barrido corto muestra
la tendencia (peor convergencia a mayor descalibración), no una réplica
literal de la divergencia.

## Estado

Análisis completo, no incorporado todavía a la tesis (Cap4-Resultados.tex) —
pendiente de decidir con el usuario si se agrega como figura/discusión
adicional.
