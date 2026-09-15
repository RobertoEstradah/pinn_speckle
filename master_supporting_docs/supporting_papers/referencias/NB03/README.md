# Literatura incorporada para NB03

Estos documentos se copiaron desde el proyecto equivalente de Claude al
proyecto Codex. La copia se hizo solo en `C:\roberto\Tesis_Maestria - codex`;
el proyecto fuente no fue modificado.

## PINNs, condiciones de frontera y optimización

- `Dolean_etal_2023_MultilevelDomainDecompositionFBPINNs.pdf`: subdominios y
  normalización local para PINNs.
- `MHPINN_2026_HardConstrainedUnboundedWaveProblems.pdf`: condiciones duras en
  problemas de ondas no acotados.
- `SpectralAnalysis_2025_HardConstraintPINNsBoundaryFunctions.pdf`: efecto
  espectral de funciones de restricción de frontera.
- `Sukumar_Srivastava_2021_ExactBoundaryConditionsDistanceFunctionsPINN.pdf`:
  imposición exacta de condiciones de frontera mediante funciones de distancia.
- `Wang_etal_2021_EigenvectorBiasFourierFeaturePINNs.pdf`: sesgo espectral y
  características de Fourier en PINNs.
- `Wang_etal_2024_RespectingCausalityPINNs.pdf`: entrenamiento causal para
  problemas con evolución espacial o temporal.
- `Jagtap_Karniadakis_2020_AdaptiveActivationPINNs.pdf`: activaciones con
  pendiente entrenable; incluye un experimento de Helmholtz. Esta fue la base
  directa de la variante de frecuencia adaptativa ensayada en NB03.
- `Rathore_etal_2024_PINN_LossLandscape_Adam_LBFGS_NNCG.pdf`: paisaje de
  pérdidas mal condicionado y comparación Adam/L-BFGS/NysNewton-CG.
- `Wang_etal_2023_ExpertsGuideTrainingPINNs.pdf`: protocolo de entrenamiento,
  normalización, Fourier, balance de pérdidas y prácticas de evaluación.
- `Wang_etal_2024_PirateNets.pdf`: versión final JMLR sobre conexiones
  residuales adaptativas e inicialización de derivadas de PINNs.

Los cuatro PDFs anteriores fueron verificados mediante lectura estructural y
renderizado de sus portadas. La ficha BibTeX candidata está en
`referencias_candidatas.bib`.

## Uso correcto en la tesis

Estos papers respaldan motivación, diseño de experimentos y discusión de
limitaciones. No demuestran que la arquitectura de esta tesis funcione en
speckle óptico 2D. Cada afirmación deberá citar el artículo original y
separarse de los resultados propios de NB03.

La lista de PDFs ópticos complementarios se encuentra en:

`../optica_y_bien_puesto/`

Ahí se incorporaron referencias sobre espectro angular, truncación de Cauchy,
Helmholtz 2D y redes neuronales espectrales.
