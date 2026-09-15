# Citas sin copia local — lista de obtención manual

**Fecha:** 2026-09-15
**Estado:** 21 de 28 citas tienen PDF local y su contenido fue verificado. Estas
7 no. (Actualizado: se obtuvieron Alkhalifah et al. y Fang y Zhan, ambas de
acceso abierto.) **Todas existen y están correctamente citadas**; lo que falta es el
documento para comprobar que dicen lo que la tesis les atribuye.

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
- **Dónde:** biblioteca UJAT o préstamo interbibliotecario. No hay versión
  legal gratuita.

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
- **Dónde:** ScienceDirect (de pago). Acceso institucional UJAT, o escribir a
  los autores.

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

| Prioridad | Cuántas | Acción |
|---|---:|---|
| Alta | 2 | Goodman y Zhang: biblioteca o acceso institucional |
| ~~Acceso abierto~~ | ~~2~~ | **Obtenidas el 2026-09-15.** La de Fang reveló una atribución incorrecta, ya corregida en Cap2 |
| Baja, acceso institucional | 5 | Jin, McKay, Lagaris, Hornik, Nocedal |

Quedan **7** sin copia local, de las cuales sólo dos son de prioridad alta.
