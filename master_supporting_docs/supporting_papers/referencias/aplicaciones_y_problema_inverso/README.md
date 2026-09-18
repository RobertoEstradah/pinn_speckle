# Aplicaciones y problema inverso

**Creada:** 2026-09-18
**Qué es:** literatura para la **línea de trabajo futuro** — llevar el modelo
directo validado en la tesis hacia problemas inversos y aplicaciones reales.

**Qué NO es:** ninguno de estos papers sostiene cifra alguna de la tesis. No
están en `references.bib` ni los toca `verifica_cifras_tesis.py`. Se guardan
aparte precisamente para que no se mezclen con el material de respaldo.

---

## La lógica de la carpeta

La tesis entrega un **modelo directo**: dada la pantalla rugosa, calcula el
campo. La aplicación interesante es la contraria — medir el campo y recuperar la
superficie. Estos trabajos muestran cómo otros grupos han hecho ese salto.

```
modelo directo validado  →  problema inverso  →  aplicación
     (la tesis)              (estos papers)      (metrología, imagen médica)
```

---

## Lo que hay

### 1. Saba, Gigli, Ayoub y Psaltis (2022) — el patrón a seguir

`Saba_etal_2022_PINN_DiffractionTomography.pdf` · 25 pág.
*Advanced Photonics* 4(6), 066001 · arXiv:2207.14230 · EPFL

**Es el más cercano a lo que querríamos hacer.** Usa un PINN como **modelo
directo** para tomografía de difracción óptica, entrenado con la ecuación de
Helmholtz como pérdida física, y de ahí resuelve el problema de dispersión.

Del propio resumen: *«can be generalized for any forward and inverse scattering
problem»*. Y algo práctico: una red preentrenada se **afina** para muestras
distintas, lo que ataca de frente la limitación de la tesis de que cada pantalla
exige entrenar desde cero (~350 s).

Validan con resultados numéricos **y experimentales**.

### 2. Chen y Dal Negro (2021) — del mismo grupo que ya citas

`Chen_DalNegro_2021_PINN_CampoCercano_Nanoestructuras.pdf` · 9 pág.
arXiv:2109.12754 · Boston University

PINN para **imagen y recuperación de parámetros a partir de datos de campo
cercano**. Dos coincidencias con la tesis: es campo cercano, que es el régimen
exacto de NB03, y **recupera parámetros**, que es la estructura del inverso.

**Conexión útil:** Yuyao Chen y Luca Dal Negro firman también
`Chen_Lu_Karniadakis_DalNegro_2020_NanoOpticsMetamaterials.pdf`, que ya está en
`referencias/` y que la tesis cita. Este trabajo es la continuación de aquél.

### 3. Yang et al. (2025) — el estado del arte en rayos X

`Yang_etal_2025_PINN_FaseHolograma_RayosX_OpticsExpress.pdf` · 28 pág.
*Optics Express* 33(17), 35832 · arXiv:2508.15530

Recuperación de fase desde **un solo holograma** de rayos X con redes
generativas físicamente informadas y auto-supervisadas. Lo notable: **no
requiere datos de entrenamiento** de ningún tipo.

Sirve como cota del estado del arte, y como aviso: el nicho está poblado.

---

### 4. Celestre et al. (2025) — la revisión de referencia del campo

`Celestre_etal_2025_RevisionSpeckleTracking_RayosX.pdf` · 37 pág.
*Journal of Synchrotron Radiation* 32(1), 180-199 · DOI 10.1107/S1600577524010890
Synchrotron SOLEIL y Univ. Grenoble Alpes / INSERM

Revisión **y comparación experimental** de los algoritmos de speckle tracking.
Usa granos de speckle **de campo cercano** como marcadores de frente de onda, y
compara los métodos de recuperación de fase bajo distintas condiciones, sobre
fantomas cuantitativos y muestras complejas.

**El dato que conviene retener:** trabajan a distancias de **cientos de
milímetros a metros** (aparecen 140 mm, 200 mm, 500 mm, 2 m, 5 m) con haces de
~20 keV. La tesis trabaja a **3.19 µm**. La física comparte ecuación; el régimen
experimental no tiene nada que ver.

Descargado a mano el 18/09/2026: PMC e IUCr bloquean la descarga automatizada.

Es la revisión de referencia del campo, de enero de 2025, de Synchrotron SOLEIL.

---

## Lo que dice este material, leído en conjunto

**El nicho de PINN + rayos X ya está ocupado y se mueve rápido:** cuatro
trabajos relevantes entre 2022 y 2026, dos de ellos de 2025-2026.

**La rama de rayos X trabaja en paraxial, pero el resto del campo no.** Conviene
no confundirlas, porque la distinción cambia cuál es el aporte de la tesis.

Rastreando «paraxial» y «Fresnel» sobre los PDF de `referencias/`, el reparto es
nítido:

| Grupo | Ecuación | Ejemplos |
|---|---|---|
| **PINN para ondas** | Helmholtz completo, **sin paraxial** | Schoder y Kraxberger 2024 · Panagiotakopoulos 2026 · Alkhalifah 2021 · Veerababu y Ghosh 2025 · Zhang 2025 · Saba 2022 · Chen, Lu, Karniadakis y Dal Negro 2020 |
| **Recuperación de fase con rayos X** | Fresnel, **paraxial** | Yang et al. 2025 (37 menciones de Fresnel) · la revisión de Celestre et al. 2025 (6 de paraxial) |

Los siete del primer grupo no mencionan «paraxial» ni «Fresnel» **ni una vez**.

**Consecuencia para la tesis:** resolver Helmholtz completo **no la distingue**
del estado del arte de PINN en ondas, donde es lo habitual. Sólo la distingue
frente a la rama de rayos X. Lo que sí la distingue del primer grupo es la
**formulación**: descomposición modal con condición de Cauchy impuesta por
construcción, que es lo que restaura la unicidad. Los demás resuelven Helmholtz
con la red sobre $(x,z)$ y el residuo como penalización, y no abordan el buen
planteamiento porque sus geometrías no lo ponen en cuestión.

No decir, por tanto, «los demás usan Fresnel y nosotros no»: es cierto sólo de
los cuatro de esta carpeta.

**El camino corto no es rayos X, es rugosidad.** El régimen de la tesis --5λ
son 3.19 µm-- es el de la metrología de superficies, no el del banco óptico ni
el del sincrotrón. Ahí el modelo directo ya está en su escala.

**Y antes de cualquier aplicación están los 6λ.** El error propagante de NB03C
crece de forma acelerada: el quinto bloque aporta 3.8 veces lo que aportó el
primero, y la extrapolación conservadora cruza el 5 % en z=6λ. El coste de
cómputo no es el problema (70 s por bloque; 20λ serían 23 min por pantalla): lo
es la transferencia de error entre interfaces. Resolver eso es lo que abre todo
lo demás.
