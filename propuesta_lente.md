# Propuesta: elemento óptico tipo lente como componente parametrizable

**Estado:** trabajo futuro, no implementado. Documento de análisis, no de decisión final.
**Origen:** propuesta del Dr. José Adán Hernández Nolasco (director) — incorporar un lente como el único componente parametrizable del modelo, para que cambiar su descripción (distancia focal, fase, apertura) adapte el modelo a distintos casos de propagación sin reescribir la ecuación de Helmholtz ni la arquitectura SIREN.

**Actualizado el 2026-09-17 a la formulación modal.** La versión anterior de este
documento se escribió contra la formulación **colocada directa**, que se abandonó
(ver `sec:nb03_diagnostico` en Cap4). Sus conclusiones ya no valen tal cual: la
Opción A se vuelve más fácil, la Opción B pasa de «riesgosa» a **incompatible con
la separación modal**, y aparece una Opción D que antes no existía y que es la que
más se parece a lo que el director describió.

---

## 0. Qué cambió respecto de la versión anterior

| Punto | Antes (formulación directa) | Ahora (formulación modal) |
|---|---|---|
| Dominio | $\Omega=[0,1]^2$, BVP completo resuelto de una vez | $x\in[-10,10]\lambda$ **periódico**, marcha en $z$ por construcción |
| El lente entra por | La condición Dirichlet en $y=0$, como término de datos | La **condición de Cauchy** en $z=0$, impuesta por construcción — no hay término de datos |
| Índice variable $n(x,z)$ | Riesgoso (paisaje de optimización) | **Rompe el desacoplamiento de los 41 modos** |
| Lente en medio de la propagación | Imposible sin reescribir la formulación | **Ya hay cuatro planos donde colocarlo** (NB03C) |

El punto 4 de los supuestos anteriores decía que la formulación «no es un esquema
de marcha en $z$ tipo BPM». **Eso dejó de ser cierto.** La formulación modal con
Cauchy dura sí marcha en $z$, y NB03C la parte en cinco bloques encadenados. Es
justamente lo que hacía falta para que el lente fuera viable.

---

## 1. La formulación vigente, en lo que afecta al lente

Verificado en `scripts/experiments/nb03_modal_pinn_siren.py`,
`scripts/experiments/nb03_pinn_slabs.py` y
`results/nb03_angular_spectrum_reference_z1_corr0.10.json`:

- **Dominio transversal:** $x\in[-10,10]\lambda$, ancho $W=20\lambda$, **fronteras
  laterales periódicas**, 1024 puntos ($\Delta x = 0.0195\lambda$).
- **Base:** serie de Fourier exacta, $k_{x,m}=2\pi m/W$. De los **1024 modos
  espectrales** sólo entran los **41 propagantes** ($|k_{x,m}|\le k$, es decir
  $|m|\le 20$). Los evanescentes se ponen a cero.
- **Separación:** con $k$ constante, Helmholtz se separa en 41 EDOs
  **desacopladas** $a_m''+k_{z,m}^2a_m=0$, con $k_{z,m}^2=k^2-k_{x,m}^2$.
- **Condición de Cauchy dura:** $a_m(z)=a_m(0)+z\,a_m'(0)+z^2N_\theta(z)$.
- **Dato de entrada, y esto importa mucho:** `radiative_input()` fija
  $$a_m'(0) = i\,k_{z,m}\,a_m(0),$$
  es decir, **sólo onda saliente**. La formulación ya descarta la componente
  contrapropagante y la energía evanescente. En la pantalla, la fracción de energía
  propagante es **0.410** — el 59 % restante se desecha ahí mismo.

**Consecuencia directa para el lente:** no hay condición de frontera de datos que
modificar. Lo que se modifica es el **par de Cauchy** $(a_m, a_m')$ en un plano.

---

## 2. Supuestos (condicionan todo lo que sigue)

1. **Campo escalar** — igual que el resto de la tesis ($E$ complejo escalar, sin polarización vectorial completa).
2. **Lente delgado (thin lens)** — el lente se trata como una transformación de fase instantánea en un plano, ignorando la propagación dentro del vidrio. Aproximación estándar en óptica de Fourier (Goodman, *Introduction to Fourier Optics* — libro distinto al ya citado *Speckle Phenomena in Optics*, mismo autor, dos obras).
3. **Régimen paraxial** — la fórmula de fase cuadrática del lente ($e^{-ikx^2/2f}$) es una aproximación paraxial de la transformación esférica exacta $e^{-ik\sqrt{f^2+x^2}}$, válida para $x \ll f$.
4. **Propagación unidireccional** — ya asumida por la formulación vigente, no un supuesto nuevo que añada el lente (ver §1).
5. **Periodicidad en $x$** — la base de Fourier la exige. Cualquier máscara que se multiplique al campo tiene que ser compatible con ella (ver §4.1).

---

## 3. Formulación matemática — cuatro opciones

Un lente delgado con distancia focal $f$ y apertura $P(x)$ multiplica el campo
incidente por una transmitancia compleja:

$$t_\text{lente}(x) = P(x)\,\exp\!\left(-i\,\frac{k x^2}{2f}\right)$$

En la base modal, multiplicar por $t(x)$ en un plano es una **convolución en el
espectro**:

$$a_m^{+} = \sum_n \hat{t}_{m-n}\,a_n^{-}$$

Esto **acopla los modos en ese plano**, pero es una operación algebraica de una
sola vez (un FFT, un producto, un FFT inverso). **No acopla las EDOs**: entre
planos, los 41 modos siguen desacoplados y la arquitectura no cambia.

### Opción A — Máscara en el plano de entrada $z=0$

Se multiplica el campo de la pantalla **antes** de proyectarlo a la base:

$$E(x,0)\;\longrightarrow\;E(x,0)\cdot t_\text{lente}(x)$$

y de ahí se recalculan $a_m(0)$ y $a_m'(0)=i\,k_{z,m}a_m(0)$ con la misma rutina
que ya existe.

**Ventaja:** es un cambio de **cinco líneas en `radiative_input()`**. No toca el
residuo, ni la arquitectura, ni el entrenamiento. Más fácil que en la formulación
anterior, no menos.
**Limitación:** un solo lente, en el plano de entrada.

### Opción B — Índice variable $n(x,z)$ (medio GRIN) — DESACONSEJADA

$$\nabla^2 E + k^2 n(x,z)^2 E = 0$$

**Ya no es sólo «riesgosa»: rompe la separación de variables.** Con $n$ dependiente
de $x$, el término $k^2n^2E$ se convierte en una convolución **dentro** de la
ecuación, y las 41 EDOs dejan de estar desacopladas:

$$a_m'' + k_{z,m}^2 a_m = -k^2\!\!\sum_{n}\big(\widehat{n^2-1}\big)_{m-n}\,a_n$$

Se pasa de 41 problemas escalares independientes a un **sistema acoplado de 41
EDOs**. Es resoluble, pero **es otra tesis**: cambia el residuo, la escala modal,
el argumento de buen planteamiento de Cap3 y la referencia del espectro angular
(que deja de ser válida, porque el ASM también supone medio homogéneo).

**Sólo tiene sentido si el objetivo explícito es un medio GRIN continuo.** Para lo
que pidió el director —una secuencia de lentes delgadas— la Opción D da el mismo
efecto físico sin nada de esto.

### Opción C — Post-procesamiento

$$E_\text{con\_lente}(x,z) = E_\text{PINN}(x,z)\cdot t_\text{lente}(x)$$

**Ventaja:** cero cambios al entrenamiento.
**Limitación física seria:** sólo válido si el lente está al final del dominio, sin
propagación posterior. Aplicado en medio del dominio da un campo incorrecto, porque
no recalcula la difracción posterior al lente. Sin cambios respecto de la versión
anterior.

### Opción D — Máscaras en las interfaces de NB03C — RECOMENDADA

**Esta es la opción nueva, y es la que corresponde a lo que describió el director:**
*«llevo otra lente pegadita irregular, otra pegadita irregular… como si fuera una
secuencia de lentes, todos intentando simular la atmósfera»*. Eso es, literalmente,
**split-step**.

NB03C ya divide $[0,5\lambda]$ en cinco bloques de $1\lambda$ y transfiere en cada
interfaz el par de Cauchy exacto:

$$A_m^{(j)}=a_m^{(j-1)}(1),\qquad B_m^{(j)}={a_m^{(j-1)}}'(1)$$

con salto medido de **cero exacto** (`interface_field_max_abs = 0.0`). Meter una
máscara es interponer un paso entre esas dos líneas:

1. Reconstruir el campo en la interfaz: $E^-(x)=\sum_m a_m^{(j-1)}(1)\,e^{ik_{x,m}x}$
2. Multiplicar: $E^+(x) = t_j(x)\,E^-(x)$
3. Reproyectar y quedarse con los 41 propagantes: $A_m^{(j)} = \widehat{E^+}_m$
4. Reimponer la condición saliente: $B_m^{(j)} = i\,k_{z,m}A_m^{(j)}$

**El paso 4 no es un supuesto nuevo.** Es exactamente la regla que
`radiative_input()` ya aplica en $z=0$. Aplicarla en cada interfaz es *consistente*
con la formulación, no un compromiso adicional.

Con $t_j$ determinista y la misma $f$ en todos los planos se obtiene un lente
grueso; con $t_j(x)=\exp(i\phi_j(x))$ y $\phi_j$ aleatoria e independiente por
plano, se obtiene el medio inhomogéneo tipo atmósfera — el caso de la tesis de
maestría del director.

**Coste:** cuatro planos de máscara en la configuración actual, sin reentrenar la
arquitectura ni cambiar el residuo. Lo que sí cambia es que **cada bloque debe
reentrenarse**, porque su dato de Cauchy inicial ya no es el del caso homogéneo.

---

## 4. Los dos obstáculos reales

Ninguno es un impedimento, pero los dos condicionan qué máscara se puede usar.

### 4.1. La periodicidad, y por qué el caso aleatorio es más fácil que el lente

La base de Fourier exige que la máscara sea compatible con el periodo $W=20\lambda$.

- **Fase aleatoria (atmósfera):** se genera periódica por construcción, igual que ya
  se hace con la pantalla — el JSON de referencia lo declara explícitamente
  (`phase_model.periodic = True`). **Sin problema.**
- **Lente cuadrático $e^{-ikx^2/2f}$:** es una función **par**, así que su *valor*
  coincide en $x=-10$ y $x=+10$; pero su *pendiente* no ($\mp 10k/f$). La extensión
  periódica tiene un **pico en el borde del periodo**, y ese pico radia energía
  hacia frecuencias transversales altas — precisamente las que la base de 41 modos
  descarta.

**Mitigación:** apodizar la apertura $P(x)$ para que la máscara decaiga a uno (o a
cero) antes del borde, de modo que el empalme sea suave. Es lo físicamente honesto
de todos modos: una lente real tiene apertura finita.

**Conclusión práctica, y es contraintuitiva:** el caso que el director pospuso «para
después» —el medio inhomogéneo aleatorio— es **más fácil de implementar** que el
lente convergente clásico.

### 4.2. La fuga evanescente en cada máscara

Cada multiplicación por $t(x)$ ensancha el espectro. La parte que cae fuera de
$|k_{x,m}|\le k$ es evanescente y **se descarta**, porque la base no la representa.
Con $N$ máscaras la pérdida se acumula.

El orden de magnitud está medido: en la pantalla de entrada sólo el **41 %** de la
energía es propagante. Una máscara con detalle fino haría algo parecido en cada
plano.

Y hay un resultado propio que dice que ampliar la base no es la salida: el
experimento de base extendida bajó el piso evanescente de 3.8184 % a 0.0020 %, pero
**subió el error en banda de 1.98 % a 24.70 %**. El truncamiento está justificado
por tratabilidad numérica, y esa justificación sigue aplicando aquí.

**Mitigación:** máscaras **suaves** (fase de bajo orden, longitud de correlación
$\gtrsim\lambda$). Una máscara con escala de variación menor que $\lambda$ está
fuera del alcance de esta formulación y hay que decirlo, no ocultarlo.

**Diagnóstico barato y obligatorio antes de entrenar nada:** aplicar la máscara al
campo y medir qué fracción de energía sobrevive al filtro propagante. Si cae mucho
por plano, la máscara es demasiado agresiva. Son diez líneas de NumPy y no requiere
PINN.

---

## 5. Compatibilidad con la PINN

La arquitectura **no se toca en ninguna de las opciones salvo la B**.

El residuo exige que $a_m(z)$ sea diferenciable dos veces por autodiff en el
interior de cada bloque; la máscara actúa **entre** bloques, sobre valores, no
dentro del residuo. SIREN no tiene que diferenciar $t(x)$: sólo recibe unos
coeficientes iniciales distintos. Es la misma razón por la que ya funciona con la
fase aleatoria de la pantalla, que es irregular punto a punto.

La Opción B es la única que entra en el residuo, y por eso es la única que obliga a
tocar la escala modal, `src/losses.py` y el argumento de Cap3.

---

## 6. Parametrización (si se implementa A o D)

```
src/
├── models.py          # SIREN — SIN CAMBIOS
├── losses.py          # residuo modal — SIN CAMBIOS
├── optics.py          # NUEVO: máscaras de transmitancia
│   ├── lens_phase(x, f, k)            -> exp(-i k x^2 / (2f))
│   ├── random_phase(x, sigma, ell)    -> exp(i phi(x)), periódica
│   ├── aperture(x, radio, apodizado)  -> P(x)
│   └── apply_mask(a_m, kx, kz, t)     -> (A_m, B_m) tras la máscara
└── training.py        # SIN CAMBIOS
```

`apply_mask()` es la pieza central y encapsula los cuatro pasos de la Opción D. Debe
**devolver también la fracción de energía perdida** al filtro propagante — es el
diagnóstico de §4.2 y conviene que salga solo, no que haya que pedirlo.

Fijo entre casos: arquitectura, residuo, optimizador, condición de Cauchy dura.
Variable entre casos: sólo la lista de máscaras y en qué planos actúan. Los
parámetros del lente ($f$, apertura, apodización, $\sigma_\phi$, $\ell_\phi$) son
argumentos de esas funciones, **no hiperparámetros de la red**.

---

## 7. Efecto esperado sobre la generación de speckle

Si la máscara va **antes** de la pantalla rugosa: cambia la amplitud $A(x)$ y el
frente de fase incidente, pero no debería cambiar la naturaleza estadística del
speckle (las estadísticas de Goodman dependen de que la fase de salida siga siendo
$\sim\mathcal{U}(0,2\pi)$ punto a punto, que la pantalla sigue imponiendo después).
Predicción: cambia el **tamaño del grano**, no rompe $C\approx1$.

Si la máscara va **después**: actúa como sistema de imagen y cambia el tamaño
aparente del grano observado.

Si son **varias máscaras aleatorias encadenadas** (Opción D, caso atmósfera): el
contraste debería **subir** por encima de 1 conforme se acumulan, que es la firma
del régimen de speckle sobre speckle. Es la predicción más falsable de las tres y
la más interesante de medir.

**Las tres son predicciones físicas falsables, no certezas — verificar
empíricamente una vez implementado.**

---

## 8. Referencias verificadas (búsqueda hecha, no de memoria)

| Referencia | Relevancia |
|---|---|
| Luo, Zhang, Wang, Jiang, Song & Wang (2025), "PINN-BPM: An Enhanced Physics-Informed Neural Network Framework of Solving Helmholtz Equation for Light Field Propagation in Optical Fiber", *J. Lightwave Technol.* 43(23), 10380–10401 | Combina PINN con BPM (marcha en $z$) — **el precedente más cercano a la Opción D**, ahora que la formulación sí marcha en $z$ |
| Song, Alkhalifah & Bin Waheed (2022), "A versatile framework to solve the Helmholtz equation using physics-informed neural networks", *Geophysical Journal International* 228(3), 1750–1762 | Mismo grupo que el ya-citado Alkhalifah et al. (2021); Helmholtz con velocidad variable — precedente de la Opción B |
| Es'kin & Ivanov (2025), "Physics-informed neural networks and neural operators for a study of EUV electromagnetic wave diffraction from a lithography mask", arXiv:2507.04153 | PINN + máscara de fase/amplitud — precedente más cercano a «PINN + máscara» |
| Goodman, *Introduction to Fourier Optics* (McGraw-Hill) | Fórmula de transmitancia de lente delgado. Distinto del *Speckle Phenomena in Optics* ya citado |
| Andrés-Zárate, Angulo Córdova, Gutiérrez Tepach & Hernández-Nolasco (2019), *Rev. Mex. Fis.* 65, 299–306, y su capítulo de libro de 2024 | **Del propio director.** Difracción en las regiones convergente y divergente de una lente esférica, con experimento y simulación por espectro angular. Es el patrón a reproducir, y su método de simulación es el mismo que hoy sirve de referencia a NB03 |

**No se encontró ningún trabajo que combine específicamente PINN + lente delgado +
generación de speckle.** Si se implementa, probablemente sea genuinamente nuevo.

---

## 9. Próximo paso sugerido (no iniciado)

En este orden, y **los dos primeros no requieren entrenar nada**:

1. **Diagnóstico de fuga (§4.2).** Tomar el campo de NB03 en $z=1\lambda$, aplicarle
   una máscara candidata, medir qué fracción de energía sobrevive al filtro
   propagante. Decide si la máscara es viable antes de gastar una sola época.
2. **Validación contra el espectro angular.** Propagar con ASM + máscara —el método
   del paper de 2019— y usarlo como referencia. Es semianalítico, igual que la
   referencia actual, con la misma salvedad ya documentada.
3. **Opción A con onda plana**, sin speckle: verificar que la fase del lente no
   rompe el entrenamiento de SIREN.
4. **Opción D con una sola máscara aleatoria** en la primera interfaz de NB03C, una
   pantalla, contra la referencia ASM del paso 2.
5. Sólo entonces, las cuatro máscaras.

**Orden de prioridad respecto del resto de la tesis:** esto es trabajo futuro. El
director lo pospuso explícitamente el 2026-09-08 («primero es homogéneo»), y el
hueco que bloquea hipótesis y Cap5 sigue siendo **NB04**, no el lente.
