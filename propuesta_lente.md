# Propuesta: elemento óptico tipo lente como componente parametrizable

**Estado:** trabajo futuro, no implementado. Documento de análisis, no de decisión final.
**Origen:** propuesta del Dr. José Adán Hernández Nolasco (director) — incorporar un lente como el único componente parametrizable del modelo, para que cambiar su descripción (distancia focal, fase, apertura) adapte el modelo a distintos casos de propagación sin reescribir la ecuación de Helmholtz ni la arquitectura SIREN.

---

## Supuestos (condicionan todo lo que sigue)

1. **Campo escalar** — igual que el resto de la tesis ($E$ complejo escalar, sin polarización vectorial completa).
2. **Lente delgado (thin lens)** — el lente se trata como una transformación de fase instantánea en un plano, ignorando la propagación dentro del vidrio. Aproximación estándar en óptica de Fourier (Goodman, *Introduction to Fourier Optics* — libro distinto al ya citado *Speckle Phenomena in Optics*, mismo autor, dos obras).
3. **Régimen paraxial** — la fórmula de fase cuadrática del lente ($e^{-ikr^2/2f}$) es una aproximación paraxial de la transformación esférica exacta $e^{-ik\sqrt{f^2+r^2}}$, válida para $r \ll f$.
4. **Punto crítico de la formulación actual:** el dominio $\Omega=[0,1]^2$ **no es un esquema de marcha en $z$** (tipo BPM, *Beam Propagation Method*) — es un BVP de Helmholtz completo resuelto de una vez, con $y=0$ como plano de "fuente" y los otros 3 lados libres. Esto determina cuál de las opciones de abajo es viable sin reescribir la formulación de fondo.

---

## 1. Formulación matemática — 3 opciones

### Opción A — Fase en la condición de frontera (transmitancia del lente)

Un lente delgado con distancia focal $f$ y apertura $P(x)$ multiplica el campo incidente por una transmitancia compleja:
$$t_\text{lente}(x) = P(x) \, \exp\!\left(-i\, \frac{k x^2}{2f}\right)$$

Colocado justo en el plano de fuente $y=0$, la condición de frontera actual
$$E(x,0) = A(x)\, e^{i\psi(x)}$$
se reemplaza por
$$E(x,0) = A(x)\, e^{i\psi(x)} \cdot t_\text{lente}(x) = A(x)\, e^{i\psi(x)} \, P(x)\, e^{-ikx^2/2f}$$

**Ventaja:** no toca el residuo de Helmholtz ni la arquitectura — solo cambia el dato de frontera que ya alimenta $\mathcal{L}_\text{datos}$. Es la que más se ajusta al pedido original ("sin reescribir la ecuación ni la arquitectura").
**Limitación:** solo modela un lente en el plano de entrada, no en medio de la propagación.

### Opción B — Variación del índice de refracción $n(x,y)$ (medio GRIN)

$$\nabla^2 E(x,y) + k^2 n(x,y)^2 E(x,y) = 0$$

Un lente GRIN parabólico: $n(x,y) = n_0\left(1 - \frac{\alpha^2}{2}x^2\right)$, con $\alpha$ relacionado a la distancia focal equivalente. Matemáticamente análogo a la velocidad variable $v(x,y)$ en propagación sísmica (mismo rol que $n(x,y)^2$ en óptica).

**Ventaja:** modela lentes de índice gradual reales y cualquier medio inhomogéneo en general.
**Limitación:** modifica el residuo físico (`src/losses.py`), no solo la frontera — justo lo que se quería evitar.

### Opción C — Transformación aplicada al campo (post-procesamiento)

$$E_\text{con\_lente}(x,y) = E_\text{PINN}(x,y) \cdot t_\text{lente}(x)$$

**Ventaja:** cero cambios al entrenamiento.
**Limitación física seria:** solo válido si el lente está al final del dominio (sin propagación posterior). Aplicado en medio del dominio da un campo físicamente incorrecto, porque no recalcula la difracción posterior al lente.

---

## 2. Compatibilidad con la PINN

**Opción A es la más compatible, por una razón concreta, no solo de conveniencia:** el residuo físico exige que $\nabla^2 E$ sea diferenciable vía autodiff de segundo orden en el *interior* del dominio, pero la condición de frontera es un término de *datos*, no de residuo — SIREN no necesita diferenciar la función de frontera, solo ajustarse a sus valores en los puntos de colocación. Por eso ya funciona con la condición de fase aleatoria actual $\psi(x)\sim\mathcal{U}(0,2\pi)$ (discontinua punto a punto), y por la misma razón una fase de lente tampoco debería romper el entrenamiento.

La Opción B es riesgosa si $n(x,y)$ tiene un borde abrupto (apertura dura): un salto de índice en el *interior* del dominio es exactamente el tipo de problema que documenta Krishnapriyan et al. (2021, ya citado en Cap4) sobre paisajes de optimización mal condicionados en PINNs. Si $n(x,y)$ es suave (perfil GRIN sin borde duro) es más manejable, pero deja de ser un "lente delgado" clásico.

La Opción C es la más simple de programar pero la más frágil físicamente.

**Recomendación:** Opción A si el lente es una máscara de fase en el plano de entrada; Opción B solo si se necesita el lente en medio de la propagación, aceptando modificar `src/losses.py` y el riesgo de entrenamiento con aperturas de borde duro.

---

## 3. Parametrización para intercambiabilidad (si se implementa Opción A)

```
src/
├── models.py         # SIREN — SIN CAMBIOS
├── losses.py         # residuo de Helmholtz — SIN CAMBIOS
├── optics.py          # NUEVO: funciones de transmitancia (lente, apertura, fase aleatoria)
│   ├── lens_phase(x, f, k)      -> exp(-i k x^2 / (2f))
│   ├── aperture(x, radio)       -> P(x)
│   └── boundary_condition(x, caso)  -> arma E(x,0) según el caso activo
└── training.py        # SIN CAMBIOS — sigue recibiendo E(x,0) como dato de entrada
```

Fijo entre casos: arquitectura SIREN, residuo de Helmholtz, Adam+L-BFGS, LHS. Variable entre casos: solo la función que genera `E(x,0)`. Parámetros del lente ($f$, apertura, apodización) como argumentos de esa función, no como hiperparámetros de la red.

---

## 4. Efecto esperado sobre la generación de speckle

Si el lente se coloca **antes** de la frontera rugosa: cambia la distribución de amplitud $A(x)$ y el frente de fase incidente sobre la superficie difusora, pero no debería cambiar la naturaleza estadística del speckle en sí (las estadísticas de Goodman dependen de que la fase de salida siga siendo $\sim\mathcal{U}(0,2\pi)$ punto a punto, lo cual la condición de frontera sigue imponiendo después del lente). Predicción esperable: cambia el tamaño efectivo del grano de speckle (vía la relación de Goodman entre área iluminada y correlación espacial del patrón), no rompe $C\approx1$ si $N_\psi$ es suficientemente grande y $\sigma_\psi>2\pi$. **Esto es una predicción física falsable, no una certeza — verificar empíricamente una vez implementado.**

Si el lente se coloca **después** (enfocando el speckle ya generado): actúa como sistema de imagen, cambiaría el tamaño aparente del grano observado — análogo al efecto conocido de "speckle imagenado a través de una lente" en óptica estadística.

---

## 5. Referencias verificadas (búsqueda hecha, no de memoria)

| Referencia | Relevancia |
|---|---|
| Luo, Zhang, Wang, Jiang, Song & Wang (2025), "PINN-BPM: An Enhanced Physics-Informed Neural Network Framework of Solving Helmholtz Equation for Light Field Propagation in Optical Fiber", *J. Lightwave Technol.* 43(23), 10380–10401 | Combina PINN con BPM (marcha en $z$) para Helmholtz óptico — punto de partida si se necesita marcha en $z$ para un lente en medio del dominio |
| Song, Alkhalifah & Bin Waheed (2022), "A versatile framework to solve the Helmholtz equation using physics-informed neural networks", *Geophysical Journal International* 228(3), 1750–1762 | Mismo grupo que el ya-citado Alkhalifah et al. (2021); resuelve Helmholtz con índice/velocidad variable — precedente directo para la Opción B |
| Es'kin & Ivanov (2025), "Physics-informed neural networks and neural operators for a study of EUV electromagnetic wave diffraction from a lithography mask", arXiv:2507.04153 | PINN + máscara de fase/amplitud (litografía) — precedente más cercano a "PINN + máscara" encontrado, aunque en dominio de aplicación distinto |
| Goodman, *Introduction to Fourier Optics* (McGraw-Hill) | Clásico no-PINN — fuente de la fórmula de transmitancia de lente delgado. Distinto del *Speckle Phenomena in Optics* ya citado (mismo autor) |

**No se encontró ningún trabajo que combine específicamente PINN + lente delgado + generación de speckle.** Si se implementa, probablemente sea genuinamente nuevo — no hay un "cómo se hizo antes" exacto que replicar; habría que validar empíricamente que el patrón de speckle post-lente se comporta como predice la teoría clásica.

---

## Próximo paso sugerido (no iniciado)

Prueba de concepto mínima: Opción A con un caso simple (lente + onda plana, sin speckle todavía) para verificar que la fase cuadrática del lente no rompe el entrenamiento de SIREN, antes de combinarlo con la frontera de fase aleatoria de NB03.
