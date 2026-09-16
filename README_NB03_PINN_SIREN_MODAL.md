# Reproducción de NB03: PINN-SIREN modal para speckle 2D

Actualización de robustez: una pantalla reservada (31415) con semilla neuronal
73 no alcanzó el umbral con la SIREN fija (L2 completo 6.7397 %). Una variante
con frecuencia sinusoidal global entrenable, respaldada por Jagtap, Kawaguchi
y Karniadakis (2020), redujo el L2 propagante a 0.7548 %, el máximo en 201
planos a 0.8854 % y el L2 completo a 2.1018 %. Una confirmación predefinida
aprobó el criterio de L2 completo en 2 de 3 semillas neuronales, pero una
inicialización falló de forma catastrófica; por ello aún no sustituye el
protocolo principal. Véase `results/nb03_holdout/README.md`.

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

Estado posterior: la configuración oficial con `omega_0 = 1` se extendió de
manera controlada hasta `z = 2 lambda` en las mismas cinco pantallas. El L2
completo final medio fue 0.993 %, el peor máximo propagante en 201 planos fue
1.165 % y las cinco pantallas cumplieron todos los criterios. Una prueba
reservada adicional en `z = 1 lambda`, con pantalla 31415 y semilla neuronal
73, terminó en 6.740 % con la configuración fija y no fue aceptada. Por ello
existe evidencia sólida para las cinco pantallas conocidas entre 1 y 2
longitudes de onda, pero aún no de generalización a cualquier pantalla o
inicialización. Véanse `results/nb03_distance_pilot/z2_omega1_five_120s/` y
`results/nb03_holdout/README.md`.

## Resultado oficial que debe reproducirse

Se entrenó la misma arquitectura con cinco pantallas físicas distintas y la
semilla de la red fija en 42.

| Semilla de pantalla | L2 complejo en z=1 | Coherencia | C referencia | C PINN | Error absoluto de C | Residuo RMSE |
|---:|---:|---:|---:|---:|---:|---:|
| 42 | 3.82 % | 0.9993 | 0.9063 | 0.9012 | 0.0051 | 0.00232 |
| 123 | 2.40 % | 0.9997 | 0.8827 | 0.8821 | 0.0006 | 0.00224 |
| 321 | 3.57 % | 0.9994 | 0.9200 | 0.9231 | 0.0030 | 0.00240 |
| 777 | 2.95 % | 0.9996 | 1.2246 | 1.2403 | 0.0157 | 0.00246 |
| 2026 | 3.06 % | 0.9995 | 0.7812 | 0.7841 | 0.0029 | 0.00229 |

Resumen: L2 medio de **3.16 %**, desviación poblacional de **0.50 puntos
porcentuales**, peor resultado final de **3.82 %** y cinco de cinco pantallas
aceptadas por fidelidad de campo y contraste.

## Puente analítico NB02B hasta 2 lambda

La misma arquitectura modal de NB03, con `omega` de primera capa igual a 1,
se contrastó también contra una solución analítica multimodal sobre
`z/lambda in [0,2]`. Esta prueba no utiliza speckle aleatorio y, por tanto, no
sustituye la validación de NB03; verifica de manera controlada la arquitectura,
la condición de Cauchy dura y el residuo de Helmholtz antes de aplicarlos al
campo aleatorio.

| Modos complejos | L2 global | L2 en z=2 | Coherencia | Residuo normalizado |
|---:|---:|---:|---:|---:|
| 1 | 0.210 % | 0.150 % | 1.000000 | 0.00768 |
| 5 | 0.334 % | 0.180 % | 1.000000 | 0.00663 |
| 41 | 0.195 % | 0.184 % | 0.999999 | 0.00413 |

Los tres casos satisfacen el umbral L2 menor que 5 %. Los artefactos se
encuentran en `results/nb02b_modal_bridge/z_2lambda/` y se reproducen desde
`notebooks/02b_validacion_puente_arquitectura_modal_nb03.ipynb`.

## NB03B: speckle aleatorio hasta 2 lambda

Después del puente analítico NB02B, la PINN-SIREN modal se entrenó sin
etiquetas interiores para propagar cinco campos aleatorios conocidos desde
`z=0` hasta `z=2 lambda`. La referencia del espectro angular se consultó solo
después del entrenamiento. Se mantuvieron `omega_0=1`, 41 modos propagantes,
la condición de Cauchy dura y la selección del modelo mediante el residuo de
Helmholtz.

| Pantalla | L2 completo final | L2 propagante final | Máximo propagante en z | Coherencia | Error de C | Residuo normalizado |
|---:|---:|---:|---:|---:|---:|---:|
| 42 | 1.0377 % | 0.9321 % | 1.1648 % | 0.999951 | 0.002666 | 0.005417 |
| 123 | 0.9409 % | 0.8944 % | 1.0810 % | 0.999961 | 0.000582 | 0.005385 |
| 321 | 1.0057 % | 0.8931 % | 1.0780 % | 0.999951 | 0.001406 | 0.004924 |
| 777 | 0.8637 % | 0.7940 % | 0.9986 % | 0.999965 | 0.000720 | 0.004501 |
| 2026 | 1.1175 % | 1.0542 % | 1.0542 % | 0.999960 | 0.000446 | 0.004867 |
| **Resumen** | **media 0.9931 %** | **media 0.9136 %** | **peor 1.1648 %** | **media 0.999958** | **media 0.001164** | **media 0.005019** |

Las cinco pantallas fueron aceptadas. El notebook reproducible es
`notebooks/03b_validacion_speckle_2d_z2lambda.ipynb`; el resumen verificable
está en
`results/nb03_distance_pilot/z2_omega1_five_120s/validation_summary.json`.

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
| `omega` primera capa | 1 |
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
$env:NB03_MODAL_FIRST_OMEGA = "1"
$env:NB03_MODAL_HIDDEN_OMEGA = "1"
$env:NB03_MODAL_HIDDEN_DIM = "128"
$env:NB03_MODAL_NUM_LAYERS = "4"
$env:NB03_MODAL_GRAD_CLIP = "1"
$env:NB03_MODAL_VALIDATION_N_Z = "1001"
$env:NB03_MODAL_RESUME_MODEL = ""
$env:NB03_MODAL_OUTPUT_SUFFIX = "_z1_screen42_omega1"
python -u scripts/experiments/nb03_modal_pinn_siren.py
```

### 3. Afinación

```powershell
$env:NB03_MODAL_EPOCHS = "3000"
$env:NB03_MODAL_LR = "0.00005"
$env:NB03_MODAL_RESUME_MODEL = "results/models/nb03_modal_pinn_siren_z1_screen42_omega1.pt"
$env:NB03_MODAL_OUTPUT_SUFFIX = "_z1_screen42_omega1_finetune"
python -u scripts/experiments/nb03_modal_pinn_siren.py
```

### 4. Consolidar las cinco pantallas

```powershell
$env:NB03_SUMMARY_VARIANT = "_omega1"
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
| `notebooks/03_simulacion_speckle_2d_pinn_siren_modal.ipynb` | Presentación interactiva de NB03 |
| `results/nb03_modal_multiseed_z1_omega1_summary.json` | Resultados consolidados oficiales |
| `results/nb03_modal_multiseed_z1_omega1_l2_curves.npz` | Curvas L2 para las cinco pantallas |
| `results/figures/nb03_modal_multiseed_z1_omega1_l2.png` | Figura comparativa |
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

- El resultado está validado para cinco pantallas conocidas tanto en
  `z=1 lambda` como en `z=2 lambda`.
- Cada pantalla requiere entrenamiento; todavía no es un operador neuronal
  capaz de generalizar sin reentrenamiento.
- Cuatro pantallas conservaron L2 menor que 5 % en todo el intervalo. La
  pantalla 123 alcanzó temporalmente 5.27 % en un plano interior, aunque
  terminó con 2.91 % en `z=1 lambda`.
- La formulación aprovecha un medio homogéneo y periodicidad transversal.
- El espectro angular y la PINN modal comparten una base Fourier compatible;
  la comparación futura con FEM aportará una validación numérica adicional.
- En `z=2 lambda`, el L2 completo final medio fue 0.993 % y el peor error
  propagante observado en 201 planos fue 1.165 %, ambos muy por debajo del
  umbral de 5 %.
- No se ha demostrado generalización sin reentrenamiento a pantallas nuevas ni
  validez universal a 5, 10 o 20 longitudes de onda.
- Una pantalla y semilla neuronal reservadas no alcanzaron el umbral de 5 %;
  la robustez entre inicializaciones permanece abierta.
- No se ha medido aún aceleración frente a FEM.
