# Reproducción de NB03: PINN-SIREN modal para speckle 2D

Actualización: se ejecutó una comparación adicional con selección de pesos
corregida y Adam/L-BFGS en las pantallas 42 y 123. L-BFGS float32 redujo el
error propagante final a 0.5145 % y 0.3740 %; los errores frente al campo
completo fueron 3.8529 % y 2.4300 %. Véase el
[protocolo y resultados de afinación](results/nb03_refinement/pilot1/README.md).
Esta mejora es un piloto de dos pantallas, todavía no una nueva validación
de cinco. Las instrucciones siguientes conservan el protocolo histórico.

Precisión sobre las referencias: la tabla final histórica compara contra
el campo completo (incluye evanescentes), pero las curvas históricas en z
comparan contra su proyección propagante. La condición de Cauchy dura es la
del campo proyectado. Ambos errores deben distinguirse; el 5.27 % interior
no es el máximo frente a la pantalla completa.

Este documento reproduce el modelo de NB03 que obtuvo los mejores resultados
en la propagación de speckle óptico hasta `z = 1 lambda`. El campo final sigue
expresado en coordenadas cartesianas `(x,z)`, pero la PINN utiliza internamente
una representación espectral-modal.

## Resultado que debe reproducirse

Se entrenó la misma arquitectura con cinco pantallas físicas distintas y la
semilla de la red fija en 42.

| Semilla de pantalla | L2 complejo en z=1 | Coherencia | C referencia | C PINN | Error absoluto de C | Residuo RMSE |
|---:|---:|---:|---:|---:|---:|---:|
| 42 | 4.12 % | 0.9992 | 0.9063 | 0.9019 | 0.0044 | 0.0387 |
| 123 | 2.91 % | 0.9996 | 0.8827 | 0.8841 | 0.0014 | 0.0370 |
| 321 | 3.89 % | 0.9993 | 0.9200 | 0.9211 | 0.0011 | 0.0363 |
| 777 | 3.25 % | 0.9995 | 1.2246 | 1.2391 | 0.0144 | 0.0357 |
| 2026 | 3.54 % | 0.9995 | 0.7812 | 0.7822 | 0.0010 | 0.0363 |

Resumen: L2 medio de **3.54 %**, desviación poblacional de **0.43 puntos
porcentuales**, peor resultado final de **4.12 %** y cinco de cinco pantallas
aceptadas por fidelidad de campo y contraste.

## Formulación física

El campo complejo se reconstruye mediante 41 modos propagantes:

```text
u(x,z) = sum_m a_m(z) exp(i kx_m x)
```

Al sustituir esta representación en Helmholtz 2D, cada coeficiente satisface:

```text
a_m''(z) + (k^2-kx_m^2) a_m(z) = 0
```

La condición de Cauchy es dura:

```text
a_m(z) = a_m(0) + z a_m'(0) + z^2 N_theta(z)
```

Por construcción, el campo y su derivada longitudinal se cumplen exactamente
en `z=0`. No se usan etiquetas del espectro angular dentro del dominio; esa
solución se consulta después del entrenamiento para calcular las métricas.

## Cambio que permitió alcanzar L2 menor que 5 %

Cada modo tiene una amplitud física diferente. Una salida neuronal con la
misma escala para todos los modos introducía energía artificial en los modos
débiles. La versión aceptada aplica:

```text
escala_m = k^2 max(|a_m(0)|, |a_m'(0)|/k, piso)
```

La corrección producida por la red y el residuo modal se normalizan con esa
escala. Este condicionamiento redujo el L2 desde 232.75 % en el piloto modal
sin escalado hasta 4.88 %, y la afinación lo redujo a 4.12 % en la pantalla 42.

## Parámetros congelados

### Problema óptico

| Parámetro | Valor |
|---|---:|
| Longitud transversal | `20 lambda` |
| Intervalo transversal | `x/lambda in [-10,10)` |
| Distancia | `z/lambda in [0,1]` |
| Número de muestras en x | 1024 |
| Número de planos de referencia | 101 |
| Número de modos propagantes | 41 |
| Número de onda normalizado | `k = 2*pi` |
| Correlación de la fase | `0.10 lambda` |
| Desviación de la fase | `2 rad` |
| Realizaciones para estadística de referencia | 64 |

### Arquitectura y entrenamiento

| Parámetro | Valor |
|---|---:|
| Arquitectura | SIREN modal |
| Capas ocultas | 4 |
| Neuronas por capa | 128 |
| Salidas reales | 82: parte real e imaginaria de 41 modos |
| `omega` primera capa | 30 |
| `omega` capas ocultas | 1 |
| Puntos z remuestreados por época | 256 |
| Recorte de gradiente | 1.0 |
| Entrenamiento inicial | 5000 épocas, Adam, `lr=2e-4` |
| Afinación | 3000 épocas, Adam, `lr=5e-5` |
| Agenda de aprendizaje | Cosine annealing, mínimo 2 % del lr inicial |
| Semilla de la red | 42, fija |
| Malla independiente del residuo | 1001 puntos en z |

## Entorno

El entorno declarado por el proyecto se crea desde la raíz con:

```powershell
conda env create -f environment.yml
conda activate pinn_speckle
```

La ejecución registrada en esta validación utilizó CPU con Python 3.12.14,
PyTorch 2.14.0+cpu, NumPy 2.3.5 y Matplotlib 3.11.1. El archivo
`environment.yml` también contempla un entorno PyTorch con CUDA; pequeñas
diferencias numéricas entre CPU y GPU son posibles aun usando la misma semilla.

Compruebe el entorno activo:

```powershell
python --version
python -c "import torch, numpy, matplotlib; print(torch.__version__, numpy.__version__, matplotlib.__version__)"
```

## Reproducción automática de las cinco pantallas

Desde la raíz del proyecto:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/experiments/run_nb03_modal_multiseed.ps1
```

El script no sobrescribe entrenamientos existentes. Para ejecutar nuevamente
todo el protocolo y reemplazar los archivos con los mismos nombres:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/experiments/run_nb03_modal_multiseed.ps1 -Overwrite
```

En el CPU utilizado, las cinco secuencias de entrenamiento inicial más
afinación tardaron aproximadamente 23 minutos. Una GPU puede cambiar el tiempo
y producir diferencias menores por el carácter no determinista de algunas
operaciones.

Puede limitar la reproducción a algunas pantallas:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/experiments/run_nb03_modal_multiseed.ps1 -ScreenSeeds 42,123
```

## Reproducción manual de una pantalla

Ejemplo para la pantalla 42, ejecutado desde la raíz:

### 1. Generar la referencia independiente

```powershell
$env:NB03_REFERENCE_SEED = "42"
$env:NB03_DISTANCE_LAMBDA = "1"
$env:NB03_TARGET_Z_LAMBDA = "1"
$env:NB03_REFERENCE_N_Z = "101"
$env:NB03_REFERENCE_N_REALIZATIONS = "64"
$env:NB03_PHASE_CORRELATION_LAMBDA = "0.10"
$env:NB03_PHASE_STD_RAD = "2.0"
$env:NB03_REFERENCE_SUFFIX = "_z1_corr0.10"
python -u scripts/experiments/nb03_angular_spectrum_reference.py
```

### 2. Entrenamiento inicial

```powershell
$env:NB03_SEED = "42"
$env:NB03_MODAL_EPOCHS = "5000"
$env:NB03_MODAL_N_Z_TRAIN = "256"
$env:NB03_MODAL_LR = "0.0002"
$env:NB03_MODAL_FIRST_OMEGA = "30"
$env:NB03_MODAL_HIDDEN_OMEGA = "1"
$env:NB03_MODAL_HIDDEN_DIM = "128"
$env:NB03_MODAL_NUM_LAYERS = "4"
$env:NB03_MODAL_GRAD_CLIP = "1"
$env:NB03_MODAL_VALIDATION_N_Z = "1001"
$env:NB03_MODAL_RESUME_MODEL = ""
$env:NB03_MODAL_OUTPUT_SUFFIX = "_z1_modal_scaled1"
python -u scripts/experiments/nb03_modal_pinn_siren.py
```

### 3. Afinación

```powershell
$env:NB03_MODAL_EPOCHS = "3000"
$env:NB03_MODAL_LR = "0.00005"
$env:NB03_MODAL_RESUME_MODEL = "results/models/nb03_modal_pinn_siren_z1_modal_scaled1.pt"
$env:NB03_MODAL_OUTPUT_SUFFIX = "_z1_modal_scaled1_finetune"
python -u scripts/experiments/nb03_modal_pinn_siren.py
```

### 4. Consolidar las cinco pantallas

```powershell
python -u scripts/experiments/nb03_modal_multiseed_summary.py
```

## Criterios de validación

Para cada pantalla individual:

```text
L2 complejo < 0.05
abs(C_PINN - C_referencia) < 0.05
```

La condición histórica `abs(C_PINN-1)<0.1` se conserva como diagnóstico, pero
no debe usarse para rechazar una realización individual. En cinco pantallas,
las propias referencias presentaron contrastes entre 0.7812 y 1.2246. La
cercanía `C aproximadamente 1` corresponde a la estadística de conjunto.

## Archivos principales

| Archivo | Función |
|---|---|
| `scripts/experiments/nb03_angular_spectrum_reference.py` | Genera pantalla y referencia por espectro angular |
| `scripts/experiments/nb03_modal_pinn_siren.py` | Entrena y evalúa la PINN-SIREN modal |
| `scripts/experiments/nb03_modal_multiseed_summary.py` | Recalcula métricas agregadas y L2 a lo largo de z |
| `scripts/experiments/run_nb03_modal_multiseed.ps1` | Ejecuta el protocolo completo |
| `notebooks/03_pinn_optical_speckle_simulation.ipynb` | Presentación interactiva de NB03 |
| `results/nb03_modal_multiseed_z1_summary.json` | Resultados consolidados |
| `results/nb03_modal_multiseed_z1_l2_curves.npz` | Curvas L2 para las cinco pantallas |
| `results/figures/nb03_modal_multiseed_z1_l2.png` | Figura comparativa |
| `results/nb03_modal_z1_report.md` | Reporte técnico resumido |

Cada corrida individual produce cuatro artefactos con el mismo sufijo:

```text
results/nb03_modal_pinn_siren<SUFIJO>.json
results/nb03_modal_pinn_siren<SUFIJO>.npz
results/models/nb03_modal_pinn_siren<SUFIJO>.pt
results/figures/nb03_modal_pinn_siren<SUFIJO>.png
```

## Comprobaciones mínimas

Una reproducción correcta debe verificar:

1. Los scripts terminan sin pérdidas `NaN` o infinitas.
2. `hard_boundary_field_rmse` es cercano a cero.
3. El JSON final indica `complex_l2_below_5_percent: true`.
4. El error absoluto entre el contraste PINN y la referencia es menor que 0.05.
5. El NPZ contiene únicamente valores finitos.
6. La figura muestra concordancia de intensidad y fase.

## Alcance y limitaciones

- El resultado está validado preliminarmente para cinco pantallas y
  `z=1 lambda`.
- Cada pantalla requiere entrenamiento; todavía no es un operador neuronal
  capaz de generalizar sin reentrenamiento.
- Cuatro pantallas conservaron L2 menor que 5 % en todo el intervalo. La
  pantalla 123 alcanzó temporalmente 5.27 % en un plano interior, aunque
  terminó con 2.91 % en `z=1 lambda`.
- La formulación aprovecha un medio homogéneo y periodicidad transversal.
- El espectro angular y la PINN modal comparten una base Fourier compatible;
  la comparación futura con FEM aportará una validación numérica adicional.
- No se ha demostrado todavía propagación a 2, 5, 10 o 20 longitudes de onda.
- No se ha medido aún aceleración frente a FEM.
