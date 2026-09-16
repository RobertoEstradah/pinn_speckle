# Citas sin copia local — lista de obtención manual

**Fecha:** 2026-09-15
**Estado (recontado el 2026-09-15 contra el inventario real de PDFs):** la tesis
cita **28 claves**. De ellas **17 tienen copia local completa**, **2 la tienen
parcial** (Goodman: sólo preliminares de la 2.ª ed.; Born y Wolf: vista previa
legal con el capítulo 1) y **9 no tienen ninguna**.

El conteo anterior de esta ficha decía «21 de 28 … estas 7» y era **incorrecto**:
omitía tres claves sin copia --`wang2022ntk`, `karniadakis2021physics` y
`moseley2020wave`-- que se añaden abajo. **Todas las citas existen y están
correctamente referenciadas**; lo que falta es el documento para comprobar que
dicen lo que la tesis les atribuye.

Al conseguir cada una, guardarla en
`master_supporting_docs/supporting_papers/referencias/` con el patrón
`Apellido_etal_AÑO_TituloCorto.pdf`.

---

## Prioridad alta

### 1. Goodman (2007) — *Speckle Phenomena in Optics*

- **Autor:** Joseph W. Goodman
- **Editorial:** Roberts & Company, 2007. Englewood, CO
- **ISBN:** 978-0-9747077-9-7 (hay 2.ª ed., SPIE Press, 2020)
- **Usos:** 11 citas, en los cuatro capítulos
- **Por qué importa:** sostiene todo el criterio estadístico del trabajo —
  contraste `C = 1`, distribución exponencial de intensidad, speckle
  completamente desarrollado.
- **Qué hay que verificar en él:**
  - Capítulo 2–3: la deducción de que el campo es gaussiano circular por el
    teorema del límite central, y que de ahí sale `p(I)` exponencial y `C = 1`.
  - **Confirmar que el umbral `|C−1| < 0.1` NO aparece en el libro.** La tesis
    ya se corrigió para declararlo como tolerancia operativa propia; conviene
    confirmarlo con el texto en mano.
  - La condición sobre la desviación de fase del difusor (la tesis usa 2.0 rad).
- **Dónde conseguirlo (enlaces verificados el 2026-09-15):**

  | Vía | Enlace | Qué obtienes |
  |---|---|---|
  | ~~**Muestra oficial de SPIE**~~ **OBTENIDA** | `https://spie.org/samples/PM312.pdf` | 26 páginas de preliminares de la 2.ª ed.: créditos, **índice completo** y prefacio. **No trae capítulos.** Ver más abajo |
  | Espejo de la muestra | `https://www.spiedigitallibrary.org/samples/PM312.pdf` | Mismo archivo |
  | Ficha de la 2.ª edición | `https://spie.org/publications/book/2548482` | Índice completo y compra |
  | Vista previa de Google Books | `https://books.google.com/books/about/Speckle_Phenomena_in_Optics.html?id=TynXEcS0DncC` | Búsqueda dentro del libro: sirve para localizar páginas exactas y citar |
  | Biblioteca UJAT / préstamo interbibliotecario | — | El ejemplar completo |
  | Dr. Adán | — | Probablemente lo tenga; es doctor en óptica |

  **Ediciones:** 1.ª ed. Roberts & Company, 2007 (la que cita tu `.bib`).
  2.ª ed. SPIE Press, 2020, ISBN 9781510631489 (papel) y 9781510631496 (PDF),
  con material nuevo sobre speckle polarizado y estadística de superficies
  «lisas». Si consigues la 2.ª, actualiza la entrada del `.bib`.

  La vista previa de Google Books es la vía más rápida para **verificar el
  umbral**: busca «contrast» dentro del libro y comprueba si aparece alguna
  tolerancia numérica, o sólo `C = 1`.

- **Parcialmente obtenida el 2026-09-15.** La muestra de SPIE está en
  `referencias/Goodman_2020_SpecklePhenomena_2ed_SPIE_Muestra.pdf` (excluida del
  repositorio: lleva «All rights reserved»; ver el `_SOURCE.md` que la acompaña).
  Trae sólo preliminares, de modo que **no verifica ninguna de las tres cosas de
  la lista de arriba**. Lo que sí aporta:

  - Las **ubicaciones exactas** para citar con sección y página en la 2.ª ed.:
    camino aleatorio §2.2 p. 10; estadística de primer orden §3 p. 25; intensidad
    y fase §3.2 p. 27 (ahí viven la exponencial y `C = 1`); pupila y rugosidad
    frente al contraste §5.10 p. 167.
  - Un hallazgo: la 2.ª ed. tiene un **Apéndice B, «Contrast of Partially
    Developed Speckle Intensity and Phase», p. 389**, que trata exactamente el
    régimen de NB03 --la pantalla usa 2.0 rad de desviación de fase, por debajo
    de 2π, así que el speckle no está completamente desarrollado--. Es la
    referencia correcta para justificar ese régimen y hoy no está citada.
  - Confirmación de que la 2.ª ed. es de SPIE Press, 2020, ISBN 9781510631489.
    Si se adopta, hay que actualizar la clave `goodman2007speckle` del `.bib`.

  Sigue haciendo falta el **texto completo** para cerrar §3.2 y el umbral.

### 2. Zhang et al. (2025) — FE-PIRBN

- **Autores:** Huajian Zhang, Chao Li, Rui Xia, Xinhai Chen, Tiaojie Xiao,
  Xiao-Wei Guo, Jie Liu
- **Publicación:** *Journal of Computational Physics* **527**, 113798 (2025)
- **DOI:** `10.1016/j.jcp.2025.113798`
- **Usos:** 2 (Cap2 y Cap4)
- **Por qué importa:** Cap4 le atribuye en la tabla comparativa un error `L²`
  **entre 1.40 % y 5.82 %**. Ese rango **ya se verificó contra el resumen
  publicado**, pero no es reproducible desde el repositorio.
- **Qué hay que verificar:** que el rango corresponda a la métrica y al tipo de
  referencia que la tabla comparativa declara.
- **Dónde conseguirlo (enlaces verificados el 2026-09-15):**

  | Vía | Enlace |
  |---|---|
  | Artículo en ScienceDirect (de pago) | `https://www.sciencedirect.com/science/article/abs/pii/S0021999125000816` |
  | Resolutor DOI | `https://doi.org/10.1016/j.jcp.2025.113798` |
  | Ficha en NASA ADS | `https://ui.adsabs.harvard.edu/abs/2025JCoPh.52713798Z/abstract` |
  | Acceso institucional UJAT a Elsevier | — |

  **No existe preprint. Confirmado dos veces**, el 2026-09-15 y el 2026-09-16,
  en arXiv y en buscadores académicos. El antecedente PIRBN sí está abierto
  (arXiv:2304.06234), pero es otro artículo y no contiene la cifra que la tesis
  cita.

  **Lo que sí se pudo verificar del resumen publicado (2026-09-16):** el rango
  1.40–5.82 % corresponde a dispersión electromagnética de **uno y dos
  cilindros** a escala sub-longitud de onda, contrastada con simulación
  numérica. Ese contexto ya se incorporó a la nota (c) de `tab:comparativa` en
  Cap4, junto con la declaración explícita de que es la única cifra de esa tabla
  cuya fuente primaria no se tuvo a la vista.

  **Sigue siendo la prioridad número uno de esta lista**, porque es la única
  referencia sin copia local que sostiene un número dentro de la tesis.

  **La vía más efectiva es escribir a los autores**, que pueden compartir su
  propio trabajo legítimamente. Los correos están en la primera página del
  artículo; la afiliación se ve en la ficha de ADS. Borrador:

  > Asunto: Request for a copy of your JCP paper on FE-PIRBN
  >
  > Dear Dr. Zhang,
  >
  > I am a master's student at Universidad Juárez Autónoma de Tabasco, working
  > on physics-informed neural networks for the Helmholtz equation. I would like
  > to cite your paper *FE-PIRBN* (J. Comput. Phys. 527, 113798) in my thesis,
  > in particular the reported L² error range of 1.40–5.82%. Unfortunately I do
  > not have institutional access to ScienceDirect. Would you be willing to
  > share a copy?
  >
  > Thank you for your time.

---

## Prioridad media — detectadas en el recuento del 2026-09-15

Las tres se omitieron en la revisión anterior. Ninguna sostiene una cifra de la
tesis, pero las dos primeras hacen una afirmación de contenido sobre lo que sus
autores hicieron, que es exactamente la clase de afirmación que falló en el caso
de Fang y Zhan.

### 2b. Moseley, Markham y Nissen-Meyer (2020) — Ecuación de onda con PINNs
- arXiv:2006.11894 · **Acceso abierto**
- **Usos:** 1 (Cap2) · Afirmación: «aplicaron PINNs para resolver la ecuación de
  onda acústica 2D en modelos de velocidad variables»
- **Cuidado:** en `referencias/NB03/` hay un `Moseley_etal_2023_FBPINNs.pdf`, que
  es **otro artículo** de los mismos autores. No sirve para verificar esta cita.
- Descargable: `https://arxiv.org/pdf/2006.11894`

### 2c. Wang, Yu y Perdikaris (2022) — Perspectiva NTK
- *Journal of Computational Physics* **449**, 110768 · DOI `10.1016/j.jcp.2021.110768`
- Preprint **abierto**: arXiv:2007.14527
- **Usos:** 2 (Cap2 y Cap4) · La tesis **aplica su método**: la
  Sección~`sec:ntk_analisis` de Cap4 calcula la traza NTK física/datos. Las
  cifras son propias, no atribuidas a ellos, pero conviene tener el texto para
  respaldar cómo se aplica.
- **Cuidado:** `referencias/NB03/Wang_etal_2021_PINN_gradient_pathologies.pdf`
  corresponde a `wang2021failure`, que es **otra** cita. No confundir.
- Descargable: `https://arxiv.org/pdf/2007.14527`

### 2d. Karniadakis et al. (2021) — Aprendizaje automático informado por física
- *Nature Reviews Physics* **3**, 422–440 · DOI `10.1038/s42254-021-00314-5`
- **Usos:** 1 (Cap2) · Afirmación: es una revisión extensa del tema. De contexto,
  sin cifras.
- De pago, sin preprint en arXiv. Acceso institucional UJAT o biblioteca.

---

## Prioridad baja — citas de contexto, sin cifras atribuidas

Ninguna sostiene un número de la tesis. Conviene tenerlas, pero no comprometen
ninguna afirmación cuantitativa.

### 3. Jin (2014) — *The Finite Element Method in Electromagnetics*
- Jian-Ming Jin. John Wiley & Sons, 3.ª ed., 2014
- **Usos:** 2 (Cap1, Cap2) · Afirmación: costo del mallado sub-longitud de onda
- Biblioteca. Relevante también para NB04.

### 4. McKay, Beckman y Conover (1979) — Muestreo por hipercubo latino
- *Technometrics* **21**(2), 239–245 · DOI `10.1080/00401706.1979.10489755`
- **Usos:** 3 (Cap1, Cap2, Cap3) · Afirmación: propiedades del LHS
- JSTOR / Taylor & Francis. Acceso institucional.

### 5. Lagaris, Likas y Fotiadis (1998) — Redes neuronales para EDO y EDP
- *IEEE Transactions on Neural Networks* **9**(5), 987–1000 · DOI `10.1109/72.712178`
- **Usos:** 1 (Cap2) · Afirmación: función de prueba que satisface las
  condiciones de frontera exactamente
- IEEE Xplore. **Nota:** esta afirmación ya está corroborada indirectamente —
  Sukumar y Srivastava (2021), que sí está en local, la describe en su §1.

### 6. Hornik, Stinchcombe y White (1989) — Aproximación universal
- *Neural Networks* **2**(5), 359–366 · DOI `10.1016/0893-6080(89)90020-8`
- **Usos:** 1 (Cap2) · Afirmación estándar del teorema
- ScienceDirect.

### 7. Nocedal y Wright (2006) — *Numerical Optimization*
- Springer, 2.ª ed., 2006
- **Usos:** 1 (Cap2) · Afirmación: L-BFGS como método cuasi-Newton
- Biblioteca. El PDF circula ampliamente.

### ~~8. Alkhalifah et al. (2021) — Soluciones de campo de onda~~ OBTENIDA
- *Artificial Intelligence in Geosciences* **2**, 11–19 · DOI `10.1016/j.aiig.2021.08.002`
- **Usos:** 1 (Cap2)
- **OBTENIDA** el 2026-09-15 como preprint arXiv:2106.01433v1, 23 páginas, en
  `arxiv_verificacion/Alkhalifah_etal_2021_WavefieldHelmholtz.pdf`. ScienceDirect
  bloquea la descarga automatizada; el preprint tiene los mismos cuatro autores.
  **Nota:** el título del preprint es *Wavefield solutions from machine learned
  functions*, sin el sufijo *constrained by the Helmholtz equation* que añadió la
  versión publicada. **Afirmación verificada:** Cap2 le atribuye usar Helmholtz
  como restricción en la función de pérdida, y el abstract lo confirma.

### ~~9. Fang y Zhan (2020) — PINNs para diseño de metamateriales~~ OBTENIDA
- *IEEE Access* **8**, 24506–24513 · DOI `10.1109/ACCESS.2019.2963375`
- **Usos:** 1 (Cap2)
- **OBTENIDA** el 2026-09-15 de IEEE Xplore (documento 8946546), en
  `referencias/Fang_Zhan_2020_DeepPINN_MetamaterialDesign.pdf`.
- **La sospecha se confirmó.** Cap2 decía que aplicaron PINNs a «dispersión de
  ondas en medios inhomogéneos 2D». El abstract real: proponen un enfoque de
  PINN para *diseño de metamateriales electromagnéticos* (encubrimiento,
  rotadores, concentradores) y, «as a byproduct», un método para la ecuación de
  Helmholtz de alta frecuencia. **Cap2 ya fue corregido.**

---

## Resumen

Inventario verificado contra `master_supporting_docs/supporting_papers/referencias/`
el 2026-09-15.

| Prioridad | Cuántas | Acción |
|---|---:|---|
| Alta | 2 | Goodman y Zhang: biblioteca o acceso institucional. De Goodman ya se tienen los preliminares de la 2.ª ed. (índice y paginación), no el texto |
| ~~Acceso abierto~~ | ~~2~~ | **Obtenidas el 2026-09-15.** La de Fang reveló una atribución incorrecta, ya corregida en Cap2 |
| Media | 3 | Moseley y Wang (NTK): **acceso abierto en arXiv**. Karniadakis: de pago |
| Baja, acceso institucional | 5 | Jin, McKay, Lagaris, Hornik, Nocedal |

**Actualizado el 2026-09-16: quedan 6 sin copia local.** Se obtuvieron Moseley (arXiv:2006.11894) y Wang, Yu y Perdikaris (arXiv:2007.14527), y ambas atribuciones se verificaron contra el texto. De las 6 restantes, **sólo Zhang sostiene una cifra de la tesis**; las otras cinco --Jin, McKay, Lagaris, Hornik y Nocedal-- son de contexto. A ellas se suman 2 con copia parcial (Goodman y Born y Wolf).

De las 28 claves citadas, **22 tienen copia local verificable**.


---

## Plan B: si no llegan a tiempo

Ninguna de las dos bloquea la tesis. Basta declarar el alcance de la
verificación.

**Zhang et al.** — nota al pie en la tabla comparativa de Cap4:

> El rango reportado se verificó contra el resumen publicado del artículo; no se
> dispuso del texto completo para comprobar la configuración experimental a la
> que corresponde.

**Goodman** — ya está cubierto. La tesis declara en Cap3 y Cap4 que la
tolerancia `|C−1| < 0.1` es una decisión operativa de este trabajo y no un
umbral publicado por ese autor, que es exactamente la afirmación que requeriría
el libro para sostenerse. Citar un texto canónico sin tener el ejemplar es
práctica habitual; lo que no se puede es atribuirle un umbral que no da, y eso
ya se corrigió.
