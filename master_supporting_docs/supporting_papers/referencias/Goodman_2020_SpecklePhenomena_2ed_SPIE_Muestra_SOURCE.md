# Goodman — muestra oficial de la 2.ª edición

- **Título:** *Speckle Phenomena in Optics: Theory and Applications*
- **Autor:** Joseph W. Goodman
- **Editorial:** SPIE Press, Bellingham, Washington, **2.ª edición, 2020**
- **ISBN:** 9781510631489 (papel) · 9781510631496 (PDF)
- **LCCN:** 2019033832 · **Clasificación LC:** QC427.8.S64 G66 2020
- **Origen:** `https://spie.org/samples/PM312.pdf`, muestra oficial publicada
  por la editorial. Descargada el 2026-09-15.
- **Archivo local:** `Goodman_2020_SpecklePhenomena_2ed_SPIE_Muestra.pdf`,
  26 páginas.

## Qué contiene

Sólo los preliminares: página de créditos, **índice completo** y prefacio de la
segunda edición. **No incluye ningún capítulo.**

## Por qué está excluido del repositorio

Lleva la nota «All rights reserved. No part of this publication may be
reproduced or distributed in any form or by any means without written
permission of the publisher». Mismo criterio que la vista previa de Born y Wolf:
se conserva en disco para consulta y se excluye del repositorio público, que es
abierto. El enlace de arriba permite a cualquiera obtenerla por la vía legítima.

## Para qué sirve, pese a no traer capítulos

El índice da las **ubicaciones exactas** del material que la tesis cita, lo que
permite citar con precisión de sección y página aunque el texto se consulte por
otra vía:

| Contenido relevante | Ubicación en la 2.ª ed. |
|---|---|
| Camino aleatorio con gran número de pasos independientes (el argumento del teorema del límite central) | §2.2, p. 10 |
| **Propiedades estadísticas de primer orden del speckle óptico** | §3, p. 25 |
| **Estadística de primer orden de la intensidad y la fase** — aquí viven la exponencial negativa y `C = 1` | §3.2, p. 27 |
| Suma de dos intensidades de speckle independientes | §3.3.2, p. 46 |
| Suma de N intensidades independientes | §3.3.3, p. 50 |
| Efecto del tamaño de pupila y la rugosidad rms sobre el contraste | §5.10, p. 167 |
| **Contraste del speckle parcialmente desarrollado** | Apéndice B, p. 389 |

## Hallazgo relevante para esta tesis

El **Apéndice B, «Contrast of Partially Developed Speckle Intensity and
Phase»**, trata exactamente el régimen en el que trabaja NB03: la pantalla
implementada usa una desviación de fase de 2.0 rad, menor que 2π, de modo que el
speckle **no está completamente desarrollado**. Eso explica los contrastes
observados entre 0.78 y 1.22 por realización.

Ese apéndice es la referencia correcta para justificar formalmente ese régimen,
y no aparece citado en la tesis. Conviene consultarlo al obtener el libro
completo.

## Lo que esta muestra NO permite verificar

- Que `C = 1` se deduzca como la tesis lo enuncia (haría falta §3.2, p. 27).
- **Que el umbral `|C−1| < 0.1` no aparezca en el libro.** La tesis ya lo
  declara como tolerancia operativa propia, de modo que la afirmación está
  correctamente formulada; confirmarlo con el texto completo sería deseable pero
  no es indispensable.

## Nota sobre la edición

El `.bib` de la tesis cita la **1.ª edición (Roberts & Company, 2007)**. Esta
muestra es de la 2.ª (SPIE, 2020), que añade material sobre speckle polarizado,
speckle en el ojo y estadística de superficies «lisas». Si se adopta la 2.ª
edición como referencia, hay que actualizar la entrada `goodman2007speckle`
--incluida su clave, que lleva el año-- y revisar que los números de sección
citados correspondan a esa edición.
