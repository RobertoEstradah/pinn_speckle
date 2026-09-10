# NB03 — Speckle óptico vía PINN (pausado, 2026-09-10)

Este directorio archiva el intento de resolver la ecuación de Helmholtz 2D con
frontera de fase aleatoria mediante PINN-SIREN (el "NB03" numerado del
proyecto). Se pausó para poder retomar el trabajo de validación 1D/2D
(NB01, NB02) sin que discrepancias de NB03 interfirieran con esas
modificaciones. **El título de la tesis, la pregunta de investigación y las
hipótesis no cambian** — el objetivo de simular speckle óptico sigue siendo
la meta final; este directorio existe para retomarlo con toda la información
ya reunida, sin repetir el trabajo de diagnóstico.

## Contenido

- `notebooks/03_pinn_optical_speckle_simulation.ipynb` — el notebook tal como
  quedó, con frontera rugosa φ~U(0,2π) en y=0 y bordes libres.
- `scripts/diagnose_nb03_speckle_regime.py` — diagnóstico físico de por qué
  k=2π solo permite propagar 3 de 256 modos de la frontera.
- `results/nb03_speckle_regime.json` — salida de ese diagnóstico.
- `results/models/nb03_speckle.pt` — últimos pesos entrenados (no convergen a
  speckle real, ver hallazgos abajo).
- `quality_reports/resumen_nb03_estado_2026-09-10.md`,
  `quality_reports/tesis_fuente_conNB03_writer_critic.md` — revisiones previas.
- `hallazgos_y_diagnostico.md` — **el documento más importante**: resume todo
  lo investigado (en CLAUDE.md y en la sesión del 2026-09-10) sobre por qué
  NB03 no converge, qué se intentó, y qué dirección parece más prometedora
  para cuando se retome.

## No archivado (sigue activo)

- `notebooks/validacion_estadistica/03_speckle_distancias_estadistico.ipynb`
  — generación estadística directa de speckle (sin PINN, ruido gaussiano
  filtrado según Goodman) a 10 distancias reales. No usa la frontera de fase
  aleatoria por PINN y no ha causado ninguna discrepancia — se queda donde
  está, fuera de la numeración del proyecto.
- `results/speckle_distances.json` y las figuras `results/figures/speckle_*`
  — pertenecen a ese notebook estadístico, no a este intento por PINN.

## Para retomar este trabajo

Leer `hallazgos_y_diagnostico.md` primero — documenta qué NO funciona y por
qué, para no repetir el mismo camino.
