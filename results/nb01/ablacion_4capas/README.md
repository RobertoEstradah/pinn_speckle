# Ablación: 4 capas frente a 5, en 1D

Mismo protocolo de NB01 (k, λ, puntos de colocación y de frontera, optimizador
y semilla), cambiando sólo el número de capas ocultas de 5 a 4.
Script: `scripts/experiments/ablation_4layers_nb01.py`. Salida: `nb01_4layers.json`.

| | 5 capas | 4 capas |
|---|---|---|
| Parámetros | 16 833 | 12 673 |
| Error $L^2$ | **0.006 %** | 0.0133 % |

Con 4 capas el error es mayor, aunque sigue muy por debajo del umbral de 5 %.
La capacidad de la quinta capa sí se traduce en precisión. El caso 2D está en
`results/nb02/ablacion_4capas/`.
