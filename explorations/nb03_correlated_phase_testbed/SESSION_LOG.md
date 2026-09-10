# Session Log

## 2026-09-10 — Primera corrida: dominio=20λ, corr=2λ (10 celdas)

**Hipótesis probada:** duplicar el dominio (de 10λ a 20λ) manteniendo la
misma longitud de correlación absoluta (2λ) —duplicando así el número de
celdas de correlación independientes de 5 a 10— mejoraría la propagación
del campo respecto a la prueba anterior (dominio=10λ, 5 celdas,
amp_mean=0.0773, sin mejora apreciable sobre fase i.i.d.).

**Resultado:** `output/corr2lambda_domain20lambda.json`

| Configuración (N_colloc=60,000, dominio=20λ) | amp_mean | amp_mean en y=1 (borde lejano) |
|---|---|---|
| Fase i.i.d. (sin correlación) | 0.0314 | — |
| Fase correlacionada 2λ, dominio=10λ (5 celdas) | 0.0773 | — |
| **Fase correlacionada 2λ, dominio=20λ (10 celdas)** | **0.0115** | **0.0007** |

**Hipótesis REFUTADA.** Agrandar el dominio empeoró la propagación en vez de
mejorarla — es el peor resultado registrado hasta ahora, incluso peor que la
fase i.i.d. al mismo dominio. Explicación física: la longitud de decaimiento
evanescente escala con la longitud de onda, no con el tamaño del dominio: al
agrandar el dominio en unidades de λ, la fracción del dominio "alcanzada"
por el campo cerca de la frontera se hace más pequeña sin importar la
longitud de correlación de la fase.

**Conclusión para esta línea de investigación:** "dominio más grande + más
longitud de correlación" no es la dirección correcta — descartada con este
dato. De las direcciones listadas en
`archive/nb03_speckle_pausado/hallazgos_y_diagnostico.md`, quedan sin
probar: sesgo del optimizador (otras semillas/inicializaciones), capacidad
de red, y muestreo de colocación concentrado cerca de y=0.
