# `results/`

Una carpeta por notebook, y **cada `.json` lo escribe su propio notebook**.
Hasta septiembre de 2026 los escribian guiones aparte en `scripts/experiments/`;
hoy esas rutinas viven dentro del notebook que las explica, cada una tras un
interruptor que por defecto esta en `False`.

## `nb01/`: Helmholtz 1D

| Ruta | Qué contiene | Lo genera |
|---|---|---|
| `validation_summary.json` | Resumen de la validación 1D | notebook `01` |
| `figures/` | Solución, métricas y el caso del seno | notebook `01` |
| `barrido_omega0/` | Barrido de ω₀ sobre el problema de NB01 | notebook `01`, `RUN_NB01_OMEGA0_SWEEP` |
| `ablacion_4capas/` | 4 capas frente a 5 en 1D | notebook `01`, `RUN_NB01_4LAYER_ABLATION` |
| `models/` | Los pesos de las dos redes, coseno y seno | notebook `01`, `RUN_TRAINING` |

## `nb02/`: Helmholtz 2D con campo complejo

| Ruta | Qué contiene | Lo genera |
|---|---|---|
| `validation_summary.json` | Resumen canónico de la validación 2D | notebook `02` |
| `multiseed_results.json`, `seed777_result.json` | Dispersión frente a la semilla | notebook `02`, `RUN_NB02_MULTISEED` |
| `ablation_lambda.json` | Peso de la física: λ = 0.01, 0.1 y 1.0 | notebook `02`, `RUN_NB02_LAMBDA_ABLATION` |
| `multidirectional/` | Onda plana en cuatro direcciones | notebook `02`, `RUN_NB02_MULTIDIRECTIONAL` |
| `diagnostico_ntk/` | Traza NTK de física frente a datos | notebook `02`, `RUN_NB02_NTK` |
| `ablacion_4capas/` | 4 capas frente a 5 en 2D | notebook `02`, `RUN_NB02_4LAYER_ABLATION` |
| `figures/` | Solución, métricas y validación multidireccional | notebook `02` |
| `models/` | Los pesos de la red 2D | notebook `02`, `RUN_TRAINING` |

## `nb02b/`: Reducción modal

| Ruta | Qué contiene | Lo genera |
|---|---|---|
| `modal_bridge/` | `ModalSiren` con 1, 5 y 41 modos | notebook `02b`, `FORCE_RETRAIN` |
| `modal_basis/` | Bases modales seno, coseno y general | notebook `02b`, `FORCE_RETRAIN_BASIS` |
| `bien_vs_mal_puesto/` | Dirichlet frente a Cauchy con los mismos datos | notebook `02b`, `FORCE_RETRAIN_BVP` |
| `figures/` | Las ocho figuras, con prefijo `nb02b_` | notebook `02b` |

**Los tres puntos de control de NB01 y NB02 sí están** (412 KB entre los tres),
porque los notebooks cargan en vez de reentrenar y sin ellos fallarían al abrirse.
Los campos grandes (`.npz`) no viajan por tamaño: se regeneran poniendo en `True`
el interruptor correspondiente.
