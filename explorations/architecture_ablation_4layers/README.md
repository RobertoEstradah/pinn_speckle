# Ablación adicional: 4 capas vs 5 capas (inspirado en Panagiotakopoulos et al. 2026)

**Pregunta:** Panagiotakopoulos et al. (2026) usan SIREN de 4 capas × 128
neuronas (no calibran ω₀ ni validan cuantitativamente, pero es su elección
arquitectónica). ¿Mejora o iguala NB01/NB02 con 4 capas en vez de 5?

**Método:** mismo protocolo exacto de NB01/NB02 (mismo k, λ_fís, N_colloc,
puntos de frontera, optimizador, semilla), cambiando únicamente
`num_layers` de 5 a 4. Scripts nuevos y separados — **NB01/NB02 reales no
se tocan.**

## Resultados

| | 5 capas (real, verificado) | 4 capas (esta ablación) |
|---|---|---|
| NB01 — parámetros | 16,833 | 12,673 |
| NB01 — L² | **0.006%** | 0.0133% |
| NB01 — R² | 1.000000 | 1.000000 |
| NB02 — parámetros | 66,690 | 50,178 |
| NB02 — L² promedio | **0.171%** | 0.2279% |

## Conclusión

4 capas da resultados **peores, no mejores**, en ambos casos (~2.2× y ~1.3×
el error de 5 capas, respectivamente) — aunque ambos siguen muy por debajo
del umbral de tesis (5%) por más de un orden de magnitud. Esto confirma que
5 capas **no está sobredimensionado**: la capacidad adicional sí se traduce
en mejor precisión, no es superflua. La arquitectura de 5 capas actual queda
respaldada por este dato, no cuestionada.

No hay motivo para cambiar la arquitectura de NB01/NB02 a partir de este
resultado.
