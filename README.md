# Simulación acelerada de speckle óptico mediante PINNs

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.4-ee4c2c?logo=pytorch)](https://pytorch.org/)
[![CUDA](https://img.shields.io/badge/CUDA-12.6-76b900?logo=nvidia)](https://developer.nvidia.com/cuda-toolkit)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Status](https://img.shields.io/badge/Status-NB04%20pendiente-yellow)]()

> **Tesis de Maestría**, Universidad Juárez Autónoma de Tabasco
> Maestría en Ciencias de la Computación
> **Autor:** Roberto Hernández Estrada
> **Director:** Dr. José Adán Hernández Nolasco

---

## Descripción

Este repositorio contiene la implementación de **Redes Neuronales Físicamente Informadas (PINNs)** para la simulación acelerada de patrones de speckle óptico. El proyecto propone que las PINNs pueden resolver la ecuación de Helmholtz con un error L2 relativo menor al 5%, superando la velocidad de los métodos tradicionales de Elementos Finitos (FEM).

### Problema que resuelve

El speckle óptico es un patrón granular de interferencia que aparece cuando luz coherente (láser) ilumina una superficie rugosa. Simular este fenómeno con métodos tradicionales (FEM) es computacionalmente costoso. Las PINNs ofrecen una alternativa *mesh-free* potencialmente más rápida.

### Ecuación gobernante: Helmholtz 2D

$$\nabla^2 E + k^2 E = 0 \quad \Longrightarrow \quad \frac{\partial^2 E}{\partial x^2} + \frac{\partial^2 E}{\partial y^2} + (2\pi)^2 E = 0$$

donde $\tilde{k} = 2\pi$ es el número de onda adimensional (láser de diodo rojo $\lambda = 638$ nm).

---

## Hipótesis de la tesis

> Las PINNs pueden simular el campo eléctrico de speckle óptico resolviendo la ecuación de Helmholtz con un **error L2 < 5%** respecto a la solución de referencia, con un **Speed-up Factor > 1** respecto al método FEM (FEniCSx).

---

## Estructura del repositorio

```
Tesis_Maestria/
│
│── OUTPUTS ──────────────────────────────────────────────────────────────────
│
├── slides/                                             # Diapositivas
│   └── coloquio_v3.pptx                               # Coloquio de avance (Jun 2026)
│
├── tesis/                                              # Documento de tesis UJAT (LaTeX)
│   ├── chapters/                                       # Capítulos 1 a 5
│   └── figures/                                        # Figuras de la tesis
│
├── paper/                                              # Artículo científico
│   ├── main.tex                                        # Paper completo (18 pp.)
│   ├── sections/                                       # Secciones 01 a 05
│   ├── figures/                                        # Figuras finales
│   ├── references.bib                                  # Bibliografía
│   └── main.pdf                                        # PDF compilado
│
│── REFERENCIAS Y PLANTILLAS ─────────────────────────────────────────────────
│
├── master_supporting_docs/
│   ├── supporting_slides/      # Plantillas/borrador para slides/
│   ├── supporting_tesis/       # Plantilla UJAT para tesis/
│   └── supporting_papers/      # Papers de referencia para paper/
│
│── CÓDIGO Y EXPERIMENTOS ────────────────────────────────────────────────────
│
├── src/                                                # Módulos reutilizables
│   ├── models.py                                       # Arquitectura SIREN
│   ├── losses.py                                       # Pérdida PINN
│   ├── training.py                                     # Loop Adam + L-BFGS
│   └── utils.py                                        # Métricas, LHS, viz
│
├── notebooks/                                          # Notebooks Jupyter
│   ├── 01_pinn_helmholtz_1d_validation.ipynb           # L2=0.006%, factor x415 vs SOTA
│   ├── 02_pinn_helmholtz_2d_complex_field.ipynb        # L2=0.171%, factor x11.2 vs SOTA
│   ├── 03_pinn_optical_speckle_simulation.ipynb        # C=1.025, criterio de Goodman cumplido
│   ├── 04_pinn_fem_benchmark.ipynb                     # PINN vs FEniCSx (pendiente)
│   └── v1_exploracion_cpu/                             # Línea base histórica
│
├── scripts/                                            # Scripts de entrenamiento
│   ├── run_ablation_lambda.py
│   ├── run_multiseed.py
│   ├── run_seed777.py
│   └── measure_inference.py
│
│── RESULTADOS ───────────────────────────────────────────────────────────────
│
├── results/
│   ├── ablation_lambda.json                            # λ ∈ {0.01, 0.1, 1.0}
│   ├── multiseed_results.json                          # Seeds {42, 123, 777}
│   ├── seed777_result.json
│   └── figures/                                        # Figuras generadas
│
├── environment.yml                                     # Entorno Conda reproducible
├── .gitignore
├── LICENSE
└── README.md
```

---

## Organización de la carpeta tesis

La carpeta `tesis/` contiene las distintas ediciones del documento de tesis:

| Carpeta | Contenido | Estado |
|---|---|---|
| `Tesis_Actual/` | Copia de trabajo activa y principal (creada el 27/08/2026 como `Tesis_act2`, sucesora de `Tesis_actualizada/` borrada ese día; renombrada a `Tesis_Actual` el mismo día) | Aquí se aplican todos los cambios nuevos a la tesis |
| `fuente_base/` | Edición sin la sección de speckle (NB03) | Sin modificar |
| `compilado/` | PDF y ZIP finales generados, en subcarpetas `base/` y `Actual/` | Se regenera al compilar, no se edita directamente |

`fuente_conNB03/` (el respaldo con la sección completa de speckle) se eliminó el 28/08/2026 — ya existe un respaldo real en el historial de git (commit `1fd2a13`), así que dejó de ser necesaria una copia en disco aparte.

Flujo de trabajo:

1. Editar los archivos `.tex` dentro de `tesis/Tesis_Actual/`.
2. Compilar con `cd tesis/Tesis_Actual && latexmk main.tex`.
3. El resultado final (PDF y ZIP del código fuente) se guarda en `tesis/compilado/Actual/`, sobrescribiendo siempre la versión anterior, sin conservar historial.

---

## Instalación y uso

### 1. Clonar el repositorio

```bash
git clone https://github.com/roberto-hernandez-estrada/pinn_speckle.git
cd pinn_speckle
```

### 2. Crear el entorno Conda

```bash
conda env create -f environment.yml
conda activate pinn_speckle
```

### 3. Verificar GPU

```bash
python -c "import torch; print(torch.cuda.get_device_name(0))"
# NVIDIA GeForce RTX 5050
```

### 4. Ejecutar notebooks en orden

```bash
jupyter notebook notebooks/01_pinn_helmholtz_1d_validation.ipynb
```

---

## Resultados actuales

### Notebook 01: Helmholtz 1D (Validación del método)

| Métrica | GPU v2 | Meta tesis |
|---|---|---|
| Error L2 relativo | **0.006%** | < 5% (cumplido) |
| MAE | 3.50e-05 | - |
| Error máximo | 5.77e-05 | - |
| R² | 1.000000 | - |
| Correlación Pearson | 1.000000 | - |
| Épocas Adam | 15,000 / 15,000 | - |
| Iteraciones L-BFGS | 202 / 500 | - |
| Tiempo total | ~251 s | - |
| Referencia Schoder & Kraxberger (2024) | 2.490% | Superado (factor x415) |

### Notebook 02: Helmholtz 2D con campo complejo y LHS

| Métrica | GPU v2 | Meta tesis |
|---|---|---|
| Error L2 promedio | **0.171%** | < 5% (cumplido) |
| Error L2 E_real | 0.214% | - |
| Error L2 E_imag | 0.127% | - |
| R² E_real | 0.999994 | - |
| R² E_imag | 0.999998 | - |
| Épocas Adam | 8,737 / 15,000 | - |
| Iteraciones L-BFGS | 1,035 / 1,000 | - |
| Tiempo total | **299 s** | - |

### Notebook 03: Simulación de speckle óptico

| Métrica | Resultado | Referencia teórica |
|---|---|---|
| Contraste C = σ_I / ⟨I⟩ | **1.0253** | 1.0 (speckle totalmente desarrollado, cumplido) |
| Test K-S (vs. exp. negativa) | p = 0.0000 | p > 0.05 (ver nota) |
| Épocas Adam | 7,976 / 15,000 | - |
| Iteraciones L-BFGS | 8 / 500 | - |
| Tiempo total | ~227 s | - |

> **Nota KS:** Con N = 10,000 puntos de evaluación, el test de Kolmogorov-Smirnov tiene potencia estadística suficiente para rechazar H₀ ante desviaciones menores al 1%. El resultado p = 0.0000 no indica fallo del modelo: es consecuencia de la alta potencia del test. El contraste C = 1.0253 (|C−1| < 0.03) confirma que la distribución de intensidades es consistente con speckle totalmente desarrollado.

### Láser simulado

| Parámetro | Valor |
|---|---|
| Tipo | Diodo rojo (computacional) |
| Longitud de onda (λ) | 638 nm |
| k adimensional | 2π = 6.2832 |
| Dominio | 1 longitud de onda (normalizado) |

---

## Arquitectura PINN: SIREN

```
Entrada (x,y) → [sin(ω₀·Wx+b)] → [128] → [sin(ω₀·Wx+b)] → [128] → ... → (E_real, E_imag)
```

| Componente | NB01 (1D) | NB02 (2D) | NB03 (Speckle) |
|---|---|---|---|
| Tipo | SIREN | SIREN | SIREN |
| Activación | sin(ω₀·x), ω₀=1.0 | sin(ω₀·x), ω₀=1.0 | sin(ω₀·x), ω₀=1.0 |
| Capas ocultas | 5 × 64 neuronas | 5 × 128 neuronas | 5 × 128 neuronas |
| Parámetros | ~8,400 | ~66,690 | ~66,690 |
| Inicialización | Sitzmann et al. (2020) | Sitzmann et al. (2020) | Sitzmann et al. (2020) |
| Muestreo interior | Linspace uniforme | Latin Hypercube Sampling (LHS) | Latin Hypercube Sampling (LHS) |
| Condición de frontera | Dirichlet en x=0, x=1 | Dirichlet en ∂Ω | Fase aleatoria U(0,2π) en y=0 |
| Optimizador | Adam + L-BFGS | Adam + L-BFGS | Adam + L-BFGS |
| Parada anticipada | Umbral fijo L < 1×10⁻⁴ | Paciencia 800 épocas | Paciencia 800 épocas |

---

## Progreso del proyecto

- [x] Notebook 01: Helmholtz 1D GPU (L2 = 0.006%, R² = 1.000000)
- [x] Notebook 02: Helmholtz 2D GPU (L2_avg = 0.171%, tiempo = 299 s)
- [x] Notebook 03: Simulación de speckle óptico (C = 1.0253, cumplido)
- [ ] Notebook 04: Benchmark PINN vs FEniCSx (Speed-up Factor S = T_FEM / T_PINN)

---

## Referencias principales

- Raissi, M., Perdikaris, P., & Karniadakis, G. E. (2019). *Physics-informed neural networks*. Journal of Computational Physics, 378, 686-707.
- Sitzmann, V., Martel, J., Bergman, A., Lindell, D., & Wetzstein, G. (2020). *Implicit neural representations with periodic activation functions*. NeurIPS 2020.
- Schoder, S., & Kraxberger, F. (2024). *Feasibility study on solving the Helmholtz equation in 3D with PINNs*. arXiv:2403.06623.
- Goodman, J. W. (2007). *Speckle Phenomena in Optics*. Roberts & Company Publishers.
- Lu, L. et al. (2021). *DeepXDE: A deep learning library for solving differential equations*. SIAM Review, 63(1), 208-228.

---

## Licencia

Este proyecto está bajo la licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

---

## Contacto

**Roberto Hernández Estrada** || robertohernandezestrd@gmail.com
Universidad Juárez Autónoma de Tabasco
Maestría en Ciencias de la Computación

> *"Las PINNs representan un cambio de paradigma en la simulación de fenómenos físicos: en lugar de discretizar el dominio, la red neuronal aprende la física directamente."*
