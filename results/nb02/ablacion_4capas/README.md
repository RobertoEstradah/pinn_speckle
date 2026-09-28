# Ablación: 4 capas frente a 5, en 2D

Mismo protocolo de NB02 (k, λ, puntos de colocación y de frontera, optimizador
y semilla), cambiando sólo el número de capas ocultas de 5 a 4.
Script: `scripts/experiments/ablation_4layers_nb02.py`. Salida: `nb02_4layers.json`.

| | 5 capas | 4 capas |
|---|---|---|
| Parámetros | 66 690 | 50 178 |
| Error $L^2$ promedio | **0.171 %** | 0.2279 % |

Misma conclusión que en 1D: la quinta capa mejora la precisión. El caso 1D
está en `results/nb01/ablacion_4capas/`.
