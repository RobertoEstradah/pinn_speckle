# Plan predefinido de confirmación de frecuencia adaptativa

Definido antes de ejecutar las corridas adicionales.

- Pantalla física reservada: 31415.
- Semillas neuronales: 73 (piloto completado), 101 y 211.
- Arquitectura: SIREN modal, 4 capas, 128 neuronas, 41 modos.
- Modificación: multiplicador global entrenable `n*a`, con `n=10` y
  `n*a=1` al inicio.
- Entrenamiento por semilla: Adam 180 s, seguido por L-BFGS 180 s acumulados.
- Selección: residuo físico en 997 puntos fijos.
- Prueba: residuo en 2001 puntos y campo en 201 planos.
- Referencia de campo: espectro angular, nunca usada para entrenamiento ni
  selección de checkpoints.

Criterios por corrida:

1. L2 completo final menor que 5 %.
2. L2 propagante final menor que 1 %.
3. Máximo L2 propagante en 201 planos menor que 1 %.
4. Error absoluto de contraste respecto a la referencia menor que 0.05.
5. Condiciones de Cauchy satisfechas a precisión numérica.

La variante se considerará confirmada en esta pantalla si al menos dos de las
tres semillas cumplen el criterio primario de L2 completo menor que 5 %. Los
criterios propagantes se reportarán por separado y no se redefinirán después
de observar los resultados.
