# NB03: escalera de distancias de propagación

La longitud de onda física del proyecto es una sola: `lambda = 638 nm`. Las
cantidades 1, 2, 5, 10 y 20 lambda son distancias de propagación expresadas
como múltiplos de esa longitud de onda.

| Distancia normalizada | Distancia física | Estado actual |
|---:|---:|---|
| 1 lambda | 0.638 micrometros | Validada |
| 2 lambda | 1.276 micrometros | Validada en cinco pantallas |
| 5 lambda | 3.190 micrometros | Dos inicializaciones aprobadas; faltan pantallas independientes |
| 10 lambda | 6.380 micrometros | Pendiente |
| 20 lambda | 12.760 micrometros | Objetivo final declarado en Generalidades |

No se debe interpretar esta tabla como el uso de cinco longitudes de onda del
láser. En todos los casos se conserva `lambda = 638 nm`; cambia únicamente la
distancia longitudinal `z`.

La propagación adaptativa por bloques alcanzó 5 lambda en la pantalla reservada
31415 con dos inicializaciones. Los L2 completos finales fueron 0.7890 % y
0.9149 %, y el peor máximo propagante fue 1.1500 %. La continuidad de campo y
derivada fue exacta. Esto supera el piloto directo, cuyo error propagante final
fue 111.4212 %.

El avance sigue siendo progresivo. Antes de declarar 5 lambda como validación
general y continuar a 10 o 20 lambda, se debe repetir el encadenamiento con
pantallas independientes. Además, se deben
separar dos pruebas estadísticas: fidelidad de contraste respecto al espectro
angular y el criterio absoluto de Goodman |C-1|<0.1. En el plano final de esta
realización, PINN y referencia coinciden en contraste (diferencia 0.00106),
pero ambos dan C aproximadamente 1.147 y no pasan todavía el criterio absoluto.

---

## ADVERTENCIA (2026-09-15) — la fila de 2 lambda no está validada

La tabla de arriba declara 2 lambda como «Validada en cinco pantallas». Esa
afirmación proviene de la tabla de `results/nb03_distance_pilot/README.md`, que
**mezcla dos presupuestos de cómputo distintos** (180 s para las pantallas 42 y
123, 120 s para las otras tres) y promedia sobre la mezcla.

Al relanzar las cinco pantallas con presupuesto uniforme de 180 s
(`results/nb03_distance_pilot/z2_cinco_uniforme_180s/`), el resultado es:

| Pantalla | L² completo | Máximo propagante |
|---:|---:|---:|
| 42 | 1.750 % | 2.499 % |
| 123 | **6.151 %** | 7.373 % |
| 321 | **8.082 %** | 10.010 % |
| 777 | 4.192 % | **5.651 %** |
| 2026 | 1.111 % | 1.722 % |
| Media | 4.257 % | **5.451 %** |

Dos pantallas superan el 5 % en el error final y tres en el máximo. Además el
error **no decrece de forma monótona con el presupuesto**: la pantalla 321 pasa
de 3.108 % (120 s) a 8.069 % (180 s). El procedimiento no está convergiendo de
forma estable en ese régimen.

**Estado real de la escalera:** sólo 1 lambda está validada (cinco pantallas,
reentrenadas y verificadas). Las filas de 2, 5, 10 y 20 lambda son trabajo
pendiente. Ningún valor de esta tabla se ha incorporado a la tesis salvo el de
1 lambda.
