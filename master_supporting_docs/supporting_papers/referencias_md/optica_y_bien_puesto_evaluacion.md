# Literatura de óptica y buen planteamiento — búsqueda, análisis y evaluación

**Fecha:** 2026-09-12
**Motivo:** la colección del proyecto tenía ~20 papers de PINNs y prácticamente nada
de óptica ni de teoría de problemas mal puestos, que son las dos áreas donde el
trabajo se movió al adoptar la formulación modal de NB03.
**Ubicación de los PDFs:** `master_supporting_docs/supporting_papers/referencias/optica_y_bien_puesto/`

---

## 1. Nguyen, Khoa, Minh y Tran (2014) — Truncamiento para el problema de Cauchy de Helmholtz

`Nguyen_etal_2014_TruncacionCauchyHelmholtz.pdf` · arXiv:1408.1932 · 26 pp. · licencia arXiv

> *Reconstruction of the electric field of the Helmholtz equation in 3D*

**Qué hace.** Investiga rigurosamente el **método de truncamiento** como
regularización del problema de Cauchy para Helmholtz. Examina el mal
planteamiento a través de la representación de la solución en modos de Fourier,
construye la solución regularizada acotando la frecuencia por un parámetro de
regularización, y demuestra estabilidad y convergencia fuerte con estimaciones
de error en norma L².

**Por qué sirve — el más importante de los cuatro.** Es la justificación
matemática de la decisión central de NB03. Hoy el truncamiento a los 41 modos
propagantes se presenta como una consecuencia de la descomposición modal; con
esta cita pasa a ser **la regularización canónica de un problema mal puesto,
con estimación de error demostrada**. Cambia el argumento de «funcionó» a «es lo
que la teoría prescribe».

**Dónde citarlo.** Cap3, al introducir la base modal y el corte en `|kx| ≤ k`.
Cap4, al reportar el piso evanescente de 3.16% como el sesgo del parámetro de
regularización.

**Advertencia.** Es matemática aplicada densa (espacios de Sobolev, estimaciones
a priori). No hace falta seguir las demostraciones: la introducción y el
planteamiento del problema regularizado bastan para citarlo con propiedad.

---

## 2. Xiong, Zhang, Hu, Gao y Deng (2025) — Redes espectrales de variable separada

`Xiong_etal_2025_SeparatedVariableSpectralNeuralNetworks.pdf` · arXiv:2508.00628 · 35 pp. · licencia arXiv

> *Separated-Variable Spectral Neural Networks: A Physics-Informed Learning Approach for High-Frequency PDEs*

**Qué hace.** Combina separación de variables con métodos espectrales adaptativos
para atacar el sesgo espectral de las PINNs. Tres componentes: descomposición de
funciones multivariadas en productos de univariadas con redes independientes por
variable; características espectrales de Fourier con parámetros de frecuencia
aprendibles; y un marco teórico basado en SVD para cuantificar el sesgo
espectral. Evalúan en Heat, **Helmholtz**, Poisson y Navier-Stokes, reportando
mejoras de 1 a 3 órdenes de magnitud con 90% menos parámetros.

**Por qué sirve — y por qué hay que leerlo con cuidado.** Es **el trabajo
publicado más cercano a tu formulación modal**. Separación de variables + base
espectral + red que aprende los coeficientes + motivación por sesgo espectral: es
tu mismo esquema conceptual. Dos consecuencias:

1. **Posicionamiento obligatorio.** No puedes presentar la formulación modal como
   novedad sin discutir este trabajo. Tus diferencias reales: ellos aprenden
   frecuencias, tú las fijas por física (`kxₘ` viene de la periodicidad, `kzₘ` de
   la relación de dispersión); ellos no imponen Cauchy dura; ellos no tratan el
   problema mal puesto ni el truncamiento como regularización; y tu activación es
   SIREN con la regla `ω₀ ≈ k/2π`, no características de Fourier aprendidas.
2. **Respaldo.** Confirma de forma independiente que la ruta separación de
   variables + espectral es la respuesta correcta al sesgo espectral en PDEs de
   alta frecuencia. Tu resultado de ω₀ (0.049% vs 1.545%) es evidencia del mismo
   fenómeno por otra vía.

**Dónde citarlo.** Cap2, en el estado del arte, junto a Panagiotakopoulos. Cap5,
al delimitar la aportación.

---

## 3. Veerababu y Ghosh (2025) — Helmholtz 2D con solución de prueba

`Veerababu_Ghosh_2025_Helmholtz2D_SolucionPrueba_RedesNeuronales.pdf` · arXiv:2503.20222 · 59 pp. · **CC BY 4.0**

> *Solving 2-D Helmholtz equation in the rectangular, circular, and elliptical domains using neural networks*

**Qué hace.** Plantea Helmholtz 2D con condiciones de frontera prescritas como
optimización **no restringida** mediante el método de la *solución de prueba*:
construye una red que satisface las condiciones de frontera **antes** del
entrenamiento, usando interpolación transfinita y teoría de funciones R. Lo
aplica a dominios rectangular, circular y elíptico, y compara contra **elemento
finito 2D**. Aborda explícitamente el problema de gradiente evanescente al
resolver Helmholtz.

**Por qué sirve.** Tres cosas a la vez:
- Es la **teoría general de lo que hace tu Cauchy dura**: imponer la frontera en
  la arquitectura en vez de como penalización. Junto con Sukumar y Srivastava
  (2021), que ya tienes, cubre tu decisión metodológica más importante.
- Compara contra FEM, que es justo tu NB04 pendiente. Sirve de modelo
  metodológico para armarlo.
- Licencia CC BY 4.0: puedes reproducir figuras citando la fuente.

**Dónde citarlo.** Cap3, al justificar la frontera dura. Cap5, al plantear NB04.

---

## 4. Carbajal-Domínguez, Bernal, Gómez-Correa y Martínez-Niconoff (2010) — Espectro angular en campo cercano

`CarbajalDominguez_etal_2010_EspectroAngular_DifraccionCampoCercano_FFT.pdf` · arXiv:1002.1999 · 16 pp. · licencia arXiv

> *Numerical calculation of near field scalar diffraction using angular spectrum of plane waves theory and FFT*

**Qué hace.** Implementación numérica por FFT de la teoría del espectro angular
de ondas planas para difracción de **campo cercano**, con resultados numéricos y
**experimentales** para una apertura circular y una rendija espiral.

**Por qué sirve.** Tu referencia de verdad es espectro angular por FFT y hasta
ahora **no citabas ninguna fuente que lo defina**. Además tu propagación es de
1λ: campo cercano estricto, no Fresnel ni Fraunhofer. Es el régimen de este
paper. La validación experimental refuerza que el método no es sólo un
artificio numérico.

**Limitación honesta.** Es un paper de implementación: no analiza criterios de
muestreo ni el papel de las ondas evanescentes con la profundidad que te
convendría. Para eso hace falta el punto 5 de abajo.

---

## 5. Pendiente de descarga manual — Matsushima y Shimobaba (2009)

> *Band-Limited Angular Spectrum Method for Numerical Simulation of Free-Space
> Propagation in Far and Near Fields*
> **Optics Express 17(22), 19662–19673.** DOI: 10.1364/OE.17.019662

**Estado:** no descargado. Optics Express es de acceso abierto y el artículo es
de lectura libre, pero el servidor de Optica bloquea descargas automatizadas
(devuelve HTML en vez del PDF). **Hay que bajarlo manualmente** desde
`https://opg.optica.org/oe/fulltext.cfm?uri=oe-17-22-19662` y guardarlo en la
misma carpeta.

**Por qué vale la pena el trámite.** Es la referencia canónica sobre los
**errores numéricos del método del espectro angular**: el muestreo de la función
de transferencia produce errores severos, y la solución es limitar la banda del
campo propagado para satisfacer Nyquist y evitar aliasing. Con ~380 citas.

Te importa directamente porque tu referencia «exacta» es una ASM por FFT sobre
1024 puntos, y **no has verificado que cumpla el criterio de muestreo de
Matsushima**. Si no lo cumple, tu verdad de referencia tiene un error sistemático
no cuantificado, y todas tus métricas L² heredan ese error. Vale la pena
revisarlo antes de escribir Cap4.

---

## Hallazgo adicional: hay un experto en este método en tu propia universidad

El primer autor del punto 4 es **Dr. José Adrián Carbajal Domínguez**,
adscrito a la **UJAT**, División Académica de Ciencias Básicas, Departamento de
Física y Matemáticas (`adrian.carbajal@ujat.mx`). Licenciatura en Física por la
UJAT (1995), maestría (2000) y doctorado (2005) en Ciencias con especialidad en
Óptica por el **INAOE**. Líneas: óptica física, difracción escalar, nanoóptica,
plasmones de superficie, haces Bessel.

Es decir: en tu propia universidad hay un doctor en óptica por el INAOE que
**publicó justamente el método del espectro angular en campo cercano** sobre el
que construiste toda tu verdad de referencia.

Esto atiende de raíz el desbalance que originó esta búsqueda: el lado óptico del
proyecto no tiene respaldo experto, mientras el lado computacional sí. Vale la
pena plantearlo con el Dr. Adán, sea como co-asesor o como sinodal.

*(Verificar la adscripción vigente antes de cualquier gestión: los datos provienen
de su CV público en el sitio de la UJAT y de su perfil de Google Scholar.)*

---

## Resumen de prioridad

| # | Trabajo | Hueco que cubre | Prioridad |
|---|---|---|---|
| 1 | Nguyen et al. (2014) | Truncamiento como regularización, con estimación de error | **Alta** — sostiene la decisión central de NB03 |
| 2 | Xiong et al. (2025) | Trabajo publicado más cercano a la formulación modal | **Alta** — obligatorio para el posicionamiento |
| 3 | Veerababu y Ghosh (2025) | Frontera dura por solución de prueba; comparación con FEM | Media-alta |
| 4 | Carbajal-Domínguez et al. (2010) | Espectro angular por FFT en campo cercano | Media |
| 5 | Matsushima y Shimobaba (2009) | Muestreo y aliasing del ASM — **descarga manual** | **Alta** — puede afectar la validez de la referencia |

**Lo que no se encontró.** No apareció una fuente de acceso abierto realmente
buena sobre simulación de speckle desde pantallas de fase aleatoria con
estadística de Goodman. Ese hueco sigue siendo mejor cubierto por los libros
*Speckle Phenomena in Optics* y *Statistical Optics* de Goodman, que no están en
acceso abierto y habría que conseguir por biblioteca.
