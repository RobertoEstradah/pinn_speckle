# `results/`

Una carpeta por notebook. Cada `.json` lo escribe el notebook correspondiente o
un guion de `scripts/experiments/`.

## `nb01/` — Helmholtz 1D

| Ruta | Qué contiene | Lo genera |
|---|---|---|
| `validation_summary.json` | Resumen de la validación 1D | notebook `01` |
| `figures/` | Solución, métricas y el caso del seno | notebook `01` |
| `barrido_omega0/` | Barrido de ω₀ sobre el problema de NB01 | `omega0_spectral_sweep.py` |
| `ablacion_4capas/` | 4 capas frente a 5 en 1D | `ablation_4layers_nb01.py` |

## `nb02/` — Helmholtz 2D con campo complejo

| Ruta | Qué contiene | Lo genera |
|---|---|---|
| `multiseed_results.json`, `seed777_result.json` | Dispersión frente a la semilla | `run_multiseed.py`, `run_seed777.py` |
| `ablation_lambda.json` | Peso de la física: λ = 0.01, 0.1 y 1.0 | `run_ablation_lambda.py` |
| `multidirectional/` | Onda plana en cuatro direcciones | `nb02_multidirectional_validation.py` |
| `diagnostico_ntk/` | Traza NTK de física frente a datos | `ntk_analysis_nb02.py` |
| `ablacion_4capas/` | 4 capas frente a 5 en 2D | `ablation_4layers_nb02.py` |
| `figures/` | Solución, métricas y validación multidireccional | notebook `02` y su guion |

## `nb02b/` — Reducción modal

| Ruta | Qué contiene | Lo genera |
|---|---|---|
| `modal_bridge/` | `ModalSiren` con 1, 5 y 41 modos | `nb02b_modal_analytic_validation.py` |
| `modal_basis/` | Bases modales seno, coseno y general | `nb02b_modal_fundamental_basis_validation.py` |
| `bien_vs_mal_puesto/` | Dirichlet frente a Cauchy con los mismos datos | `nb02b_bvp_vs_cauchy.py` |
| `figures/` | Las ocho figuras, con prefijo `nb02b_` | los tres guiones |

Los pesos entrenados (`.pt`) y los campos grandes (`.npz`) no están en el
repositorio por tamaño; se regeneran al ejecutar los notebooks y los guiones.
