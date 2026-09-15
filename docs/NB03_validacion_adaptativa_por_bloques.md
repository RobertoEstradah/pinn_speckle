# NB03: validación adaptativa por bloques hasta 5 lambda

## Qué significa 2D cuando z = 1 lambda

El problema sigue siendo bidimensional porque el campo complejo depende de
dos coordenadas cartesianas, u(x,z), y satisface

    u_xx + u_zz + k^2 u = 0.

El valor 1 lambda no reduce el problema a una dimensión; fija únicamente la
extensión longitudinal inicial del dominio. El dominio del primer piloto es
x/lambda en [-10,10] y z/lambda en [0,1]. Por ello valida Helmholtz 2D en un
dominio restringido, pero no por sí solo el alcance declarado [0,20].

## Implementación

Se encadenaron subdominios cartesianos de ancho 1 lambda. Cada red usa una
condición de Cauchy dura,

    u_j(x,s) = u_{j-1}(x,1) + s u_{j-1,z}(x,1) + s^2 N_j(x,s),

donde s está entre 0 y 1. Así, tanto el campo como su derivada longitudinal son
continuos por construcción. Los pesos SIREN y la frecuencia adaptativa se
transfieren al bloque siguiente. El espectro angular se usa únicamente después
del entrenamiento como referencia independiente.

## Resultados de la pantalla reservada 31415

| Semilla | Distancia | L2 complejo final | L2 propagante final | Máximo propagante | Correlación de intensidad |
|---:|---:|---:|---:|---:|---:|
| 73 | 2 lambda | 0.6694 % | 0.6328 % | 0.8853 % | 0.999965 |
| 211 | 2 lambda | 0.7901 % | 0.7592 % | 1.1500 % | 0.999931 |
| 73 | 5 lambda | 0.7890 % | 0.7890 % | 0.8851 % | 0.999971 |
| 211 | 5 lambda | 0.9149 % | 0.9149 % | 1.1500 % | 0.999964 |

Todas las filas cumplen L2 menor que 5 %. La continuidad de interfaces fue
exacta y la diferencia máxima de contraste respecto a la referencia fue
0.001062.

El método por bloques reduce el error propagante final a 5 lambda desde
111.4212 % en la extensión directa hasta 0.7890 %.

## Límite estadístico observado

En 5 lambda, la referencia tiene C=1.1463 y la PINN C=1.1474. La diferencia
entre ambas es mínima, por lo que el solucionador reproduce la referencia. No
obstante, |C-1| es aproximadamente 0.146 y no satisface el umbral de 0.1 en ese
plano. Esto debe estudiarse con varias realizaciones y/o estadística de
ensamble; no se debe ocultar ni atribuir a un error de la PINN.

## Estado de la evidencia

El resultado demuestra propagación Helmholtz 2D hasta 5 lambda para una pantalla
y dos inicializaciones aceptadas. Esto aporta robustez frente a los pesos
iniciales condicionada a que el bloque de 1 lambda haya convergido, pero todavía
no demuestra generalización entre pantallas, cumplimiento estadístico general
ni validez hasta 20 lambda. El siguiente control es repetir la cadena con
pantallas independientes antes de ampliar el dominio.
