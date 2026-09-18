# Puntos abiertos del Capítulo 1 — para revisión con el Dr. Adán

**Autor:** Roberto Hernández Estrada
**Fecha:** 18 de septiembre de 2026

> Este `.md` es la fuente editable. El entregable que se imprime es
> `reunion_dr_adan_puntos_abiertos.pdf`, compilado desde el `.tex`. **Si se edita
> uno, editar el otro**: son dos copias del mismo documento y divergen solas.

El Capítulo 1 (Generalidades) conserva el planteamiento del protocolo de octubre
de 2025. El trabajo realizado desde entonces cambió el método, y hay
afirmaciones del capítulo que el código ya no respalda.

**Los puntos 1 y 2 ya se resolvieron** en la conversación del 18 de septiembre y
están aplicados: el título y el objetivo general. Los tres restantes siguen
abiertos y se presentan aquí con su texto actual, lo que muestran los
resultados, y la decisión concreta que hay que tomar.

---

## Dónde está el trabajo hoy

| Experimento | Resultado | Estado |
|---|---|---|
| NB01 — Helmholtz 1D | L² = 0.006 % | Cerrado |
| NB02 — Helmholtz 2D, campo complejo | L² = 0.171 % | Cerrado |
| NB02B — puente de arquitectura | L² = 0.0078 % | Cerrado |
| NB03 — speckle en z=1λ | L² = 3.161 %, 5/5 | Cerrado |
| NB03B — speckle en z=2λ | L² = 0.993 %, 5/5 | Cerrado |
| NB03C — speckle hasta z=5λ | L² = 2.244 %, 5/5 | Cerrado |
| NB03D — speckle hasta z=10λ | L² = 2.617 %, 5/5 | Cerrado |
| **NB04 — benchmark contra FEM** | — | **No iniciado** |

La tesis está en 81 páginas, sin errores de compilación, y 369 cifras del texto
se verifican automáticamente contra los archivos de resultados que las
generaron.

**Novedad desde la última versión de este documento:** la cadena de subdominios
se extendió a z=10λ con diez bloques, reutilizando sin reentrenar el tramo 0–5λ
ya validado. Duplicar la distancia eleva el error de 2.244 % a 2.617 % (un
incremento de 0.373 puntos por cinco bloques adicionales), con las cinco
pantallas aceptadas. Una cadena de veinte bloques hasta 20λ, ensayada sobre una
sola pantalla y sin refinamiento, *no* alcanza el criterio (8.743 %).

**El hallazgo que condiciona todo lo demás:** la formulación directa que
planteaba el protocolo resultó estar **mal planteada**. Cumplía la ecuación de
Helmholtz a 10⁻¹⁴ y la frontera exactamente, y aun así daba **92.75 % de
error**: sin condición de radiación el problema admite infinitas soluciones. Se
sustituyó por una formulación modal con condición de Cauchy dura, que es la
regularización canónica de este problema (Nguyen et al., 2014).

---

## 1. El título *(resuelto el 18/09)*

### Texto anterior

> Simulación **acelerada** de speckle óptico: **Un enfoque basado** redes
> neuronales físicamente informadas (PINN's)

### Qué dice el trabajo

- **«Acelerada» no tiene respaldo.** El factor de aceleración se define contra
  FEM, y ese benchmark no se ha hecho. Lo que sí está medido es la comparación
  contra el espectro angular: **18.5× a favor del espectro angular** para un
  plano, y **1.76× a favor de la PINN** para 101 planos simultáneos. Es un
  resultado condicional, y un título no admite condiciones.
- El **8 de septiembre** usted pidió quitar «acelerada» y «un enfoque basado».
- «(PINN's)» lleva un apóstrofo que no corresponde al plural.

### Decisión

Propuesta, 14 palabras:

> **Simulación del speckle óptico mediante Redes Neuronales Informadas por
> Física: formulación modal de Helmholtz**

La parte anterior a los dos puntos es la que quedó acordada en esa llamada. El
añadido es propuesta mía: **la formulación modal es precisamente lo que
distingue el trabajo entregado del que prometía el protocolo**, y es lo que lo
separa de Panagiotakopoulos et al. (2026), que valida cualitativamente sin dar
cifras.

**Aprobado y aplicado.** El título figura ya en la portada, y se añadió al
Dr. Noel Zacarías Morales como coasesor. Se conserva aquí el razonamiento porque
sostiene los puntos 2 y 3.

---

## 2. El objetivo general *(resuelto el 18/09)*

### Texto anterior (Cap. 1, *Objetivo general*)

> …para la simulación acelerada y físicamente precisa de patrones de speckle
> óptico, mediante la **resolución directa** de la ecuación de Helmholtz
> bidimensional con campo eléctrico complejo.

### Qué dice el trabajo

La resolución directa es exactamente el enfoque que **se abandonó**. El método
vigente expande el campo en serie de Fourier (exacta, por las fronteras
laterales periódicas) y resuelve 41 ecuaciones diferenciales ordinarias
desacopladas, una por modo propagante.

### Decisión

> …para la simulación **físicamente precisa** de patrones de speckle óptico,
> mediante una **formulación modal** de la ecuación de Helmholtz bidimensional
> con campo eléctrico complejo, en la que la condición de Cauchy se impone por
> construcción.

**Aplicado.** Sale también «acelerada», por la misma razón que del título. Se
retiró además el adjetivo «directa» de la segunda contribución (Cap. 1), donde
significaba resolver la física frente a ajustar datos medidos: el sentido era
correcto, pero colisionaba con el que «resolución directa» tiene en los
Capítulos 3 y 4. Cap. 1 ya no contiene ninguna de las dos expresiones.

---

## 3. La hipótesis (ii) no tiene respuesta

### Texto actual

> (ii) obtener un factor de aceleración S = T_FEM / T_PINN > 1 en la fase de
> inferencia

### Qué dice el trabajo

NB04 no se ha hecho, así que **la hipótesis (ii) queda sin contestar**. Tres
obstáculos concretos:

1. **FEniCSx no corre en Windows nativo.** Requiere WSL2 o Docker, no
   instalados.
2. **La comparación está condicionada** por el propio Capítulo 1 a que el
   problema se formule con fronteras absorbentes (ver punto 4).
3. **El resultado sería probablemente desfavorable.** El entrenamiento cuesta
   351.9 s por pantalla, y el espectro angular ya resultó más rápido en
   evaluación de un solo plano.

Conviene señalar que el protocolo de octubre pedía **una aceleración de al menos
10×**; el texto actual de la tesis la relajó a «mayor que 1». Esa rebaja está en
el documento y conviene decidirla explícitamente.

### Decisión — tres opciones

| Opción | Qué implica |
|---|---|
| **A.** Hacer NB04 | Instalar WSL2 o Docker. Cierra la hipótesis, sea cual sea el resultado. Requiere resolver antes el punto 4 |
| **B.** Reformular | Cambiarla por el benchmark que sí está hecho: evaluación libre de malla frente a una referencia de propagación. Honesto, y ya está medido |
| **C.** Trabajo futuro | Dejarla enunciada y explicar en Cap. 5 por qué no se resolvió |

Mi lectura: la contribución de la tesis quedó en **precisión y buen
planteamiento**, no en velocidad. El Capítulo 4 ya está escrito en esos
términos.

### Existe un precedente, y es de esta misma dirección

La tesis de Gabriel Omar Domínguez Ruiz, aprobada el 9 de julio de 2026 bajo su
dirección, se topó con esta misma cuestión y la resolvió. Su Sección 3.4 compara
contra métodos clásicos y **el resultado le es desfavorable**: Runge–Kutta
alcanza errores de 10⁻⁹ en milisegundos y las diferencias finitas llegan a
10⁻⁶, frente al 0.2 % de sus PINN. Su redacción:

> …la aportación de las PINN **no debe entenderse como una superioridad en
> exactitud puntual o en velocidad de cálculo**, sino en la *naturaleza* de la
> solución que cada enfoque produce.

> La comparación **no es una competencia por la menor cifra de error** (en una
> sola corrida, los métodos numéricos son rápidos y muy precisos), sino el
> reconocimiento de **dos objetos distintos**.

Desplazó la afirmación de velocidad a diferenciabilidad y ausencia de malla, y
lo acompañó de una tabla comparativa cualitativa. Ese planteamiento ya pasó por
el comité.

Este trabajo está además en mejor posición que aquél en un punto: **el benchmark
contra la referencia de propagación ya está hecho**, y arroja 1.76× a favor de
la PINN en evaluación de 101 planos simultáneos. No se partiría de cero.

**¿Qué opción se toma?**

---

## 4. Fronteras absorbentes frente a periódicas

### Texto actual (Cap. 1, *Alcances*)

> Se realizará una evaluación comparativa del tiempo de inferencia contra una
> referencia numérica de propagación y, **cuando el problema se formule con
> fronteras absorbentes**, contra una implementación FEM.

### Qué dice el trabajo

NB03 usa **fronteras laterales periódicas**, y no por comodidad: la periodicidad
es lo que hace que la serie de Fourier sea **exacta** y que los 41 modos queden
desacoplados. Cambiarlas a absorbentes destruiría la formulación modal entera.

Es decir: **la condición que el Capítulo 1 pone para comparar contra FEM es
incompatible con el método que la tesis usa.**

### Decisión

- **A.** Retirar la condición, y comparar contra FEM con fronteras periódicas
- **B.** Mantenerla, aceptando que NB04 exige reformular el problema
- **C.** Retirar la mención a FEM del alcance, coherente con el punto 3

**¿Cuál?**

---

## Una oportunidad, no un problema

El protocolo incluía una tercera pregunta de investigación que la tesis ya no
plantea:

> ¿Cómo impacta la complejidad del medio difusor (rugosidad de la superficie) en
> la precisión y el tiempo de entrenamiento del modelo PINN?

**Hay material para contestarla.** Existen en disco referencias generadas con
cinco longitudes de correlación distintas (0.10, 0.20, 0.30, 0.40 y 0.50 λ), y
la tesis sólo reporta la de 0.10λ.

Recuperar esa pregunta costaría un barrido comparativo, sin formulación nueva ni
arquitectura nueva. **¿Vale la pena, o se deja fuera del alcance?**

---

## Resumen de decisiones

| # | Punto | Decisión pedida |
|---|---|---|
| 1 | Título | *Resuelto el 18/09: aprobado y aplicado* |
| 2 | Objetivo general | *Resuelto el 18/09: aplicado* |
| 3 | Hipótesis (ii) | ¿Hacer NB04, reformular, o declarar trabajo futuro? |
| 4 | Fronteras absorbentes | ¿Retirar la condición, mantenerla, o quitar FEM del alcance? |
| 5 | Rugosidad | ¿Se recupera la pregunta del protocolo? |

El **punto 4 condiciona al 3**: no se puede decidir sobre NB04 sin resolver
antes la cuestión de las fronteras, porque la comparación con FEM está
condicionada en el propio Capítulo 1 a un planteamiento que la tesis no usa.
