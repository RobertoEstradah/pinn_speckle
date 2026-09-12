# Literatura candidata para NB03

Estado: material verificado para orientar experimentos. Estas fuentes no se
incorporan todavía a la tesis como respaldo de resultados propios.

## Fuentes con copia local

| Fuente | Tipo y verificacion | Aporte concreto a NB03 | Archivo |
|---|---|---|---|
| Sitzmann et al. (2020), *Implicit Neural Representations with Periodic Activation Functions* | NeurIPS 2020; titulo, autores y resumen comprobados en el PDF | Justifica SIREN para campos oscilatorios, derivadas y ecuaciones de Helmholtz/ondas | `Sitzmann_etal_2020_SIREN.pdf` |
| Wang, Teng y Perdikaris (2021), *Understanding and Mitigating Gradient Flow Pathologies in Physics-Informed Neural Networks* | SIAM J. Sci. Comput.; DOI 10.1137/20M1318043 | Explica el desequilibrio de gradientes entre terminos de la perdida y propone balance adaptativo | `Wang_etal_2021_PINN_gradient_pathologies.pdf` |
| Krishnapriyan et al. (2021), *Characterizing Possible Failure Modes in Physics-Informed Neural Networks* | NeurIPS 2021; titulo y autores comprobados | Sustenta curriculum de dificultad y resolucion por etapas cuando una PINN falla aunque sea expresiva | `Krishnapriyan_etal_2021_CharacterizingFailureModesPINNs.pdf` |
| Moseley, Markham y Nissen-Meyer (2023), *Finite Basis Physics-Informed Neural Networks (FBPINNs)* | Advances in Computational Mathematics 49:62; DOI 10.1007/s10444-023-10065-9 | Fundamenta subdominios solapados, normalizacion local y entrenamiento desde la frontera para dominios grandes/multiescala | `Moseley_etal_2023_FBPINNs.pdf` |
| Kharazmi, Zhang y Karniadakis (2019), *Variational Physics-Informed Neural Networks for Solving Partial Differential Equations* | Preprint primario arXiv:1912.00873 | Formula el residuo debil y reduce el orden de las derivadas mediante integracion por partes | `Kharazmi_etal_2021_VPINN.pdf` |
| Panagiotakopoulos, Velissaris y Rapsomanikis (2026), *Physics-Informed Neural Network Solution of the 2D Helmholtz Equation with a Gaussian Source* | Manuscrito institucional UCF, no tratado aqui como articulo arbitrado | Caso computacional cercano: SIREN 4x128, Adam+L-BFGS, cosine annealing, clipping, remuestreo por epoca y 40 000 puntos interiores | `Panagiotakopoulos_etal_2026_Helmholtz2DGaussianSource.pdf` |

## Fuentes verificadas sin copia PDF abierta

| Fuente | Metadatos verificados | Aporte | Acceso |
|---|---|---|---|
| Chai et al. (2024), *Overcoming the Spectral Bias Problem of Physics-Informed Neural Networks in Solving the Frequency-Domain Acoustic Wave Equation* | IEEE TGRS 62, articulo 5923520; DOI 10.1109/TGRS.2024.3440471 | Fourier multiescala, transferencia entre frecuencias, crecimiento de capacidad y muestreo mas denso | https://doi.org/10.1109/TGRS.2024.3440471 |
| Luo et al. (2025), *PINN-BPM: An Enhanced Physics-Informed Neural Network Framework of Solving Helmholtz Equation for Light Field Propagation in Optical Fiber* | Journal of Lightwave Technology 43(23), 10380-10401 | Muestreo por residuo, pesos auto-adaptativos y prioridad causal para propagacion optica; usa SVHE/BPM, no Helmholtz completo | https://opg.optica.org/jlt/abstract.cfm?uri=jlt-43-23-10380 |

Los portales de IEEE y Optica devolvieron paginas de acceso en lugar de PDF;
por ello no se guardaron archivos con contenido incompleto ni se buscaron
copias no autorizadas.

## Decision experimental derivada de la literatura

1. Mantener la condicion de Cauchy dura y SIREN/Fourier que ya redujeron el
   error complejo de 105.63 % a 23.57 % en `z=1 lambda`.
2. Entrenar por curriculum de modos transversales y transferir pesos entre
   etapas, sin cambiar la ecuacion fisica final.
3. Remuestrear puntos interiores durante Adam para ampliar cobertura sin
   almacenar 40 000 puntos con segundas derivadas a la vez.
4. Medir Helmholtz en una malla densa independiente del entrenamiento.
5. Si el error no baja de 5 %, pasar a balance adaptativo de gradientes o a
   VPINN; reservar FBPINN para distancias mayores.

## Resultado experimental posterior

El curriculum de frecuencia no supero la mejor PINN cartesiana: obtuvo
47.39 % de error y 27.65 % tras afinacion. El diagnostico mostro que el
problema dominante era el condicionamiento desigual de los modos.

Se implemento entonces una PINN-SIREN modal que conserva Helmholtz completo y
la condicion de Cauchy dura, sin etiquetas interiores. Al escalar cada salida
y su residuo por la amplitud fisica del modo se obtuvo, para `z=1 lambda`,
un error L2 complejo de 4.12 %, coherencia de 0.9992 y contraste de 0.9019.
La repeticion posterior con cinco pantallas produjo un L2 medio de 3.54 % y
un maximo final de 4.12 %; todas reprodujeron el contraste de su referencia
con error absoluto menor que 0.015. Esto constituye reproducibilidad
preliminar en `z=1 lambda`, no aun generalizacion a otras distancias.
