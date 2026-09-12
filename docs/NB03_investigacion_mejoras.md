# NB03: diagnóstico y alternativas de mejora

Esta revisión se basa en los scripts y modelos guardados del proyecto y en
fuentes primarias consultadas el 11 de septiembre de 2026. No se realizaron
nuevos entrenamientos ni se modificaron los experimentos existentes. Las
alternativas siguientes son propuestas, no resultados obtenidos.

## 1. Qué explica realmente el error actual

La red conserva 41 modos propagantes, pero el plano final se compara contra
`field_all_z`, que conserva también los evanescentes. La curva multisemilla
en z, por su parte, compara contra una referencia proyectada a los 41 modos.
Son dos referencias diferentes: sus métricas no deben presentarse como una
sola prueba homogénea de precisión.

Se recalcularon los errores a partir de los NPZ existentes:

| Pantalla | L2 frente al campo completo | Límite por omitir evanescentes | L2 frente al campo propagante |
|---:|---:|---:|---:|
| 42 | 4.1185 % | 3.8184 % | 1.5443 % |
| 123 | 2.9056 % | 2.4011 % | 1.6367 % |
| 321 | 3.8925 % | 3.5725 % | 1.5466 % |
| 777 | 3.2518 % | 2.9467 % | 1.3758 % |
| 2026 | 3.5407 % | 3.0634 % | 1.7761 % |

Para calcular el límite se proyecta el campo completo final a los modos
propagantes mediante FFT. Por ortogonalidad de los modos en la malla periódica:

\[
\|u_\theta-u_{full}\|_2^2 =
\|u_\theta-u_{prop}\|_2^2+\|u_{evan}\|_2^2.
\]

La identidad se verificó en las cinco pantallas con discrepancia inferior a
3e-17 para los errores relativos al cuadrado. La última columna usa la norma
del campo propagante; las dos primeras usan la del completo.

Por tanto, entrenar mejor puede reducir el error de aproximación de la red,
pero no eliminar el error por modos ausentes. No sería realista proponer
L2 total menor al 1 % manteniendo los 41 modos en estas pantallas a z=1.

En z=0, el error frente a la pantalla COMPLETA se encuentra entre 76.63 % y
80.90 %: la condición dura corresponde a su proyección propagante, no a la
pantalla completa. Esto no es un fallo de la condición dura; identifica que
se resuelve un problema de frontera filtrado. El máximo interior previamente
reportado de 5.27 % se refiere exclusivamente a la referencia propagante.

La interpretación física de las componentes evanescentes y su decaimiento
está descrita en [TU Delft, Wavefield propagation](https://qiweb.tudelft.nl/aoi/wavefieldpropagation/wavefieldpropagation/).

## 2. Corregir evaluación y selección antes de comparar algoritmos

Hallazgos del código `nb03_modal_pinn_siren.py`:

- Cada época usa un lote aleatorio nuevo, pero se selecciona el mínimo
  histórico de pérdidas de esos lotes distintos.
- Se calcula la pérdida antes de `optimizer.step()`, pero se guardan los
  pesos después del paso. La pérdida y el modelo seleccionado no corresponden
  exactamente al mismo estado.
- El modelo 42 registra una mejor pérdida de entrenamiento de 0.00039547 y
  una MSE independiente de 0.00149458. Esto no prueba sobreajuste por sí solo,
  pero confirma que el mínimo de los lotes no es una medida suficiente.
- El residuo medio 0.03866 de ese modelo convive con un máximo absoluto
  normalizado de 0.63302; un promedio pequeño no implica precisión uniforme.

Propuesta: seleccionar pesos por residuo evaluado DESPUÉS del paso, sobre una
malla de validación fija y suficientemente densa; reservar otra malla distinta
para el reporte final. No seleccionar por los campos de referencia de prueba.
Reportar ambos errores de campo, error por truncamiento, máximos, percentiles,
derivada en la frontera, flujo y residuo saliente, con sus normalizaciones.

La prueba de cinco pantallas mantuvo fija la semilla de la red. Demuestra
repetibilidad del protocolo frente a esas pantallas, no robustez ante distintas
inicializaciones. Además, el criterio |C_PINN-C_ref|<0.05 se introdujo después
de observar resultados: debe identificarse como exploratorio y validarse con
pantallas nuevas reservadas antes de entrenar. No es un umbral universal de
Goodman. La regla histórica |C-1|<0.1 produjo 2/5 aprobaciones; no se debe
sustituir silenciosamente por la nueva al evaluar la hipótesis de la tesis.

## 3. Alternativas priorizadas

### A. Adam seguido de L-BFGS, con prueba separada de float64

La versión modal actualmente usa Adam en ambas etapas. Probar L-BFGS sobre
un conjunto fijo de puntos después del calentamiento Adam es la intervención
inicial más acotada. Comparar luego float32 y float64 permite averiguar si la
precisión numérica limita la afinación. Float64 por sí sola no garantiza mejora.
Mantener fijo el lote dentro de las reevaluaciones de la búsqueda de paso.

[Rathore et al., ICML 2024](https://proceedings.mlr.press/v235/rathore24a.html)
estudian el mal condicionamiento de PINN y encuentran ventajas de Adam+L-BFGS;
también proponen NysNewton-CG. Esa evidencia respalda el ensayo, sin garantizar
el mismo resultado en speckle.

### B. SOAP si la optimización sigue estancada

[Wang et al. (2025)](https://arxiv.org/abs/2502.00604) analizan conflictos de
gradientes y precondicionamiento con SOAP, incluyendo un benchmark de ondas.
Los autores también reportan mayor coste de entrenamiento en su configuración.
Por ello hay que comparar error a igual tiempo de cómputo, no solo a igual
número de épocas. El modelo actual tiene condiciones duras y una pérdida
modal: el beneficio frente a problemas con muchas penalizaciones no se puede
asumir automáticamente.

Código del optimizador: [implementación oficial de SOAP](https://github.com/nikhilvyas/SOAP).

### C. Muestreo más uniforme y refinamiento por residuo

Primero comparar puntos estratificados o una malla densa, aprovechando que la
red solo recibe z. Después probar RAD/RAR-D con una fracción de puntos uniformes
que mantenga cobertura global. Los picos de error del campo no necesariamente
coinciden con los máximos del residuo; no elegir puntos usando la solución de
prueba. El muestreo adaptativo fallido de la PINN cartesiana anterior no prueba
que tampoco funcione en esta formulación modal.

[Wu et al.](https://arxiv.org/abs/2207.10289) comparan métodos de muestreo
uniformes y adaptativos basados en el residuo. Se trata de una opción posterior
a corregir la selección de pesos, no de una garantía de precisión.

### D. Representar los modos evanescentes relevantes

Si el objetivo sigue siendo el campo completo a una longitud de onda,
incorporar componentes evanescentes es necesario para superar el límite de
la tabla. Debe definirse una tolerancia espectral y comprobar convergencia al
aumentar el corte; no fijar arbitrariamente un nuevo número de modos.

Para esos modos, k²-kx² es negativo y la ecuación modal admite crecimiento y
decaimiento. La condición saliente debe seleccionar la rama decreciente.
Agregar modos sin tratar esta estabilidad puede empeorar el entrenamiento.
La instrucción actual `maximum(k²-kx²,0)` no sirve para ellos.

En z=0 los evanescentes contienen mucha norma del campo; una selección
suficiente solo en z=1 no implica precisión en todo el intervalo. Como
alternativa física, se puede definir explícitamente una entrada filtrada y
evaluarla frente a su referencia filtrada, documentando el cambio de problema.

### E. Formulación de primer orden conservando Helmholtz

Introducir b_m=a_m' y resolver el sistema equivalente:

\[
a_m'-b_m=0,\qquad b_m'+(k^2-k_{x,m}^2)a_m=0.
\]

Se sustituyen segundas derivadas de la red por primeras derivadas a cambio de
más salidas y condiciones de compatibilidad. Es una modificación de
arquitectura que requiere una comparación controlada con la versión actual.

[Gladstone et al., FO-PINNs](https://arxiv.org/abs/2210.14320) presentan esta
familia de reformulaciones y reportan mejoras en sus casos parametrizados.
No equivale a afirmar que Helmholtz se vuelve paraxial: el sistema anterior
es equivalente a la ecuación modal de segundo orden.

### F. Aprender un propagador reutilizable para nuevas pantallas

En el medio homogéneo actual, la ecuación es lineal y cada modo evoluciona
independientemente. Se puede entrenar una respuesta unitaria H_m(z):

\[
H_m''+k_{z,m}^2H_m=0,\quad H_m(0)=1,\quad H_m'(0)=i k_{z,m},
\qquad a_m(z)=a_m(0)H_m(z).
\]

Esta es una propuesta derivada de la estructura del problema actual. Una
PINN-SIREN podría aprender las respuestas unitarias una sola vez para la
base fija y reutilizarlas con coeficientes de pantallas nuevas. La identidad
lineal es exacta; la precisión del H neuronal debe medirse en datos reservados.

Para parámetros o geometrías más generales, los operadores neuronales ofrecen
una extensión: [Wang, Wang y Perdikaris, Physics-informed DeepONets](https://arxiv.org/abs/2103.10974).
No es imprescindible introducir DeepONet completo para la base fija de NB03.

Hay que reconocer una comparación exigente: en este mismo medio H_m tiene
solución cerrada exp(i kz_m z), usada por el espectro angular. Aprenderla
mediante una red no implica ser más rápido que evaluarla directamente.
La aceleración debe medirse contra espectro angular además de FEM, incluyendo
FFT, reconstrucción, entrenamiento, inferencia y número de consultas que
amortiza el entrenamiento. No insertar la solución cerrada como ansatz y
atribuir su exactitud al aprendizaje.

### G. Distancias mayores mediante bloques o subdominios

Si el error crece al ampliar z, probar bloques cortos con control del error
transferido en cada interfaz. [FBPINNs, Moseley et al.](https://arxiv.org/abs/2107.07871)
respaldan descomposición y normalización local en otros problemas.
[Wang et al., entrenamiento causal](https://arxiv.org/abs/2203.07404) estudian
problemas evolutivos: adaptar esa idea al avance espacial de una rama saliente
de Helmholtz exige justificación, no una aplicación automática.

## 4. Orden de experimentos propuesto

1. Registrar ambas referencias y el límite espectral, corregir la selección
   del modelo y separar validación de selección de la prueba final.
2. Comparar Adam+Adam, Adam+L-BFGS en float32 y Adam+L-BFGS en float64,
   con igual presupuesto de tiempo y las mismas pantallas de desarrollo.
3. Medir mejora del error propagante y su máximo a lo largo de z. Un objetivo
   exploratorio razonable es bajar el error propagante final de 1.4–1.8 % a
   menos de 1 %; no es una predicción del resultado.
4. Si se pretende L2 total menor al 1 %, desarrollar y validar la rama
   evanescente con corte espectral convergente.
5. Evaluar pantallas y semillas de optimización nuevas con reglas fijadas
   previamente; no declarar generalización por reentrenar cinco veces.
6. Probar el propagador reutilizable y después ampliar a z=2 y z=5 con
   referencia y costes de cómputo comparables.

## 5. Relación con la tesis y reproducibilidad

La tesis mantiene una hipótesis de precisión, una de aceleración y otra
estadística. El 5/5 de error final respalda preliminarmente la primera en
z=1; no completa las otras dos. El contraste de conjunto cercano a 1 tampoco
demuestra por sí solo speckle completamente desarrollado: faltan pruebas de
distribución de intensidad y correlaciones con suficiente muestra efectiva.

El campo actual tiene una dimensión transversal x y una longitudinal z.
Es Helmholtz 2D escalar; un plano speckle con dos coordenadas transversales
(x,y) propagado en z requeriría otro alcance dimensional.

El README usa environment.yml, que declara Python 3.14 y PyTorch 2.11/CUDA,
mientras el runtime registrado de estos pilotos fue Python 3.12.14 y
PyTorch 2.14.0+cpu. Se necesita un entorno fijado específico de NB03 y registrar
versiones, hardware, configuración, estados aleatorios y hashes de modelos.
El notebook conserva entrenamiento histórico ejecutable: validar su sintaxis
no equivale a haber comprobado una ejecución completa de la versión modal.

Veredicto: conservar el resultado existente como referencia experimental y
mejorar primero evaluación, selección de pesos y optimización. Ampliar la
representación si se exige precisión del campo completo; aprender una respuesta
reutilizable si se busca acelerar simulaciones de muchas pantallas.
