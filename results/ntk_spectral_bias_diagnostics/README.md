# Diagnóstico NTK y barrido de ω₀

Dos análisis que explican por qué funcionan las decisiones de NB01 y NB02.
Ninguno reentrena ni modifica sus resultados finales.

## Kernel tangente neuronal sobre NB02

`scripts/experiments/ntk_analysis_nb02.py` carga el modelo final de NB02 y
calcula el NTK empírico del término de datos (frontera) y del término de
física (residuo de Helmholtz), cada uno sobre una muestra aleatoria de 80
puntos. Salida: `ntk_nb02.json`.

| Término | Traza NTK | Autovalor máximo |
|---|---|---|
| Datos (frontera) | 14 488 | 5 293 |
| Física (residuo) | 12 431 223 | 8 494 677 |
| **Razón física/datos** | **858×** | **1 605×** |

A peso igual, el gradiente de la física domina la optimización. Es coherente
con la ablación de `results/ablation_lambda.json`: con λ = 1.0 la corrida
falla en `float32` y λ = 0.1 es estable. Como ambas muestras son aleatorias,
las razones deben leerse como un orden de magnitud, no como valores exactos.

## Barrido de ω₀ sobre el problema de NB01

`scripts/experiments/omega0_spectral_sweep.py` hace corridas cortas nuevas
(3 000 épocas de Adam, frente al entrenamiento completo de NB01 con Adam y
L-BFGS) con k = 2π.
Salida: `omega0_sweep.json`.

| ω₀ | Pérdida final |
|---|---|
| **1.0 (ω₀ ≈ k/2π)** | **0.2656** |
| 5.0 | 0.5355 |
| 15.0 | 0.4375 |
| 30.0 | 0.6030 |

ω₀ = 1.0 converge claramente mejor. La tendencia no es monótona (15 queda por
delante de 5), y ninguna corrida divergió en 3 000 épocas: el barrido muestra
peor convergencia con la descalibración, no una réplica de la divergencia.
