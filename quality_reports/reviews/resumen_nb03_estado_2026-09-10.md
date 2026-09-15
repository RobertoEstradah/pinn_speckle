# Estado de NB03 — resumen para Adán

**Fecha:** 2026-09-10 · **Autor:** Roberto Hernández Estrada

## En una frase

NB03 no genera *speckle* óptico real: el dominio hereda `k = 2π` de la validación 1D/2D,
lo que equivale a una placa de **1 longitud de onda de ancho** — demasiado pequeña para
que el fenómeno estadístico exista. Se intentó corregir subiendo la escala del dominio,
pero el entrenamiento de la PINN no converge en ese régimen. El problema sigue abierto.

## Cómo se conecta con lo que ya discutimos de las distancias

En la llamada del 8 de septiembre, Adán pidió generar la propagación a distancias reales
(1λ a 10λ primero, luego 2-20 cm) en lugar de trabajar en unidades de λ sin escala física,
y sugirió acercar la simulación a algo realista antes de fijar las distancias — lo que dio
origen a NB04.

Es la misma corrección, vista desde otro ángulo. NB04 usa generación estadística directa
(no PINN) y por eso no tropieza con esto. NB03 sí resuelve Helmholtz con PINN, y ahí el
tamaño del dominio deja de ser cosmético: determina si el fenómeno de *speckle* puede
existir físicamente.

## El diagnóstico (verificado, reproducible)

Con `k = 2π` sobre `[0,1]²`, la frontera rugosa (256 fases aleatorias independientes en
`y=0`) se descompone en modos de Fourier. Solo los modos con `|k_x| ≤ k` se propagan; el
resto es evanescente y decae antes de entrar al dominio.

Resultado medido (script `scripts/experiments/diagnose_nb03_speckle_regime.py`, solución
exacta por espectro angular, sin entrenar nada):

| Dominio | Modos que propagan | Energía que entra | Contraste $C$ (exacto) |
|---|---|---|---|
| 1λ (NB03 actual) | 3 de 256 | 0.47 % | 1.368 |
| 10λ | 21 de 256 | 5.0 % | 0.985 |
| 20λ | 41 de 256 | 14.1 % | 0.966 |
| 30λ | 61 de 256 | — | 0.972 |

El campo interior en 1λ es la superposición de 3 ondas planas — interferencia suave, no
*speckle*. El contraste `C = σ_I/⟨I⟩` no lo detecta porque es invariante de escala: hasta
un campo de 5 modos puede dar `C≈1` sin ser *speckle* real.

**El test más estricto (Kolmogorov-Smirnov contra la exponencial teórica) es más exigente
todavía.** Incluso con la solución exacta (sin red, sin error de entrenamiento), el
umbral de aceptación (`p > 0.05`) no se cruza hasta:

| Dominio | KS p-valor (solución exacta) |
|---|---|
| 10λ | 0.00006 |
| 20λ | 0.044 (al límite) |
| **30λ** | **0.47 (pasa)** |

Es decir: **el corte físico real está en ~30λ, no en 10λ.**

## El intento de corrección — por qué no se aplicó todavía

Siguiendo la regla ya establecida del proyecto (`ω₀ ≈ k/2π`), se probó reescalar NB03 a
`k = 2π·10` con `ω₀ = 10`, y luego a `k = 2π·30` con `ω₀ = 30`, entrenando la misma
arquitectura SIREN.

**En ambos casos el entrenamiento no ajusta la frontera.** La pérdida de datos
(`L_datos`) queda estancada cerca de su valor inicial durante miles de épocas — el mismo
síntoma que ya tenía NB03 a escala 1λ, pero ahora persiste incluso ajustando el peso
relativo entre pérdida física y pérdida de frontera (se probó bajar `λ_fís` hasta `10⁻⁵`
y subir el peso de la frontera hasta 50×, con mejora parcial pero sin convergencia real).

Una corrida completa a 10λ con la mejor configuración encontrada dio, después de 15,000
épocas de presupuesto:

```
L_datos final      : 0.367   (se necesita <0.05 para un ajuste real)
|E| en la frontera  : 0.43   (debía acercarse a 1.0)
Contraste C         : 7.82   (peor que el 1.025 de NB03 actual)
KS p-valor          : 0.0    (falla total)
```

Es decir, el resultado fue **peor** que el problema original, no mejor.

## Interpretación

Esto no es un ajuste de hiperparámetros — es el tipo de falla que Krishnapriyan et al.
(2021) (ya citado en la tesis, `Cap2-Marcos.tex`) documenta para PINNs en problemas de
alta frecuencia: el paisaje de optimización se vuelve genuinamente más difícil a medida
que crece `k`, independientemente del balance de pesos en la función de pérdida. Puede
requerir una estrategia distinta (currículo de escalas crecientes, arquitectura con más
capacidad, otra forma de imponer la frontera) que no se ha explorado todavía por falta de
tiempo.

## Estado actual del proyecto (sin cambios aplicados a NB03)

- **NB01, NB02:** sin tocar, resultados verificados y re-ejecutados hoy con éxito.
- **NB03:** congelado, sin modificar. Todo lo anterior son pruebas fuera del notebook.
- **NB04:** sin tocar, no depende de este problema.
- **Tesis y papers:** actualizados solo en la parte 1D/2D (tiempos, tabla multi-semilla,
  correcciones de redacción). La sección de *speckle* de la tesis (Cap. 4) sigue
  reportando el resultado antiguo de NB03, sin corregir, a la espera de esta decisión.

## Lo que se necesita decidir con Adán

1. ¿Priorizamos seguir intentando resolver NB03 (con más tiempo para explorar estrategias
   de entrenamiento), o lo dejamos como trabajo futuro — igual que ya está NB05 — y se
   documenta honestamente en la tesis como una limitación identificada?
2. Si se sigue intentando, ¿qué tanto tiempo es razonable invertir antes del coloquio
   final?
3. La pregunta de investigación de la tesis (*"¿Puede una PINN-SIREN simular speckle
   óptico con L² < 5% y contraste C≈1?"*) depende de esto. Sin NB03 resuelto, la
   respuesta honesta hoy es "no todavía" — hay que decidir cómo se refleja eso en las
   conclusiones.

**Archivos de referencia:**
`scripts/experiments/diagnose_nb03_speckle_regime.py` (diagnóstico, reproducible) ·
`results/nb03_speckle_regime.json` (resultados numéricos) ·
`quality_reports/reviews/tesis_actual_writer_critic_2026-09-09.md` (revisión completa)
