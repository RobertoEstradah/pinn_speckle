# Ablación: 4 capas frente a 5

Mismo protocolo de NB01 y NB02 (k, λ, puntos de colocación y de frontera,
optimizador y semilla), cambiando sólo el número de capas ocultas de 5 a 4.
Scripts: `scripts/experiments/ablation_4layers_nb01.py` y
`ablation_4layers_nb02.py`. Salidas: `nb01_4layers.json`, `nb02_4layers.json`.

| | 5 capas | 4 capas |
|---|---|---|
| NB01: parámetros | 16 833 | 12 673 |
| NB01: L² | **0.006 %** | 0.0133 % |
| NB02: parámetros | 66 690 | 50 178 |
| NB02: L² promedio | **0.171 %** | 0.2279 % |

Con 4 capas el error es mayor en ambos casos, aunque sigue muy por debajo del
umbral de 5 %. La capacidad de la quinta capa sí se traduce en precisión.
