# Reporte de cambios -- Tesis Roberto Hernandez Estrada

**Fecha de generacion:** 21/08/2026 15:17
**Comparacion:** `conNB03` (antes)  vs.  `actualizada` (despues)
**Cambios detectados:** 25

| Correccion | Pagina | Antes | Despues |
|---|---|---|---|
| REDES NEURONALES F�ISICAMENTE INFORMADAS (PINN'S) -> EN REDES NEURONALES F�ISIC... | 1 | BASADO REDES NEURONALES F�ISICAMENTE INFORMADAS (PINN'S) | BASADO EN REDES NEURONALES F�ISICAMENTE INFORMADAS (PINNS) |
| REDES NEURONALES F�ISICAMENTE INFORMADAS (PINN'S) -> EN REDES NEURONALES F�ISIC... | 2 | BASADO REDES NEURONALES F�ISICAMENTE INFORMADAS (PINN'S) | BASADO EN REDES NEURONALES F�ISICAMENTE INFORMADAS (PINNS) |
| mica de Ciencias y Tecnolog�ias de la Informacio� n, de la Universidad Jua� rez... | 3 | be Roberto Herna� ndez Estrada, alumno del Programa de la Maestr�ia en Ciencias de la Computacio� n con nu� mero de matr�icula 252H21004, adscrito a la Divisio� n Acade� mica de Ciencias y Tecnolog�ias de la Informacio� n, de la Universidad Jua� rez Auto� nom... | be Roberto Herna� ndez Estrada, alumno del Programa de la Maestr�ia en Ciencias de la Computacio� n con nu� mero de matr�icula 252H21004, adscrito a la Divisio� n Acade� mi- ca de Ciencias y Tecnolog�ias de la Informacio� n, de la Universidad Jua� rez Auto� n... |
| redes neuronales f�isicamente informadas (PINN's). -> en redes neuronales f�isi... | 5 | o� ptico: Un enfoque basado redes neuronales f�isicamente informadas (PINN's). | o� ptico: Un enfoque basado en redes neuronales f�isicamente informadas (PINNs). |
| 14 -> 15 | 7 | 3.1.2. Experimento 2 (NB02): Validacio� n 2D con campo complejo . . . . . . . . . . 14 | 3.1.2. Experimento 2 (NB02): Validacio� n 2D con campo complejo . . . . . . . . . . 15 |
| 3.14: -> 3.11: | 25 | Python 3.14: Lenguaje de implementacio� n principal. | Python 3.11: Lenguaje de implementacio� n principal. |
| E(0) = 1, E(1) = cos(k), -> E(xj) = cos(kxj), xj {0, 0.25, 0.5, 0.75, 1}, | 26 | d2E + k2E = 0, E(0) = 1, E(1) = cos(k), (3.1) dx2 | d2E + k2E = 0, E(xj) = cos(kxj), xj {0, 0.25, 0.5, 0.75, 1}, (3.1) dx2 |
| (vacio) -> Se imponen cinco puntos de frontera (en lugar de u� nicamente los do... | 26 | de pe� rdida. | de pe� rdida. Se imponen cinco puntos de frontera (en lugar de u� nicamente los dos extremos x = 0 y x = 1): la condicio� n sime� trica E(0) = E(1) = 1 colapsa la red hacia la solucio� n constante trivial durante el entrenamiento, ya que ambos extremos son co... |
| kx = ky = , (3.2) 2 14 Cap�itulo 3. Modelo e implementacio� n -> (3.2) kx = ky ... | 26->27 | Eexacta(x, y) = ei(kxx+kyy), k kx = ky = , (3.2) 2 14 Cap�itulo 3. Modelo e implementacio� n | Eexacta(x, y) = ei(kxx+kyy), k (3.2) kx = ky = , 2 |
| (vacio) -> (vacio) | 27 | Ereal(x, y) = cos(kxx + kyy), Eimag(x, y) = sin(kxx + kyy). (3.3) | Ereal(x, y) = cos(kxx + kyy), Eimag(x, y) = sin(kxx + kyy). (3.3) |
| (vacio) -> (vacio) | 27 | E(x, 0) = ei(x), (x) U (0, 2), (3.4) | E(x, 0) = ei(x), (x) U (0, 2), (3.4) |
| (vacio) -> 15 Cap�itulo 3. Modelo e implementacio� n | 27 | (sin contenido previo) | 15 Cap�itulo 3. Modelo e implementacio� n |
| (vacio) -> caso 1D. | 27->28 | (sin contenido previo) | caso 1D. |
| caso 1D. Para� metros totales: 8,400 -> Para� metros totales: 16,833 | 27->28 | caso 1D. Para� metros totales: 8,400 (NB01) y 66,690 (NB02/NB03). | Para� metros totales: 16,833 (NB01) y 66,690 (NB02/NB03). |
| 15 Cap�itulo 3. Modelo e implementacio� n -> (vacio) | 27->28 | 15 Cap�itulo 3. Modelo e implementacio� n | (contenido eliminado) |
| (vacio) -> (vacio) | 28 | L = Ldatos + f�is LRreal + LRimag , (3.5) | L = Ldatos + f�is LRreal + LRimag , (3.5) |
| (vacio) -> (vacio) | 28 | Rreal(r) = 2Ereal(r) + k2Ereal(r), Rimag(r) = 2Eimag(r) + k2Eimag(r), (3.6) | Rreal(r) = 2Ereal(r) + k2Ereal(r), Rimag(r) = 2Eimag(r) + k2Eimag(r), (3.6) |
| (vacio) -> 16 Cap�itulo 3. Modelo e implementacio� n | 28 | (sin contenido previo) | 16 Cap�itulo 3. Modelo e implementacio� n |
| 16 Cap�itulo 3. Modelo e implementacio� n -> (vacio) | 28->29 | 16 Cap�itulo 3. Modelo e implementacio� n | (contenido eliminado) |
| E(rjb)) -> E(rbj)) | 29 | fase aleatoria en NB03) y se construye el par (rjb, E(rjb)) utilizado en Ldatos. | fase aleatoria en NB03) y se construye el par (rjb, E(rbj)) utilizado en Ldatos. |
| NB01, NB02, NB03 Semilla global (SEED) 100 -> -- Semilla global (SEED) 50 (NB01... | 29 | Historial L-BFGS 500 (NB01), 1,000 (NB02/03) NB01, NB02, NB03 Semilla global (SEED) 100 NB01, NB02, NB03 | Historial L-BFGS 500 (NB01), 1,000 (NB02/03) -- Semilla global (SEED) 50 (NB01), 100 (NB02/03) NB01, NB02, NB03 |
| (8,400 para� metros) con los hiperpara� metros de la Tabla 3.1. Los puntos de c... | 32 | ecuacio� n de Helmholtz 1D. Se empleo� la arquitectura SIREN 5 � 64 (8,400 para� metros) con los hiperpara� metros de la Tabla 3.1. Los puntos de colocacio� n son Nc = 1,000 puntos uniformes en [0, 1] y las condiciones de frontera Dirichlet son E(0) = 1 y E(1... | ecuacio� n de Helmholtz 1D. Se empleo� la arquitectura SIREN 5 � 64 (16,833 para� metros) con los hiperpara� metros de la Tabla 3.1. Los puntos de colocacio� n son Nc = 2,000 puntos uniformes en [0, 1] y las condiciones de frontera Dirichlet se imponen en cin... |
| y -> & | 41 | Schoder y Kraxberger (2024) 1D 2.490 � | Schoder & Kraxberger (2024) 1D 2.490 � |
| y -> & | 41 | Schoder y Kraxberger (2024) 2D 0.006 �415 | Schoder & Kraxberger (2024) 2D 0.006 �415 |
| y Kraxberger (2024) aborda el caso 3D con activacio� n tanh; este trabajo opera... | 41 | dominios normalizados. Schoder y Kraxberger (2024) aborda el caso 3D con activacio� n tanh; este trabajo opera en 1D/2D adimensionales con arquitectura SIREN. El factor de mejora refleja tanto la ventaja arquitectural de SIREN sobre tanh/ReLU como la diferenc... | dominios normalizados. Schoder & Kraxberger (2024) aborda el caso 3D con activacio� n tanh; este trabajo opera en 1D/2D adimensionales con arquitectura SIREN. El factor de mejora refleja tanto la ventaja arquitectural de SIREN sobre tanh/ReLU como la diferen-... |
