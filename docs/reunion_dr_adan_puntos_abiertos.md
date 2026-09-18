# Puntos abiertos del Capítulo 1 — para revisión con el Dr. Adán

**Preparado:** 2026-09-18
**Autor:** Roberto Hernández Estrada
**Motivo:** el Capítulo 1 (Generalidades) conserva el planteamiento del protocolo
de octubre de 2025. El trabajo realizado desde entonces cambió el método, y hay
cuatro afirmaciones del capítulo que el código ya no respalda.

**Ninguna se ha modificado.** Este documento presenta cada una con su texto
actual, lo que muestran los resultados, y la decisión concreta que hay que tomar.

---

## Dónde está el trabajo hoy

| Experimento | Resultado | Estado |
|---|---|---|
| NB01 — Helmholtz 1D | $L^2 = 0.006\%$ | Cerrado |
| NB02 — Helmholtz 2D, campo complejo | $L^2 = 0.171\%$ | Cerrado |
| NB02B — puente de arquitectura | $L^2 = 0.0078\%$ | Cerrado |
| NB03 — speckle en $z=1\lambda$ | $L^2 = 3.161\%$, 5/5 aceptadas | Cerrado |
| NB03B — speckle en $z=2\lambda$ | $L^2 = 0.993\%$, 5/5 aceptadas | Cerrado |
| NB03C — speckle hasta $z=5\lambda$ | $L^2 = 2.244\%$, 5/5 aceptadas | Cerrado |
| **NB04 — benchmark contra FEM** | — | **No iniciado** |

La tesis está en 78 páginas, sin errores de compilación, y 292 cifras del texto
se verifican automáticamente contra los archivos de resultados que las generaron.

**El hallazgo que condiciona todo lo demás:** la formulación directa que
planteaba el protocolo resultó estar **mal planteada**. Cumplía la ecuación de
Helmholtz a $10^{-14}$ y la frontera exactamente, y aun así daba **92.75 % de
error**: sin condición de radiación el problema admite infinitas soluciones. Se
sustituyó por una formulación modal con condición de Cauchy dura, que es la
regularización canónica de este problema (Nguyen et al., 2014).

---

## Punto 1 — El título

### Texto actual

> *Simulación **acelerada** de speckle óptico: **Un enfoque basado** redes
> neuronales físicamente informadas (PINN's)*

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

**¿Se acepta el subtítulo, o se deja sólo la parte corta?**

---

## Punto 2 — El objetivo general dice «resolución directa»

### Texto actual (Cap. 1, sección *Objetivo general*)

> «…para la simulación acelerada y físicamente precisa de patrones de speckle
> óptico, mediante la **resolución directa** de la ecuación de Helmholtz
> bidimensional con campo eléctrico complejo.»

### Qué dice el trabajo

La resolución directa es exactamente el enfoque que **se abandonó**. El método
vigente expande el campo en serie de Fourier —exacta, por las fronteras
laterales periódicas— y resuelve 41 ecuaciones diferenciales ordinarias
desacopladas, una por modo propagante.

El objetivo general, tal como está, describe un método que la tesis ya no usa.

### Decisión

Propuesta:

> «…mediante una **formulación modal** de la ecuación de Helmholtz bidimensional
> con campo eléctrico complejo, con la condición de Cauchy impuesta por
> construcción.»

**¿Se corrige, o se prefiere otra redacción?**

---

## Punto 3 — La hipótesis (ii) no tiene respuesta

### Texto actual

> «(ii) obtener un factor de aceleración $S = T_{FEM} / T_{PINN} > 1$ en la fase
> de inferencia»

### Qué dice el trabajo

NB04 no se ha hecho, así que **la hipótesis (ii) queda sin contestar**. Tres
obstáculos concretos:

1. **FEniCSx no corre en Windows nativo.** Requiere WSL2 o Docker, no instalados.
2. **La comparación está condicionada** por el propio Capítulo 1 a que el
   problema se formule con fronteras absorbentes (ver punto 4).
3. **El resultado sería probablemente desfavorable.** El entrenamiento cuesta
   351.9 s por pantalla, y el espectro angular ya resultó más rápido en
   evaluación de un solo plano.

Conviene señalar que el protocolo de octubre pedía **una aceleración de al menos
10×**; el texto actual de la tesis la relajó a «mayor que 1». Esa rebaja está en
el documento y conviene decidirla explícitamente.

### Decisión — tres opciones

| | Qué implica |
|---|---|
| **A. Hacer NB04** | Instalar WSL2 o Docker. Cierra la hipótesis, sea cual sea el resultado. Requiere resolver antes el punto 4 |
| **B. Reformular la hipótesis** | Cambiarla por el benchmark que sí está hecho: evaluación libre de malla frente a una referencia de propagación. Honesto, y ya está medido |
| **C. Declararla trabajo futuro** | Dejarla enunciada y explicar en Cap. 5 por qué no se resolvió |

Mi lectura: la contribución de la tesis quedó en **precisión y buen
planteamiento**, no en velocidad. El Capítulo 4 ya está escrito en esos términos.

**¿Qué opción se toma?**

---

## Punto 4 — Fronteras absorbentes frente a periódicas

### Texto actual (Cap. 1, *Alcances*)

> «Se realizará una evaluación comparativa del tiempo de inferencia contra una
> referencia numérica de propagación y, **cuando el problema se formule con
> fronteras absorbentes**, contra una implementación FEM.»

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

> «¿Cómo impacta la complejidad del medio difusor (rugosidad de la superficie)
> en la precisión y el tiempo de entrenamiento del modelo PINN?»

**Hay material para contestarla.** Existen en disco referencias generadas con
cinco longitudes de correlación distintas —0.10, 0.20, 0.30, 0.40 y 0.50 λ—, y
la tesis sólo reporta la de 0.10λ.

Recuperar esa pregunta costaría un barrido comparativo, sin formulación nueva ni
arquitectura nueva. **¿Vale la pena, o se deja fuera del alcance?**

---

## Resumen de decisiones

| # | Punto | Decisión pedida |
|---|---|---|
| 1 | Título | ¿Se acepta el subtítulo «formulación modal de Helmholtz»? |
| 2 | Objetivo general | ¿Se corrige «resolución directa» → «formulación modal»? |
| 3 | Hipótesis (ii) | ¿Hacer NB04, reformular, o declarar trabajo futuro? |
| 4 | Fronteras absorbentes | ¿Retirar la condición, mantenerla, o quitar FEM del alcance? |
| 5 | Rugosidad | ¿Se recupera la pregunta del protocolo? |

Los puntos **2 y 3 están ligados**: si la hipótesis (ii) se reformula, el
objetivo general debe decir lo mismo. Y el **4 condiciona al 3**: no se puede
decidir sobre NB04 sin resolver antes la cuestión de las fronteras.
