#  Simulación acelerada de speckle óptico mediante PINNs

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.4+-ee4c2c?logo=pytorch)](https://pytorch.org/)
[![CUDA](https://img.shields.io/badge/CUDA-12.6-76b900?logo=nvidia)](https://developer.nvidia.com/cuda-toolkit)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Status](https://img.shields.io/badge/Status-En%20desarrollo-yellow)]()

> **Tesis de Maestría** — Universidad Juárez Autónoma de Tabasco  
> Maestría en Ciencias de la Computación  
> **Autor:** Roberto Hernández Estrada  
> **Director:** Dr. José Adán Hernández Nolasco

---

##  Descripción

Este repositorio contiene la implementación de **Redes Neuronales Físicamente Informadas (PINNs)** para la simulación acelerada de patrones de speckle óptico. El proyecto propone que las PINNs pueden resolver la ecuación de Helmholtz con un error L2 relativo menor al 5%, superando la velocidad de los métodos tradicionales de Elementos Finitos (FEM).

### Problema que resuelve

El speckle óptico es un patrón granular de interferencia que aparece cuando luz coherente (láser) ilumina una superficie rugosa. Simular este fenómeno con métodos tradicionales (FEM) es computacionalmente costoso. Las PINNs ofrecen una alternativa *mesh-free* potencialmente más rápida.

### Ecuación gobernante — Helmholtz 2D

$$\nabla^2 E + k^2 E = 0 \quad \Longrightarrow \quad \frac{\partial^2 E}{\partial x^2} + \frac{\partial^2 E}{\partial y^2} + (2\pi)^2 E = 0$$

donde $\tilde{k} = 2\pi$ es el número de onda adimensional (láser de diodo rojo $\lambda = 638$ nm).

---

##  Hipótesis de la tesis

> Las PINNs pueden simular el campo eléctrico de speckle óptico resolviendo la ecuación de Helmholtz con un **error L2 < 5%** respecto a la solución de referencia, con un **Speed-up Factor > 1** respecto al método FEM (FEniCSx).

---

##  Estructura del repositorio

```
pinn_speckle/
│
├── notebooks/                              # Notebooks de Jupyter
│   ├── 01_helmholtz_1D_tesis.ipynb         # ✅ Helmholtz 1D — CPU (L2 = 0.009%)
│   ├── 01_helmholtz_1D_tesis_v2_gpu.ipynb  # ✅ Helmholtz 1D — GPU (L2 = 0.006%)
│   ├── 02_helmholtz_2D_tesis.ipynb         # ✅ Helmholtz 2D — CPU (L2 = 0.222%)
│   ├── 02_helmholtz_2D_tesis_v2_gpu.ipynb  # ✅ Helmholtz 2D — GPU (L2 = 0.188%)
│   ├── 03_speckle.ipynb                    # 🔜 Simulación de speckle I=|E|²
│   └── 04_benchmark.ipynb                  # 🔜 PINN vs FEniCSx (Speed-up Factor)
│
├── src/                              # Módulos reutilizables
│   ├── models.py                     # Arquitecturas de red (SIREN)
│   ├── losses.py                     # Funciones de pérdida PINN
│   ├── training.py                   # Loop de entrenamiento (Adam + L-BFGS)
│   └── utils.py                      # Métricas, visualización, LHS
│
├── results/                          # Resultados generados
│   ├── figures/                      # Gráficas y visualizaciones
│   └── metrics/                      # Tablas de error L2 y tiempos
│
├── docs/                             # Documentación del proyecto
│   └── reporte_avance.docx           # Reporte para director de tesis
│
├── data/
│   └── reference/                    # Soluciones de referencia FEM
│
├── environment.yml                   # Entorno Conda reproducible
├── .gitignore                        # Archivos ignorados por Git
├── LICENSE                           # Licencia MIT
└── README.md                         # Este archivo
```

---

##  Instalación y uso

### 1. Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/pinn_speckle.git
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
jupyter notebook notebooks/01_helmholtz_1D_tesis.ipynb
```

---

##  Resultados actuales

### Notebook 01 — Helmholtz 1D (Validación del método)

| Métrica | CPU | GPU | Meta tesis |
|---|---|---|---|
| Error L2 relativo | **0.009%** | **0.006%** | < 5% ✅ |
| MAE | 6.02e-05 | 3.50e-05 | — |
| Error máximo | 9.81e-05 | 5.77e-05 | — |
| R² | 1.000000 | 1.000000 | — |
| Correlación Pearson | 1.000000 | 1.000000 | — |
| Épocas Adam (early stop) | 15,000 / 15,000 | 15,000 / 15,000 | — |
| Referencia Schoder & Kraxberger (2024) | 2.490% | 2.490% | Superado ✅ |

### Notebook 02 — Helmholtz 2D con campo complejo y LHS

| Métrica | CPU | GPU | Meta tesis |
|---|---|---|---|
| Error L2 promedio | **0.222%** | **0.188%** | < 5% ✅ |
| Error L2 E_real | 0.302% | 0.234% | — |
| Error L2 E_imag | 0.143% | 0.141% | — |
| MAE E_real | 1.79e-03 | 1.39e-03 | — |
| MAE E_imag | 8.79e-04 | 8.77e-04 | — |
| R² E_real | 0.999991 | 0.999994 | — |
| R² E_imag | 0.999998 | 0.999998 | — |
| Épocas Adam (early stop) | 11,258 / 15,000 | 10,849 / 15,000 | — |
| Tiempo total | ~1,278 s | **353 s** | — |

### Láser simulado

| Parámetro | Valor |
|---|---|
| Tipo | Diodo rojo (computacional) |
| Longitud de onda (λ) | 638 nm |
| k adimensional | 2π = 6.2832 |
| Dominio Fase 1 | 1 longitud de onda = 0.638 μm |

---

##  Arquitectura PINN — SIREN

```
Entrada (x,y) → [sin(ω₀·x)] → [128] → [sin(ω₀·x)] → [128] → ... → (E_real, E_imag)
```

| Componente | NB01 (1D) | NB02 (2D) |
|---|---|---|
| Tipo | SIREN | SIREN |
| Activación | sin(ω₀·x), ω₀=1.0 | sin(ω₀·x), ω₀=1.0 |
| Capas ocultas | 5 × 64 neuronas | 5 × 128 neuronas |
| Parámetros | ~8,400 | ~66,690 |
| Inicialización | Sitzmann et al. (2020) | Sitzmann et al. (2020) |
| Muestreo | Linspace uniforme | Latin Hypercube Sampling (LHS) |
| Optimizador | Adam + L-BFGS | Adam + L-BFGS |
| Early stopping | Paciencia 500 épocas | Paciencia 800 épocas |

---

##  Progreso del proyecto

- [x] Notebook 01 — Helmholtz 1D CPU (L2 = 0.009%)
- [x] Notebook 01 — Helmholtz 1D GPU (L2 = 0.006%)
- [x] Notebook 02 — Helmholtz 2D CPU (L2 = 0.222%)
- [x] Notebook 02 — Helmholtz 2D GPU (L2 = 0.188%)
- [ ] Notebook 03 — Simulación de speckle óptico
- [ ] Notebook 04 — Benchmark PINN vs FEniCSx

---

##  Referencias principales

- Raissi, M., Perdikaris, P., & Karniadakis, G. E. (2019). *Physics-informed neural networks*. Journal of Computational Physics, 378, 686–707.
- Sitzmann, V., Martel, J., Bergman, A., Lindell, D., & Wetzstein, G. (2020). *Implicit neural representations with periodic activation functions*. NeurIPS 2020.
- Schoder, S., & Kraxberger, F. (2024). *Feasibility study on solving the Helmholtz equation in 3D with PINNs*. arXiv:2403.06623.
- Goodman, J. W. (2007). *Speckle Phenomena in Optics*. Roberts & Company Publishers.
- Lu, L. et al. (2021). *DeepXDE: A deep learning library for solving differential equations*. SIAM Review, 63(1), 208–228.

---

##  Licencia

Este proyecto está bajo la licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

---

##  Contacto

**Roberto Hernández Estrada** || robertohernandezestrd@gmail.com  
Universidad Juárez Autónoma de Tabasco  
Maestría en Ciencias de la Computación

> *"Las PINNs representan un cambio de paradigma en la simulación de fenómenos físicos: en lugar de discretizar el dominio, la red neuronal aprende la física directamente."*
