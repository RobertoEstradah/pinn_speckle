# Testbed: fase correlacionada para NB03 (speckle vía PINN)

**Objetivo:** probar si aumentar la longitud de correlación de la frontera
de fase Y el tamaño del dominio (en longitudes de onda) simultáneamente
—en vez de solo una de las dos, ya probado y sin éxito en la sesión
2026-09-10 (ver `archive/nb03_speckle_pausado/hallazgos_y_diagnostico.md`)—
logra que el campo interior sea genuinamente propagante (no evanescente).

**Por qué aquí y no en NB01/NB02 ni en NB03 directamente:** es la dirección
de investigación pendiente más prometedora de `hallazgos_y_diagnostico.md`.
No se modifica NB01/NB02 (verificados y finales, reportados en la tesis) ni
se reactiva NB03 todavía — este es un experimento nuevo y aislado que, si
funciona, informa cómo retomar NB03 más adelante.

**Hipótesis a probar:** con corr=2λ y dominio=10λ (5 celdas de correlación)
la mejora sobre fase i.i.d. fue nula (amp_mean 0.068→0.077). Con el mismo
corr=2λ pero dominio=20λ (10 celdas), ¿mejora la propagación o el resultado
sigue igual de evanescente?

## Estado

- 2026-09-10: primera corrida (`scripts/correlated_phase_20lambda_corr2lambda.py`),
  ver `SESSION_LOG.md` para resultados.

## Estructura

```
scripts/   — scripts de la prueba (no notebooks, exploración rápida)
output/    — resultados JSON de cada corrida
```
