# Protocolo de Tesis de Maestría — Roberto Hernández Estrada

> Fuente: `Protocolo_tesis_maestria_Roberto_Hernandez_Estrada.pdf` (convertido con pdftotext desde `master_supporting_docs/supporting_protocolo/`)

---

   UNIVERSIDAD JUÁREZ AUTÓNOMA DE TABASCO

  DIVISIÓN ACADÉMICA DE CIENCIAS Y TECNOLOGÍAS DE LA
                                   INFORMACIÓN

SIMULACIÓN ACELERADA DE SPECKLE ÓPTICO: UN ENFOQUE
  BASADO REDES NEURONALES FÍSICAMENTE INFORMADAS
                                        (PINN’S)

                             PROTOCOLO DE TESIS
           MAESTRÍA EN CIENCIAS DE LA COMPUTACIÓN

                                      PRESENTA:
                     ROBERTO HERNÁNDEZ ESTRADA

                            BAJO LA DIRECCIÓN DE:
                DR. JOSÉ ADÁN HERNÁNDEZ NOLASCO

                                                               CUNDUACÁN, TABASCO, A: Octubre de 2025
   UNIVERSIDAD JUÁREZ AUTÓNOMA DE TABASCO

  DIVISIÓN ACADÉMICA DE CIENCIAS Y TECNOLOGÍAS DE LA
                                   INFORMACIÓN

SIMULACIÓN ACELERADA DE SPECKLE ÓPTICO: UN ENFOQUE
  BASADO REDES NEURONALES FÍSICAMENTE INFORMADAS
                                        (PINN’S)

                             PROTOCOLO DE TESIS
           MAESTRÍA EN CIENCIAS DE LA COMPUTACIÓN

                                      PRESENTA:
                     ROBERTO HERNÁNDEZ ESTRADA

                            BAJO LA DIRECCIÓN DE:
                DR. JOSÉ ADÁN HERNÁNDEZ NOLASCO

                                JURADO REVISOR:
                          PABLO PANCARDO GARCÍA
                    MIGUEL ANTONIO WISTER OVANDO
                   OSCAR ALBERTO CHÁVEZ BOSQUEZ

                                                               CUNDUACÁN, TABASCO, A: Octubre de 2025
Índice

1. Antecedentes                          1

2. Marco conceptual                      2

3. Estado del arte                       3

4. Planteamiento del problema            4

5. Preguntas de investigación            5

6. Hipótesis                             6

7. Objetivos                             6

7.1. Objetivo general . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 6

7.2. Objetivos específicos . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 6

8. Alcances y limitaciones               7

9. Justificación                         8

10. Método                               9

11. Contribución y resultados esperados  12

12. Cronograma                           13

Referencias                              14
1 1. Antecedentes

2 La simulación de la propagación de la luz es una herramienta fundamental en la cien-
3 cia y la ingeniería, con aplicaciones que abarcan desde el diseño de sistemas de teleco-
4 municaciones y la nanofotónica hasta el desarrollo de técnicas de imagenología médica.
5 Un fenómeno de particular interés es el speckle óptico, un patrón de interferencia comple-
6 jo que surge cuando luz coherente, como la de un láser, se dispersa en un medio difusor
7 o una superficie rugosa.
8 Tradicionalmente, la simulación de estos fenómenos ondulatorios se aborda mediante
9 métodos numéricos robustos como el Método de Elementos Finitos (FEM) o métodos
10 estocásticos como el de Monte Carlo. Sin embargo, estos métodos presentan un ”cuello
11 de botella” computacional significativo. Requieren una discretización (mallado) extrema-
12 damente fina del dominio espacial para resolver las rápidas oscilaciones del campo de
13 luz, lo que resulta en un consumo masivo de memoria y tiempos de cómputo que pueden
14 extenderse por días.
15 En paralelo, el campo de la inteligencia artificial ha experimentado un crecimiento
16 disruptivo. Una innovación reciente son las Redes Neuronales Físicamente Informadas
17 (PINNs, por sus siglas en inglés), una metodología que fusiona el Deep Learning con
18 las leyes físicas fundamentales. Las PINNs (Raissi et al., 2019; Thuerey et al., 2021)
19 son redes neuronales entrenadas no solo para ajustarse a datos, sino para obedecer
20 directamente una Ecuación Diferencial Parcial (EDP) que gobierna un sistema.
21 Este proyecto se sitúa en la intersección de la óptica computacional y la inteligen-
22 cia artificial, buscando aplicar el paradigma de las PINNs para superar las limitaciones
23 computacionales de los métodos clásicos en la simulación de speckle óptico.

                                                              1
24 2. Marco conceptual

25 Para establecer una base sólida para esta investigación, es crucial definir los siguien-
26 tes conceptos y sus interrelaciones:

27 Ecuación de onda de Helmholtz: Es la ley física fundamental que describe la propa-

28  gación de ondas monocromáticas (de una sola frecuencia) en el espacio, como

29  un frente de onda láser. Se expresa como una Ecuación Diferencial Parcial (EDP):

30  ∇2E(x, y, z) + k2E(x, y, z) = 0, donde E es el campo eléctrico (la luz), ∇2 es el ope-

31  rador Laplaciano y k es el número de onda (relacionado con la longitud de onda y

32  el medio).

33 Speckle óptico: Es el patrón de interferencia granular y de alto contraste que se ob-

34  serva cuando la luz coherente es dispersada por un medio ópticamente rugoso

35  (Goodman, 2007). Es el resultado de la interferencia constructiva y destructiva de

36  múltiples frentes de onda con fases aleatorias.

37 Método de Elementos Finitos (FEM): Un método numérico para resolver EDPs que

38  funciona dividiendo un dominio complejo en un gran número de elementos simples

39  (una "malla"), resolviendo la ecuación en cada elemento y ensamblando la solución

40  global (Jin, 2014). Su precisión depende directamente de la densidad de la malla.

41 Redes Neuronales Físicamente Informadas (PINNs): Es una arquitectura de Deep Lear-

42  ning, en donde la red neuronal N (x, t) aproxima la solución de una EDP. Su inno-

43  vación radica en la función de pérdida (loss function). Esta función se compone de

44  dos términos:

45  1. Error de datos (Ldatos): Mide la discrepancia entre la predicción de la red y los

46  valores conocidos (condiciones de frontera).

47  2. Error físico (Lfísica): Mide el ”residuo” de la ecuación diferencial parcial. Se

48  utilizan técnicas de diferenciación automática para calcular las derivadas de

                        2
49  la salida de la red (el campo E) e insertarlas en la Ecuación de Helmholtz.

50  Si la ecuación no se cumple (el residuo no es cero), la red es penalizada.

51  Esto la ”fuerza” a aprender una solución que es físicamente precisa en todo

52  el dominio (Cuomo et al., 2022), sin necesidad de una malla.

53 3. Estado del arte

54 El uso de redes neuronales para resolver EDPs fue propuesto inicialmente en los
55 90, pero ha sido revitalizado por el trabajo seminal de Raissi, Perdikaris y Karniadakis
56 (Raissi et al., 2019) sobre PINNs, quienes demostraron su capacidad para resolver una
57 amplia gama de problemas físicos. En este contexto, investigaciones recientes como la
58 de Maiocchetti et al. (Maiocchetti et al., 2025) han validado la eficacia de las PINNs
59 (específicamente en arquitecturas MLP) para resolver balances de energía y movimiento
60 descritos por EDO y EDPs.
61 En el campo específico de la óptica y el electromagnetismo, la investigación ha co-
62 menzado a adoptar esta técnica. Estudios recientes (ej. Fang et al., 2020 (Fang & Zhan,
63 2020); Lu et al., 2021 (Lu et al., 2021)) han aplicado PINNs para resolver las ecuaciones
64 de Maxwell y problemas de scattering (dispersión) de ondas en medios 2D y 3D, demos-
65 trando una alta precisión. En fotónica, se han utilizado para el diseño inverso de guías de
66 onda y metasuperficies (Chen et al., 2020 (Chen et al., 2020)).
67 Sin embargo, se identifica una brecha en el conocimiento: la aplicación específica de
68 PINNs para la simulación del speckle óptico en medios difusores complejos. El speckle es
69 un problema notoriamente difícil debido a su naturaleza estadísticamente rica (Goodman,
70 2007) y las altas frecuencias espaciales que contiene. Donde estudios recientes en el
71 uso de PINNs para resolver EDPs está consolidado. Específicamente, en la propagación
72 de ondas, Schoder y Kraxberger Schoder y Kraxberger, 2024 realizaron un estudio de
73 factibilidad resolviendo la Ecuación de Helmholtz, demostrando la viabilidad de la técnica

                                                              3
74 en entornos complejos.
75 Este estudio es clave para la presente investigación por sus resultados cuantitativos:

76  Precisión: Se reportó un error relativo L2 de 0.0249 (aproximadamente 2.5 %) en

77  la comparación entre la solución PINN y la solución FEM de referencia (malla fina)

78  para la propagación de onda.

79  Eficiencia: Aunque el entrenamiento del PINN es costoso, la fase de inferencia

80  (predicción) fue comparada con la solución FEM, encontrando que la inferencia del

81  modelo PINN era más de 20,000 veces más rápida que la solución completa de

82  un caso equivalente en FEM, validando el valor de la inferencia acelerada para

83  problemas inversos y en tiempo real.

84 El problema de resolver la Ecuación Paraxial en 2D para generar speckle se ajusta
85 a este marco, aprovechando la velocidad de inferencia de las PINNs para superar las
86 limitaciones de memoria de FEM en simulaciones de dominios grandes.

87 4. Planteamiento del problema

88 La simulación precisa de cómo la luz se dispersa y forma patrones de speckle es
89 crucial para el diseño de sistemas ópticos avanzados en imagenología biomédica (ej. to-
90 mografía de coherencia óptica), metrología (medición de vibraciones) y seguridad (crip-
91 tografía óptica).
92 El desafío central radica en el costo computacional prohibitivo de los métodos numé-
93 ricos actuales:

94 1. Métodos Basados en Malla (FEM): Para capturar con precisión los detalles finos

95  de un patrón de speckle, la malla debe tener una resolución espacial menor que

96  la longitud de onda de la luz (Jin, 2014). Esto conduce a sistemas de ecuaciones

                                          4
97   con millones (o miles de millones) de incógnitas, requiriendo clústeres de cómputo

98   de alto rendimiento, una cantidad masiva de memoria RAM y tiempos de ejecución

99   que frenan la investigación.

100 2. Métodos basados en trazado de rayos (Monte Carlo): Requieren simular un nú-

101  mero astronómico de fotones individuales para construir un patrón de interferencia

102  estadísticamente preciso, lo que los hace extremadamente lentos.

103 Este cuello de botella limita significativamente la capacidad de los científicos e in-
104 genieros para modelar medios difusores complejos, optimizar diseños ópticos o realizar
105 simulaciones 3D a gran escala.
106 Aunque la aplicación de las PINNs para resolver la ecuación de Helmholtz ha sido
107 validada en simulaciones de ondas acústicas (Schoder & Kraxberger, 2024), hasta don-
108 de alcanza nuestro conocimiento, la aplicación de este paradigma para la simulación
109 eficiente de speckle óptico de alta resolución no ha sido abordada sistemáticamente.
110 Por lo tanto, existe la necesidad urgente de un nuevo paradigma computacional que
111 sea "libre de malla"(mesh-free), eficiente en el uso de memoria y capaz de acelerar estas
112 simulaciones en un orden de magnitud, sin sacrificar la precisión dictada por la física
113 fundamental (la ecuación de Helmholtz).

5. 114 Preguntas de investigación

115 1. ¿Puede un modelo de Red Neuronal Físicamente Informada (PINN) aproximar con

116  precisión la solución de la ecuación de onda de Helmholtz para la simulación de

117  patrones de speckle óptico en medios difusores 2D?

118 2. ¿Cuál es la ganancia en eficiencia computacional (tiempo de cómputo y uso de

119  memoria) del enfoque basado en PINNs en comparación con un FEM para simular

120  el mismo fenómeno de speckle?

                                    5
121 3. ¿Cómo impacta la complejidad del medio difusor (ej. rugosidad de la superficie) en

122  la precisión y el tiempo de entrenamiento del modelo PINN?

6. 123 Hipótesis

124 El desarrollo de un modelo computacional basado en Redes Neuronales Físicamen-
125 te Informadas (PINNs) para la resolución de la ecuación de Helmholtz en 2D permitirá
126 simular la generación de speckle óptico logrando una aceleración en el tiempo de infe-
127 rencia de al menos un orden de magnitud (10×) respecto al Método de Elementos Finitos
128 (FEM). Asimismo, se mantendrá una precisión física validada mediante un error relativo
129 L2 < 5 % y se preservarán las propiedades estadísticas del fenómeno, específicamente
130 un Contraste de Speckle (C) con una desviación menor al 5 % respecto a la teoría de
131 Goodman Goodman, 2007.

7. 132 Objetivos

133 7.1. Objetivo general

134 Construir un modelo computacional basado en PINNs para la simulación acelerada y
135 físicamente precisa de frentes de onda y speckle óptico, mediante la resolución directa
136 de la ecuación de Helmholtz.

137 7.2. Objetivos específicos

138  Definir una arquitectura de red neuronal profunda (PINN) que incorpore el residuo

139  de la ecuación de Helmholtz en su función de pérdida.

140  Entrenar y validar la precisión base del modelo PINNs en un escenario simple (pro-

141  pagación 2D en espacio libre) comparando sus resultados con la solución analítica

                                6
142  conocida (utilizando el Error L2)

143  Aplicar el modelo validado a la simulación de speckle óptico en medios difusores

144  complejos y validar su precisión utilizando métricas ópticas estadísticas clave.

145  Evaluar y comparar cuantitativamente el rendimiento (precisión, eficiencia de infe-

146  rencia y uso de memoria) del modelo PINN contra una implementación de refe-

147  rencia del FEM para demostrar una aceleración de al menos 10× en el tiempo de

148  predicción.

8. 149 Alcances y limitaciones

150 Para definir con claridad los límites de la investigación, se establecen los siguientes
151 puntos:

152 Alcances

153  El proyecto entregará un prototipo de software funcional, implementado en Python

154  (PyTorch o TensorFlow), capaz de construir y entrenar un modelo PINN para resol-

155  ver la ecuación de Helmholtz en dominios 2D.

156  Se validará cuantitativamente la precisión del modelo PINN contra una solución

157  analítica conocida (propagación de onda Gaussiana en espacio libre 2D).

158  El modelo será capaz de simular la generación de patrones de speckle óptico en

159  2D, mediante la introducción de una frontera con fase aleatoria.

160  Se realizará una evaluación comparativa (benchmark) en términos de precisión,

161  tiempo de cómputo y uso de memoria contra un método numérico estándar (FEM).

                                        7
162 Limitaciones

163  Dimensionalidad: La limitación principal del proyecto es su dimensionalidad. Todas

164  las simulaciones, validaciones y comparativas se restringirán a dominios de dos

165  dimensiones (2D). El desarrollo y la simulación en 3D completo están fuera del

166  alcance de este trabajo de maestría.

167  Alcance computacional: Esta es una investigación puramente computacional y de

168  simulación. No se incluye la construcción de montajes ópticos experimentales ni la

169  validación del modelo contra datos físicos reales.

170  Simplificación del medio: El medio difusor se modelará como una frontera con

171  fase aleatoria. El proyecto no abordará la simulación de medios difusores volumé-

172  tricos complejos o medios con propiedades ópticas no lineales.

9. 173 Justificación

174 Este proyecto de investigación se justifica en tres ejes principales:

175  Justificación computacional: El principal obstáculo en la simulación óptica avan-

176  zada es el costo computacional prohibitivo de los métodos numéricos actuales, co-

177  mo el FEM y Monte Carlo. Estos métodos imponen un ”cuello de botella” que frena

178  la iteración y el diseño. Esta investigación se justifica al proponer un nuevo para-

179  digma ”libre de malla” (mesh-free) que busca reducir los tiempos de simulación en

180  órdenes de magnitud.

181  Justificación científica y de aplicación: La simulación precisa de speckle no es

182  un problema puramente teórico; es crucial para el avance de tecnologías aplicadas.

183  Campos como la imagenología biomédica (ej. tomografía de coherencia óptica), la

                                           8
184  metrología de precisión y la criptografía óptica dependen directamente de un en-

185  tendimiento y modelado profundo de la dispersión de la luz. Acelerar la simulación

186  impacta directamente en la capacidad de innovar en estas áreas.

187  Justificación metodológica y programática: El proyecto se alinea estratégica-

188  mente con la Línea de Generación y Aplicación del Conocimiento (LGAC) en Cien-

189  cia de datos e inteligencia artificial de la Maestría en Ciencias de la Computación.

190  Se justifica al aplicar una técnica de vanguardia en Deep Learning (PINNs) para

191  resolver una Ecuación Diferencial Parcial fundamental de la física, demostrando la

192  sinergia entre la IA y la ciencia computacional avanzada.

193 10. Método

194 La metodología se basa en el marco de trabajo de las PINNs propuesto por Raissi et
195 al., 2019, adaptado para la ecuación de Helmholtz. Este proyecto es un estudio de inves-
196 tigación computacional cuantitativo y experimental. Se desarrollará en fases alineadas
197 con los objetivos específicos, utilizando herramientas de la LGAC de Ciencia de Datos e
198 Inteligencia Artificial.

199 Fase 1: Desarrollo y arquitectura del modelo

200  Herramientas: Se utilizará Python 3.x. La red neuronal se implementará usan-

201  do la biblioteca PyTorch (o TensorFlow), debido a su robusto módulo de dife-

202  renciación automática (Autodiff).

203  Arquitectura de red: Se diseñará un Perceptrón Multicapa (MLP) que toma

204  como entrada coordenadas espaciales (x, y) y retorna el campo de luz com-

205  plejo E(x, y) (representado por sus partes real e imaginaria).

206  Función de Pérdida: Se implementará la función de pérdida compuesta

207  Ltotal = Ldatos + λLfísica.

                                        9
208          1. Ldatos será un Error Cuadrático Medio (MSE) sobre las condiciones de fron-

209          tera conocidas (ej. el frente de onda láser incidente).

210          2. Lfísica será el MSE del residuo de la ecuación de Helmholtz (∇2E + k2E =

211          0), evaluado en puntos de colocación muestreados aleatoriamente dentro

212          del dominio. La diferenciación automática de PyTorch se usará para calcu-

213          lar ∇2E.

     Figura 1. Esquema conceptual de la arquitectura de una Red Neuronal Físicamente Informada (PINN). La
     red (NN) predice la solución (u), cuyas derivadas alimentan el residuo de la Ecuación Diferencial Parcial
     (EDP) para calcular la pérdida de física (M SER).
     Nota. Adaptado de "Ppinn: Parareal physics-informed neural network for time-dependent pdes,"por X.
     Meng, Z. Li, D. Zhang, y G. E. Karniadakis, 2020, Computer Methods in Applied Mechanics and Engi-
     neering, 370, 113250.

214 Fase 2: Validación analítica y estrategía de entrenamiento

215  Se entrenará el modelo para la propagación de una onda gaussiana en espacio

216  libre.

217          Muestreo (Collocation Points): Se utilizará Muestreo Latino Hipercúbico (LHS,

                       10
218  por sus siglas en inglés Latin Hypercube Sampling) para seleccionar los pun-

219  tos de colocación dentro del dominio Ω, garantizando una cobertura espacial

220  más eficiente que una malla aleatoria simple.

221  Optimizador Híbrido: Para acelerar la convergencia y evitar mínimos locales,

222  se empleará una estrategia de dos etapas: primero el optimizador Adam para

223  una aproximación global rápida, seguido del optimizador de segundo orden L-

224  BFGS para el ajuste fino de alta precisión, siguiendo la metodología validada

225  por Schoder y Kraxberger, 2024.

226  Evaluación:La métrica de evaluación será el error L2 relativo para validar la

227  precisión del modelo.

228 Fase 3: Experimentación y comparativa

229  Se introducirá una frontera con fase aleatoria para generar speckle y se

230  comparará contra un benchmark FEM (ej. FEniCS o COMSOL).

231  Evaluación de Métricas de Rendimiento: Para validar la mejora compu-

232  tacional, se aplicarán las siguientes métricas estándar en Scientific Machi-

233  ne Learning (Karniadakis et al., 2021; Thuerey et al., 2021):

234  1. Factor de Aceleración (Speed-up Factor): Razón entre el tiempo de eje-

235  cución del solver FEM (TF EM ) y el tiempo de inferencia de la PINN (TP INN ):

                                           S = TF EM                (1)
                                           TP INN

236  2. Huella de Memoria Pico (Peak Memory Footprint): Monitorización del

237  uso máximo de RAM/VRAM para demostrar que el enfoque PINN evita el

238  crecimiento exponencial de memoria asociado al mallado denso.

239  3. Grados de Libertad por Segundo (DOFs/sec): Tasa de puntos del cam-

                            11
240  po óptico resueltos por unidad de tiempo

                               η = Npuntos              (2)
                                       Tcmputo

241 11. Contribución y resultados esperados

242  Contribución

243  El resultado principal de esta investigación será un nuevo paradigma computacional

244  "libre de malla"(mesh-free) para la simulación de fenómenos de dispersión de luz

245  coherente. Esta contribución es relevante para la LGAC de Ciencia de Datos e

246  Inteligencia Artificial, ya que aplica una técnica de Deep Learning de vanguardia

247  (PINNs) para resolver un problema físico complejo (ecuación de Helmholtz) que

248  actualmente sufre de un cuello de botella computacional con métodos tradicionales.

249  Resultados Esperados

250  1. Un prototipo de software funcional, implementado en Python y PyTorch, capaz

251  de simular la generación de speckle óptico en 2D.

252  2. Un análisis cuantitativo y comparativo (presentado en tablas y gráficas) que

253  demuestre la ganancia en eficiencia computacional (tiempo y memoria) del

254  modelo PINN sobre el método FEM.

255  3. La validación de la precisión del modelo PINN, demostrando que puede ge-

256  nerar patrones de speckle estadísticamente equivalentes a los métodos de

257  referencia.

258  4. La generación de al menos un artículo científico derivado de los hallazgos,

259  para ser enviado a una revista indexada o un congreso especializado en óptica

                           12
260  computacional o inteligencia artificial aplicada.

261  12. Cronograma

262  La tabla 1 resume las actividades programadas.

                        2025                            2026                                2027
                     1º Semestre
                                  2º Semestre 3º Semestre 4º Semestre

                     AGO
                        SEP
                            OCT
                                NOV
                                    DIC
                                        ENE
                                            FEB
                                                MAR
                                                    ABR
                                                        MAY
                                                           JUN
                                                               JUL
                                                                   AGO
                                                                       SEP
                                                                           OCT
                                                                               NOV
                                                                                   DIC
                                                                                       ENE
                                                                                           FEB
                                                                                               MAR
                                                                                                  ABR
                                                                                                        MAY

                              1. Revisión de literatura
                              2. Definición del problema
                              3. Diseño y desarrollo (Fase 1)
                              4. Validación analítica (Fase 2)

263

                              5. Implementación Benchmark FEM
                              6. Experimentación Speckle (Fase 3)
                              7. Evaluación comparativa (Fase 3)
                              8. Optimización del modelo
                              9. Análisis de resultados
                              10. Redacción y revisión de tesis
                              11. Redacción y envío de artículo
                              12. Presentación de la tesis

                                                Tabla 1. Diagrama de Gantt de actividades.

                     13
264  Referencias

265  Chen, Y., Lu, L., Karniadakis, G. E., & Dal Negro, L. (2020). Physics-informed neural

266  networks for inverse problems in nano-optics and plasmonics. Optics Express,

267  28(8), 11618-11633. https://doi.org/10.1364/OE.384875

268  Cuomo, S., Di Cola, V. S., Giampaolo, F., Rozza, G., Raissi, M., & Piccialli, F. (2022).

269  Scientific machine learning through physics-informed neural networks: A re-

270  view. Journal of Computational Science, 62, 101709. https://doi.org/10.1016/

271  j.jocs.2022.101709

272  Fang, Z., & Zhan, J. (2020). A physics-informed neural network framework for wave

273  scattering in inhomogeneous media. IEEE Antennas and Wireless Propagation Letters,

274  19(9), 1640-1644. https://doi.org/10.1109/ACCESS.2019.2963390

275  Goodman, J. W. (2007). Speckle Phenomena in Optics: Theory and Applications. Ro-

276  berts; Company Publishers.

277  Jin, J.-M. (2014). The Finite Element Method in Electromagnetics. John Wiley & Sons.

278  Karniadakis, G. E., Kevrekidis, I. G., Lu, L., Perdikaris, P., Wang, S., & Yang, L.

279  (2021). Physics-informed machine learning. Nature Reviews Physics, 3(6),

280  422-440. https://doi.org/10.1038/s42254-021-00314-5

281  Lu, L., Meng, X., Mao, Z., & Karniadakis, G. E. (2021). DeepXDE: A deep learning

282  library for solving differential equations. SIAM Review, 63(1), 208-228. https:

283  //doi.org/10.1137/19M1274067

284  Maiocchetti, E., Irigoyen Gordo, E., Larrea, M., & Tronci, S. (2025). Estudio de las

285  Redes PINN como modelos de sistemas dinámicos. XX Simposio CEA de Control Inteligen

286  https://doi.org/10.64117/simposioscea.v1i2.88

287  Raissi, M., Perdikaris, P., & Karniadakis, G. E. (2019). Physics-informed neural net-

288  works: A deep learning framework for solving forward and inverse problems

289  involving nonlinear partial differential equations. Journal of Computational Physics,

290  378, 686-707. https://doi.org/10.1016/j.jcp.2018.10.045

                                 14
291  Schoder, S., & Kraxberger, F. (2024). Feasibility study on solving the Helmholtz

292  equation in 3D with PINNs. arXiv preprint arXiv:2403.06623v1. https : / / doi .

293  org/10.48550/arXiv.2403.06623

294  Thuerey, N., Holl, P., Mueller, M., Schnell, P., Trost, F., & Um, K. (2021). Physics-based Deep Learn

295  Independently published. https://physicsbaseddeeplearning.org

     15
