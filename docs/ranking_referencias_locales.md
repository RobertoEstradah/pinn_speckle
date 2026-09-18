# Ranking de las referencias locales por impacto de su venue

**Generado:** 2026-09-18
**Alcance:** los 42 papers de referencia que hay en
`master_supporting_docs/supporting_papers/referencias/` (excluye tus propios
documentos, el protocolo, la tesis del Dr. Adán y las plantillas de slides).
**Métrica:** SJR y cuartil de SCImago, consultados vía búsqueda web el 18/09/2026.

---

## Cómo leer esto, antes de usarlo

**1. El venue sale del `.bib` de la tesis, no del PDF.** La mayoría de tus copias
locales son **preprints de arXiv**, no la versión publicada. Que el PDF diga
`arXiv:1711.10561` no significa que el trabajo no esté en *Journal of
Computational Physics* — Raissi et al. es exactamente ese caso. Para las 28
entradas citadas, el venue viene de `references.bib`, que está curado. Para las
demás, del propio PDF.

**2. SCImago bloquea el acceso automatizado.** Tiene verificación anti-bot y no
la sorteé. Los números vienen de búsqueda web sobre agregadores que citan a
SCImago. **Donde no conseguí una cifra fiable, la celda dice `—`, no un número
inventado.**

**3. Congresos y preprints no tienen SJR.** NeurIPS, ICML e ICLR se rankean por
h5-index o CORE, que es otra escala. Van en tabla aparte. Compararlos con
revistas en una sola columna sería falso.

**4. Y lo más importante: este ranking NO dice qué estilo copiar.** Está aquí
para decidir *dónde publicar*. Los modelos de redacción se eligen por cercanía de
venue y de tema — ver la sección final.

---

## Tabla A — Revistas, ordenadas por SJR

| # | Venue | SJR | Cuartil | h-index | Papers locales |
|---|---|---|---|---|---|
| 1 | Nature Reviews Physics | 9.803 | Q1 | 87 | Karniadakis et al. 2021 *(citado, sin copia local)* |
| 2 | IEEE Trans. Neural Networks & Learning Systems | 3.686 | Q1 | 234 | Lagaris et al. 1998 *(sin copia local)* |
| 3 | Computer Methods in Applied Mechanics and Eng. | 2.412 | Q1 | 217 | Sukumar & Srivastava 2022 |
| 4 | Journal of Computational Physics | 1.552 | Q1 | 321 | **Raissi et al. 2019** · Wang, Yu & Perdikaris 2022 · **Zhang et al. 2025** |
| 5 | Neural Networks (Elsevier) | 1.491 | Q1 | 186 | Hornik et al. 1989 *(sin copia local)* |
| 6 | Artificial Intelligence in Geosciences | 0.907 | Q1 | — | Alkhalifah et al. 2021 |
| 7 | IEEE Access | 0.849 | Q1 | 338 | Fang & Zhan 2020 |
| 8 | Optics Express | 0.836 | Q1 | 341 | Chen, Lu, Karniadakis & Dal Negro 2020 |
| 9 | Sensors (MDPI) | — | Q1 | — | Jayabarathi & Ratnam 2022 |
| 10 | SIAM Review | — | Q1 | — | Lu et al. 2021 (DeepXDE) |
| 11 | Journal of Machine Learning Research | — | Q1 | — | Wang et al. 2024 (PirateNets) · Baydin et al. 2018 |
| 12 | SIAM J. on Scientific Computing | — | Q1 | — | Wang et al. 2021 (gradient pathologies) |
| 13 | Journal of Scientific Computing | — | Q1 | — | Cuomo et al. 2022 |
| 14 | Technometrics | — | — | — | McKay et al. 1979 *(sin copia local)* |
| 15 | **Revista Mexicana de Física** | 0.211 | Q3–Q4 | 36 | **Andrés-Zárate et al. 2019** |
| 16 | **Computación y Sistemas** | 0.188 | Q3–Q4 | — | *(ninguno — es tu revista objetivo)* |

Las fuentes discrepan entre Q3 y Q4 para las dos últimas, según el año y la
categoría. Lo dejo como rango en lugar de elegir el que más convenga.

## Tabla B — Congresos y preprints (sin SJR)

| Venue | Tipo | Papers locales |
|---|---|---|
| NeurIPS | Congreso top-tier | **Sitzmann et al. 2020 (SIREN)** · Krishnapriyan et al. 2021 · Tancik et al. 2020 |
| ICML | Congreso top-tier | Rahaman et al. 2019 · Rathore et al. 2024 |
| ICLR | Congreso top-tier | Kingma & Ba 2015 (Adam) |
| XX Simposio CEA de Control Inteligente (Huelva, 2025) | Congreso, **en español** | Maiocchetti et al. 2025 |
| arXiv, sin venue confirmado | Preprint | Dolean 2023 · MHPINN 2026 · Panagiotakopoulos 2026 · Schoder & Kraxberger 2024 · SpectralAnalysis 2025 · Wang 2021 (Fourier) · Wang 2024 (causality) · Cai & Xu 2020 · Costabal 2024 · Jagtap & Karniadakis 2020 · Kharazmi 2021 · Moseley 2020 y 2023 · Wang 2023 · Nguyen 2014 · Veerababu & Ghosh 2025 · Xiong 2025 |
| Por confirmar | Artículo | Carbajal-Domínguez et al. 2010 — **autores de la UJAT** |

## Tabla C — Libros

| Obra | Editorial |
|---|---|
| Born & Wolf, *Principles of Optics* (1999) | Cambridge University Press |
| Goodman, *Speckle Phenomena in Optics* (2020) | SPIE |
| Jin, *The Finite Element Method in Electromagnetics* (2014) | Wiley |
| Nocedal & Wright, *Numerical Optimization* (2006) | Springer |
| Thuerey et al., *Physics-based Deep Learning* (2021) | Libro en línea |
| Andrés-Zárate et al. 2024 | Capítulo de libro |

---

## Los diez modelos de redacción

**No son los diez de más impacto.** Elegidos por dos criterios: que el venue se
parezca a CyS o COMIA en extensión y formato, y que el tema sea cercano
(PINNs, Helmholtz, óptica).

Por qué no por impacto: tú escribes 9 páginas para una revista mexicana de
computación Q3, y para un congreso en formato LNCS. *Nature Reviews Physics* y
*Journal of Computational Physics* tienen otra extensión, otra introducción y
otro nivel de formalismo. Imitarlos te llevaría en dirección contraria.

| # | Paper | Por qué es modelo |
|---|---|---|
| 1 | **Andrés-Zárate et al. 2019**, Rev. Mex. Fis. | El más cercano de todos: revista mexicana, 8 páginas, óptica, y **es de tu director**. Estructura modelo-experimento-simulación |
| 2 | **Carbajal-Domínguez et al. 2010** | Autores de la **UJAT**, espectro angular, difracción de campo cercano — tu método de referencia exacto |
| 3 | **Maiocchetti et al. 2025**, Simposio CEA | PINNs **escrito en español**, formato de congreso corto. El único modelo de cómo suena esta terminología en tu idioma |
| 4 | **Schoder & Kraxberger 2024** | PINN para Helmholtz 3D. Ya está en `tab:comparativa`; comparte tu métrica L² |
| 5 | **Zhang et al. 2025** (FE-PIRBN) | Helmholtz de alta frecuencia. **Leer cómo define su error** — usa L¹, no L², y es el caso que te obligó a corregir la tabla |
| 6 | **Panagiotakopoulos et al. 2026** | Helmholtz 2D con fuente gaussiana: tu antecedente más directo, el que valida sin dar cifras |
| 7 | **Alkhalifah et al. 2021** | Helmholtz con velocidad variable. Artículo corto de revista aplicada |
| 8 | **Chen et al. 2020**, Optics Express | PINNs en óptica. Formato de revista óptica, extensión media |
| 9 | **Sitzmann et al. 2020** (SIREN) | Tu arquitectura. Modelo de cómo enunciar una contribución arquitectónica en pocas páginas |
| 10 | **Krishnapriyan et al. 2021** | Modelo de **cómo reportar un modo de fallo sin que hunda el trabajo** — justo lo que necesitas para NB04 y para el piso evanescente |

### Qué extraer de cada uno

- cómo abre el abstract y en qué frase aparece la contribución
- cómo enuncia lo que aporta, y de qué se abstiene
- cómo reporta métricas e incertidumbre (media ± desviación, rangos, número de corridas)
- cómo matiza un resultado negativo o una limitación
- tiempo verbal y voz (pasiva/activa, primera persona del plural)
- cómo se posiciona frente al trabajo previo sin sobrevenderse

---

## Fuentes

Consultadas el 18/09/2026:

- [Computación y Sistemas — Resurchify](https://www.resurchify.com/impact/details/21100223167)
- [Journal of Computational Physics — Resurchify](https://www.resurchify.com/impact/details/13191)
- [Nature Reviews Physics — Resurchify](https://www.resurchify.com/impact/details/21100972445)
- [Computer Methods in Applied Mechanics and Engineering — Resurchify](https://www.resurchify.com/impact/details/18158)
- [Optics Express — Resurchify](https://www.resurchify.com/impact/details/12862)
- [Revista Mexicana de Física — Resurchify](https://www.resurchify.com/impact/details/29758)
- [IEEE Access — Resurchify](https://www.resurchify.com/impact/details/21100374601)
- [Neural Networks — Resurchify](https://www.resurchify.com/impact/details/24804)
- [IEEE TNNLS — Resurchify](https://www.resurchify.com/impact/details/21100235616)
- [Artificial Intelligence in Geosciences — Resurchify](https://www.resurchify.com/impact/details/21101107176)
- [Sensors — SCImago](https://www.scimagojr.com/journalsearch.php?q=130124&tip=sid&clean=0)
- [SIAM Review — Researcher.Life](https://researcher.life/journal/siam-review/724)
- [JMLR — journalmetrics.org](https://www.journalmetrics.org/journal/journal-of-machine-learning-research)

Las cifras cambian cada año. Antes de usarlas para decidir dónde enviar algo,
vuelve a comprobarlas.
