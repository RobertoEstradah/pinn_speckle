# Exploración Inicial — Versiones v1 (Línea base)

> **Estado:** Archivado — superado por las versiones GPU v2.  
> **Propósito de este directorio:** conservar evidencia del proceso de desarrollo para futuras publicaciones y reproducibilidad histórica.

---

## Notebooks contenidos

| Notebook | Descripción | Resultado |
|---|---|---|
| `01_pinn_helmholtz_1d_v1_baseline.ipynb` | Helmholtz 1D — primera implementación SIREN | L2 ≈ 0.009%, tiempo ≈ 189 s |
| `02_pinn_helmholtz_2d_v1_baseline.ipynb` | Helmholtz 2D con campo complejo y LHS — primera implementación | L2_avg ≈ 0.222%, tiempo ≈ 1,278 s |

---

## Por qué se dejaron de usar

### 1. Rendimiento computacional

La motivación principal para migrar a la arquitectura v2 fue el tiempo de entrenamiento.

| Métrica | v1 (línea base) | v2 GPU (definitivo) | Mejora |
|---|---|---|---|
| Helmholtz 1D — tiempo | ~189 s | **251 s** (más épocas) | — |
| Helmholtz 2D — tiempo | **~1,278 s** | **299 s** | **×4.3 más rápido** |
| Helmholtz 2D — L2_avg | 0.222% | 0.171% | −23% error |
| Helmholtz 2D — Adam | 11,258 épocas | 8,737 épocas | −22% iteraciones |

> **Nota 1D:** la v2 tarda más porque maximiza las épocas Adam hasta convergencia; la v1 terminó antes por early stopping más agresivo. La mejora real en L2 fue de 0.009% → 0.006%.

### 2. Convergencia y calidad

La versión v2 GPU introduce:

- **Scheduler de tasa de aprendizaje** (`CosineAnnealingLR`) — mejora la exploración del espacio de parámetros en épocas tardías.
- **Parámetro de peso de física λ_phys = 0.1** para Helmholtz 2D — balance óptimo entre pérdida de frontera y pérdida de residuo PDE.
- **Inicialización SIREN refinada** — primera capa U(−1/n_in, 1/n_in); capas ocultas U(−√6/n·ω₀, √6/n·ω₀) conforme a Sitzmann et al. (2020), aplicado de forma más consistente.
- **GPU acceleration** — cuDNN optimizado para operaciones de autodiferenciación (torch.autograd) usadas en el residuo PDE.

### 3. Decisión de diseño

Los notebooks v1 sirvieron para:
1. Validar que la arquitectura SIREN es capaz de resolver la ecuación de Helmholtz.
2. Detectar hiperparámetros sensibles (ω₀, capas, neuronas por capa).
3. Establecer una línea base de error L2 contra la cual medir la mejora de la v2.

Una vez confirmado que la v2 GPU supera consistentemente a la v1 en velocidad y precisión, se tomó la decisión de usar **exclusivamente la v2 como resultado oficial de la tesis**.

---

## Reproducción

Estos notebooks se ejecutan con el mismo entorno conda que el proyecto principal:

```bash
conda activate pinn_speckle
jupyter notebook v1_exploracion_cpu/01_pinn_helmholtz_1d_v1_baseline.ipynb
```

> Si no hay GPU disponible, estos notebooks detectan automáticamente el dispositivo y corren en CPU — esa es precisamente su utilidad como referencia histórica.

---

## Referencias

- Sitzmann, V., Martel, J., Bergman, A., Lindell, D., & Wetzstein, G. (2020). *Implicit neural representations with periodic activation functions*. NeurIPS 2020.
- Schoder, S., & Kraxberger, F. (2024). *Feasibility study on solving the Helmholtz equation in 3D with PINNs*. arXiv:2403.06623.
