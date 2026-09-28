# Diagnóstico NTK sobre NB02

`scripts/experiments/ntk_analysis_nb02.py` carga el modelo final de NB02 y
calcula el NTK empírico del término de datos (frontera) y del término de
física (residuo de Helmholtz), cada uno sobre una muestra aleatoria de 80
puntos. Salida: `ntk_nb02.json`. No reentrena ni modifica los resultados de
NB02.

| Término | Traza NTK | Autovalor máximo |
|---|---|---|
| Datos (frontera) | 14 488 | 5 293 |
| Física (residuo) | 12 431 223 | 8 494 677 |
| **Razón física/datos** | **858×** | **1 605×** |

A peso igual, el gradiente de la física domina la optimización. Es coherente
con la ablación de `results/nb02/ablation_lambda.json`: con λ = 1.0 la corrida
falla en `float32` y λ = 0.1 es estable. Como ambas muestras son aleatorias,
las razones deben leerse como un orden de magnitud, no como valores exactos.
