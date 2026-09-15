# NB03: literatura y piloto de frecuencia adaptativa

Fecha: 2026-09-13.

## Problema observado

La SIREN modal validada funciona en las cinco pantallas conocidas con semilla
neuronal 42, pero una prueba reservada con pantalla 31415 y semilla neuronal 73
se estancó en 6.7397 % de L2 completo aun después de Adam y varias etapas
L-BFGS. Esto identifica sensibilidad a la inicialización y al condicionamiento,
no una falta de correlación: la coherencia era 0.9985.

## Literatura priorizada

| Fuente | Hallazgo aplicable | Decisión |
|---|---|---|
| Jagtap, Kawaguchi y Karniadakis, JCP 2020 | Una pendiente entrenable puede acelerar PINNs y fue ensayada en Helmholtz | Implementar primero por ser un cambio pequeño y compatible con SIREN |
| Rathore et al., ICML 2024 | Los operadores diferenciales producen pérdidas mal condicionadas; Adam+L-BFGS supera frecuentemente a cada uno por separado | Mantener la secuencia híbrida y comparar a igual presupuesto |
| Wang et al., Expert's Guide 2023 | Recomienda normalización, selección cuidadosa de frecuencias, balance y evaluación reproducible | Mantener variables normalizadas, selección física fija y prueba separada |
| Wang et al., JMLR 2024, PirateNets | Las derivadas de redes profundas son sensibles a la inicialización; las conexiones residuales adaptativas mejoran entrenabilidad | Reservar como segunda modificación si la frecuencia adaptativa no es robusta |
| Wang, Wang y Perdikaris, CMAME 2021 | Fourier multiescala reduce sesgo espectral cuando su ancho de banda está bien ajustado | No repetir todavía: el piloto Fourier previo del proyecto fue inestable |

## Modificación implementada

Se añadió un único parámetro global entrenable `a` y un multiplicador fijo
`n=10` en cada seno:

`sin(omega_l * n * a * (W_l h + b_l))`.

Se inicializó `a=0.1`, de modo que `n*a=1` y la red inicial coincide con la
SIREN fija. Se conservaron:

- 41 modos propagantes;
- Helmholtz modal completo;
- condición de Cauchy dura;
- cuatro capas de 128 neuronas;
- referencia independiente por espectro angular;
- selección del checkpoint únicamente mediante residuo físico.

## Resultado controlado

Pantalla 31415, semilla neuronal 73, `z=1 lambda`:

| Modelo | L2 propagante final | Máximo propagante | L2 completo final | Residuo RMSE |
|---|---:|---:|---:|---:|
| SIREN fija | 6.4492 % | 8.0298 % | 6.7397 % | 0.04265 |
| SIREN con frecuencia adaptativa | **0.7548 %** | **0.8854 %** | **2.1018 %** | **0.00577** |

La escala efectiva terminó en 0.46684. La variante adaptativa cumple los
criterios de campo completo menor que 5 %, propagante menor que 1 % en los 201
planos y contraste respecto a la referencia menor que 0.05.

## Alcance

El resultado demuestra que la modificación rescata una combinación que la
SIREN fija no resolvió.

La confirmación posterior usó las semillas neuronales 73, 101 y 211,
predefinidas antes de correr. Dos de tres cumplieron L2 completo menor que 5 %:
2.1018 % y 2.2738 %. La semilla 101 falló con 134.9440 %. Solo una de tres
cumplió además el umbral propagante estricto menor que 1 % en todo el intervalo.

La regla primaria predefinida quedó satisfecha, pero la falla extrema impide
declarar robustez general o sustituir incondicionalmente NB03. El siguiente
experimento debe controlar la inicialización mediante cribado multistart por
residuo físico o ensayar conexiones residuales adaptativas tipo PirateNet.
