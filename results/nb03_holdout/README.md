# NB03: prueba reservada de robustez

Se evaluó una pantalla no usada en las cinco validaciones anteriores y una
semilla neuronal distinta:

- pantalla física: 31415;
- semilla de la red: 73;
- distancia: 1 lambda;
- ancho transversal: 20 lambda;
- 41 modos propagantes;
- condición de Cauchy dura;
- selección de checkpoints únicamente por residuo físico fijo;
- referencia por espectro angular usada solo para la prueba final.

La referencia presentó contraste individual 1.0922 y contraste de conjunto
0.9663. Por tanto, la pantalla pertenece al régimen estadístico esperado.

## Resultados

| Etapa | L2 propagante final | Máximo propagante | L2 completo final | Residuo RMSE |
|---|---:|---:|---:|---:|
| Adam inicial, 3031 pasos | 100.3591 % | 100.3591 % | 100.3590 % | 0.2198 |
| Adam continuado, 7360 pasos acumulados | 35.1381 % | 35.7453 % | 35.1860 % | 0.0979 |
| L-BFGS, primera etapa desde Adam continuado | 6.5207 % | 8.1641 % | 6.8082 % | 0.0514 |
| L-BFGS, segunda etapa | **6.4492 %** | **8.0298 %** | **6.7397 %** | **0.0427** |

La coherencia compleja final fue 0.9985 y el error de contraste fue 0.0068,
pero el criterio principal de campo completo `L2 < 5 %` no se cumplió.

## Veredicto

Esta prueba no invalida las cinco pantallas conocidas ni la validación de
distancia entre 1 y 2 lambda. Sí demuestra que esos resultados no bastan para
afirmar robustez frente a cualquier inicialización neuronal. La arquitectura
puede representar bien la forma y estadística del campo mientras conserva un
error complejo mayor al umbral.

El resultado es diagnóstico y no debe sustituir el modelo aceptado. Antes de
declarar generalidad se recomienda un protocolo multiseed con semillas fijadas
antes de entrenar y selección basada solo en residuo físico.

## Mejora basada en literatura: frecuencia adaptativa

Se implementó después una SIREN con un multiplicador global entrenable `n*a`
en las activaciones sinusoidales, siguiendo la idea de activación escalable de
Jagtap, Kawaguchi y Karniadakis (JCP 2020, DOI
`10.1016/j.jcp.2019.109136`). La red comienza con `n*a=1`, por lo que su estado
inicial es equivalente a la SIREN fija; no cambia Helmholtz, los 41 modos ni la
condición de Cauchy dura.

Comparación con la misma pantalla 31415 y semilla neuronal 73:

| Método y presupuesto | L2 propagante final | Máximo propagante | L2 completo final | Residuo RMSE |
|---|---:|---:|---:|---:|
| SIREN fija, Adam 180 s + L-BFGS 60 s | 20.7186 % | 29.1618 % | 20.8073 % | 0.1007 |
| Frecuencia adaptativa, mismo presupuesto | 10.2964 % | 13.9377 % | 10.4796 % | 0.0443 |
| Frecuencia adaptativa, L-BFGS total 180 s | **0.7548 %** | **0.8854 %** | **2.1018 %** | **0.00577** |

La escala adaptativa evolucionó de 1.0 a 0.46684. El piloto cumple L2 completo
menor que 5 %, error propagante menor que 1 % en los 201 planos y error de
contraste menor que 0.05.

### Confirmación predefinida en tres semillas neuronales

Antes de ejecutar las corridas adicionales se fijaron las semillas 73, 101 y
211, el mismo presupuesto y la regla primaria de aprobación: al menos 2 de 3
con L2 completo menor que 5 %.

| Semilla neuronal | L2 propagante | Máximo propagante | L2 completo | Residuo | Escala final |
|---:|---:|---:|---:|---:|---:|
| 73 | 0.7548 % | 0.8854 % | 2.1018 % | 0.00577 | 0.46684 |
| 101 | 134.9558 % | 134.9558 % | 134.9440 % | 0.30065 | 0.88832 |
| 211 | 1.1500 % | 1.1500 % | 2.2738 % | 0.00611 | 0.28236 |

La regla primaria quedó confirmada en 2 de 3 semillas. Sin embargo, solo la
semilla 73 cumplió todos los criterios propagantes y la semilla 101 falló de
forma catastrófica. Por ello la frecuencia adaptativa es una mejora demostrada,
pero no es todavía robusta a la inicialización ni debe sustituir de manera
incondicional el protocolo principal.

## Reproducción

Los scripts creados son:

- `scripts/experiments/nb03_holdout_validation.py`;
- `scripts/experiments/nb03_holdout_continue.py`.
- `scripts/experiments/nb03_adaptive_omega_holdout.py`.

Cada subdirectorio conserva el checkpoint, las curvas de campo y un
`summary.json` con configuración, tiempos, pasos y métricas.

La consolidación está en `adaptiveomega_multiseed_summary.json` y el plan
registrado antes de las corridas en `adaptiveomega_confirmation_plan.md`.
