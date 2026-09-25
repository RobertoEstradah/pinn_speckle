# `results/`

Salidas de los tres experimentos publicados. Cada `.json` lo escribe un guion
de `scripts/experiments/` o una celda de su notebook.

| Carpeta o archivo | Qué contiene | Lo genera |
|---|---|---|
| `nb01_basis_validation/` | Resumen de la validación 1D | notebook `01` |
| `nb02_multidirectional/` | Onda plana 2D en cuatro direcciones | `nb02_multidirectional_validation.py` |
| `nb02b_modal_basis/` | Bases modales seno, coseno y general | `nb02b_modal_fundamental_basis_validation.py` |
| `nb02b_modal_bridge/` | `ModalSiren` con 1, 5 y 41 modos, en $0\le\tilde z\le 1$ | `nb02b_modal_analytic_validation.py` |
| `ablation_lambda.json` | Peso de la física en 2D: 0.01, 0.1 y 1.0 | `run_ablation_lambda.py` |
| `multiseed_results.json`, `seed777_result.json` | Dispersión frente a la semilla | `run_multiseed.py`, `run_seed777.py` |
| `ntk_spectral_bias_diagnostics/` | Barrido de ω₀ y traza NTK de NB02 | `omega0_spectral_sweep.py`, `ntk_analysis_nb02.py` |
| `architecture_ablation_4layers/` | 4 capas frente a 5 en 1D y 2D | `ablation_4layers_nb01.py`, `ablation_4layers_nb02.py` |
| `figures/` | Figuras de los notebooks | notebooks `01`, `02` y guiones |

Los pesos entrenados (`.pt`) y los campos grandes (`.npz` de NB02B) no están
en el repositorio por tamaño; se regeneran al ejecutar los notebooks.
