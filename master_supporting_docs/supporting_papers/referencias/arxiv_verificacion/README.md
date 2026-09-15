# Fuentes descargadas para verificación de citas

**Fecha:** 2026-09-15
**Motivo:** de las 28 claves citadas en la tesis, sólo 15 tenían PDF local. Sin
el documento no se puede comprobar que la fuente diga lo que la tesis le
atribuye, de modo que esas citas quedaban sin validar. Estas cuatro estaban
disponibles en arXiv y se descargaron para poder verificarlas.

Las entradas correspondientes ya existían en `references.bib` con los autores
correctos; lo que faltaba era el documento.

| Archivo | arXiv | Verificado en la portada del PDF |
|---|---|---|
| `Rahaman_etal_2019_SpectralBiasNeuralNetworks.pdf` | 1806.08734v3, 31 may 2019 | *On the Spectral Bias of Neural Networks*. Rahaman, Baratin, Arpit, Draxler, Lin, Hamprecht, Bengio, Courville |
| `Tancik_etal_2020_FourierFeatures.pdf` | 2006.10739v1, 18 jun 2020 | *Fourier Features Let Networks Learn High Frequency Functions in Low Dimensional Domains*. Tancik, Srinivasan, Mildenhall, Fridovich-Keil, Raghavan, Singhal, Ramamoorthi, Barron, Ng |
| `Baydin_etal_2018_AutomaticDifferentiation.pdf` | 1502.05767v4, 5 feb 2018 | *Automatic Differentiation in Machine Learning: a Survey*. Baydin, Pearlmutter, Radul, Siskind |
| `Kingma_Ba_2015_Adam.pdf` | 1412.6980 | *Adam: A Method for Stochastic Optimization*. Kingma, Ba. Publicado en ICLR 2015 |

## Las que siguen sin verificación local

No están en arXiv y no se descargaron. Son libros o publicaciones de pago:

| Clave | Usos en la tesis | Naturaleza | Riesgo |
|---|---:|---|---|
| `goodman2007speckle` | 11 | Libro (Roberts & Company) | **Alto**: sostiene todo el criterio estadístico del trabajo |
| `zhang2025fepirbn` | 2 | *J. Comput. Phys.* 527:113798 (Elsevier) | **Alto**: la tabla comparativa de Cap4 le atribuye «L² entre 1.40 % y 5.82 %», cifra no verificable |
| `jin2014finite` | 3 | Libro (Wiley) | Bajo: cita de contexto sobre FEM |
| `mckay1979lhs` | 3 | *Technometrics* 21(2) | Bajo: cita metodológica de LHS |
| `lagaris1998ann` | 1 | *IEEE Trans. Neural Netw.* | Bajo |
| `hornik1989universal` | 1 | *Neural Networks* 2(5) | Bajo |
| `nocedal2006numerical` | 1 | Libro (Springer) | Bajo |
| `alkhalifah2021wavefield` | 1 | *Artif. Intell. Geosci.* 2 | Bajo |
| `fang2020physics` | 1 | *IEEE Access* | Bajo |

`born1999principles` tiene una vista previa legal de 99 páginas en
`../Born_Wolf_1999_Principles_of_Optics_Legal_Preview.pdf`, suficiente para
verificar material del capítulo 1 pero no el libro completo.

## Acción pendiente

Las dos de riesgo alto requieren decisión del autor: conseguir el documento por
biblioteca, o reformular la afirmación para no atribuir cifras que no pueden
comprobarse.
