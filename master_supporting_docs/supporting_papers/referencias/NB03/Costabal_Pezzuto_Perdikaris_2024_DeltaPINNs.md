# Ficha de lectura: Delta-PINNs

## Referencia verificada

Francisco Sahli Costabal, Simone Pezzuto y Paris Perdikaris. "Delta-PINNs:
Physics-informed neural networks on complex geometries". Engineering
Applications of Artificial Intelligence, volumen 127, parte B, artículo
107324, 2024. DOI: 10.1016/j.engappai.2023.107324. Preprint: arXiv:2209.03984.

## Aporte principal

El método reemplaza las coordenadas euclidianas directas de entrada por una
codificación posicional formada con autofunciones del operador de
Laplace-Beltrami. Las autofunciones y los operadores diferenciales se aproximan
mediante elementos finitos. El objetivo es representar correctamente la
topología de dominios complejos y superficies donde la distancia euclidiana no
refleja la distancia intrínseca.

## Relación con NB03

La relación conceptual es útil: tanto Delta-PINNs como el enfoque modal de NB03
usan autofunciones de un operador espacial para proporcionar características
adecuadas a la física. En el dominio rectangular y periódico de NB03, los modos
de Fourier ya son autofunciones naturales del Laplaciano transversal.

No se recomienda sustituir ahora la PINN-SIREN modal por Delta-PINNs porque:

- NB03 no utiliza una geometría irregular ni una variedad curva.
- El método requeriría una malla FEM para obtener autofunciones y operadores.
- Cambiaría la implementación y complicaría la comparación actual con espectro
  angular.
- Los resultados por bloques ya satisfacen el umbral de campo en las pantallas
  evaluadas.

Sí puede citarse como antecedente de codificaciones espectrales informadas por
la geometría y reservarse como extensión futura si se incorpora una lente o un
dominio óptico de geometría curva.

