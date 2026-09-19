# Extensión a tres dimensiones y cómo se generan las figuras de propagación

**Creado:** 2026-09-18
**Estado:** propuesta, no ejecutada. Nada de esto está en la tesis.
**Para qué sirve:** dos cosas distintas que conviene no mezclar.

1. Dejar por escrito **qué dimensión tiene cada cosa**, porque la formulación
   modal se presta a un malentendido que ya ocurrió una vez.
2. Documentar **cómo generan sus figuras** los trabajos de referencia, y qué
   haría falta para producir imágenes del mismo tipo.

---

## 1. El malentendido de la dimensión, resuelto

> «Estoy generando en dos dimensiones, pero la parte modal lo termina generando
> en una.»

Las dos afirmaciones son ciertas y no se contradicen, porque hablan de cosas
distintas.

| Qué | Dimensión |
|---|---|
| El dominio físico | **2D**: una transversal `x` y una de propagación `z` |
| El campo `E(x,z)` | **2D** |
| La **entrada** de la red | **1D**: el escalar `z̃` |
| La salida de la red | 82 reales, que son 41 coeficientes complejos |

La razón es que la dependencia en `x` **se conoce de forma exacta** y no hay
nada que aprender en ella:

```
E(x,z) = Σ_m  a_m(z) · exp(i k_x,m x)
```

Las fronteras laterales periódicas obligan a que la parte transversal sea una
serie de Fourier. Lo único desconocido es cómo evoluciona cada amplitud `a_m`
al avanzar, y eso es una función de una sola variable.

**Enunciado correcto:** la formulación no reduce el problema a 1D. Convierte
**una EDP en 2D en 41 EDO en 1D**, desacopladas entre sí. Es separación de
variables, y es justamente lo que restaura la unicidad del problema de Cauchy.

**Cómo no decirlo:** «la red resuelve un problema unidimensional». Sugiere que
se perdió la física transversal, que es lo contrario de lo que pasa.

---

## 2. Cómo genera sus figuras cada trabajo de referencia

### 2.1 Tesis del Dr. Adán (ITESM Monterrey, 2003)

`master_supporting_docs/supporting_tesis/tesis_maestría_maestria_de_Adán.pdf`

Simula en **3D**: dos dimensiones transversales `(x,y)` más la propagación `z`,
por diferencias finitas. Láser HeNe de 632.8 nm.

| Figura | Página impresa | Qué es |
|---|---|---|
| 5.2 | 45 | Cuatro **superficies** `(x,y)`, abertura circular de radio 0.8 mm, a 0, 1.5, 3 y 6 m |
| 5.3 | 46 | Error relativo porcentual de la energía frente a `z`. Máximo ≈ 3×10⁻¹¹ |
| 5.4 | 47 | Igual que la 5.2 pero con entrada gaussiana. Muestra invariancia de forma |
| 5.5 | 48 | **Una** superficie de la sección transversal a lo largo de los 6 m |

**La 5.5 es la clave.** Para dibujarla tuvo que **sacrificar una dimensión
transversal**: es un corte `(x,z)` de un campo que es 3D. Ese corte es
exactamente lo que este trabajo produce de forma nativa, sin sacrificar nada,
porque su dominio ya es `(x,z)`.

**La 5.3 se adaptó y está en la tesis** (§`sec:nb03_z10`), con una advertencia
que no debe retirarse: su esquema de diferencias finitas conserva la energía
por construcción del operador de avance, así que su ERP mide punto flotante.
Una PINN no tiene esa garantía, de modo que aquí el ERP funciona como **medida
de error independiente de la referencia**, no como comprobación de estabilidad.
Da entre 1.666 % y 3.410 % según la pantalla.

### 2.2 Andrés-Zárate, Angulo Córdova, Gutiérrez Tepach y Hernández-Nolasco (2019)

`master_supporting_docs/supporting_papers/referencias/AndresZarate_etal_2019_DifraccionLenteEsferica.pdf`
*Revista Mexicana de Física* **65** (2019) 299-306 · DOI 10.31349/RevMexFis.65.299

También **3D**. Dos aberturas circulares de radios 1.0 y 1.5 mm, HeNe de
632 nm, doblete acromático de 25 cm de focal. Simulación por Beam Propagation
Method.

| Figura | Qué es |
|---|---|
| 3 | Cinco **fotografías experimentales** a 22, 23, 48, 24 y 35 cm |
| 4 | Las **mismas cinco distancias**, por simulación |

**Orientación de la vista:** de frente, no desde arriba. La cámara está en el
plano de observación y fotografía la mancha que llega, así que cada panel es
una rebanada `(x,y)` perpendicular al haz, a `z` fija.

**Lo valioso de este par no es la imagen sino la disposición.** Panel a) contra
panel a), b) contra b): es una **figura de validación**, referencia frente a
predicción a distancias emparejadas. El Dr. Adán no tiene ninguna así en su
tesis; valida aparte, numéricamente, con el ERP.

Esa disposición **sí se adoptó**, en la figura de cuatro planos de
§`sec:nb03_z10`, con referencia y PINN superpuestas en el mismo eje.

**Aviso al citarla:** lo suyo es experimento real contra simulación. Lo de esta
tesis es semianalítico contra red. Es una validación **más débil** y no debe
presentarse como del mismo tipo.

### 2.3 Lo que hay hoy en esta tesis

Tres figuras en §`sec:nb03_z10`, todas de
`scripts/build/figuras_nb03d_z10.py`, que no reentrena nada: lee los `.npz` ya
validados.

| Archivo | Qué es | Inspirada en |
|---|---|---|
| `nb03d_z10_paneles.png` | Cuatro perfiles transversales a 0, 1λ, 5λ y 10λ, referencia contra PINN | Adán 5.2 + Zárate 3/4 |
| `nb03d_z10_mapas.png` | Tres mapas `(x,z)`: referencia, PINN y \|diferencia\|² | Adán 5.5 |
| `nb03d_z10_erp.png` | ERP de la energía frente a `z`, cinco pantallas | Adán 5.3 |

**La diferencia obligada respecto a Adán y Zárate:** sus paneles son planos
`(x,y)` y pueden ser superficies o imágenes. Aquí sólo hay una dimensión
transversal, de modo que **cada plano es un perfil**, una curva. Está dicho en
el pie de figura, no escondido.

---

## 3. Qué haría falta para producir imágenes como las de Zárate

Harían falta **dos dimensiones transversales**. La formulación modal se
extiende sin cambiar de idea.

### 3.1 Lo que cambia

La serie de Fourier pasa a ser doble, y la EDO por modo queda:

```
a_mn'' + (k² − k_x,m² − k_y,n²) a_mn = 0
```

El truncamiento al cono propagante deja de ser un intervalo y pasa a ser un
**disco**: `m² + n² ≤ (W/λ)²`. De ahí sale todo el coste.

| | Hoy (2D) | En 3D |
|---|---|---|
| Dominio | `x` + `z` | `x`, `y` + `z` |
| Ancho | `W = 20λ` | `W = 20λ` en ambas |
| Modos propagantes | **41** | **1 257** |
| Salidas reales de la red | 82 | 2 514 |
| Factor | | **30.7×** |

Cifras calculadas con `W/λ = 20` y `k = 2π`, contando los puntos de la retícula
entera dentro del disco de radio 20. Reproducibles en dos líneas de numpy.

### 3.2 Lo que **no** cambia

Esto es lo importante, y es el argumento que vale la pena conservar:

- La **condición de Cauchy dura** `a(z) = a(0) + z·a'(0) + z²·N_θ(z)` es
  idéntica. Se aplica por modo, y el modo ahora tiene dos índices en vez de uno.
- El **truncamiento espectral** sigue siendo la misma regularización.
- La **condición de onda saliente** `a'(0) = i·k_z·a(0)` no se toca.
- La **descomposición en bloques** con acoplamiento por Cauchy funciona igual.
- El **escalamiento por modo** se generaliza sin más.

> **La formulación escala a 3D sin modificar nada de lo que constituye la
> contribución.** Lo único que crece es el conteo.

### 3.3 Lo que se ganaría

Speckle con granos en **dos** direcciones, que es como se ve de verdad. Lo que
hay hoy es su sección, no su aspecto. Permitiría además:

- Figuras directamente comparables con las de Zárate y las del Dr. Adán.
- Contraste medido sobre un área, no sobre una línea, que es la definición
  habitual en la literatura de speckle.

### 3.4 Lo que costaría, y los riesgos

**No está estimado.** Lo que se puede decir sin inventar:

- La red pasa de 82 a 2 514 salidas. No es prohibitivo, pero **no está medido**
  cuánto tarda ni si converge con el mismo presupuesto.
- La VRAM de la RTX 5050 son 8 GB, y ya hay constancia de que se satura con
  `N_colloc ≥ 90 000` en la formulación anterior. Habría que comprobarlo.
- El `ω₀ = 1` está calibrado para la entrada `z̃` normalizada actual. La entrada
  no cambia (sigue siendo escalar), así que **en principio la regla se mantiene**,
  pero conviene verificarlo y no darlo por hecho.
- La referencia por espectro angular se extiende con FFT 2D sin dificultad.

---

## 4. Recomendación, y por qué

**No incorporarlo a esta tesis.** Tres razones:

1. **Es un experimento nuevo**, y por la regla del proyecto esos se crean en
   `C:\roberto\Tesis_Maestria - codex`, no en el repositorio de redacción.
2. **NB04 sigue aparcado.** Abrir un frente en 3D sin cerrar el benchmark deja
   dos huecos en lugar de uno, y el que bloquea Cap5 es el otro.
3. **La contribución no cambia.** Está en el planteamiento, y el planteamiento
   es idéntico en 3D. Sería más caro, no más nuevo.

**Dónde sí cabe:** en trabajo futuro, con el argumento de la sección 3.2. Decir
que la formulación se extiende a dos dimensiones transversales sin tocar la
condición de Cauchy ni el truncamiento, a costa de pasar de 41 a 1 257 modos,
**afirma que el método escala sin obligar a demostrarlo**.

Pendiente de hablarlo con el Dr. Adán antes de redactarlo.

---

## 5. Fuentes de las cifras de este documento

| Cifra | De dónde sale |
|---|---|
| 41 y 1 257 modos, 30.7× | Calculado con `W/λ = 20`, `k = 2π` |
| ERP 1.666 % a 3.410 % | `results/nb03_distance_pilot/nb03d_z10_validation/validation_summary.json`, recalculado en `verifica_cifras_tesis.py` |
| ERP 3×10⁻¹¹ del director | Su tesis, figura 5.3, página impresa 46 |
| Distancias y ópticas de Zárate | Su artículo, tablas I y II |
| Parámetros de Adán | Su tesis, §5.2 |

Las cifras del ERP y de los perfiles están en `verifica_cifras_tesis.py`, que
debe terminar en `0 discrepancias`. Las de este documento que **no** están
verificadas son las de la sección 3, porque describen algo que no se ha
ejecutado.
