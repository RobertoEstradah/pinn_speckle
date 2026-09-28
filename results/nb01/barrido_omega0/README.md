# Barrido de ω₀ sobre el problema de NB01

`scripts/experiments/omega0_spectral_sweep.py` hace corridas cortas nuevas
(3 000 épocas de Adam, frente al entrenamiento completo de NB01 con Adam y
L-BFGS) con k = 2π. Salida: `omega0_sweep.json`.

| ω₀ | Pérdida final |
|---|---|
| **1.0 (ω₀ ≈ k/2π)** | **0.2656** |
| 5.0 | 0.5355 |
| 15.0 | 0.4375 |
| 30.0 | 0.6030 |

ω₀ = 1.0 converge claramente mejor. La tendencia no es monótona (15 queda por
delante de 5), y ninguna corrida divergió en 3 000 épocas: el barrido muestra
peor convergencia con la descalibración, no una réplica de la divergencia.
