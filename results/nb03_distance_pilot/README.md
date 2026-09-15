# NB03: extensión de distancia

## Resultado validado

La estrategia directa modal PINN-SIREN, con la misma arquitectura, condición
de Cauchy dura y refinamiento L-BFGS `float32`, fue probada en cinco pantallas
para (z=2\lambda).

| Pantalla | L2 propagante final | L2 completo final | Máximo propagante en 201 planos | Residuo RMSE |
|---:|---:|---:|---:|---:|
| 42 | 0.887 % | 0.997 % | 1.303 % | 0.01038 |
| 123 | 1.318 % | 1.350 % | 1.848 % | 0.01302 |
| 321 | 3.108 % | 3.142 % | 3.918 % | 0.01883 |
| 777 | 2.411 % | 2.435 % | 2.571 % | 0.01620 |
| 2026 | 1.710 % | 1.750 % | 2.595 % | 0.01412 |
| **Media** | **1.887 %** | **1.935 %** | **2.447 %** | **0.01451** |

Las cinco pantallas cumplen (L^2<5\%) tanto al final como en el máximo de
los 201 planos evaluados. Esto permite declarar la validación controlada en
(1\lambda\le z\le2\lambda), con las condiciones experimentales actuales.

## Resultado no aprobado

Un piloto directo para (z=5\lambda) en la pantalla 42, con 180 s de
refinamiento, obtuvo:

- L2 propagante final: 9.586 %.
- Máximo propagante: 16.346 %.
- Residuo RMSE: 0.02516.

También se ensayó una cadena de bloques de (1\lambda); el primer bloque
adicional no convergió de forma aceptable en 60 s y produjo 138 % de error.
Este resultado se conserva como diagnóstico, no como parte del modelo final.

Posteriormente se ensayó la frecuencia SIREN adaptativa que había alcanzado
2.1018 % de L2 completo en la pantalla reservada 31415 a (z=1\lambda). Al
extender directamente ese checkpoint a (z=5\lambda) y refinarlo durante 180 s,
se obtuvo 111.4212 % de L2 propagante, 115.3295 % de máximo propagante,
111.4212 % de L2 completo y residuo RMSE 0.1092. La extensión directa también
queda rechazada: la mejora de inicialización a una lambda no elimina la
dificultad de optimizar todo el intervalo largo de una sola vez.

## Interpretación

La metodología no se invalida: se ha ampliado de (1\lambda) a (2\lambda).
El aumento a (5\lambda) exige una mejora de entrenamiento o una
formulación de propagación por bloques más robusta. No se debe afirmar todavía
que NB03 funciona hasta (5\lambda), (10\lambda), (20\lambda) ni a
cualquier distancia.

La siguiente implementación deberá respetar la metodología declarada en las
Generalidades: bloques locales de una lambda, transferencia del campo y su
derivada, reutilización de los pesos internos y frecuencia adaptativa en cada
interfaz. Cada bloque debe aprobar el residuo y la continuidad antes de avanzar.

## Archivos

- `z2_five_120s/summary.json`: pantallas 321, 777 y 2026 a (2\lambda).
- `z2_seeds42_123_180s/summary.json`: pantallas 42 y 123 a (2\lambda).
- `z5_seed42_180s/summary.json`: piloto no aprobado a (5\lambda).
- `pilot_z2_z5_v2/summary.json`: piloto directo inicial a 2 y (5\lambda).
- `pilot_z2_slabs_v1/summary.json`: diagnóstico de bloques locales.
- `z5_screen31415_net73_adaptive180/summary.json`: extensión directa
adaptativa rechazada a (5\lambda).

## Nuevo piloto adaptativo por bloques

Se implementó la alternativa prescrita en las Generalidades: bloques locales
de una lambda, condición de Cauchy dura en cada interfaz y transferencia de
pesos y frecuencia adaptativa. En la pantalla reservada 31415 y semilla de red
73 se obtuvieron:

| Semilla de red | Alcance | L2 propagante final | L2 completo final | Máximo propagante | Correlación de intensidad | Diferencia de contraste |
|---:|---:|---:|---:|---:|---:|---:|
| 73 | 2 lambda | 0.6328 % | 0.6694 % | 0.8853 % | 0.999965 | 0.000637 |
| 211 | 2 lambda | 0.7592 % | 0.7901 % | 1.1500 % | 0.999931 | 0.000543 |
| 73 | 5 lambda | 0.7890 % | 0.7890 % | 0.8851 % | 0.999971 | 0.001062 |
| 211 | 5 lambda | 0.9149 % | 0.9149 % | 1.1500 % | 0.999964 | 0.000941 |

La continuidad máxima de campo y derivada fue cero en todas las interfaces.
El resultado a 5 lambda aprueba la fidelidad numérica para dos inicializaciones,
pero aún corresponde a una sola pantalla. Asimismo, C de la referencia fue 1.1463
y C de la PINN 1.1474: reproducen la misma estadística, aunque ese plano no
cumple el criterio absoluto de Goodman |C-1|<0.1.

Archivos nuevos:

- `z2_screen31415_net73_adaptive_slabs_v1/summary.json`.
- `z5_screen31415_net73_adaptive_slabs_v1/summary.json`.
- `z2_screen31415_net211_adaptive_slabs_v1/summary.json`.
- `z5_screen31415_net211_adaptive_slabs_v1/summary.json`.
- `adaptive_slabs_multiseed_summary.json`.

NB01 y NB02 no forman parte de estos ensayos y no se modificaron durante esta
extensión.
