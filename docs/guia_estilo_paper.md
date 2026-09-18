# Guía de estilo para el paper — extraída de los diez modelos

**Generado:** 2026-09-18
**Base:** los diez modelos de `ranking_referencias_locales.md`, leídos en su
texto real, no de memoria.
**Para:** `paper/papers_plantillas/CyS/fuente/{es,en}` y la edición de COMIA.

Esto es un **checklist**, no una reescritura. Cada punto sale de un paper
concreto que tienes en disco, y se cita cuál.

---

## 1. Cómo abren el abstract

Los diez usan una de cuatro aperturas. **Ninguna empieza con «En los últimos
años…».**

| Apertura | Quién la usa | Ejemplo |
|---|---|---|
| **El método, directo** | Andrés-Zárate 2019 | «Usando el método de propagación del espectro angular, se determinaron los modelos matemáticos…» |
| **Lo que hace el artículo** | Maiocchetti 2025 | «Este artículo presenta la aplicación de redes neuronales informadas por la física (PINN) para resolver…» |
| **Una dificultad conocida** | Carbajal-Domínguez 2010 | «It is a known fact that near field diffraction calculations are difficult to perform exactly.» |
| **Lo que hizo el trabajo previo, y dónde falla** | Sitzmann 2020, Krishnapriyan 2021 | «…current network architectures for such implicit neural representations are **incapable of** modeling signals with fine detail» |

**Para CyS en español, usa las dos primeras.** Son las de los dos papers
mexicanos del corpus, uno de ellos de tu director. Van al grano en la primera
cláusula.

## 2. Voz y tiempo verbal — y aquí los dos idiomas divergen

Esto no es preferencia, es convención de venue, y la tienes documentada en tu
propio corpus:

**En español: impersonal con «se».** Nunca primera persona.

> «se determinaron los modelos», «se establece la existencia», «se abordan dos
> casos prácticos», «se implementan redes neuronales», «se destaca el potencial»

**En inglés: primera persona del plural, activa.**

> «We propose to leverage…», «we demonstrate that…», «we show that…», «we
> analyze…»

Traducir el paper conservando el «se» impersonal en inglés lo vuelve rígido; y
traducir el «we» al español lo vuelve ajeno a la revista. **Son dos registros,
no uno traducido.**

## 3. Cómo reportar métricas — el modelo es Schoder

Schoder y Kraxberger 2024 hacen exactamente lo que tú necesitas: **dicen lo que
pierden y lo que ganan, en la misma frase, con rangos y no con un solo número.**

> «the training took **38h to 42.8h** (which is longer than the solution of the
> FEM simulation, which took **17min-19min**), and the inference took 0.05
> seconds being more than 20,000 times faster»

Tres cosas que copiar:

1. **Rango, no punto.** «38h a 42.8h», no «unas 40h». Tú tienes cinco pantallas:
   reporta media y rango, como ya haces con 3.161 ± 0.497 %.
2. **La desventaja va primero y entre paréntesis está la comparación.** No la
   esconde en la discusión.
3. **Dice contra qué compara y con qué herramienta** («openCFS», «same number of
   degrees of freedom»).

**Aplicación directa a tu problema con «acelerada»:** el entrenamiento cuesta
351.9 s por pantalla y el espectro angular es 18.5× más rápido en inferencia.
Schoder demuestra que eso se puede publicar — **diciéndolo**, no omitiéndolo.

## 4. Cómo matizar un resultado negativo — el modelo es Krishnapriyan

Estructura en tres movimientos, en un solo abstract:

1. **Enuncia el fallo sin suavizarlo:** «while existing PINN methodologies can
   learn good models for relatively trivial problems, they **can easily fail**
   to learn relevant physical phenomena for even slightly more complex problems»
2. **Localiza la causa, y descarta explícitamente la equivocada:** «Importantly,
   we show that these possible failure modes are **not due to** the lack of
   expressivity in the NN architecture, **but that** the PINN's setup makes the
   loss landscape very hard to optimize»
3. **Ofrece remedios, sin prometer que cierran el problema:** «two **promising**
   solutions»

Ese movimiento 2 es el que te falta y el que más te sirve: **decir qué NO es la
causa** es lo que convierte un resultado negativo en un hallazgo. Lo tienes ya
en dos sitios y conviene redactarlo así:

- el piso evanescente **no** es error del PINN, es la base modal
- la escala adaptativa de NB03C **no** baja porque los modos oscilen más
  despacio — `k_z,m` es constante

## 5. Cómo enunciar la contribución — el modelo es Sitzmann

Secuencia de verbos, en orden, sin adjetivos:

> propose → demonstrate → analyze → propose (a principled scheme) → show → combine

«We propose to leverage periodic activation functions… and demonstrate that
these networks, **dubbed** SIRENs, are ideally suited for…»

Dos cosas: **bautiza** lo que propone en la misma frase en que lo propone, y
cada verbo corresponde a una sección real del paper. Nada de «novel»,
«state-of-the-art» ni «superior».

Ya retiraste «superior al estado del arte» del paper. Este es el modelo de con
qué sustituirlo.

## 6. Estructura obligatoria por venue

**CyS y Rev. Mex. Fis. — bilingüe.** Andrés-Zárate y Maiocchetti llevan los dos
el mismo esqueleto:

```
Resumen (español)
Descriptores / Palabras clave
Abstract (inglés)
Keywords
[Rev. Mex. Fis. añade: PACS, DOI]
```

**No es el mismo texto traducido dos veces**: mira Andrés-Zárate, el abstract
inglés reordena las cláusulas. Y sí, trae un `resoults` mal escrito — el
bilingüe se revisa aparte, no se da por bueno porque el español esté bien.

## 7. Cómo posicionarse frente al trabajo previo

Alkhalifah 2021 abre con una afirmación grande pero **acotada a su campo**:

> «Solving the wave equation is one of the most (if not the most) fundamental
> problems we face as we try to illuminate the Earth using recorded seismic data»

El paréntesis «(if not the most)» es un matiz, no un adorno: **se cubre a sí
mismo mientras hace la afirmación.** Y la limita a «as we try to illuminate the
Earth» — no dice que sea el problema más importante de la física.

Tu equivalente honesto: acotar a Helmholtz 2D con campo complejo y pantalla
conocida, no a «simulación de speckle» en general.

---

## Checklist para aplicar

Marcar antes de dar por bueno un borrador:

- [ ] El abstract abre con el método o con lo que hace el artículo, no con «en los últimos años»
- [ ] Español impersonal con «se»; inglés en primera persona del plural
- [ ] Las cifras van con rango o desviación, no como valor único
- [ ] Donde hay una desventaja (tiempo de entrenamiento), se dice, con su comparación al lado
- [ ] Cada resultado negativo dice también **qué no es la causa**
- [ ] La contribución se enuncia con verbos que corresponden a secciones reales
- [ ] Sin «novel», «superior», «state-of-the-art», «acelerado» sin medición que lo respalde
- [ ] Bilingüe completo: Resumen, Palabras clave, Abstract, Keywords
- [ ] El inglés se revisó aparte, no se asumió correcto
- [ ] Las afirmaciones grandes están acotadas al alcance real: Helmholtz 2D, campo complejo, cinco pantallas conocidas

---

## Lo que esta guía NO autoriza

Ninguno de estos cambios puede ampliar el alcance. El paper valida **1D y 2D**,
por decisión tuya, y el speckle aparece sólo como trabajo futuro.
`verifica_paper_vs_tesis.py` lo vigila con 24 comprobaciones, incluidas «el
título no promete aceleración» y «el título no promete speckle».

**Correr el verificador después de cualquier reescritura.** Si el paper y la
tesis discrepan, se corrige el paper.
