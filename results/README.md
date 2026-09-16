# `results/` — qué hay aquí y qué se puede tocar

Salidas crudas de notebooks y scripts. Dos regímenes distintos conviven:

| | Peso | Está en git |
|---|---:|---|
| Métricas (`.json`), figuras seleccionadas y los `.npz` de la cadena vigente | ~24 MB | **Sí** |
| Campos crudos de los pilotos de distancia, la pantalla reservada y el refinamiento | ~615 MB | No, `.gitignore` |

Los `.pt` y los `.npz` de `nb03_distance_pilot/`, `nb03_holdout/` y
`nb03_refinement/` se conservan **en disco** como evidencia y son regenerables
con sus scripts. No entran al repositorio por tamaño.

## Antes de borrar nada aquí

Un archivo está protegido si lo abre la cadena que alimenta cifras de la tesis.
La forma de averiguarlo no es leer nombres, sino ejecutarla:

```bash
python scripts/experiments/nb03_estadistica_conjunto.py
NB03_SUMMARY_VARIANT=_omega1 python scripts/experiments/nb03_modal_multiseed_summary.py
python scripts/experiments/nb03_omega0_sweep_summary.py
python scripts/experiments/verifica_cifras_tesis.py
```

Los tres primeros regeneran los `.json` que la tesis cita; el cuarto comprueba
que las 80 cifras del texto siguen coincidiendo. Si el cuarto no termina en
`0 discrepancias`, algo que se borró hacía falta.

**Cuidado con los nombres construidos por sufijo.** Varios scripts arman la
ruta en tiempo de ejecución --`f"nb03_angular_spectrum_reference{sufijo}.npz"`--,
así que buscar el nombre literal en el código da falsos huérfanos.

## Limpieza del 2026-09-15

Se retiraron del repositorio **60 `.npz`, 77.6 MB**, que ninguna parte del
código, de los notebooks ni de la tesis abría:

| Grupo | Peso | Por qué se fue |
|---|---:|---|
| Comparaciones de la formulación colocada directa | 44.6 MB | Formulación abandonada. El diagnóstico está en `archive/nb03_speckle_pausado/hallazgos_y_diagnostico.md` y en Cap4 §`sec:nb03_diagnostico` |
| Comparaciones de la formulación por bloques | 19.2 MB | Igual: la formulación vigente es modal y no usa bloques |
| Referencias ASM con correlación 0.20–0.50 y `_verif` | 12.8 MB | La tesis usa sólo $\ell_\phi=0.10\lambda$. El ASM regenera bit a bit idéntico |
| Corridas modales intermedias y curriculum de frecuencia | 1.0 MB | Tanteos previos a la configuración final |

Quedan los **20 `.npz` que la cadena sí abre** (16.0 MB): las cinco
referencias ASM de las pantallas validadas, las cinco corridas modales
`_omega1_finetune`, las cuatro del barrido de $\omega_0$ y las curvas de $L^2$.

Tras el borrado se reejecutó la cadena entera y el verificador siguió en
80/80.

### Cómo recuperarlos

Estaban versionados, así que **no se perdieron**: viven en el historial. El
último commit que los contiene es `9cc926b`.

```bash
git checkout 9cc926b -- results/nb03_pinn_reference_comparison_pilot.npz
```

O todos los de un grupo:

```bash
git checkout 9cc926b -- 'results/nb03_pinn_slabs_comparison_*'
```

**El repositorio no adelgaza con esto.** Los objetos siguen en `.git`, que pesa
~617 MB. Lo que se limpia es el árbol de trabajo y lo que se descarga en un
`clone` nuevo. Sacarlos del historial exigiría reescribirlo, y eso invalida los
hashes de todos los commits posteriores.
