# Modelo matemático de difracción en región convergente y divergente de una lente esférica (Andrés-Zárate et al., 2019)

> Fuente: `AndresZarate_etal_2019_DifraccionLenteEsferica.pdf` (convertido con pdftotext desde `master_supporting_docs/supporting_papers/referencias/`)

---

RESEARCH                             Revista Mexicana de F´ısica 65 (2019) 299–306  MAY-JUNE 2019

                Modelo matema´tico de difraccio´n en regio´n convergente
                               y divergente de una lente esfe´rica

                   E. Andre´s-Za´ratea, Q. Angulo Co´rdovaa, G. Gutie´rrez Tepacha, and J.A. Herna´ndez-Nolascob
                                             aUniversidad Jua´rez Auto´noma de Tabasco, DACB,

                                         Carr. Cunduaca´n-Jalpa Km. 1.5, Tabasco, 86680 Me´xico.
                                             bUniversidad Jua´rez Auto´noma de Tabasco, DAIS,

                                         Carr. Cunduaca´n-Jalpa Km. 1.5, Tabasco, 86680 Me´xico.
                                                       e-mail: adan.hernandez@ujat.mx

                                                  Received 10 August 2018; accepted 27 November 2018

Usando el me´todo de propagacio´n del espectro angular, se determinaron los modelos matema´ticos de difraccio´n o´ptica asociados a la dis-
tribucio´n de amplitud del campo difractado por dos aberturas circulares de dia´metros diferentes. Se establece la existencia de un patro´n de
difraccio´n derecho y otro izquierdo, as´ı como el desfasamiento del campo al propagarse en las regiones de Fresnel (convergente y divergente)
de una lente esfe´rica. Se muestran resultados experimentales, as´ı como los generados mediante simulacio´n.

Descriptores: Difraccio´n; convolucio´n; convergente; divergente; Fresnel.

The mathematical models of optical diffraction were determined using spectral angular propagation, which are associated with the amplitude
distribution of the ﬁeld diffracted by two circular apertures with different diameters. The existence of a right and left diffraction pattern is
established and also the ﬁeld offset as it propagates in the Fresnel zones (convergent and divergent) of a spherical lens. Herein, experimental
and the simulation resoults are shown.

Keywords: Diffraction; convolution; convergent; divergent; Fresnel.

PACS: 42.15.Eq; 42.25.Fx; 42.30.Kq.                                 DOI: https://doi.org/10.31349/RevMexFis.65.299

1. Introduccio´n                                                    cio´n hacia las regiones convergente y divergente de la lente
                                                                    transformadora.
El problema de difraccio´n de luz coherente puede ser inter-
pretado como el mapeo de la distribucio´n de amplitud del               En este trabajo, se reporta el estudio de propagacio´n has-
campo o´ptico en algunas regiones del espacio, asociado a es-       ta la regio´n convergente y divergente del doblete cementado
te problema existe la necesidad de describir la distribucio´n de    del campo de difraccio´n producido por dos aberturas circu-
amplitud caracterizada por la funcio´n de transmitancia t(x, y)     lares con radios de diferente magnitud, contenidas en mate-
asociada a la abertura u objeto difractor en planos de la re-       rial laminado, iluminadas con ondas planas. El tratamiento
gio´n convergente, divergente y focal de una lente esfe´rica [1].   se realizo´ bajo el formalismo del me´todo de propagacio´n del
Sheppard y Hrynevych [2], realizaron el estudio de difraccio´n      espectro angular.
por una abertura circular, en el que propusieron una genera-
lizacio´n a la teor´ıa de difraccio´n de Fresnel, a trave´s de una  2. Materiales y me´todos
aproximacio´n por variacio´n paraboidal en vez de una varia-
cio´n binominal en los te´rminos de fase en la ecuacio´n. Quin-     El modelo matema´tico de difraccio´n fue generado de acuer-
tero et al., [3] estudiaron los efectos de difraccio´n e interfe-   do con el arreglo de la Fig. 1. Centrando el ana´lisis de propa-
rencia producidos por una estructura compuesta de mu´ltiples        gacio´n del campo difractado por las dos aberturas (Fig. 1,4)
aberturas circulares ide´nticas, no reportan ana´lisis de propa-    colocadas en el plano x0y0, de radios a1 y a2 de diferentes
gacio´n, ni presentan un modelo matema´tico de difraccio´n, ya
que el trabajo lo realizaron sin el uso de lente transformadora.    FIGURA 1. Procesador de Fourier usado para obtener patrones de
                                                                    difraccio´n. Sobre la ﬁgura identiﬁcamos a: (1) laser de He-Ne, (2)
    Za´rate [4] estudio´ la propagacio´n del campo difractado       ﬁltro espacial, (3) colimador, (4) objeto bajo estudio en plano x0y0,
por dos aberturas de radios con igual magnitud, su ana´lisis lo     (5) lente transformadora, y (6) plano de observacio´n xzyz.
realizo´ hasta la regio´n de Fraunhofer o de la transformada de
Fourier, usando un doblete cementado como lente transfor-
madora. Mientras que Za´rate et al., [6], realizaron un ana´lisis
de propagacio´n hasta el plano de enfoque o de Fraunhofer
de un doblete cementado como lente transformadora, adema´s
presentaron ima´genes de patrones de difraccio´n generados de
forma experimental, en las cuales no se aprecia la geometr´ıa
el´ıptica de las franjas de ma´xima y m´ınima intensidad, sin
realizar un ana´lisis de la propagacio´n del campo de difrac-
300          E. ANDRE´ S-ZA´ RATE, Q. ANGULO CO´ RDOVA, G. GUTIE´ RREZ TEPACH, AND J. A. HERNA´ NDEZ-NOLASCO

magnitudes iluminadas con ondas planas monocroma´ticas                        operacio´n de convolucio´n de funciones:
de amplitud constante E0. La funcio´n de transmitancia
                                                                              Gz (u, v) = eik[fLD+z+nL1∆L1+nL2∆L2]                       E0fLD
que se le asocia al par de aberturas como objeto difractor                                                                             (fLD − z)
es, t0(x0, y0) = lzcirc(r01 − l1/a1) + lzcirc(r02 + l1/a2)
Goodman, (2005), siendo l1 la distancia a la que se encuen-                   • lz a21e−i2πl1u                     J1(2πa1ω)
                                                                                                                        ω
tran desplazadas las aberturas circulares, respecto al origen
de coordenadas del plano objeto x0y0 ver Fig. 1, cuyo espe-                   + a22ei2πl1u                J1(2πa2ω)
sor es lz, r01 y r02 en coordenadas polares quedan deﬁnidos                                                    ω
como r01 = x201 + y021 y r02 = x022 + y022 respectiva-
mente.                                                                        ⊗ e−             iπλfL2 D  (u2  +v2  )                          .            (5)
                                                                                               (fLD −z)
    El campo de ondas monocroma´ticas difractadas por el ob-
                                                                                                                      u=     xz  ,v=      yz
jeto o aberturas circulares desplazadas del origen en la can-                                                             λfLD         λfLD
tidad l1, y distribuidas en el plano x0y0, esta´ dado por la
                                                                              3. Resultados Teo´ricos
Ec. (1).

E1(x0, y0) = E0t0(x0, y0)                                                     La Ec. (5) establece que, el patro´n de difraccio´n GzC (u, v)
                                                                              (el cual se interpreta como un patro´n de difraccio´n derecho),
             = E0      lz  circ  r01 −  l1  +  lz  circ  r02 +  l1    .  (1)
                                    a1                      a2                se ha propagado hasta la regio´n de Fresnel convergente situa-
                                                                              da en el intervalo de distancia 0 < z < fLD, donde fLD
    Za´rate et al., [6] determinaron que la distribucio´n de am-              es la distancia focal de la lente transformadora o doblete ce-
plitud del campo propagado hasta el plano xzyz, en el que se
distribuye, se obtiene mediante la Ec. (2), en la que se ha usa-              mentado. Mediante el uso de las propiedades distributiva y

do como condicio´n inicial que el objeto difractor este´ coloca-              conmutativa de la convolucio´n, la Ec. (5) se reescribe para
do a la distancia d0, la cual es la misma que la longitud focal
del doblete cementado o lente transformadora (do = fLD),                      esta regio´n de Fresnel convergente en la forma dada por la
adema´s de considerar el teorema de la transformada de Fou-
                                                                              Ec. (6). En esta ecuacio´n, el desfasamiento que ha sufrido el
rier del producto de funciones [7].                                           campo propagado desde el plano x0y0 hasta el plano xzyz en
                                                                              el intervalo arriba especiﬁcado, es de π/4, el cual se obtiene

                                                                              realizando la integral de convolucio´n de la Ec. (5) y conside-
                                                                              rando que fLD − z > 0.

Gz(u, v)  =  E e0 ik[fLD +z+nL1∆L1+nL2∆L2]               F {t0(x0, y0)}       GzC (u, v)       =  2lz E0eik[fLD +z+nL1∆L1+nL2∆L2]
                           iλfLD                                                                                λ(fLD − z)

     ⊗ F e ( ) ik                                                                              × e e iπl21(fLD −z) cos2 φ    −i  π
                          2fLD                                                                                       λfL2 D      4
                       x02 +y02  1−     z                             . (2)
                                     fLD

                                               u=     xz  ,v=     yz                                                  J1(2πa1ω)
                                                   λfLD        λfLD                                                        ω
                                                                                               • a21e−i2πl1u

    La transformada de Fourier de la funcio´n de transmitancia                                 + a22ei2πl1u        J1(2πa2ω)           .                   (6)
t0(x0, y0) en la Ec. (2) se obtiene usan√do el teorema de linea-                                                        ω
lidad, escalamiento [7]; siendo ω = u2 + v2 la frecuencia
espacial deﬁnida en el plano de frecuencias espaciales uv,                        El patro´n de difraccio´n propagado hasta la regio´n de Fres-

resultando                                                                    nel divergente de la lente transformadora, situada en el inter-
                                                                              valo de distancia z dentro del intervalo fLD < z < ∞ se
     F {t0(x0, y0)} = lz a21e−i2πl1u               J1(2πa1ω)                  interpreta como un patro´n de difraccio´n izquierdo, quedando
                                                        ω
                                                                              deﬁnido a trave´s de la Ec. (7), el desfasamiento en esta re-
                       + a12ei2πl1u         J1(2πa2ω)           .        (3)  gio´n fue de 3π/4, mismo que se determina considerando que
                                                 ω                            z − fLD > 0 y realizando la integral de convolucio´n de la
                                                                              Ec. (5).

    En tanto que la transformada de Fourier de la Funcio´n                    GzD (u, v) = eik[fLD+z+nL1∆L1+nL2∆L2]
exponencial de la Ec. (2) es:

          (x02 +y02 )               λfL2D          iπλfL2 D     (u2  +v2                    ×     2lz E0           e • e −i3π       iπl21 (fLD −z) cos2 φ
     e = ik                      −i(fLD −z )       (fLD −z)               )                                            4                         λfL2 D
F       2fLD                                       e . −
                                                                                                  λ(fLD − z)

                                                                         (4)                × a21e−i2πl1u          J1(2πa1ω)
                                                                                                                        ω

    Sustituyendo las Ecs. (3) y (4) en la Ec. (2) se determina                              + a22ei2πl1u      J1(2πa2ω)             .                      (7)
                                                                                                                   ω
que la distribucio´n de amplitud del campo difractado, que-
da deﬁnida por la Ec. (5) en la que el s´ımbolo ⊗ indica la

                                                          Rev. Mex. Fis. 65 (2019) 299–306
   MODELO MATEMA´ TICO DE DIFRACCIO´ N EN REGIO´ N CONVERGENTE Y DIVERGENTE DE UNA LENTE ESFE´ RICA                     301

Las distribuciones de intensidad para las regiones de Fres-     lente transformadora es:
nel (convergente y divergente) de la lente transformadora, se
determinan respectivamente por las Ecs. (8) y (9).                                  2(E0 lz fLD )2  2           a1J1(2πa1ω) 2
                                                                                    λ(fLD − z)                         ω
                                                                IzC (u, v) =                           a13

IzC (u, v) =   2(E0 lz fLD )2  cos(2πl1u)                                        +  2a21a22  (πa1ω)(2πa2ω)  cos(4πl1u)
            ×  λ(fLD − z)                                                                    (πa1ω + πa2ω)

               a12 2  J1(2πa1ω)  2             J1(2πa1ω)                         × 2J0(2πa1ω)J1(2πa2ω)
                           ω                        ω
                                   + 2a21a22                                     + [2J1(2πa1ω)J0(2πa2ω)]

   ×           J1(2πa2ω)  + a22 2     J1(2πa2ω)  ,  (8)                          −  2a21a22  (πa1ω)(2πa2ω)  cos(4πl1u)
                    ω                      ω                                                 (πa1ω + πa2ω)

                                                                                 × [J1(2πa1ω + 2πa2ω)]

IzD(u, v) =    2(E0 lz fLD )2  cos(2πl1u)                                        + a23       a2J1(2πa2ω)    2           (11)
            ×  λ(z − fLD)                                                                           ω
                                                                                                             .

               a21 2  J1(2πa1ω)  2             J1(2πa1ω)            La distribucio´n de intensidad en la regio´n de Fresnel di-
                           ω                        ω           vergente de la lente transformadora, se determina consideran-
                                   + 2a12a22                    do que la suma de funciones Bessel en la Ec. (10) no aporta
                                                                informacio´n relevante, bajo esta condicio´n la Ec. (9) se rees-
   ×           J1(2πa2ω)  +    a22 2  J1(2πa2ω)  .  (9)         cribe en la forma:
                    ω                      ω
                                                                                                    2           a1J1(2πa1ω) 2
                                                                                    2(E0 lz fLD )2                     ω
                                                                IzD(u, v) =         λ(fLD − z)         a31

    Los productos de funciones Bessel J1(2πa1ω)J1(2πa2ω)                         +  2a21a22  (πa1ω)(2πa2ω)  cos(4πl1u)
de las Ecs. (8) y (9), se determinan usando la siguiente ecua-                               (πa1ω + πa2ω)
cio´n [8,4].

                          (πa1ω)((πa2ω))                                         × 2J0(2πa1ω)J1(2πa2ω)
                           πa1ω + πa2ω
J1(2πa1ω)J1(2πa2ω)    =                                                          + [2J1(2πa1ω)J0(2πa2ω)]

• 2J0(2πa1ω)J1(2πa2ω) + 2J1(2πa1ω)J0(2πa2ω)                                      −  2a12a22  (πa1ω)(2πa2ω)  cos(4πl1u)
                                                                                             (πa1ω + πa2ω)
−  (πa1ω)(2πa2ω)      [J1(2πa1ω    +  2πa2ω)]
   (πa1ω + πa2ω)                                                                 × [J1(2πa1ω + 2πa2ω)]

+  (πa1ω)(2πa2ω)                                                                 + a23       a2J1(2πa2ω)    2           (12)
   (πa1ω + πa2ω)                                                                                    ω
                                                                                                             .

    s=∞                                                             En la Ec. (11) la distribucio´n del patro´n de difraccio´n que
                                                                se propaga en la regio´n de Fresnel convergente de la lente
× (−1)s Js(2πa1ω)J1+s(2πa2ω)                                    transformadora, diﬁere solo en el denominador de la distri-
                                                                bucio´n de intensidad deﬁnida con la Ec. (12) del patro´n de
   s=2                                                          difraccio´n izquierdo que se propaga en la regio´n de Fresnel
                                                                divergente de la lente transformadora. Las Ecs. (11) y (12)
+ J1+s(2πa1ω)Js(2πa2ω) .                            (10)        nos permiten aﬁrmar que en las regiones convergente y di-
                                                                vergente de la lente transformadora existe un patro´n de di-
    Considerando que los productos de las funciones Bessel      fraccio´n el´ıptico que modula franjas de Young.
de la Ec. (10) deﬁnidos por la suma
                                                                4. Resultados experimentales
                 s=∞
                                                                Los experimentos se desarrollaron empleando el sistema
                 (−1)s Js(2πa1ω)J1+s(2πa2ω)                     o´ptico de la Fig. 2a, el cual esta´ en relacio´n directa con
                                                                el esquema de la Fig. 1. El haz de luz de laser de He-Ne
                  s=2                                           (λ = 632 nm) ampliado y ﬁltrado con objetivo de microsco-
                                                                pio 40X y pinhole de 50 µm, fue colimado con lente doblete
                         + J1+s(2πa1ω)Js(2πa2ω) ,               acroma´tico de 50 cm de distancia focal. Como objeto difrac-

no aportan informacio´n relevante a la distribucio´n de inten-
sidad, por lo cual no se toman en cuenta, y combinando la
ecuacio´n referida con la Ec. (8). Se obtiene que la distribu-
cio´n de intensidad en la regio´n de Fresnel convergente de la

                                               Rev. Mex. Fis. 65 (2019) 299–306
302  E. ANDRE´ S-ZA´ RATE, Q. ANGULO CO´ RDOVA, G. GUTIE´ RREZ TEPACH, AND J. A. HERNA´ NDEZ-NOLASCO

FIGURA 2. a) Arreglo experimental, b) Aperturas con radios dife-
rentes magnitudes.

tor, se usaron dos aberturas circulares, su imagen se muestra       FIGURA 3. a), b), c), d) y e) Patrones de difraccio´n de convolucio´n
en la Fig. 2b, cuyos radios de curvatura son: a1 = 1.0 mm           grabados a diferentes distancias de la lente transformadora obteni-
y a2 = 1.5 mm, respectivamente. Contenidas en material la-          dos experimentalmente.
minado de pla´stico con lz = 2.0 mm de espesor. Se uso´ co-
mo lente transformadora un doblete acroma´tico cementado            muestra m´ınimos de irradiancia centrales en cada patro´n, se
de 25 cm de distancia focal. Las ima´genes de cada patro´n de       establece que es ma´s dominante la funcio´n de Bessel de orden
difraccio´n en intensidad, se grabaron usando una ca´mara di-       uno en el producto con la funcio´n de Bessel de orden cero a
gital de alta velocidad y precisio´n, con sensor CMOS y 18.0        la distancia z = 22 cm de propagacio´n. Mientras que a la dis-
mega-pixeles.

    En la regio´n de Fresnel convergente situada en el interva-
lo de distancia 0 < z < fLD de la lente transformadora, se
obtiene la convolucio´n de los patrones de difraccio´n, cuan-
titativamente los podemos relacionar con los valores exac-
tos dados por la Ec. (11) y se consideran derechos. La Fig.
3. a), b) y d) muestran la distribucio´n de irradiancia, de los
campos de difraccio´n de convolucio´n grabados a diferentes
distancias, ver Tabla I, en la regio´n de Fresnel convergente
antes referida, puede observarse que el patro´n de difraccio´n
esta´ formado por franjas el´ıpticas con distribucio´n tipo Bessel
modulando franjas de Young.

    Las ima´genes de la Fig. 3, fueron generadas cuando los
centros geome´tricos de las aberturas circulares Fig. 2, se
orientaron paralelas al eje x0 del plano objeto. La Fig. 3a,

     Rev. Mex. Fis. 65 (2019) 299–306
MODELO MATEMA´ TICO DE DIFRACCIO´ N EN REGIO´ N CONVERGENTE Y DIVERGENTE DE UNA LENTE ESFE´ RICA  303

TABLA I. Distancia objeto lente y lente plano de grabado, centros
geometricos paralelos al eje x0.

  Distancia lente      Distancia lente    Nu´ mero
objeto difractor d0  plano de grabado z  de imagen

       25cm                  22cm            3a
       25cm                  23cm            3b
       25cm                  48cm            3c
       25cm                  24cm            3d
       25cm                  35cm            3e

TABLA II. Distancia objeto lente y lente plano de grabado, centros
geometricos paralelos al eje y0.

  Distancia lente      Distancia lente    Nu´ mero
objeto difractor d0  plano de grabado z  de imagen

       25cm                  20cm            4a
       25cm                  23cm            4b
       25cm                  48cm            4c

tancia de propagacio´n z = 23 cm y z = 24 cm, la funcio´n           FIGURA 4. a), b), c), d) y e) Patrones de difraccio´n generados me-
de Bessel de orden cero es la dominante en el producto dan-         diante simulacio´n.
do ma´ximos centrales de difraccio´n, ver Figs. 3b y 3d. Se
observa que, conforme se acerca el plano de grabado a la dis-
tancia focal de la lente transformadora los ma´ximos centra-
les en cada patro´n se ampliﬁcan Fig. 3d. Las ima´genes de
la Fig. 3c y 3e se consideran izquierdas y dan referencia del
grabado de patrones de difraccio´n en la zona de Fresnel di-
vergente o de convolucio´n situada en el intervalo de distancia
fLD < z < ∞ de la lente transformadora; se observa que
cada patro´n contiene m´ınimos y ma´ximos de irradiancia al-
ternados, cuantitativamente se pueden relacionar con los va-
lores exactos dados por la Ec. (12), adema´s se ve que cada
patro´n de difraccio´n esta´ formado por franjas el´ıpticas con
distribucio´n tipo Bessel modulando franjas de Young.

    La Fig. 5. a), b) y c) muestran la distribucio´n de irra-
diancia, de los campos de difraccio´n de convolucio´n graba-
dos a diferentes distancias de la lente transformadora, ver
Tabla II. Cuantitativamente los podemos relacionar con los
valores exactos dados por la Ec. (11) y se consideran dere-
chos, en la regio´n de Fresnel (convergente) antes referida,
puede observarse que el patro´n de difraccio´n esta´ formado
por franjas el´ıpticas con distribucio´n tipo Bessel modulando
franjas de Young. Las ima´genes de la Fig. 5a y 5b, fueron
generadas cuando los centros geome´tricos de las aberturas
circulares ver Fig. 2, se orientaron paralelas al eje y0 del pla-
no objeto. La imagen de la Fig. 5a, muestra un ma´ximo y un
m´ınimo de irradiancia centrales en cada patro´n, se establece
que en el patro´n de difraccio´n superior es ma´s dominante la
funcio´n de Bessel de orden cero que la funcio´n de Bessel de
orden uno, en el producto de funciones de Bessel a la dis-
tancia z = 20 cm; mientras que, en el patro´n de difraccio´n
inferior, dimina la funcio´n, ma´s que la de orden cero en el
producto, de acuerdo a la Ec. (11). A la distancia de

                                         Rev. Mex. Fis. 65 (2019) 299–306
304  E. ANDRE´ S-ZA´ RATE, Q. ANGULO CO´ RDOVA, G. GUTIE´ RREZ TEPACH, AND J. A. HERNA´ NDEZ-NOLASCO

FIGURA 5. a), b), c) Patrones de difraccio´n de convolucio´n grabados en la regio´n de Fresnel convergente y divergente de la lente transforma-
dora obtenidos experimentalmente.

FIGURA 6. a), b) y c) Ima´genes de difraccio´n obtenidas mediante simulacio´n.

propagacio´n z = 24 cm, la funcio´n de Bessel de orden cero         muestran en la Fig. 7. a) y b). La imagen de la Fig. 7a corres-
es la dominante en el producto generando ma´ximos centra-           ponde al patro´n de difraccio´n de franjas el´ıpticas, producido
les de difraccio´n ver Fig. 5b. Se observa que, conforme se         por las dos aberturas circulares cuyos centros de curvatura
acerca el plano de grabado a la distancia focal de la lente         estaban orientados en el eje x0 del plano objeto, modulando
transformadora, los ma´ximos centrales en cada patro´n de di-       franjas verticales de Young. Por la forma en que la lente ha-
fraccio´n se ampliﬁcan. La imagen del patro´n de difraccio´n de     ce converger la informacio´n, las franjas el´ıpticas de ma´xima
la Fig. 5c se considera izquierdo y fue grabado en la zona de       y m´ınima intensidad, quedan orientadas hacia el eje v en el
Fresnel divergente o de convolucio´n de la lente transformado-      espacio de frecuencias espaciales. La imagen de la Fig. 7b,
ra; se observa que cada patro´n contiene m´ınimos y ma´ximos        muestra el patro´n de difraccio´n de transformada de Fourier,
de irradiancia alternados, puede observarse que el patro´n de       producido por el mismo par de aberturas circulares, con cen-
difraccio´n esta´ formado por franjas el´ıpticas con distribucio´n  tros de curvatura orientados hacia el eje y0 del plano objeto,
tipo Bessel modulando franjas de Young.                             en este caso las franjas el´ıpticas esta´n orientadas hacia el eje u
                                                                    en el espacio de frecuencias, modulando franjas horizontales
    En el plano focal, de Fraunhofer o de la transformada de        de Young.
Fourier, situado a la distancia z = 25 cm de la lente transfor-
madora, se grabaron los patrones de difraccio´n, los cuales se

     Rev. Mex. Fis. 65 (2019) 299–306
MODELO MATEMA´ TICO DE DIFRACCIO´ N EN REGIO´ N CONVERGENTE Y DIVERGENTE DE UNA LENTE ESFE´ RICA  305

FIGURA 7. a), b). Patrones de difraccio´n de transformada Fourier obtenidos de forma experimental. Las ima´genes c) y d) fueron obtenidas
mediante simulacio´n.

    El Teorema de rotacio´n publicado por Bracewell [9], es-      Propagation Method”, que es una herramienta computacio-
tablece que: Si una funcio´n f (x, y) es rotada en el plano xy,   nal ampliamente utilizada en o´ptica, y es una te´cnica nume´ri-
entonces su transformada de Fourier g(u, v) es rotada en el       ca viable para el ca´lculo de haces o´pticos en propagacio´n li-
plano uv a trave´s del mismo a´ngulo y en el mismo senti-         bre, con pequen˜as o nulas variaciones en el ´ındice de refrac-
do. En base al teorema antes referido basta establecer que la     cio´n [10].
transformada de Fourier es sensible a rotacio´n, con lo cual
se establece que los patrones de difraccio´n mostrados en las         El algoritmo se implemento´ en el software matema´tico
Figs. 7a y 7b no son iguales, es decir, tienen distribucio´n ti-  MatLab, para emular la propagacio´n del haz laser de onda
po Bessel y son de geometr´ıa el´ıptica, el primero abre en la    plana con longitud de onda de 632 nm, por dos aberturas cir-
direccio´n de las frecuencias v, mientras que el segundo abre     culares de radios de diferentes magnitudes de a1 = 1.0 mm
en la direccio´n de eje de frecuencias espaciales u, en base a    y a2 = 1.5 mm espectivamente, tomadas como objeto difrac-
que las aberturas circulares, ha sufrido una rotacio´n de π/2     tor. Se construyo una malla de 60×60 mm, considerando 975
respecto del eje x0 en el plano objeto. Aunque las aberturas      muestras tanto para el eje x, como para el eje y. La distancia
mantengan su geometr´ıa circular.                                 entre los centros de las dos aberturas es de 7 mm.

5. Simulacio´n                                                        Una lente es un objeto de fase, para emular un doblete
                                                                  acroma´tico, consideramos un retardo de fase entregado por
La simulacio´n computacional permite de una forma visual y        una lente esfe´rica perfecta convergente con una longitud fo-
pra´ctica validar los resultados del modelo matema´tico de di-    cal de 25 cm. El objeto difractor se coloco´ a la distancia ﬁja
fraccio´n, en este caso empleamos el me´todo nume´rico ”Beam      d0 = 25 cm, que es equivalente a la distancia focal frontal
                                                                  del doblete cementado. Los diferenciales en el eje de propa-
                                                                  gacio´n z son dz = 20 mm.

Rev. Mex. Fis. 65 (2019) 299–306
306  E. ANDRE´ S-ZA´ RATE, Q. ANGULO CO´ RDOVA, G. GUTIE´ RREZ TEPACH, AND J. A. HERNA´ NDEZ-NOLASCO

    Para cada valor del dz se obtuvo una gra´ﬁca de intensi-        ciones de Bessel de orden uno son las dominantes en los pro-
dad del haz o´ptico difractado, guardando las ima´genes pre-        ductos para generar los m´ınimos de la Fig. 3a; mientras que
sentadas en la Fig. 4. f), g), h), i) y j) correspondientes a las   las funciones de Bessel de orden cero son dominantes para
mismas distancias z a las que se tomaron las fotograf´ıas en        generar los ma´ximos de irradiancia central ver Figs. 3b, 3d
la parte experimental, ver Tabla I, dentro de la zona conver-       y 5b. Por lo que se reﬁere a las Figs. 3c, 3e, 5a y 5c se ob-
gente; as´ı como las del caso de la zona divergente del doblete     serva que a las distancias que se grabaron, ver Tablas I y II,
cementado; adema´s, para este caso de simulacio´n tambie´n se       se alternan tanto la funcio´n de Bessel de orden uno, como
considero´ que los centros geome´tricos de las aberturas fueron     la de orden cero en los productos, para producir de manera
orientados en el eje x0. Para el caso de los centros geome´tri-     simulta´nea un m´ınimo y un ma´ximo de irradiancia centrales.
cos paralelos al eje y0 se obtuvo una gra´ﬁca de intensidad del
haz o´ptico difractado, guardando las ima´genes simuladas, las          Los resultados de tipo experimental mostrados en las
cuales se muestran en la Fig. 6. d), e) y f), y corresponden        Figs. 7a y 7b refuerzan lo publicado por [5], en lo referen-
a las mismas distancias z a la lente de acuerdo a la Tabla II,      te a las ima´genes de transformada de Fourier, en ellas se hace
a las que se tomaron las ima´genes en la etapa experimental,        evidente la forma el´ıptica del patro´n de difraccio´n.
tanto en la zona convergente y divergente del doblete cemen-
tado.                                                                   En lo que respecta a las ima´genes de los patrones de di-
                                                                    fraccio´n Figs. 4, 6, 7c y 7d obtenidas mediante simulacio´n,
    En la Fig. 7. c) y d) se muestran los patrones de difraccio´n   tanto en la zona convergente, focal o de Fraunhofer, as´ı co-
simulados de transformada de Fourier, obtenidos en el plano         mo en la divergente del doblete cementado; los patrones de
focal o de Fraunhofer de la lente, las l´ıneas de difraccio´n de    intensidad son muy similares a los obtenidos de forma expe-
Young son bastante claras y bien deﬁnidas, y se aprecia su          rimental mostrados en las Figs. 3, 5, 7a y 7b respectivamente.
orientacio´n horizontal y vertical. En tanto que las franjas de
Bessel se distribuyen como las obtenidas de forma experi-           Agradecimientos
mental ver Fig. 7. a) y b); es decir, las franjas de ma´xima y
de m´ınima intensidad son el´ıpticas, como lo predijeron [6].       Los autores agradecen a la UJAT, el apoyo otorgado a trave´s
                                                                    del programa PFI para el desarrollo del proyecto clave UJAT-
6. Conclusiones                                                     2012-IB-45, del cual se derivo´ este trabajo. Uno de los auto-
                                                                    res (EAZ) agradece a la PLI Miroslava Za´rate Delf´ın su apo-
Los modelos matema´ticos de convolucio´n de transformadas           yo en la redaccio´n del Abstract de este trabajo.
de Fourier Ecs. (11) y (12), permiten establecer que las fun-

1. G. M. Niconoff , J. M.Lo´pez, y E. M. Mart´ınez, J. Opt. Am. A.   6. E. A. Za´rate, Q. A. Co´rdova, J. A. H. Nolasco, G. G. Tepa-
    10 (2001) 2089.                                                      ch, y C. G. T. Palacios. Elliptical Bessel-like diffraction pattern
                                                                         produced by circular apertures whith different radius, Pro. of
2. C. J. M.Sheppard y M. Hrynevych, Diffraction by a circular            SPIE, 8785 (2013) 1-6.
    aperture ageneralization of Fresnel difraction theory, J. Opt.
    Am. A, 8 (1992) 274.                                             7. J. D. Gaskill, Linear systems Fourier transforms and optics,
                                                                         John Wiley and Sons (1978) pp 150-217.
3. O. Quintero, F. B. John, R. Henao, y F. Medina, Optics Com-
    munications 206 (2006) 558.                                      8. S. I. Hayek, Advanced mathematica methods in science and en-
                                                                         gineering Weber, Marcel Dekker (2001) pp 166-176.
4. E. A. Za´rate, Estudio de patrones de difraccio´n en la Evalua-
    cio´n de Aberturas. Santa Mara´ Tonantzintla, INAOE Puebla,      9. N Bracewell Ronal, The Fourier transforms and its applica-
    Me´xico. (2011) pp 5-190.                                            tions, McGraw Hill, (2002) pp 129, 332.

5. J. W. Goodman Introduction to Fourier Optics, 3a ed. McGraw      10. D. Schmidt Jason, Numerical simulation of optical wave pro-
    Hill (2005) pp 78-84.                                                pagation with examples in MATLAB, Edit Spie press (2010).

     Rev. Mex. Fis. 65 (2019) 299–306
