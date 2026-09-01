# Propagación infrarroja de haces adifraccionales en la atmósfera — Tesis de Maestría, José Adán Hernández Nolasco (ITESM, 2003)

> Fuente: `tesis_maestría_maestria_de_Adán.pdf` (convertido con pdftotext desde `master_supporting_docs/supporting_tesis/`)

---

Instituto Tecnolo´gico y de Estudios Superiores de
                              Monterrey

                               Campus Monterrey
     Divisi´on de Electr´onica, Computaci´on, Informaci´on, y

                                 Comunicaciones

                                    Programa de Graduados

      Propagaci´on infrarroja de haces adifraccionales en la
                                      atm´osfera
                                        TESIS

Presentada como requisito parcial para obtener el grado acad´emico de
           Maestro en Ciencias en Ingenier´ıa Electr´onica
                  Especialidad en Telecomunicaciones
                   Ing. Jos´e Ad´an Hern´andez Nolasco

                                 Monterrey, N.L. Febrero de 2003
c Jos´e Ad´an Hern´andez Nolasco, 2003
Instituto Tecnolo´gico y de Estudios Superiores de
                             Monterrey

                              Campus Monterrey

    Divisi´on de Electr´onica, Computaci´on, Informaci´on, y
                                 Comunicaciones

                                   Programa de Graduados

Los miembros del comit´e de tesis recomendamos que la presente tesis de Jos´e Ad´an
   Hern´andez Nolasco sea aceptada como requisito parcial para obtener el grado
                             acad´emico de Maestro en Ciencias en:
                                     Ingenier´ıa Electr´onica
                           Especialidad en Telecomunicaciones

                                 Comit´e de tesis:

Ram´on M. Rodr´ıguez Dagnino,
                Ph.D.

          Asesor de la tesis

Julio C´esar Guti´errez Vega, Ph.D.  Servando L´opez Aguayo, M.Sc.

                   Sinodal                            Sinodal

David Garza Salazar, Ph.D.

  Programa de Graduados en
   Electr´onica, Computaci´on,
Informaci´on, y Comunicaciones

        Febrero de 2003
Con todo mi corazo´n a mi hijo Alexis David, a mi esposa Tammy Sammy y a mi
                                       hijo(a) que ya viene.
      Reconocimientos
      A mi esposa y a mi hijo, quienes son el motor de mi inspiracio´n y el motivo de
mi existencia.
      A mis padres y a mi hermana por su carin˜o y por que siempre me han alentado a
salir adelante.
      A mi asesor, Dr. Ramo´n M. Rodriguez Dagnino por su orientaci´on y gu´ıa para la
realizaci´on de este trabajo.
      A mis sinodales, el Dr. Julio C´esar Guti´errez Vega y al M.Sc. Servando L´opez
Aguayo por sus valiosas aportaciones y sugerencias.

                                             Jose´ Ada´n Herna´ndez Nolasco

 Instituto Tecnolo´gico y de Estudios Superiores de Monterrey
 Febrero 2003
       Propagaci´on infrarroja de haces adifraccionales en la
                                       atm´osfera

                               Jos´e Ad´an Hern´andez Nolasco, M.Sc.
            Instituto Tecnol´ogico y de Estudios Superiores de Monterrey, 2003

                   Asesor de la tesis: Ram´on M. Rodr´ıguez Dagnino, Ph.D.

En el presente trabajo se hace un estudio de la propagaci´on de ondas ´opticas a trav´es
del vac´ıo y de la atm´osfera, haciendo ´enfasis en los haces adifraccionales. Se realizaron
diversas simulaciones utilizando m´etodos de diferencias ﬁnitas, y tratando la turbulen-
cia atmosf´erica con modelos probabil´ısticos.
´Indice General

´Indice de Figuras                                    iii

Cap´ıtulo 1 Introducci´on                             1

1.1 Introducci´on . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 1

1.2 Justiﬁcaci´on . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 1

1.3 Objetivo . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 2

1.4 Organizaci´on de la tesis . . . . . . . . . . . . . . . . . . . . . . . . . . 2

Cap´ıtulo 2 An´alisis electromagn´etico               3

2.1 Ecuaci´on escalar de onda . . . . . . . . . . . . . . . . . . . . . . . . . . 3

2.2 Ecuaci´on de Helmholtz . . . . . . . . . . . . . . . . . . . . . . . . . . . 6

2.3 Ecuaci´on paraxial de onda . . . . . . . . . . . . . . . . . . . . . . . . . 6

2.4 Soluci´on no difractiva de la ecuaci´on escalar de onda . . . . . . . . . . 8

Cap´ıtulo 3 Propagaci´on atmosf´erica del infrarrojo  11

3.1 Introducci´on . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 11

3.2 Difracci´on . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 12

3.3 Atenuaci´on . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 14

3.4 Modelos para la turbulencia atmosf´erica . . . . . . . . . . . . . . . . . 16

3.4.1 Distribuciones de probabilidad de la intensidad . . . . . . . . . 22

3.4.2 Estad´ısticas de centelleos . . . . . . . . . . . . . . . . . . . . . . 23

3.4.3 Modelo b´asico de las variaciones del ´ındice de refracci´on . . . . 24

Cap´ıtulo 4 Simulacio´n en una dimensi´on espacial    27

4.1 M´etodo de diferencias centrales . . . . . . . . . . . . . . . . . . . . . . 27

4.2 M´etodo Crank-Nicolson . . . . . . . . . . . . . . . . . . . . . . . . . . 30

4.3 Ecuaci´on paraxial de la luz . . . . . . . . . . . . . . . . . . . . . . . . . 33

4.3.1 Resultados . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 36

                           i
ii                                                     ´INDICE GENERAL

Cap´ıtulo 5 Simulacio´n en dos dimensiones espaciales         39

    5.1 M´etodo ADI . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 39

    5.2 Resultados . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 43

Cap´ıtulo 6 Propagaci´on con ´Indice de Refracci´on Variable  59

    6.1 An´alisis del ´ındice de refracci´on . . . . . . . . . . . . . . . . . . . . . . 59

    6.2 Resultados . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 62

Cap´ıtulo 7 Conclusiones                                      71

Bibliograf´ıa                                                 73

Vita                                                          75
´Indice de Figuras

    2.1 Dominio paraxial . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 7

    3.1 Deﬁnici´on de las zonas de Fresnel. . . . . . . . . . . . . . . . . . . . . . 13
    3.2 Fase del campo producido por cada una de las fuentes secundarias. . . 14
    3.3 Atenuaci´on por A:lluvia, B:niebla y C:componentes gaseosos . . . . . . 15
    3.4 Atenuaci´on espec´ıﬁca por absorci´on molecular . . . . . . . . . . . . . . 16
    3.5 Modelo del par´ametro estructura del ´ındice de refracci´on . . . . . . . . 18

    4.1 Malla para resolver diferencias centrales en la region R. . . . . . . . . . 28
    4.2 Oscilaci´on de una cuerda homog´enea con funci´on inicial sin x . . . . . . 31
    4.3 Oscilaci´on de una cuerda homog´enea con funci´on inicial la ecuaci´on 4.14 32
    4.4 Malla para el m´etodo de Crank-Nicolson. . . . . . . . . . . . . . . . . . 33
    4.5 Oscilaci´on de una cuerda homog´enea con una funci´on inicial sin x . . . 34
    4.6 Oscilaci´on de una cuerda homog´enea con funci´on inicial la ecuaci´on 4.14 35
    4.7 Propagaci´on de un laser HeNe para una rendija rectangular . . . . . . . 37
    4.8 Propagaci´on de un laser HeNe para dos rendijas rectangulares . . . . . 37
    4.9 Propagaci´on de un laser HeNe para una entrada cosenoidal . . . . . . . 38
    4.10 Propagaci´on de un laser HeNe para una entrada Gaussiana . . . . . . . 38

    5.1 Malla para el m´etodo ADI . . . . . . . . . . . . . . . . . . . . . . . . . 40
    5.2 Propagaci´on de un laser HeNe para una entrada circular . . . . . . . . 45
    5.3 Error relativo porcentual de la energ´ıa para una entrada circular . . . . 46
    5.4 Propagaci´on de un laser HeNe para una entrada Gaussiana . . . . . . . 47
    5.5 Secci´on transversal durante la propagaci´on de un haz Gaussiano . . . . 48
    5.6 Error relativo porcentual de la energ´ıa para una entrada Gaussiana . . 49
    5.7 Perﬁl transversal de un haz Bessel de primer tipo de orden cero . . . . 50
    5.8 Propagaci´on de un haz Bessel con λ = 632.8 nm . . . . . . . . . . . . . 51
    5.9 Secci´on transversal de un haz Bessel con ventana de 3 mm . . . . . . . 52
    5.10 Propagaci´on de un haz Bessel con λ = 632.8 nm . . . . . . . . . . . . . 53
    5.11 Secci´on transversal de un haz Bessel con ventana de 4 mm . . . . . . . 54

                                                      iii
iv  ´INDICE DE FIGURAS

    5.12 Propagaci´on de un haz Bessel con λ = 750 nm . . . . . . . . . . . . . . 55
    5.13 Secci´on transversal de un haz Bessel con ventana de 3 mm . . . . . . . 56
    5.14 Propagaci´on de un haz Bessel con λ = 500 nm . . . . . . . . . . . . . . 57
    5.15 Propagaci´on de haz Bessel con λ = 500 nm en ρ = 0 . . . . . . . . . . . 58

    6.1 Propagaci´on de la luz para una entrada rectangular . . . . . . . . . . . 61
    6.2 Propagaci´on con entrada rectangular y lente convergente en z = 0 . . . 61
    6.3 Propagaci´on con entrada rectangular y lente convergente en z = 0.75 m 62
    6.4 Haz Gaussiano con turbulencia (varianza= 7.45 × 10−16). . . . . . . . . 64
    6.5 Secci´on transversal del haz Gaussiano (varianza=7.43 × 10−10). . . . . . 65
    6.6 Haz Bessel en un medio con ´ındice aleatorio (varianza= 7.45 × 10−16). . 66
    6.7 Haz Bessel en un medio con ´ındice aleatorio (varianza= 7.45 × 10−14). . 67
    6.8 Haz Bessel en un medio con ´ındice aleatorio (varianza= 7.43 × 10−10). . 68
    6.9 Secci´on transversal del haz Bessel (varianza= 7.45 × 10−16). . . . . . . 69
    6.10 Secci´on transversal del haz Bessel (varianza= 7.45 × 10−14). . . . . . . 69
    6.11 Secci´on transversal del haz Bessel (varianza= 7.43 × 10−10). . . . . . . 70
Cap´ıtulo 1

Introducci´on

1.1 Introducci´on

Anteriormente, hablar de transmisi´on de sen˜ales ´opticas implicaba la utilizaci´on de
ﬁbras ´opticas para llevar a cabo los enlaces, ya que la propagaci´on de sen˜ales ´opticas
en el espacio libre se cre´ıa que tend´ıan a dispersarse desde su salida del emisor, y esto
por no tener un conducto o paredes que mantuvieran el haz de forma estrecha, por
ejemplo la ﬁbra ´optica. Los recientes descubrimientos de la no difracci´on de las ondas
ha despertado el inter´es de investigadores por ver su aplicabilidad a diferentes ´areas de
la ciencia, como es en im´agenes m´edicas, estimaci´on de velocidad doppler, y en enlaces
de comunicacio´n inal´ambricos.

      Utilizar sen˜ales ´opticas en las comunicaciones presenta algunas ventajas importan-
tes tales como un enorme ancho de banda, requiere poca potencia para su transmisi´on,
y adem´as es inmune a interferencias electromagn´eticas de las ondas de radio. Pero
tambi´en tienen desventajas los enlaces ´opticos inal´ambricos, una es la necesidad de que
exista l´ınea de vista entre el emisor y el receptor, y otra no menos importante que es
muy susceptible a los fen´omenos meteorol´ogicos en la atm´osfera. Debido principalmen-
te a que la longitud de onda de las sen˜ales ´opticas son extremadamente pequen˜as. Por
lo que la utilizaci´on de estos sistemas de comunicacio´n ´opticos podr´ıan estar limitados
a enlaces relativamente cortos, bajo algunas condiciones controladas como por ejemplo
dentro de un centro comercial, o en oﬁcinas.

1.2 Justiﬁcaci´on

Las comunicaciones inal´ambricas han llegado hoy en d´ıa a ser una tecnolog´ıa emergente.
E´sta es, dentro de la industria de las telecomunicaciones, el segmento con mayor creci-
miento. Una variedad de servicios basados en comunicaciones inal´ambricas ya existen

                                                       1
2  CAP´ITULO 1. INTRODUCCIO´N

hoy en d´ıa y est´an disen˜ados para transmitir voz o datos principalmente.
      El surgimiento de equipos de c´omputo y multimedia port´atiles en el trabajo y en

la vida cotidiana est´a llevando a la introducci´on de nuevas l´ıneas digitales inal´ambricas
y de redes de ´area local. El infrarrojo se est´a estableciendo como un medio prome-
tedor para enlaces de comunicaci´on inal´ambricos en distancias cortas. Por lo que es
importante analizar el comportamiento de los haces ´opticos al propagarse a trav´es de la
atm´osfera, principalmente el de los haces adifraccionales, pues pudiesen ser una buena
opci´on en dichos enlaces.

1.3 Objetivo

El objetivo principal de este trabajo de investigacio´n es el de simular la propagaci´on de
las ondas ´opticas no difractivas que se encuentran en el rango del infrarrojo, teniendo
consideraciones de la afectaci´on del ruido en el canal y las irregularidades en el medio
atmosf´erico, para observar su comportamiento y determinar si presenta ventajas con
respecto a los haces difractivos.

1.4 Organizaci´on de la tesis

En el capitulo 2 se lleva a cabo la obtenci´on de la ecuaci´on de onda de Helmholtz y
la aproximacio´n paraxial. Teniendo como punto de partida las ecuaciones de Maxwell
para campos electromagn´eticos.

      En el capitulo 3 se presentan algunos factores que afectan a los rayos infrarrojos
al propagarse a trav´es de la atm´osfera. Mostrando un modelo para las ﬂuctuaciones
del ´ındice de refracci´on.

      En el capitulo 4 se realiza la simulacio´n de la propagaci´on de onda para el ca-
so de dos dimensiones, esto utilizando los m´etodos de diferencias ﬁnitas: Diferencias
Centrales y el de Crank-Nicolson.

      La simulacio´n de la propagaci´on de la luz utilizando la aproximacio´n paraxial se
realiza en el capitulo 5, para el caso de tres dimensiones, utilizando el m´etodo ADI
(Alternating direction Implicit Method).

      Y ﬁnalmente en el capitulo 6, se introducen indices de refracci´on variables en la
simulaci´on de la propagaci´on de la luz. Con el objetivo de observar el comportamiento
de los haces adifraccionales principalmente.
Cap´ıtulo 2

An´alisis electromagn´etico

Desde ﬁnales del siglo XIX el trabajo de J. Clerk Maxwell y los dem´as desarrollos
posteriores pusieron de maniﬁesto que la luz tiene naturaleza electromagn´etica [1].
La electrodin´amica cl´asica, conduce invariablemente a la idea de una transferencia
continua de energ´ıa por medio de ondas. En cambio el punto de vista m´as moderno de
la electrodin´amica cu´antica describe las interacciones electromagn´eticas y el transporte
de energ´ıa en t´erminos de part´ıculas elementales llamadas fotones. La luz tiene una
doble naturaleza que se pone de maniﬁesto por el hecho de que se propaga en el espacio
como lo hace una onda, demostrando sin embargo, un comportamiento de part´ıcula
durante los procesos de emisi´on y absorci´on. La energ´ıa radiante electromagn´etica es
creada y destruida en cuantos o fotones y no continuamente como una onda cl´asica. No
obstante su movimiento a trav´es de una lente, un agujero o un conjunto de rendijas,
est´a supeditado a sus caracter´ısticas ondulatorias.

      Los campos el´ectricos son generados tanto por cargas el´ectricas como por campos
magn´eticos variables en el tiempo. De forma an´aloga, los campos magn´eticos son ge-
nerados por corrientes el´ectricas y por campos el´ectricos variables en el tiempo. Esta
interdependencia de los campos el´ectricos y magn´eticos es un punto clave de la descrip-
ci´on de la naturaleza ondulatoria de la luz.

2.1 Ecuaci´on escalar de onda

Considerando un entorno muy general de un medio isotr´opico, homog´eneo, lineal (no
ferroel´ectrico ni ferromagn´etico) que se halla f´ısicamente en reposo, la formulacio´n de
la ecuaciones de Maxwell, que gobiernan el comportamiento de los campos el´ectricos y
magn´eticos, en su forma diferencial son

                                                       3
4                CAP´ITULO 2. ANA´LISIS ELECTROMAGNE´TICO

                 ∇    ×    E  =   −  ∂B     ,                    (2.1)
                                     ∂t                          (2.2)
                     ∇·E = ρ,                                    (2.3)
                                                                 (2.4)
                                     0

                        ∇ · B = 0,

          ∇×B           =  µ0J    + µ0      0  ∂E  .
                                               ∂t

      La ecuaci´on 2.1 es la Ley de inducci´on de Faraday, la ecuaci´on 2.2 es Ley de Gauss
el´ectrica, la ecuaci´on 2.3 Ley de Gauss magn´etica y la ecuaci´on 2.4 es la Ley circuital
de Ampere [2].

      Donde E y B son los campos el´ectrico y magn´etico respectivamente, J es la
densidad de corriente, ρ es la densidad de carga, es la constante de permitividad y µ
es la constante de permeabilidad.

      Teniendo como base estas ecuaciones es posible obtener la ecuaci´on de onda. Pri-
mero es conveniente formar las segundas derivadas con respecto a las variables espacia-
les. Si aplicamos el rotacional a la ecuaci´on 2.1 tenemos

      ∇ × (∇ × E) = ∇ ×                     −  ∂B     .          (2.5)
                                               ∂t

      El triple producto vectorial se puede simpliﬁcar aprovechando la identidad de
operadores ∇ × ∇ × A = ∇( ∇ · A) − ∇2A, dado que B se supone que es una
funci´on que exhibe un buen comportamiento, las derivadas con respecto al espacio y al
tiempo pueden intercambiarse.

      ∇   (∇  ·  E)  −  ∇2E   =   −     ∂   (∇  ×     B)  .      (2.6)
                                        ∂t

      Sustituyendo el producto punto del campo el´ectrico por la ecuaci´on 2.1 y el
producto cruz del campo magn´etico por ecuaci´on 2.4 obtenemos:

   ∇  ρ   −      ∇2E    =  −  ∂      µ0J       + µ0    ∂E     ,  (2.7)
                              ∂t                      0 ∂t
       0

ahora podemos desplazar las constantes fuera del diferencial
2.1. ECUACIO´N ESCALAR DE ONDA                                                                         5

                        ∇     ρ      − ∇2E      =  −µ0  ∂J   − µ0   0  ∂2E     .                       (2.8)
                                                        ∂t             ∂t2
                               0

      Es sabido que la densidad de corriente esta relacionado con el campo el´ectrico por
J = σE, donde σ es la constante de conductividad, por lo tanto sustituyendo esta
igualdad en la ecuaci´on 2.8, y si adem´as multiplicamos por −1 tenemos

                        ∇2E − ∇            ρ    =  µ0    ∂2E    +  µ0σ  ∂E     ,                       (2.9)
                                                        0 ∂t2           ∂t
                                            0

ﬁnalmente despejamos el Laplaciano del campo el´ectrico

                        ∇2E   =      µ0   ∂2E   +  µ0σ  ∂E      +∇      ρ      .            (2.10)
                                         0 ∂t2          ∂t
                                                                         0

Para un diel´ectrico atenuador libre de carga ρ = 0 y σ = 0 la ecuaci´on queda

                                 ∇2E     =  µ0   ∂2E    +  µ0σ  ∂E  .                       (2.11)
                                                0 ∂t2           ∂t

Pero  para  el  vac´ıo  σ  =  0   y  ρ  =  0,  adem´as  sabemos     que     c  =  √µ10   .  Aplicando  estos

                                                                                        0
resultados obtenemos la ecuaci´on escalar de onda para el espacio libre

                                         ∇2E    =  1    ∂2E  .                              (2.12)
                                                   c2   ∂t2

      De igual forma que para el campo el´ectrico se deduce la ecuaci´on de onda para el
campo magn´etico

                                         ∇2B    =  1    ∂2B  .                              (2.13)
                                                   c2   ∂t2
6                            CAP´ITULO 2. ANA´LISIS ELECTROMAGNE´TICO

2.2 Ecuaci´on de Helmholtz

Los campos dependen del tiempo y de su posici´on, por lo tanto es posible representarlos
como funciones de estos par´ametros [2], entonces la ecuaci´on de onda queda

                             ∇2E(r, t)     =  1   ∂  2E(r,  t)  ,                               (2.14)
                                              c2       ∂t2

donde r es el vector de posici´on (x, y, z). Si E esta linealmente polarizado, y desea-

mos remover la dependencia del tiempo, sustituimos E(r, t) por el fasor E0(r)e−jωt,
entonces las derivadas quedan:

                             ∂2E(r, t)  =  −ω2E0(r)e−jωt,                                       (2.15)
                                ∂t2

                             ∂2E(r, t)     =  e−jωt  ∂2E0(r)       ,                            (2.16)
                                ∂r2                     ∂r2

sustituyendo estos resultados en la ecuaci´on 2.14, obtenemos

                    e−jωt∇2E0(r)           =  −   ω2  E0(r)e−jωt.                               (2.17)
                                                  c2

   De  esta  forma  podemos  eliminar  el  exponencial,     y   si    adem´as  sustituimos  k2  =  ω2  ,
                                                                                                   c2

obtenemos ﬁnalmente la ecuaci´on de Helmholtz

                             ∇2E0(r) + k2E0(r) = 0.                                             (2.18)

2.3 Ecuaci´on paraxial de onda

Una de las consideraciones mas pr´acticas en el tratamiento de la propagaci´on de la
luz, es la aproximacio´n paraxial, la cual se reﬁere a que los haces de luz pr´oximos al
2.3. ECUACIO´N PARAXIAL DE ONDA                                             7

           Figura 2.1: Dominio paraxial

eje axial de propagaci´on, como en la ﬁgura 2.1, pueden considerarse tambi´en axiales,
debido a que su ´angulo con respecto al eje axial es muy cercano a cero.

      Paraxial signiﬁca kz |k| donde k = kxx + kyy + kzz esta aproximacio´n por ser
muy conﬁable es aplicada ampliamente en ´optica de lentes y rayos laser, donde quedan
incluidos los rayos infrarrojos los cuales son el objetivo de estudio del presente trabajo.

      Para obtener la aproximaci´on paraxial se parte de la ecuaci´on de Helmholtz. Que
sustituyendo E0 en sus componentes de posici´on nos queda:

∂2E0          +  ∂2E0     +      ∂2E0           +  k2E0  =  0,              (2.19)
 ∂x2              ∂y2             ∂z2

si sustituimos E0 por U eikzz entonces tenemos

∂2U eikzz  +  ∂2U eikzz   +      ∂2U eikzz         + k2U eikzz  =       0.  (2.20)
   ∂x2           ∂y2                ∂z2

Las derivadas para el caso de la componente en z quedan

           ∂E0   =  ∂U    eikz   z  + ikzU eikzz,                           (2.21)
            ∂z      ∂z                                                      (2.22)

∂2E0  =    ∂2U   eikz  z  +  2   ∂U  ikz        eikz  z  − kz2U eikzz,
 ∂z2       ∂z2                   ∂z

sustituyendo estos resultados en la ecuaci´on 2.21,
8                                      CAP´ITULO 2. ANA´LISIS ELECTROMAGNE´TICO

   ∂2U   eikz z  +  ∂2U  eikz z  +  ∂2U  eikz z  +  2  ∂U   ikz eikz z  −  kz2U eikzz  +  k2U eikzz.        (2.23)
   ∂x2              ∂y2             ∂z2                ∂z

      Podemos eliminar los exponenciales ya que se encuentran en todos los t´erminos y
agrupando los t´erminos semejantes se obtiene

                    ∂2U  +   ∂2U    +2      ik   ∂U    +    ∂2U  + (k2     − kz2)U     =  0,                (2.24)
                    ∂x2      ∂y2                 ∂z         ∂z2

pero como kz k, su diferencia es aproximadamente cero reduci´endose la ecuaci´on a

                            ∂2U     +  ∂2U  +2         ik   ∂U   +      ∂2U  =  0,                          (2.25)
                            ∂x2        ∂y2                  ∂z          ∂z2

adem´as  ∂2U        2k   ∂U      debido  a  que     k  es   un  nu´mero    muy  grande,       por  lo  tanto  ∂2U

         ∂z2             ∂z                                                                                   ∂z2

es despreciable.    Finalmente sustituyendo el Laplaciano transversal ∇T2                          =   + ∂2   ∂2
                                                                                                       ∂x2    ∂y2

llegamos a la ecuaci´on paraxial de onda

                                         ∇2T U   +     2ik  ∂U  = 0.                                        (2.26)
                                                            ∂z

2.4 Soluci´on no difractiva de la ecuaci´on escalar de
       onda

El inter´es que existe en los campos ´opticos invariantes, es debido a que en condicio-
nes ideales, ellos se propagan indeﬁnidamente sin presentar cambios es la distribuci´on
transversal de intensidad [3]. Ahora si se logra que se transmitan sen˜ales que se propa-
gan sin difractarse, podr´ıamos tener una mayor potencia en la recepci´on. Esto debido
a que la energ´ıa estar´ıa m´as concentrada, contrario a lo que sucede cuando la sen˜al se
dispersa como ocurre en rangos de frecuencia bajos. Si utilizamos estas sen˜ales en los
sistemas de comunicacio´n inal´ambrica, y debido a que este tipo de ondas se encuentran
2.4. SOLUCIO´N NO DIFRACTIVA DE LA ECUACIO´N ESCALAR DE ONDA 9

en el rango de los sistemas ´opticos, se podr´ıan ofrecer servicios que requieran anchos
de banda muy grandes, por ejemplo multimedia.

      Durnin descubri´o recientemente los rayos no difractivos que pueden alcanzar dis-
tancias relativamente grandes sin que el rayo se difracte signiﬁcativamente. Compara-
dos con otros tipos de rayos como el Gaussiano, los no difractivos tienen mucho mayor
alcance. Los rayos no difractables tienen un l´obulo central angosto y relativamente
largo con l´obulos laterales que viajan en paralelo junto con el l´obulo central; esto trae
como consecuencia una mayor concentraci´on de la energ´ıa, logrando un mayor alcance.

      Partimos de la ecuaci´on escalar de onda para el espacio libre. Uno puede veriﬁcar
que la soluci´on exacta de la ecuaci´on 2.12, para una propagaci´on del campo escalar
dentro de una regi´on libre z ≥ 0, es [4]

                                                                        2π

E(x, y, z ≥ 0, t) = exp{i(βz − ωt)} A(φ) exp{−iα(x cos φ + y sin φ)}dφ, (2.27)

                                                                      0

donde  β2 + α2   =   (  ω  )2  y  A(φ)  es  una funci´on  arbitraria    compleja de       φ.   Cuando     β  es
                        c

real la ecuaci´on 2.12 representa a la clase de campos no difractivos en el sentido de que
en un tiempo promedio la intensidad del perﬁl en z = 0,

                                  I(x, y, z  ≥  0)  =  1  |E(r, t)|2 ,                         (2.28)
                                                       2                                       (2.29)

                                                   = I(x, y, z ≥ 0).

      Esto se repite exactamente para toda z en un plano normal al eje z.
      El u´nico campo no difractable teniendo una simetr´ıa axial para la cual A(φ) es
independiente de φ, es aquel campo que tenga una amplitud proporcional a [4][5]

                                                   2π                                      dφ
                                                                                           2π
           E(r, t) = exp{i(βz − ωt)}                   exp{−iα(x  cos   φ  +  y  sin  φ)}      (2.30)

                                                0

                        = exp i(βz − ωt)J0(αρ).

Aqu´ı ρ2 = x2 + y2 y J0(αρ) es la funci´on Bessel de orden cero de primer tipo.

Cuando  α  =  0  es  simplemente        una  onda  plana,  pero  para   0  <     α  ≤  ω   la  soluci´on  que
                                                                                       c

se obtiene es un rayo no difractable, en el que la intensidad decae a una velocidad
10  CAP´ITULO 2. ANA´LISIS ELECTROMAGNE´TICO

inversamente proporcional a αρ. El ancho efectivo del rayo es determinado por α, y
cuando α = ω/c = 2π/λ (el m´aximo valor posible para un campo no evanescente) el
m´ınimo di´ametro posible para el l´obulo central es de aproximadamente 3λ/4.

      Hoy en d´ıa se continu´a estudiando estas sen˜ales no difractivas, proponiendo nuevas
formulaciones para los campos ´opticos invariantes, con el ﬁn de poder aplicarlas en
diferentes ´areas.
Cap´ıtulo 3

Propagaci´on atmosf´erica del infrarrojo

3.1 Introducci´on

La propagaci´on en el espacio libre responde a un modelo ideal an´alogo a las condiciones
de propagaci´on en el vac´ıo. En el entorno terrestre muy pocas situaciones se ajustan a
este modelo. La presencia de la tierra, la atm´osfera, de ediﬁcios y de una gran cantidad
de materiales alteran en la mayor´ıa de casos reales las condiciones de propagaci´on de
el infrarrojo.

      Las caracter´ısticas el´ectricas de la tierra inﬂuyen en la propagaci´on de las ondas
electromagn´eticas. Al incidir una onda sobre la tierra se produce una reﬂexi´on. La
presencia de obst´aculos y la propia esfericidad de la tierra limitan la visibilidad entre los
equipos transmisor y receptor. Al incidir una onda electromagn´etica sobre un obst´aculo
se produce un fen´omeno de difracci´on por el cual el obst´aculo reirradia parte de la
energ´ıa interceptada.

      La concentraci´on de gases en la atm´osfera introduce diferencias entre la propa-
gaci´on en el espacio libre y la atm´osfera. La mayor concentraci´on de gases se da en
la capa mas baja de la atm´osfera, llamada trop´osfera, que se extiende desde el nivel
del mar hasta unos 10 km de altitud aproximadamente. En condiciones atmosf´ericas
normales la disminuci´on de gases disminuye con la altura, lo que provoca una variacio´n
del ´ındice de refracci´on de la atm´osfera en funci´on de la altura. Por tanto, la atm´osfera
constituye un medio de propagaci´on no homog´eneo, lo que provoca una curvatura de
las trayectorias de propagaci´on y refracci´on. Adem´as, la presencia de gases introduce
atenuaci´on, especialmente importante en las frecuencias de resonancia de las mol´eculas
de oxigeno y del vapor de agua, que son los gases con mayor presencia en la atm´osfera.
Finalmente incidencias meteorol´ogicas como la lluvia pueden introducir atenuaciones
adicionales en funci´on de la frecuencia y la intensidad de precipitaci´on.

      En la pr´actica los problemas de propagaci´on se tratan estudiando por separado
cada uno de los fen´omenos y cuantiﬁcando su efecto respecto a la propagaci´on en

                                                      11
12   CAP´ITULO 3. PROPAGACIO´N ATMOSFE´RICA DEL INFRARROJO

el espacio libre. As´ı, al proyectar un servicio deben identiﬁcarse en primer lugar los
fen´omenos que son relevantes en funci´on de la longitud de onda a emplear y la ubicaci´on
de los transmisores y receptores.

      Factores tales como la intensidad y frecuencia de las lluvias, el ´ındice de refrac-
ci´on de la atm´osfera, o la densidad de ionizaci´on de la ionosfera son variables en el
tiempo y en el espacio, en la mayor´ıa de los casos desconocidos de forma exacta y, sin
embargo, con una inﬂuencia importante en la cuantiﬁcaci´on de los distintos procesos
que intervienen en la propagaci´on de ondas en el entorno terrestre. Generalmente debe
recurrirse a los valores medios o valores de referencia de estas magnitudes para una
regi´on o ´epoca del an˜o que proporcionar´an estimaciones aproximadas en los c´alculos de
propagaci´on.

3.2 Difracci´on

La difracci´on es el fen´omeno que ocurre cuando una onda electromagn´etica incide sobre
un obst´aculo. La tierra y sus irregularidades pueden impedir la visibilidad entre un
transmisor y un receptor en ciertas ocasiones. La zona oculta al receptor se denomina
la zona de difracci´on. En esta zona los campos no son nulos debido a la difracci´on
causada por el obst´aculo y, por tanto, es posible la recepci´on, si bien con atenuaciones
superiores a las del espacio libre.

      En primer lugar es necesario deﬁnir la condici´on de visibilidad entre antenas, es
decir, cuando debe considerarse que un obst´aculo interrumpe el camino directo entre la
antena transmisora y la receptora y, por tanto, la difracci´on es un mecanismo relevante
en la propagaci´on.

      Consid´erese la situaci´on de la ﬁgura 3.1 en que dos antenas isotr´opicas est´an
separadas una distancia R. A una distancia d1 de la antena transmisora, donde se
halla el obst´aculo, se deﬁne un plano P inﬁnito, perpendicular a la l´ınea que una a la
antena transmisora con la receptora.

     Se deﬁnen las zonas de Fresnel como aquellos puntos del espacio que cumplen con:

[6]

     (r1 + r2) − R = nλ/2; n = 1, 2, 3, ....  (3.1)

donde λ es la longitud de onda de la sen˜al. Las l´ıneas de fresnel son elipsoides de

revoluci´on cuya longitud del eje mayor es R + nλ/2. La intersecci´on de las zonas de
Fresnel con el plano P son circunferencias cuyo radio puede calcularse para el caso en
que sea mucho menor que d1 y d2 como
3.2. DIFRACCIO´N                                 13

Figura 3.1: Deﬁnici´on de las zonas de Fresnel.

                  Rn =  nλ   d1d2    .           (3.2)
                            d1 + d2

      Aplicando el principio de Huygens, el campo sobre la antena receptora puede
formarse por la superposici´on de fuentes elementales de ondas esf´ericas situadas en
el plano P , radiando cada una de estas fuentes con un desfase que es funci´on de la
distancia r1. A estas fuentes equivalentes se les llama fuentes secundarias.

      A partir de la deﬁnici´on de las zonas de Fresnel, los campos producidos por las
fuentes equivalentes de Huygens situadas en la zona 1 (ﬁgura 3.2) se sumar´an en la
antena receptora con una fase inferior a 180o, es decir, constructivamente. Las contri-
buciones de las fuentes situadas en las zonas 2 y 3 tienden a cancelarse mutuamente, lo
mismo que las zonas 4 y 5, 6 y 7, y as´ı sucesivamente. Por tanto, si en la situaci´on del
plano P se situ´a en un plano conductor con un oriﬁcio de radio R1, esto es, dejando
solamente las fuentes secundarias comprendidas dentro de la primera zona de Fresnel
y anulando el resto, la potencia en el receptor no disminuir´a de forma apreciable. Por
tanto, el radio de la primera zona de Fresnel permite deﬁnir la condici´on de visibilidad
entre antenas, de forma que mientras no exista un obst´aculo dentro de la primera zona
de Fresnel se considera que la trayectoria no ha sido obstruida. Por el contrario, cuando
el obst´aculo se considera dentro de la primera zona de Fresnel existir´a una disminuci´on
apreciable de la potencia recibida, por lo que se considera que la trayectoria ha sido
obstruida y deber´a considerarse el efecto de difracci´on.
14  CAP´ITULO 3. PROPAGACIO´N ATMOSFE´RICA DEL INFRARROJO

    Figura 3.2: Fase del campo producido por cada una de las fuentes secundarias.

       λ(m)     R1(m)   R1/λ   Banda de frecuencia
    0.5 × 10−6   0.07  140000     espectro visible
                  17                  banda X
        0.03    1.414    566             MF
        200               7

Tabla 3.1: Radios de la primera zona de Fresnel en el punto medio de un enlace de 40
km de longitud [6].

3.3 Atenuacio´n

La absorci´on molecular de los gases contenidos en la atm´osfera y la atenuacio´n produ-
cida por los hidrometeoros son las principales causas de la atenuacio´n atmosf´erica. En
la ﬁgura 3.3 se muestra la atenuaci´on especiﬁca (dB/km) en funci´on de la frecuencia
para un trayecto pr´oximo a la superﬁcie de la tierra.

      La atenuacio´n por absorci´on molecular se debe principalmente a las mol´eculas de
ox´ıgeno y vapor de agua. Para frecuencias inferiores a 10 Ghz es pr´acticamente des-
preciable, mientras que a frecuencias superiores presenta un comportamiento creciente
3.3. ATENUACIO´N  15

Figura 3.3: Atenuacio´n espec´ıﬁca por A:lluvia, B:niebla y C:componentes gaseosos [6].

con la frecuencia y la aparici´on de rayas de atenuaci´on asociadas a las frecuencias de
resonancia de las mol´eculas. A frecuencias de infrarrojo y visible existe una fuerte ate-
nuaci´on por parte del vapor de agua, hechos tales como nubes o niebla. En la ﬁgura
3.4 se muestra la absorci´on molecular en la banda de infrarrojos. Se observa que existe
una ventana de baja atenuacio´n para longitudes de onda comprendidas entre 8 y 13
µm.

      En cuanto a la atenuacio´n por hidrometeoros, es especialmente importante la
lluvia, la niebla, la nieve y el granizo. La atenuacio´n por lluvia depende de la intensidad
y de factores tales como el tipo de lluvia, el taman˜o y velocidad de las gotas de agua.
En la ﬁgura 3.3 se observa que la lluvia puede ser una causa importante de atenuacio´n
a frecuencias superiores de 1 GHz. La atenuaci´on total producida por la lluvia se
obtiene multiplicando la atenuaci´on especiﬁca por la longitud de la celda de la lluvia.
En la consideraci´on de un servicio de telecomunicaciones debe considerarse de forma
estad´ıstica teniendo en cuenta la probabilidad de que una cierta intensidad de lluvia
ocurra, y sobredimensionando el sistema de forma que la atenuaci´on adicional asociada
a esta intensidad de lluvia no afecte al sistema.

      La atenuaci´on por lluvia aumenta al aumentar la frecuencia. Hasta alcanzar un
m´aximo a partir del que disminuye levemente para mantener un valor constante a
16  CAP´ITULO 3. PROPAGACIO´N ATMOSFE´RICA DEL INFRARROJO

Figura 3.4: Atenuacio´n espec´ıﬁca por absorci´on molecular en la banda de infrarrojos
[6].

frecuencias ´opticas.
      Para predecir los efectos de las lluvias en la zona donde se realiza el enlace. Es

fundamental disponer de datos de observacio´n meteorol´ogica que permitan cuantiﬁcar
de forma probabil´ıstica las diferentes intensidades de lluvia. Para ello es necesario
disponer de series de observaci´on largas que garanticen la ﬁabilidad estad´ıstica de los
datos.

3.4 Modelos para la turbulencia atmosf´erica

El comportamiento de las ondas electromagn´eticas (EM) en un medio turbulento es
complejo pero interesante, particularmente cuando hay cambios fuertes es la amplitud
en una propagaci´on realizada.

      Una onda o rayo que atraviesa mas de unos cuantos metros de una atm´osfera
ordinaria turbulenta tiene una redistribuci´on de la energ´ıa y exhibe ﬂuctuaciones en la
intensidad, conocidas como centelleos [7].
3.4. MODELOS PARA LA TURBULENCIA ATMOSFE´RICA     17

      El patr´on aleatorio instanta´neo del centelleo, observado en un plano paralelo al
frente de onda, muestra componentes espaciales de Fourier con una pequen˜a variaci´on
d√e escalas, pero el taman˜o de la escala predominante es el taman˜o de la zona-Fresnel
( λL) donde λ es la longitud de onda ´optica y L es el taman˜o de la longitud del camino
o para caminos espacio-tierra la distancia entre el observador y la capa atmosf´erica
turbulenta. El taman˜o de la escala predominante varia de 1 cm para caminos de un
kil´ometro de longitud hasta 7 u 8 cm para caminos inclinados a trav´es de toda la
atm´osfera. La frecuencia temporal de la variacio´n de intensidad observada en un punto
ﬁjo depende de la componente transversal del viento que mueve la turbulencia que cruza
el rayo. La frecuencia predominante es obtenida dividiendo la velocidad del viento entre
el taman˜o de la zona - Fresnel. Para la mayor´ıa de trayectorias la frecuencia temporal
importante se encuentre en el rango de 1 a 100 Hz. La saturaci´on ocurre hasta, que la
varianza de la intensidad logar´ıtmica var´ıa inversamente a 7/6 potencia de la longitud
´optica.

      El par´ametro estructura del ´ındice de refracci´on Cn2 es medido en unidades de
metros−2/3. Estos valores var´ıan de 10−17 o menos cuando la turbulencia es extre-
madamente tranquila, de 10−13 o m´as cuando la turbulencia, generada proxima a la
tierra es fuerte. Las mediciones que existen son insuﬁcientes para predecir el valor
medio y la varianza de Cn2 bajo condiciones geogr´aﬁcas y meteorol´ogicas especiﬁcas.
Una representacio´n usada comu´nmente es la ﬁgura 3.5 donde se muestra un modelo del
par´ametro estructura propuesto por Hufnagel. Este modelo es derivado de mediciones
de centelleos estelares y de unas pocas mediciones directas de las ﬂuctuaciones de la
temperatura, usualmente dentro de unos 30 m sobre la tierra [7]. Es observable adem´as
en la ﬁgura 3.5 como el valor de Cn2 disminuye al incrementar la altura, recordemos que
es debido a que a mayor altura menor concentraci´on de gases. Se pueden ver adem´as
dos tipos de l´ıneas, la l´ınea continua representa una atm´osfera normal y la l´ınea discon-
tinua muestra los efectos esperados por los disturbios meteorol´ogicos en una atm´osfera
normal. El modelo de Hufnagel es comu´nmente usado.

      La forma de caracterizar un canal turbulento es hacer una descripci´on f´ısica de
sus propiedades. Una de las mas importantes en la atm´osfera es el ´ındice de refracci´on
aleatorio que presenta.

      La relaci´on entre el ´ındice de refracci´on n y la temperatura en la atm´osfera es
aproximadamente dada por [8]

n  −  1  =  77.6  P  1 + 7.52 × 10−3λ−2  × 10−6,  (3.3)
                  T

donde P es la presi´on en milibares, T es la temperatura en grados Kelvin, y λ es la
18  CAP´ITULO 3. PROPAGACIO´N ATMOSFE´RICA DEL INFRARROJO

        Figura 3.5: Modelo del par´ametro estructura del ´ındice de refracci´on [7].

longitud de onda de la luz en micr´ometros. Para muchas aplicaciones en ingenier´ıa
puede reducirse

    n − 1 = 7.8 × 10−5P/T.          (3.4)

      Las ﬂuctuaciones en el ´ındice de refracci´on en la atm´osfera puede ser inducido
por correspondientes variaciones en temperatura atmosf´erica que son transportadas
naturalmente por variaciones en la velocidad del viento llamadas ﬂuctuaciones. Ahora
podemos reescribir el ´ındice de refracci´on como la suma del ´ındice en el espacio libre
mas las ﬂuctuaciones aleatorias debidas a la presencia de turbulencia:

    n(r, t) = n0(r, t) + n1(r, t).  (3.5)

donde n0(r, t) = 1 y n1(r, t) es la componente de ﬂuctuaciones y r es funci´on de la

posici´on dentro de la atm´osfera y del tiempo t. Si asumimos que la dependencia tempo-
ral del ´ındice de refracci´on es principalmente dependiente de los vientos atmosf´ericos,
entonces

    n(r, t) = n0 + n1(r − v(r)t).   (3.6)
3.4. MODELOS PARA LA TURBULENCIA ATMOSFE´RICA                      19

      En esta consideraci´on se asume que v(r) es la componente local de la velocidad
del tiempo perpendicular a la l´ınea de vista del enlace. Esta consideraci´on es conocida
como la hip´otesis ”Taylor´s frozen ﬂow”que asume que la forma de la turbulencia del
campo debido a las ﬂuctuaciones del ´ındice se mueve en forma ﬁja con la media local del
viento. Ciertamente esto no es estrictamente correcto pues nosotros podr´ıamos esperar
cambios en las ﬂuctuaciones con respecto a su movimiento, muchas de las formas de
las nubes cambia con los movimientos del viento. Sin embargo, estos cambios son muy
pequen˜os comparados con la velocidad de movimiento para un observador estaciona-
rio. Consecuentemente, la hip´otesis de Taylor es aceptada para algunas aplicaciones
pr´acticas. Es notorio que la componente de v(r) perpendicular a la l´ınea de vista causa
cambios temporales en la recepci´on del campo de luz.

      Debido a que la turbulencia es un proceso estoc´astico, es posible describirlo en
funci´on de cantidades estad´ısticas. La funci´on estructura es

Dn1(r1,r2) = E[{n1(r1) − n1(r2)}2].                                (3.7)

Y la funci´on de correlaci´on del ´ındice de refracci´on

Γn1(r1,r2) = E[n1(r1)n1(r2)].                                      (3.8)

donde E[ ] denota el promedio en ensamble. Es conveniente deﬁnir nuevas variables

R = (r1 + r2),                                                     (3.9)
ρ = (r1 − r2).

Entonces la estructura y la correlaci´on pueden ser escritas como  (3.10)

                                 Dn1(r1,r2) = Dn1(R, ρ),
                                   Γn1(r1,r2) = Γn1(R, ρ).

      Si el medio es homog´eneo, la dependencia de R puede ser suprimida y tener
entonces

 Γn1(r1,r2) = Γn1(ρ),                                              (3.11)
Dn1(r1,r2) = Dn1(ρ).
20  CAP´ITULO 3. PROPAGACIO´N ATMOSFE´RICA DEL INFRARROJO

      Por lo tanto la funci´on estructura y la funci´on de correlaci´on est´an relacionadas
por

                                Dn1(ρ) = 2[V ar(n1) − Γn1(R, ρ)],      (3.12)
donde V ar(n1) es la varianza de n1 y adem´as E[n1] = 0.

      Usando el teorema de Wiener-Khintchine, deﬁnimos el espectro del nu´mero de
onda de las ﬂuctuaciones del ´ındice de refracci´on Φn(K):

    Φn(K)       =   2     ∞                                            (3.13)
                    π3
                            Γn1(ρ) exp(iK · ρ)d3ρ,

                        −∞

y usando las ecuaciones 3.12 y 3.13 se obtiene la siguiente relaci´on

    Dn1 (ρ)  =  2     ∞                                                (3.14)
                π3
                        Φn1(K){1 − exp(iK · ρ)}d3ρ.

                    −∞

      Lo cual nos permite calcular la funci´on estructura del ´ındice de refracci´on dado el
espectro del nu´mero de onda de n1.

      Los trabajos anteriores de Booker-Gordon y los modelos Gaussianos son amplia-
mente usados dado que su forma simple disminuyo´ la complejidad de los c´alculos [8].
De La f´ormula de Booker-Gordon se asume que la funci´on

                Γn1 = V ar(n1exp(−ρ/l)).                               (3.15)

      El par´ametro l se reﬁere a la escala de la turbulencia que es dada por exp(−l)
de la correlaci´on de la distancia de las ﬂuctuaciones del ´ındice de refracci´on. Aproxi-
madamente l es el taman˜o promedio de los remolinos de turbulencia. La funci´on de
correlaci´on Gaussiana

                Γn1 = V ar(n1exp(−ρ/l)2),                              (3.16)

y se asume que es la mejor aproximaci´on del comportamiento del medio aleatorio.

      Los remolinos turbulentos son caracterizados por una escala externa L0 y una
escala interna l0. T´ıpicamente, l0 se encuentra en el orden de los mil´ımetros mientras
que L0 puede ser de unos cuantos metros. Adem´as la turbulencia es caracterizada por
3.4. MODELOS PARA LA TURBULENCIA ATMOSFE´RICA                     21

tres rangos los cuales est´an relacionados con las escalas de L0 y l0. El rango de entrada
es caracterizado por un remolino mas grande que L0. Aqu´ı la energ´ıa de turbulencia es
introducida por el viento y los gradientes de temperatura. En el siguiente subrango el
taman˜o del remolino es mayor que l0 pero menor que L0. La turbulencia es isotr´opica
y la energ´ıa cin´etica del remolino sobrepasa la disipaci´on debida a la viscosidad. El
rango de disipaci´on es caracterizado por un remolino menor que l0. En este caso, la
energ´ıa perdida debido a la viscosidad domina y el espectro es pequen˜o.

      Sobre el subrango inerte, la funci´on estructura de temperatura obedece a dos
tercios de la ley isotr´opica de potencia:

                                           DT (ρ) = CT2 ρ2/3,     (3.17)
donde CT2 ρ2/3 es el par´ametro de estructura de la temperatura.

      Las ecuaciones 3.3 y 3.17 implican la siguiente forma de la funci´on estructura del
´ındice de refracci´on

                Dn(ρ) = Cn2ρ2/3,                                  (3.18)

donde Cn2 es el par´ametro de estructura del ´ındice de refracci´on, y esta relacionado con

CT2 por

y similarmente       Cn2 = (dn/dt)2CT2 ,                          (3.19)
                Φn(K) = (dn/dt)2ΦT (K),                           (3.20)

      Podemos llegar a la siguiente expresi´on de el espectro de Kolmogorov de las ﬂuc-
tuaciones del ´ındice de refracci´on.

                Φn(K) = 0.033Cn2k−11/3.                           (3.21)

      Para algunas aplicaciones, es necesario conocer la forma de la ﬂuctuaciones del
espectro del ´ındice de refracci´on. Se han propuesto ciertas modiﬁcaciones para suavizar
la transici´on a la entrada y en los rangos de disipaci´on. Para el rango de disipaci´on, es
22  CAP´ITULO 3. PROPAGACIO´N ATMOSFE´RICA DEL INFRARROJO

claro que el espectro cae mas r´apidamente que k−2/3. Tatarski ha propuesto la siguiente
modiﬁcaci´on a la ecuaci´on 3.21 la cual es [8]

           Φn(K) = 0.033Cn2k−11/3exp(−k/km2),                           (3.22)

donde km = 5.92/l0. Para cierto rango de entrada la energ´ıa en el remolino mas larga

que l0 podr´ıa ser menor que la predecida por el modelo de Kolmogorov.

3.4.1 Distribuciones de probabilidad de la intensidad

Para el c´alculo de la probabilidad de error en un enlace de comunicaci´on es necesario

conocer la distribuci´on de probabilidad que satisface la intensidad de la sen˜al ´optica
recibida. Para el caso en que σ12 = 1.23k7/6Cn2x11/6 << 1 ha sido encontrado que la
distribuci´on de probabilidad de la intensidad es casi lognormal [9][10]. Esto es, para

una amplitud unitaria de la onda plana, la densidad de probabilidad p(I) satisface

    p(I )  =  √1      exp  −  ln  I  +  σ2  2         ,                 (3.23)
                2πσI                    2
                                             (2σ2)−1

donde σ2 = ln[I + σI2].

      Para σ12 > 0.3 no es totalmente cierto que p(I) tiene una distribuci´on lognormal.
Se han hecho mediciones experimentales para 0 < σ12 < 100, y para σ12 < 0.3 la
distribuci´on en 3.23 ocurre razonablemente; tambi´en, para 25 < σ12 < 100, la ecuaci´on
3.23 es una razonable aproximaci´on. Sin embargo, para 1 ≤ σ12 ≤ 25, en las mediciones
de la distribuci´on de probabilidad aparecen desviaciones signiﬁcativas del resultado
en 3.23. Esto es espec´ıﬁcamente cierto para 0 ≤ σ12 ≤ 4. En estudios realizados los
resultados indican que la distribuci´on de probabilidad es Rayleigh [10]. Sin embargo,
es esperado de consideraciones f´ısicas que para σ12 → ∞ la distribuci´on de probabilidad
p(I) podr´ıa aproximarse a

                      p(I) = exp(−I).                                   (3.24)

      En el modelo f´ısico propuesto por Wolf [11], es argumentado que hay dos principa-
les componente que contribuyen en la recepci´on del campo en un punto (x, 0): uno es
el componente dispersado reenviado por remolinos largos sobre la propagaci´on axial, el
cual podr´ıa ser denotado por A exp(iφ), donde la fase φ se asume que tiene una distri-
buci´on Gaussiana y la amplitud A satisface la distribuci´on lognormal. En turbulencia
3.4. MODELOS PARA LA TURBULENCIA ATMOSFE´RICA   23

tranquilas toda la sen˜al recibida es aproximadamente dispersada por remolinos en el eje
axial, y la ecuaci´on 3.23 es una buena aproximaci´on para la amplitud del campo. Sin
embargo, cuando la longitud del camino de propagaci´on es incrementada, y σ12 empieza
a ser comparable o mayor que la unidad, no hay algu´n remolino axial suﬁcientemente
largo que reenv´ıe la energ´ıa dispersada, y aproximadamente la sen˜al recibida en (x, 0) es
debida a la energ´ıa que es reenviada por dispersi´on de remolinos fuera del eje axial. El
campo en (x, 0) debido a todos los diferentes componentes fuera del eje axial puede ser
denotado por Zeiθ; por que estas contribuciones son estad´ısticamente independientes,
entonces Z es una distribuci´on Rayleigh de acuerdo a

p(Z) =  2Z  exp  −  Z2  .                       (3.25)
        Z2          Z2

      Nosotros notamos que Z2 es una funci´on de σ12; Z2 es bastante pequen˜a para
σ12 1, pero es considerable para σ12 1. Una relaci´on expl´ıcita entre Z2 y σ12 au´n
no ha sido determinada. El campo total en (x, 0) es la suma de los dos componentes

Zeiθ y A exp iφ.

3.4.2 Estad´ısticas de centelleos

Se ha demostrado que las ﬂuctuaciones espaciales y temporales aleatorias en el ´ındice
de refracci´on atmosf´erico genera centelleos en la irradiancia recibida en un sistema
de comunicaciones ´optico. No es posible en general determinar la funci´on de densi-
dad de probabilidad para los centelleos en la intensidad bajo condiciones arbitrarias
atmosf´ericas y par´ametros del rayo. Las estad´ısticas del centelleo continu´an siendo
objeto de numerosos experimentos y de investigaciones te´oricas.

      Heur´ısticamente, uno puede ver que un medio turbulento consiste de una serie de
secciones transversales (slabs) [12] , cada uno de los cuales es m´as delgado que una
escala externa L0, as´ı que las ﬂuctuaciones entre las etapas son independientes. Por lo
tanto el campo despu´es de N secciones transversales esta dado por:

fN (r) = exp {φ0(r) + φ1(r)},                   (3.26)

                                            N   (3.27)

fN (r) = exp {φ0(r) + φ1i(r)},

                                           i=1
24  CAP´ITULO 3. PROPAGACIO´N ATMOSFE´RICA DEL INFRARROJO

 donde Ti(r) = exp {φ1i(r)} es la amplitud compleja de la transmitancia para una

secci´on transversal , dado que la secci´on transversal es mas delgada que L0 entonces
los φ1i(r), i = 1, ..., N son variables aleatorias independientes. Por que el nu´mero de
secciones transversales puede ser grande, el campo recibido es el resultado de muchos
efectos multiplicativos, Alternadamente el campo puede ser escrito como la suma de
fasores de N campos complejos ai:

                 N         N

    f (r) = ai = ai exp {iθi},                                                         (3.28)

                 i=1       i=1

donde la longitud de las etapas fasoriales ai es generada por el centelleo de las in-

homogeneidades de el ´ındice de refracci´on y θi esta asociada con los cambios de fase.
Conjuntamente con ciertas proposiciones adicionales, es posible demostrar estos mode-
los para el esparcimiento de campos pueden ser usados para evaluar la estad´ısticas de
los centelleos de la intensidad.

      Considerando la representaci´on 3.26, por que el nu´mero de slabs puede ser grande,
el campo recibido es el resultado de muchos efectos multiplicativos. Esto por el teorema
de limite central.

                                                                                   N   (3.29)
                                                                                       (3.30)
                                           φ1(r) = φ1i(r),

                                                                                  i=1

y la parte real, X = Reφ1i(r) podr´ıa ser normalmente distribuida

    P (X)  =       1       exp {(X  −  E [X ])2 }.
              (2πσX2 )1/2

3.4.3 Modelo b´asico de las variaciones del ´ındice de refracci´on

Las variaciones del ´ındice de refracci´on en la atm´osfera turbulenta puede ser considerada
como la suma de lentes independientes ya que cada una es una funci´on u´nicamente del
taman˜o de un par´ametro l (claro que l puede variar) [11]. La contribuci´on de todos los
remolinos de taman˜o l a las variaciones del ´ındice de refracci´on son

    δnl(r, t) =        δn(l) exp  −[r − R(t)]2      .                                  (3.31)
                                        l2
                 R(t)
3.4. MODELOS PARA LA TURBULENCIA ATMOSFE´RICA                     25

      Se ha demostrado que la distribuci´on del taman˜o de los remolinos puede ser ajus-
tado para un determinado espectro de frecuencia espacial del ´ındice de refracci´on. Aqu´ı,
R(t) es el movimiento aleatorio del centro del remolino, y escoger una forma Gaussiana
es justo lo mas conveniente [11]. Las siguientes asunciones adicionales son hechas.

• Las lentes son casi transparentes, δn(l) 1.

• El rango del taman˜o de las lentes l va de una microescala l0 a una macroescala
  L0, esto es, l0 < l < L0.

• La distancia de propagaci´on L es mucho mas larga que la macroescala L0; L L0.

• La varianza del ´ındice de refracci´on es del taman˜o integral de δn2(l) de l = l0 a

l = L0, y la varianza de δn(l) corresponde al espectro del ´ındice de refracci´on de

Kolmogorov y es

                 δn2(l) ∼ Cn2l−1/3                                (3.32)

donde Cn2 es la constante estructura del ´ındice de refracci´on.

• El radio de la primera zona de Fresnel (λL)1/2 se encuentra dentro de la micro y
  la macro escala: l0 < (λL)1/2 L0.

      Estas consideraciones nos permitir´an mas adelante poder llevar a cabo las simu-
laciones correspondientes a la propagaci´on de la luz a trav´es de la atm´osfera.
26  CAP´ITULO 3. PROPAGACIO´N ATMOSFE´RICA DEL INFRARROJO
Cap´ıtulo 4

Simulaci´on en una dimensi´on espacial

Como pudimos observar la ecuaci´on que describe el comportamiento de las ondas elec-
tromagn´eticas al propagarse, es una ecuaci´on diferencial parcial (EDP). Varias t´ecnicas
generales has sido investigadas por m´as de un siglo para resolver EDPs. Por mencionar
algunos ejemplos tenemos: M´etodo de separaci´on de variables, el m´etodo de ecuaci´on
integral, m´etodos anal´ıticos basados en transformaci´on con integrales tales como las
transformadas de Fourier y Laplace, y ﬁnalmente los m´etodos num´ericos.

      En ocasiones es muy dif´ıcil o imposible obtener soluciones anal´ıticas, en estos casos
la u´nica opci´on es implementar t´ecnicas num´ericas.

      En este capitulo se presentan las soluciones num´ericas para la ecuaci´on escalar de
onda y para la aproximaci´on paraxial de onda en dos dimensiones. Son dos m´etodos
basados en esquemas de diferencias ﬁnitas: el m´etodo de diferencia centrales (CTCS)
y el m´etodo de Crank-Nicolson.

4.1 M´etodo de diferencias centrales

Recordemos la ecuaci´on escalar de onda, considerando solo un componente espacial x,
la ecuaci´on nos queda

∂2Ex  =  1   ∂2Ex  .                    (4.1)
 ∂x2     c2   ∂t2

      Como sabemos varios fen´omenos en la naturaleza presentan comportamiento on-
dulatorio, y la ecuaci´on de onda es tambi´en aplicada a ellos. Para mostrar el m´etodo
CTCS presentamos el caso cl´asico de una cuerda de longitud L sujeta por los dos ex-
tremos. La cuerda tiene una masa por unidad de longitud λ y esta sujeta a una tensi´on
T . Para representar la forma que describe la cuerda utilizamos U (x, t) que es funci´on

                                                      27
28  CAP´ITULO 4. SIMULACIO´N EN UNA DIMENSIO´N ESPACIAL

de su posici´on x y del tiempo t, tenemos entonces

            ∂2U (x, t)   =  1   ∂  2U (x,           t)  .  (4.2)
               ∂x2          c2       ∂t2

    Las condiciones de contorno para este ejemplo son:

    U (0, t) = 0 y U (a, t) = 0 para 0 ≤ t ≤ b             (4.3)
                                                           (4.4)
    U (x, 0) = f (x)               para 0 ≤ x ≤ a
                                                           (4.5)
    ∂U (x,  t)  =  g(x)  =  0      para 0 ≤ x ≤ a
        ∂t

      Que nos indican u´nicamente que la amplitud en los extremos de la cuerda es cero,
y en el resto es una funci´on de la variable x.

            Figura 4.1: Malla para resolver diferencias centrales en la region R.

      La construcci´on de la ecuaci´on de diferencias, se realiz´o de la siguiente forma:
Suponemos un rect´angulo R = (x, t) : 0 ≤ x ≤ a, 0 ≤ t ≤ b en una malla que consta de
n − 1 por m − 1 rect´angulos de lados ∆x = h y ∆t = k como en la ﬁgura 4.1.

      Las f´ormulas en diferencias centradas para aproximar las derivadas quedan
4.1. ME´TODO DE DIFERENCIAS CENTRALES                                             29

∂2U (x, t)  =  U (x   +   h, t)  −  2U (x, t)  +    U (x  −  h, t)  +  O(h2),  (4.6)
   ∂x2                                 h2                                      (4.7)
∂2U (x, t)
    ∂t2     =  U (x, t    +  k)  −  2U (x, t)  +    U (x, t  −  k)  +  O(k2).
                                       k2

      El espacio entre los puntos de la malla es uniforme en todas las ﬁlas: xi+1 = xi+h y
xi−1 = xi − h y tambi´en es uniforme en todas las columnas: tj+1 = tj + k y tj−1 = tj − k,
de esta forma obtenemos la ecuaci´on en diferencias eliminando los t´erminos de orden
O(k2) y O(h2) de las ecuaciones 4.6 y 4.7, y utilizando U i,j en vez de U (xi, tj) y
sustituyendo todo esto en la ecuaci´on 4.2 nos queda

U i,j+1     − 2U i,j  + U i,j−1     =   c2 U i+1,j  − 2Ui,j  + U i−1,j .       (4.8)
                k2                                      h2

Si pasamos la constante k al lado derecho y hacemos r = ck/h tenemos

U i,j+1 − 2U i,j + U i,j−1 = r2(U i+1,j − 2U i,j + U i−1,j ).                  (4.9)

      Reordenando los t´erminos, es posible determinar las aproximaciones a la soluci´on
en los puntos de la (j + 1)-´esima ﬁla de la malla, suponiendo que conocemos las apro-
ximaciones a la soluci´on en las dos puntos de las ﬁlas anteriores, la j-´esima y la ﬁla
(j − 1)-´esima:

U i,j+1 = (2 − 2r2)U i,j + r2(U i+1,j + U i−1,j) − U i,j−1.                    (4.10)

      Si queremos usar la ecuaci´on 4.10 para calcular las aproximaciones en los puntos de
la tercera ﬁla de la malla, es necesario disponer de las aproximaciones de las dos primeras
ﬁlas. Los valores de la primera ﬁla ya se tienen, vienen dados por la condici´on inicial
U (x, 0) = f (x). Sin embargo los valores de la segunda ﬁla no se pueden proporcionar,
as´ı que se usa la expansi´on de Taylor para obtener la aproximacio´n en la segunda ﬁla.
Recordando que la f´ormula de Taylor de orden 2 es

U (x,  t)   =  U (x,  0)  +  t  ∂U (x,  0)  +  t2  ∂2U (x,   0)  +  O(k3).     (4.11)
                                    ∂t         2       ∂t2
30                    CAP´ITULO 4. SIMULACIO´N EN UNA DIMENSIO´N ESPACIAL

      Las aproximaciones para las derivadas en esta ecuaci´on son conocidas y vienen
dadas por las ecuaciones 4.4 y 4.7, las sustituimos en la ecuaci´on 4.11 y si adem´as para
la segunda l´ınea t = k, as´ı la ecuaci´on para encontrar la aproximaci´on en la segunda
ﬁla nos queda:

        U (x,  k)  =  fi  +  kgi  +  c2k2    (fi+1  −  2fi   +  fi−1)  +  O(h2)O(k2)O(k3),  (4.12)
                                     2h2

puesto  que  r  =  ck/h,     y  ∂U (x,t)  =  g(x).  Finalmente         tenemos

                                    ∂t

                          U i,k   =  (1   −  r2)fi  +  kg(x)    +  r2  (fi+1  +  fi−1).     (4.13)
                                                                   2

    Para la simulacio´n de la cuerda vibrante se usaron los siguientes par´ametros: Una

longitud de 1 m, una tension T = 8 N y una densidad de masa de λ = 0.02 kg/m

las cuales son constantes a lo largo de toda la cuerda, es decir, se trata de una cuerda

homog´enea, con estos par´ametros de tensi´on y densidad de masa se puede obtener la

constante de    propagaci´on c2      =    λ  .  Para   una funci´on inicial U (x) = sin x   el resultado
                                          T

se muestra en la ﬁgura 4.2 en la que podemos observar la amplitud de las oscilaciones,

donde u´nicamente se muestran tres oscilaciones de la cuerda, pero se puede observar

como se va deformando la forma senoidal conforme avanzan las oscilaciones. Y con una

funci´on inicial con una forma triangular descrita por la siguiente ecuaci´on

                                     f (x) =           h  x  0≤x≤p                          (4.14)
                                                       p
                                                      h
                                                    L−p   x  p  ≤x≤L

el resultado de la simulacio´n se muestra en la ﬁgura 4.3, de igual forma observamos
como se va deformando la forma triangular inicial, adem´as de ir sufriendo atenuacio´n.

4.2 M´etodo Crank-Nicolson

Para el m´etodo de Crank-Nicolson el proceso para obtener las ecuaciones en diferencias
se muestra a continuacio´n:
4.2. ME´TODO CRANK-NICOLSON                                                                                                                  31

                Amplitud   0.03
                           0.02
                           0.01

                               0
                          −0.01
                          −0.02
                          −0.03

                            150

                                  100                   00                                                                1
                                                    50                                                      0.8
                                                                                               0.6
                                        tiempo                                   0.4
                                                                    0.2

                                                                                  Longitud

Figura 4.2: Oscilaci´on de una cuerda homog´enea con funci´on inicial sin x, utilizando
CTCS.

      Teniendo como base la ecuaci´on 4.1 suponemos nuevamente un rect´angulo R =
(x, t) : 0 ≤ x ≤ a, 0 ≤ t ≤ b en una malla que consta de n − 1 por m − 1 rect´angulos
de lados ∆x = h y ∆t = k como en la ﬁgura 4.4.

      Por lo tanto las aproximaciones para las derivadas quedan:

                           ∂2U (x, t)       =           U i,j+1  −  2U i,j  + U i,j−1 ,                                                      (4.15)
                               ∂t2                                   k2

∂2U (x, t)  =   U i−1,j+1  −      2U i,j+1  + U i+1,j+1 + U i−1,j−1               −  2U i,j−1                                + U i+1,j−1 ,   (4.16)
   ∂x2                                                    h2

sustituyendo en la ecuaci´on 4.2 tenemos

U i,j+1 − 2U i,j + U i,j−1

            k2                              +                      +   U i−1,j−1
            c2 U i−1,j+1   −      2U i,j+1              U i+1,j+1  h2             −  2U i,j−1                                +  U i+1,j−1 ,
=                                                                                                                                            (4.17)

acomodando y haciendo r = kc/h nos queda

2 (U i,j+1 − 2U i,j + U i,j−1)
         = r2 (U i−1,j+1 − 2U i,j+1 + U i+1,j+1 + U i−1,j−1 − 2U i,j−1 + U i+1,j−1) , (4.18)
32  CAP´ITULO 4. SIMULACIO´N EN UNA DIMENSIO´N ESPACIAL

    Amplitud     0.02
               0.015
                 0.01
               0.005

                    0
              −0.005
               −0.01
              −0.015
               −0.02

                 150

                       100                   00                                                       1
                                         50                                              0.8
                                                                           0.6
                             tiempo                           0.4
                                                 0.2

                                                               Longitud

Figura 4.3: Oscilaci´on de una cuerda homog´enea con funci´on inicial la ecuaci´on 4.14,
utilizando CTCS.

 reordenando los t´erminos, es posible determinar las aproximaciones a la soluci´on en
los puntos de la ﬁla (j + 1)-´esima de la malla

−r2U i−1,j+1 + (2 + 2r2)U i,j+1 − r2U i+1,j+1 = r2U i−1,j−1 − (2 + 2r2)U i,j−1 − 4U i+1,j .
                                                                                                        (4.19)

      Como resultado tenemos un sistema de matrices tridiagonal. Que son relativa-
mente f´aciles de manejar. Para la primer ﬁla tenemos nuevamente U (x, 0) = f (x) y
para encontrar la segunda ﬁla es necesario utilizar la expansi´on de Taylor de nuevo, es
decir, se obtiene la ecuaci´on 4.13.

      Para la simulacio´n de este m´etodo para la cuerda se utilizan los mismos par´ametros
que para el m´etodo CTCS, es decir una longitud de la cuerda de 1 m, una tensi´on de
8 N y una densidad de masa de 0.02 kg/m. Los resultados son mostrados en la ﬁgura
4.5 y 4.6. Si observamos detenidamente estas gr´aﬁcas resultan muy similares a las
que se obtuvieron por el m´etodo CTCS. La ventaja que presenta el m´etodo Crank-
Nicolson es que de acuerdo al criterio de estabilidad de von Neuman este m´etodo es
incondicionalmente estable, a diferencia del m´etodo CTCS que no lo es [13].
4.3. ECUACIO´N PARAXIAL DE LA LUZ                                          33

                     Figura 4.4: Malla para el m´etodo de Crank-Nicolson.

4.3 Ecuaci´on paraxial de la luz

Como ya se explic´o anteriormente, la aproximacio´n paraxial de la luz es sumamente
conﬁable y m´as au´n para aquellos rayos que al propagarse lo hacen de forma directiva,
adem´as de facilitar grandemente las simulaciones al reducir el nu´mero de variables
involucradas en la propagaci´on.

      El m´etodo num´erico que se utiliz´o es el de Crank-Nicolson, cuyo proceso de dis-
cretizaci´on es muy similar al de realizado para el ejemplo de la cuerda. Para el caso de
la aproximaci´on paraxial, la derivada temporal de la ecuaci´on es de primer orden, por
lo que es suﬁciente con tener la funci´on inicial para que el m´etodo pueda obtener las
siguientes aproximaciones.

      Retomando la ecuaci´on paraxial de onda, y considerando u´nicamente dos dimen-
siones, la ecuaci´on 2.26 queda:

∂2U  +  i2k                        ∂U  = 0,                                (4.20)
∂x2                                ∂z

      donde k es la constante de propagaci´on, y k = 2πλ. Si despejamos el diferencial
con respecto a z, el lado derecho de la ecuaci´on quedar´ıa negativo pero si pasamos la
constante imaginaria del denominador al numerador, nos queda:

∂U   =   i                         ∂2U  .                                  (4.21)
∂z      2k                         ∂x2
34                  CAP´ITULO 4. SIMULACIO´N EN UNA DIMENSIO´N ESPACIAL

                        0.03
                        0.02
                        0.01

                            0
                       −0.01
                       −0.02
                       −0.03

                         150

                                  100                           00                                                          1
                                                     50                                                       0.8
                                                                                                0.6
                                        Tiempo                                    0.4
                                                                    0.2

                                                                                   Longitud

Figura 4.5: Oscilaci´on de una cuerda homog´enea con una funci´on inicial sin x, utilizando
Crank-Nicolson.

    La discretizaci´on para esta ecuaci´on utilizando el m´etodo de Crank-Nicolson queda

U i,j+1  − U i,j−1  =   i U i−1,j+1  − 2U i,j+1                 + U i+1,j+1 + U i−1,j−1  − 2U i,j−1                            + U i+1,j−1 ,
         z             2k                                                     h2
                                                                                                                               (4.22)

para  simpliﬁcar    hacemos    r  =    iz  ,             y  si  adem´as  agrupamos  y  factorizamos                            obtenemos
                                     2kh2

−rU i−1,j+1 + (2 + 2r)U i,j+1 − rU i+1,j+1 = rU i−1,j + (2 − 2r)U i,j + rU i+1,j. (4.23)

      Reformulando esta ecuaci´on de forma matricial, obtenemos un sistema lineal de
ecuaciones de la forma CU j+1 = DU j, cuya forma matricial es:
4.3. ECUACIO´N PARAXIAL DE LA LUZ                                                                                                                               35

                                 0.02
                               0.015

                                 0.01
                               0.005

                                    0
                              −0.005

                               −0.01
                              −0.015

                               −0.02
                                 150

                                       100                         00                                                               1
                                                          50                                                          0.8
                                                                                                        0.6
                                            Tiempo                                        0.4
                                                                             0.2

                                                                                            Longitud

Figura 4.6: Oscilaci´on de una cuerda homog´enea con funci´on inicial la ecuaci´on 4.14,
utilizando Crank-Nicolson.

           2(1 + r) −r                0                      0 ...          0         0                                                  

  −r        2(1 + r) −r 0                                  0     ...        0                                                  U j+1 =
               0                                                                       ...
               0        −r 2(1 + r) . . .                              0     0          0
              ···                                                                       0
               0        0              −r . . . −r                           0         −r

                        0              0     . . . 2(1 + r) −r

                        ...            0                      0 −r 2(1 + r)

             0           0            ··· 0                         0       −r 2(1 + r)                                                                       (4.24)
                            r                                         ...
  2(1 − r)                    0                   0        0        0                                                      0   U j.
                        2(1 − r)                                       0
               r            r             r                   0        r        ...    0
               0            0                                      2(1 − r)      0     ...
               0            0          2(1 − r) . . .                  r         0     0
              ···          ...                                                   r     0
               0                          r                   ...            2(1 − r)   r

                                          0                   ...

                                          0                   0

                 0         0           ··· 0                              0     r 2(1 − r)

Aqu´ı podemos despejar U j+1, y la ecuaci´on quedar´ıa U j+1 = C−1DU j, de esta forma
obtenemos f´acilmente las aproximaciones a la soluci´on en la j-esima ﬁla.
36  CAP´ITULO 4. SIMULACIO´N EN UNA DIMENSIO´N ESPACIAL

4.3.1 Resultados

Recordemos que el principio de Huygens-Fresnel establece que cada punto sin obstruc-
ci´on de un frente de onda, en un instante de tiempo determinado, sirve como fuente de
trenes de ondas secundarios esf´ericos (de la misma frecuencia que la onda primaria). La
amplitud del campo ´optico en cualquier punto es la superposici´on de todos esos trenes
de onda. Para el caso donde la longitud de onda es mayor que la rendija (ventana), las
ondas se extender´an segu´n ´angulos grandes en la regi´on mas all´a de la obstrucci´on. Y
cuanto mas pequen˜a sea la ventana, mas circulares ser´an las ondas difractadas. Cuando
la longitud de onda es menor que la ventana, el ´area donde la longitud de onda es mayor
que la m´axima diferencia de las longitudes de camino ´optico, se limita a una pequen˜a
regi´on que se extiende hacia afuera directamente frente a la ventana, siendo solamente
ah´ı donde todas las ondas secundarias interﬁeren constructivamente. Fuera de esta
zona, algunas de estas ondas secundarias interﬁeren negativamente, presenta´ndose as´ı
la sombra en las otras zonas.

      Los resultados que a continuaci´on se presentan son para un laser de He-Ne, es
decir, con una longitud de onda λ = 632.8 nm. Los longitud de los intervalos utilizados
son: ∆x = 2.34 × 10−5 y ∆z = 7.5 mm.

      En la ﬁgura 4.7 se muestra la propagaci´on para el caso de una rendija u´nica
rectangular de 0.2 mm, por lo tanto su longitud de onda es mayor que la longitud
de onda de la sen˜al. Observemos como al iniciar la propagaci´on la intensidad de la
onda sobrepasa la intensidad unitaria inicial, esto es debido a los efectos de borde de la
ventana. Es decir, de acuerdo al principio de Huygens-Fresnel cada punto en la ventana
emitir´a ondas en cualquier direcci´on, algunos se propagar´an directamente al frente de la
ventana, y otros con ciertos ´angulos con respecto al eje axial de propagaci´on. Algunos
rayos interferira´n de forma constructiva otros en forma destructiva. Si observamos
cuidadosamente la ﬁgura 4.7. Inicialmente la parte central de la intensidad disminuye,
mientras que la intensidad en los bordes de la ventana incrementa, y as´ı continu´a hasta
alcanzar un m´aximo. Todo esto lo hace de forma irregular debido a que se encuentra
dentro de la zona de difracci´on de Fresnel. Posteriormente empieza a atenuarse sin sufrir
cambios en la forma de la intensidad, es decir cuando alcanza la zona de difracci´on de
Fraunhofer.

      Ahora para dos rendijas la propagaci´on que resulta es la ﬁgura 4.8. Inicialmente el
fen´omeno de difracci´on para cada ventana es igual que para el de la ventana u´nica, aqu´ı
tambi´en es observable el efecto de borde. Pero adem´as es interesante ver como a partir
de cierta distancia los frentes de onda de las dos rendijas se empiezan a superponer
y, si bien la amplitud de cada cual tiene que ser esencialmente igual, sus fases pueden
diferir signiﬁcativamente. Como la misma onda primaria excita las fuentes secundarias
4.3. ECUACIO´N PARAXIAL DE LA LUZ  37

         Figura 4.7: Propagaci´on de un laser HeNe para una rendija rectangular
en cada ventana, los trenes de onda resultantes ser´an coherentes y por lo tanto existir´a
interferencia. Hasta alcanzar una forma de la intensidad regular, una vez alcanzado la
zona de difracci´on de Fraunhofer.

       Figura 4.8: Propagaci´on de un laser HeNe para dos rendijas rectangulares
      Si tenemos una rendija con forma cosenoidal, en la ﬁgura 4.9 se observa la manera
en que se propaga la onda, lo relevante de esta entrada es que la propagaci´on presenta
caracter´ısticas de los rayos adifraccionales, es decir, que sufre de poca difracci´on para
ciertas distancias. Solamente que la energ´ıa requerida es demasiado grande, siendo esta
una desventaja.
      Uno de los haces tradicionalmente m´as usados es el Gaussiano. Si el medio de
38  CAP´ITULO 4. SIMULACIO´N EN UNA DIMENSIO´N ESPACIAL

         Figura 4.9: Propagaci´on de un laser HeNe para una entrada cosenoidal
propagaci´on es homog´eneo, como por ejemplo en el vac´ıo, estos haces mantienen su
forma Gaussiana durante la propagaci´on. Solamente va disminuyendo su intensidad e
incrementando su ancho, por lo que es de relativa facilidad predecir los valores del haz
Gaussiano para ciertas distancias de propagaci´on. En la ﬁgura 4.10, se observa clara-
mente esta caracter´ıstica, la desventaja de estos haces es que se atenu´an r´apidamente,
por lo que para cubrir distancias grandes se requiere de grandes cantidades de energ´ıa.

        Figura 4.10: Propagaci´on de un laser HeNe para una entrada Gaussiana
      Es importante mencionar que para el caso de una dimensi´on espacial no es posible
observar las caracter´ısticas adifraccionales de haces Bessel, ya que solamente estar´ıamos
introduciendo una secci´on transversal del haz y no un haz de forma completa.
Cap´ıtulo 5

Simulaci´on en dos dimensiones espaciales

5.1 M´etodo ADI

Los campos electromagn´eticos, como la gran mayor´ıa de eventos en el mundo real,
ocurren en forma tridimensional. Por lo que para que una simulacio´n se apegue mas a
la realidad, es necesario llevarla a cabo en forma tridimensional.

      Para realizar esta simulacio´n se utilizar´a la ecuaci´on paraxial de onda, conside-
rando que la onda se encuentra en el plano x, y y se propaga a lo largo del eje z.

      Partimos de la ecuaci´on 2.26 que, sustituyendo todos sus componentes queda

                                    ∂2U    +  ∂2U  =  i2k  ∂U        ,  (5.1)
                                    ∂x2       ∂y2          ∂t

donde  el  nu´mero  de  onda  k  =  2π  .
                                    λ

      El m´etodo de discretizaci´on utilizado es el ADI (Alternating direction Implicit
Method). En este m´etodo se utiliza una discretizaci´on hacia adelante para los pasos
temporales, solo que cada paso lo realiza mediante dos pasos intermedios. Para el
primer paso intermedio (subpaso) la variable que es impl´ıcita es la x, y para el siguiente
subpaso la impl´ıcita es la variable y. En la ﬁgura 5.1 se muestra la forma en que
se llevan a cabo las discretizaciones. Donde el nu´mero de intervalos para x y y en
cada subpaso es m, es decir, los valores para los ´ındices i y j ser´an i = 1, 2, 3...m y
j = 1, 2, 3...m. El diferencial de tiempo queda

                                    ∂U     =  Uin,j+1/2 −  Uin,j  .     (5.2)
                                    ∂t             ∆t/2

      La discretizaci´on de los par´ametros x y y se llevan a cabo utilizando el m´etodo de
Crank-Nicolson, por tanto el m´etodo ADI tambi´en es incondicionalmente estable [13].

                                                      39
40        CAP´ITULO 5. SIMULACIO´N EN DOS DIMENSIONES ESPACIALES

                                                                               n +1
                                                                               n +1/2

                            Dx                                                 n

                                       i

                                    j

                            Dy

                            Figura 5.1: Malla para el m´etodo ADI

Los diferenciales espaciales quedan de la siguiente forma:

                                       ∂2U  =  Uin+1,j  −  2Uin,j  +  Uin−1,j  ,                            (5.3)
                                       ∂x2                  ∆2x                                             (5.4)

                                       ∂2U  =  Uin,j+1  −  2Uin,j  +  Uin,j−1 ,
                                       ∂y2                  ∆y2

      Sustituyendo todas las discretizaciones en la ecuaci´on 5.1, para cada subpaso te-
nemos

Uin,j+1/2 − Uin,j    =   i  Uin++11,j/2 − 2Uin,j+1/2 + Uin−+11,j/2    +     i     Uin,j+1 − 2Uin,j + Uin,j−1        ,
     ∆t/2               2k                 ∆2x                             2k                ∆2y

                                                                                                            (5.5)

Uin,j+1 − Uin,j+1/2  =   i  Uin++11,j/2 − 2Uin,j+1/2 + Uin−+11,j/2    +   i       Uin,j++11 − 2Uin,j+1 + Uin,j+−11     .
      ∆t/2              2k                 ∆2x                           2k                    ∆2y

                                                                                                            (5.6)

    Para  simpliﬁcar        las  notaciones    hacemos     αx  =     i∆t   y   αy  =    i∆t   .  Ahora  si  reorde-
                                                                    2k∆x2              2k∆2y
namos y agrupamos los t´erminos que conocemos del lado derecho de la igualdad y los

que deseamos encontrar del lado izquierdo, tenemos entonces

αxUin−+11,j/2 − 2(1 + αx)Uin,j+1/2 + αxUin++11,j/2 = −αyUin,j−1 − 2(1 − αy)Uin,j − αyUin,j+1, (5.7)
5.1. ME´TODO ADI                                                                                 41

αyUin,j+−11 − 2(1 + αy)Uin,j+1 + αyUin,j++11 = −αxUin−+11,j/2 − 2(1 − αx)Uin,j+1/2 − αxUin++11,j/2. (5.8)

      En estas ecuaciones, se puede ver que de ambos lados de la igualdad es posible
hacer una simpliﬁcaci´on utilizando matrices tridiagonales. Lo cual es otra de las venta-
jas que ofrece este m´etodo, pues el manejo de estas matrices es relativamente sencillo,
y u´nicamente teniendo precauci´on con las propiedades aritm´eticas de las matrices al
realizar las operaciones.

      El lado izquierdo de la ecuaci´on 5.7 quedar´ıa de la siguiente forma:

                          αxUin−1,j − 2(1 + αx)Uin,j + αxUin+1,j = Uin,jA,                       (5.9)
donde A es la siguiente matriz tridiagonal de taman˜o m × m .

                              αx         0     0       ...        0        0    
                                         αx              0        ...
A =   −2(1+αx)  −2(1+αx)            0        0         0              .
                                      −2(1+αx)  ...     αx         0
                  αx           αx               ...               αx        0                    (5.10)
                   0            0        αx     ...  −2(1+αx)               ...
                   0            0         0                    −2(1+αx)     0
                  ···          ...        0     0       αx                  0
                   0                                                        αx

                  0         0         ··· 0 0                  αx        −2(1+αx)

      Es importante observar que la matriz tridiagonal se encuentra del lado derecho
de la funci´on U , esto es debido a que los valores que se toman en cada operaci´on
corresponden a diferentes columnas, es decir (i − 1, i, i + 1); para el caso donde las
posiciones cambien en la ﬁlas (j − 1, j, j + 1). La matriz tridiagonal se tiene que colocar
del lado izquierdo de la funci´on U para que la igualdad sea correcta, por lo tanto

                          αyUin,j−1 − 2(1 + αy)Uin,j + αyUin,j+1 = BUin,j,                       (5.11)
donde B es la matriz tridiagonal de taman˜o m × m
42                    CAP´ITULO 5. SIMULACIO´N EN DOS DIMENSIONES ESPACIALES

                                  −αy          0      0       ...         0      0     
                                              −αy               0         ...
    B =   −2(1−αy )  −2(1−αy )             0        0          0             .
                                            −2(1−αy )  ...    −αy          0
                      −αy          −αy                 ...               −αy        0                   (5.12)
                        0            0        −αy      ...  −2(1−αy )              ...
                        0            0          0                      −2(1−αy )    0
                      ···           ...         0      0      −αy                   0
                        0                                                         −αy

                      0          0          ··· 0 0                    −αy −2(1−αy)

      De esta forma las matrices tridiagonales simpliﬁcan grandemente los c´alculos,
ahora podemos sustituir en las ecuaciones 5.7 y 5.8 y obtenemos

                                            Uin,j+1/2A = BUin,j ,                                       (5.13)

                                            AUin,j+1 = Uin,j+1/2B.                                      (5.14)

      Podemos observar que podemos despejar la funci´on Uin,j+1/2 de la ecuaci´on 5.13 y
sustituirla en la ecuaci´on 5.14, para ﬁnalmente despejar la funci´on Uin,j+1 y obtener la
siguiente matriz de aproximaciones

                                            Uin,j+1 = A−1BUin,j A−1B.                                   (5.15)

      El resultado encontrado representa el siguiente desplazamiento de la onda de luz.
Por esta raz´on a partir de estas ecuaciones se realiz´o el programa que simula la propa-
gaci´on de dichas ondas.

      El m´etodo ADI nos permite avanzar en la soluci´on sobre un paso de tiempo resol-
viendo dos pseudo problemas impl´ıcitos unidimencionales, el cual equivale a desacoplar
el proceso de difusi´on en dos direcciones espaciales. Para demostrar esto, nosotros
introducimos los siguientes operadores en diferencias centrales

                                    δx2Uik,j ≡ Uik−1,j − 2Uik,j + Uik+1,j ,                             (5.16)
5.2. RESULTADOS                                                                               43

                           δy2Uik,j ≡ Uik,j−1 − 2Uik,j + Uik,j+1.                             (5.17)

      Ahora, si sustituimos esta notaci´on en la ecuaci´on 5.5 y 5.6, reescribimos para
obtener

                2(Uin,j+1/2 − Uin,j ) = αx(δx2Uin,j+1/2) + αy(δy2Uin,j ),                     (5.18)

                2(Uin,j+1 − Uin,j+1/2) = αx(δx2Uin,j+1/2) + αy(δy2Uin,j+1),                   (5.19)

agrupando

                           (2 − αxδx2)Uin,j+1/2 = (2 + αyδy2)Uin,j,                           (5.20)

                           (2 − αyδy2)Uin,j+1 = (2 + αxδx2)Uin,j+1/2,                         (5.21)

combinando  la  ecuaci´on  5.20  y  la  5.21  para  eliminar  el  paso  intermedio  n+  1  ,  obtenemos
                                                                                        2

                (2 − αxδx2)(2 − αyδy2)Uin,j+1 = (2 + αxδx2)(2 + αyδy2)Uin,j.                  (5.22)

      El desacoplo antes mencionado se maniﬁesta como una factorizaci´on natural del
operador en diferencias en cualquier lado de la ecuaci´on 5.22. Ahora, la discretiza-
ci´on total de Crank-Nicolson impl´ıcito de la ecuaci´on de difusi´on en dos dimensiones
espaciales puede ser expresada en forma simbo´lica de la siguiente forma

                (2 − αxδx2 − αyδy2)Uin,j+1 = (2 + αxδx2 + αyδy2)Uin,j.                        (5.23)

      Cabe mencionar que esta ecuaci´on u´nicamente es una notaci´on simpliﬁcada del
m´etodo, y no es utilizada para la simulacio´n.

5.2 Resultados

A continuaci´on se presentan los resultados obtenidos en cada una de las simulaciones.
En esta secci´on, en todos los casos el medio por donde se propagan las sen˜ales es el
vac´ıo, es decir con un ´ındice de refracci´on homog´eneo igual a uno.
44      CAP´ITULO 5. SIMULACIO´N EN DOS DIMENSIONES ESPACIALES

      Las longitudes de onda utilizadas se encuentran dentro del rango denominado
infrarrojo cercano, denominado as´ı por su proximidad al rango ´optico visible. Las
unidades que representan las intensidades son unidades arbitrarias solo con ﬁnes repre-
sentativos.

      Primeramente presentamos una rendija circular, con una distribuci´on de intensi-
dad unitaria. La difracci´on de Fraunhofer en una abertura circular, es un efecto de
enorme importancia en el estudio de la instrumentacio´n ´optica. Para esta simulacio´n
se utiliz´o una longitud de onda de 632.8 nm que corresponde a un laser de HeNe y
una ventana con una radio de 0.8 mm. La gr´aﬁca 5.2 (a), nos muestra la intensidad
inicial, es decir en z = 0, las siguientes ﬁguras (b), (c) y (d), representan la intensidad
a 1.5 m, 3 m y 6 m respectivamente. Podemos observar que a una distancia de 1.5 m
el patr´on de intensidad ya es uniforme, esto es debido a que ya ha alcanzado la zona
de difracci´on de campo lejano, donde la intensidad se concentrara en un disco central
rodeado de una serie de anillos alternativamente oscuros y brillantes, los cuales ser´an
muy d´ebiles. Es importante mencionar que la energ´ıa inicial es sumamente grande, y a
pesar de eso la intensidad decae r´apidamente despu´es de haber alcanzado un m´aximo
a una distancia de R2/λ [1], donde R es el radio de la ventana y λ es la longitud de
onda.

      En muchas simulaciones, el monitoreo constante de cantidades que se deben con-
servar, como por ejemplo la energ´ıa, sirven para veriﬁcar la estabilidad de la simulacio´n,
pudiendo utilizar este hecho para tener la certeza que la simulaci´on esta evolucionan-
do de forma correcta. Para esto encontraremos el error relativo porcentual (ERP) de
la energ´ıa del frente de onda en funci´on de la distancia de propagaci´on. Para cada
iteraci´on se calcula la energ´ıa del haz utilizando la siguiente f´ormula:

        Energia(z) = U 2dx ≈      (Ui,j )2 ,        (5.24)

                              ji

donde i, j son los contadores de la la funci´on. El error relativo porcentual se calcula

usando

        ERP (z) = 100 ×  Einicial − Eenergia(z)  .  (5.25)
                                 Einicial

      Incluiremos para algunas simulaciones la gr´aﬁca que muestre el error relativo por-
centual, para veriﬁcar de esta forma su estabilidad, donde lo recomendable es que el
5.2. RESULTADOS                                                      45

(a) Funcio´n inicial  (b) a 1.5 metros

(c) a 3 metros        (d) a 6 metros

Figura 5.2: Propagaci´on de un laser HeNe para una entrada circular
46  CAP´ITULO 5. SIMULACIO´N EN DOS DIMENSIONES ESPACIALES

este error sea muy pequen˜o (ERP (z) 0.001). En la ﬁgura 5.3 se muestra el ERP
de la simulaci´on correspondiente a la ventana circular, donde se puede ver que el valor
m´aximo se encuentra alrededor de 3 × 10−11, mostrando de esta forma que la energ´ıa
se conserva.

                                                                           x 10−11
                                                                         3

                               2.5

    Error Relativo Porcentual  2

                               1.5

                               1

                               0.5

                               0    0  1  2  3    4  5  6

                                             Mts

Figura 5.3: Error relativo porcentual de la energ´ıa durante la propagaci´on para una
entrada circular

      Recordemos que los haces Gaussianos en condiciones ideales tienen la propiedad
de que la secci´on transversal del patr´on de intensidad a cualquier distancia sigue siendo
Gaussiano, u´nicamente se va atenuando y ensanchando. En la ﬁgura 5.4, se muestran
los patrones de intensidad en forma para una entrada Gaussiana, la longitud de onda
utilizada corresponde nuevamente a la del laser HeNe 632.8 nm. En a) tenemos la
funci´on inicial, y posteriormente se presenta el haz a 1.5 m, 3 m y 6 m de distancia,
observando las ﬁguras se puede veriﬁcar que la forma inicial se mantiene a lo largo de
la propagaci´on. Para tener una visi´on m´as amplia de la propagaci´on en la ﬁgura 5.5 se
muestra las secci´on transversal a lo largo de los 6 m de propagaci´on.

      Para veriﬁcar la conservaci´on de energ´ıa del caso Gaussiano aplicamos la ecuaci´on
5.25, en la ﬁgura 5.6 y se observa nuevamente que los resultados son satisfactorios.

      Imaginemos que pudi´esemos enviar sen˜ales ´opticas y estas llegaran al receptor con
la forma id´entica a la que fue transmitida. Esto es posible con lo haces adifraccionales
para distancias cortas bajo condiciones de espacio libre, pues para grandes distancias
5.2. RESULTADOS                                                       47

(a) Funci´on inicial  (b) a 1.5 metros

(c) a 3 metros        (d) a 6 metros

Figura 5.4: Propagaci´on de un laser HeNe para una entrada Gaussiana
48  CAP´ITULO 5. SIMULACIO´N EN DOS DIMENSIONES ESPACIALES

    Figura 5.5: Secci´on transversal durante la propagaci´on de un haz Gaussiano

se requerir´ıa de ventanas de dimensiones ilimitadas. Recordemos la ecuaci´on para los
haces no difractivos mostrada en el capitulo 2

                                  2π                                     dφ
                                                                         2π
    E(r, t) = exp{i(βz − ωt)}         exp{−iα(x  cos  φ  +  y  sin  φ)}      (5.26)

                               0

    = exp i(βz − ωt)J0(αρ).

donde ρ2 = x2 + y2, J0(αρ) es la funci´on Bessel de orden cero de primer tipo y

α = ksin(θ) es la magnitud transversal del vector de onda.
      El patr´on de intensidad transversal de un haz Bessel se muestra en la ﬁgura 5.7

donde el radio del l´obulo principal est´a determinado por el valor de α y es aproxima-
damente α−1 [5]. Adem´as es notorio que la energ´ıa contenida en el m´aximo central
representa u´nicamente el 5% de la energ´ıa total del haz.

      Uno puede ver que de acuerdo a la ecuaci´on 5.26 el haz es la superposici´on de
ondas planas, todas teniendo una amplitud similar y viajando a un ´angulo similar
θ = sin−1(αλ/2π) relativo al eje de propagaci´on z. La distancia que el haz permanecer´a
con una intensidad cuasi constante, queda determinada por la f´ormula

    zmax = R/tanθ                                                            (5.27)
5.2. RESULTADOS                                                              49

                                                x 10−11
                                            4.5

                                            4

                                            3.5

                 Error relativo porcentual  3

                                            2.5

                                            2

                                            1.5

                                            1

                                            0.5

                                            0    0       1  2  3    4  5  6

                                                               Mts

Figura 5.6: Error relativo porcentual de la energ´ıa durante la propagaci´on para una
entrada Gaussiana

      Por ejemplo: para un haz de laser de HeNe (λ = 632.8 nm), con una ventana de
radio R = 3 mm y un ´angulo θ = 0.0381◦, el valor de α ser´a 6619.5 m−1, y zmax = 4.499
m. Las intensidades para esta simulacio´n se presentan en la ﬁgura 5.8, (a) en z = 0,
(b) en z = 1.5 m, (c) en z = 3 m y (d) z = 4.5 m.

      Una forma apropiada de ver el comportamiento a lo largo de la propagaci´on es
graﬁcar la secci´on transversal de la sen˜al en el eje x y observarlo en cada punto de la
propagaci´on. Esto se presenta en la ﬁgura 5.9, donde podemos observar que efectiva-
mente antes de alcanzar la distancia zmax = 4.5 m la sen˜al se mantiene cuasi invariante.
Se presentan tambi´en algunas oscilaciones en la intensidad del l´obulo principal alrede-
dor de la intensidad inicial, ocasionadas por el efecto de borde. Adem´as es notorio que
la intensidad de los anillos no sobrepasa la intensidad del l´obulo principal au´n en los
m´ınimos de las oscilaciones.

      Mostremos ahora como entre mayor es el radio de la ventana mayor ser´a la distan-
cia en la que el haz no sufrir´a difracci´on. Por supuesto que al ser mayor el radio mayor
ser´a la energ´ıa inicial requerida. Para un radio de 4 mm con los mismos par´ametros
del ejemplo anterior λ = 632.8 nm y θ = 0.0381◦ la distancia ser´a ahora zmax = 5.999
m, lo cual se veriﬁca en la ﬁgura 5.10. Y de una forma m´as clara en la ﬁgura 5.11,
50  CAP´ITULO 5. SIMULACIO´N EN DOS DIMENSIONES ESPACIALES

                1

                0.9

                0.8

                0.7

    Intensidad  0.6

                0.5

                0.4

                0.3

                0.2

                0.1

                0            0    2
                −6   −4  −2          4  6

                             Mts        x 10−3

    Figura 5.7: Perﬁl transversal de un haz Bessel de primer tipo de orden cero

donde vemos que alcanza casi los 6 m sin sufrir difracci´on. Las oscilaciones en el l´obulo
principal debido al efecto de borde son similares a los que se obtuvieron en la simulacio´n
para la ventana de 3 mm.

      Ahora hagamos una simulacio´n para un valor diferente de longitud de onda, por
ejemplo 750 nm, una ventana de R = 3 mm, un ´angulo θ = 0.0381◦. El valor de
alfa obtenido con estos valores es 5585.1 m−1, y el valor te´orico de zmax es 4.499 m.
Los resultados son mostrados en las ﬁguras 5.12 y 5.13. Podemos ver que el l´obulo
principal tiene un di´ametro mayor que cuando se utiliz´o la longitud de onda del laser
HeNe, esto por tener una α menor, sin embargo la distancia de propagaci´on del haz sin
que se difracte es la misma, inclusive con un comportamiento muy similar, inclusive en
el efecto de borde.

      A continuacio´n se muestra un u´ltimo ejemplo de un haz Bessel propagado en el
vac´ıo con los par´ametros iguales a los que se dan en la publicaci´on de Durnin [4] para
mostrar el funcionamiento correcto de las simulaciones. La longitud de onda es de
0.5µm, el radio de la ventana R = 2 mm, un ´angulo de 0.1089◦. Con estos datos la
distancia maxima de propagaci´on zmax = 1.052 m. Los resultados son mostrados en
5.2. RESULTADOS                         51

(a) Funci´on inicial  (b) a 1.5 metros

(c) a 3 metros        (d) a 4.5 metros

Figura 5.8: Propagaci´on de un haz Bessel de λ = 632.8 nm y una ventana de 3 mm de
radio
52  CAP´ITULO 5. SIMULACIO´N EN DOS DIMENSIONES ESPACIALES

Figura 5.9: Secci´on transversal durante la propagaci´on del haz Bessel de λ = 632.8 nm
y una ventana de 3 mm

la gr´aﬁca 5.14. Los valores de intensidad en ρ = 0 se presentan en la gr´aﬁca 5.15,
podemos observar claramente como la intensidad presenta las oscilaciones ocasionadas
por el efecto de borde, para caer abruptamente una vez alcanzado el valor de zmax
comprobando que estos resultados concuerdan con dicha publicaci´on.
5.2. RESULTADOS                         53

(a) Funcio´n inicial  (b) a 1.5 metros

(c) a 3 metros        (d) a 6 metros

Figura 5.10: Propagaci´on de un haz Bessel de λ = 632.8 nm y una ventana de 4 mm
de radio.
54  CAP´ITULO 5. SIMULACIO´N EN DOS DIMENSIONES ESPACIALES

Figura 5.11: Secci´on transversal durante la propagaci´on del haz Bessel de λ = 632.8
nm y una ventana de 4 mm
5.2. RESULTADOS                         55

(a) Funci´on inicial  (b) a 1.5 metros

(c) a 3 metros        (d) a 4.5 metros

Figura 5.12: Propagaci´on de un haz Bessel de λ = 750 nm y una ventana de 3 mm de
radio.
56  CAP´ITULO 5. SIMULACIO´N EN DOS DIMENSIONES ESPACIALES

Figura 5.13: Secci´on transversal durante la propagaci´on del haz Bessel de λ = 750 nm
y una ventana de 3 mm
5.2. RESULTADOS                         57

(a) Funci´on inicial  (b) a 0.3 metros

(c) a 0.6 metros      (d) a 1.2 metros

Figura 5.14: Propagaci´on de un haz Bessel de λ = 500 nm y una ventana de 2 mm de
radio.
58  CAP´ITULO 5. SIMULACIO´N EN DOS DIMENSIONES ESPACIALES

                1.6

                1.4

                1.2

                1

    Intensidad  0.8

                0.6

                0.4

                0.2

                0    0  0.2  0.4  0.6  0.8                        1  1.2  1.4

                                  Distancia de propagacion (Mts)

Figura 5.15: Propagaci´on en ρ = 0, de un haz Bessel con λ = 500 nm y ventana de 2
mm.
Cap´ıtulo 6

Propagaci´on con ´Indice de Refracci´on Variable

6.1 An´alisis del ´ındice de refracci´on

El cociente entre la velocidad de una onda electromagn´etica en el vac´ıo y en la materia
se le denomina ´ındice de refracci´on.

n  =   c  .                                                               (6.1)
       v

Que tambi´en es obtenida a partir de la constante diel´ectrica del medio

n = √ r.                                                                  (6.2)

      El ´ındice de refracci´on surge cuando el proceso de absorci´on y emisi´on, durante
la propagaci´on de la onda, adelanta o atrasa las fases de los fotones dispersados, au´n
cuando ellos se propagan a una velocidad c [1].

      A medida que una onda de luz avanza a trav´es de un medio, el fen´omeno de
esparcimiento tiene lugar una y otra vez. La luz que atraviesa la sustancia se va
retrasando, o adelantando progresivamente. Es evidente que la velocidad de la onda es
el ritmo de avance de la condici´on de fase, cualquier cambio que se produzca en la fase
provocar´a as´ı mismo un cambio de velocidad.

      Es importante demostrar que un desfasamiento en la onda equivale a una diferencia
en la velocidad de fase. En el espacio libre podemos representar la perturbaci´on que se
produce en un punto P como

Ep(t) = E0 cos ωt.                                                        (6.3)

      Si P esta rodeada por un diel´ectrico se producir´a un desplazamiento de fase acu-
mulativo εp, ocasionado a medida que la onda atraviesa el medio en direcci´on hacia
P . A los niveles de irradiaci´on normales, el medio se comportar´a de forma lineal, y la

   59
60 CAP´ITULO 6. PROPAGACIO´N CON ´INDICE DE REFRACCIO´N VARIABLE

frecuencia en el diel´ectrico ser´a la misma que en el vac´ıo, aunque la longitud de onda
y la velocidad no coincidan. Entonces, la perturbaci´on en P ser´a

Ep(t) = E0 cos ωt − εp.  (6.4)

      Donde la sustracci´on de εp corresponde al retraso en fase. Un observador que
estuviera en P tendr´ıa que esperar m´as tiempo en el medio material que en el vac´ıo
para que una cresta determinada llegara a ´el. Es decir, si imaginamos dos ondas
paralelas de la misma frecuencia, una en el vac´ıo y la otra en un medio material, la
primera pasar´a por P en un tiempo εp/ω menor que la otra. Vemos pues que, un
desfase de εp corresponde a una reducci´on en velocidad, v < c y n > 1. De manera
similar un adelanto de la fase da como resultado un aumento a la velocidad, v > c y
n > 1.

      Ahora, sabiendo que al pasar de un medio a otro con diferente ´ındice de refracci´on
ocasiona un cambio de fase en la onda que se propaga, podemos simular una lente que
nos permita controlar la propagaci´on de la onda. Lo u´nico que tenemos que hacer es
multiplicar el vector que contiene los valores de la onda en ese punto por

T = exp  ikn(r)  ,       (6.5)
           2f

que es la ecuaci´on de transmitancia de una lente. Donde n(r) es el ´ındice de refracci´on
en funci´on de la posici´on y f es la longitud del foco .

      La funci´on para el ´ındice de refracci´on de una lente convergente es n(r) = −x2.
Por lo tanto si multiplicamos la funci´on inicial por la transmitancia de esta lente con
un foco de 0.75 m, tendremos la ﬁgura 6.2 como resultado. Podemos observar que la
energ´ıa se concentra a una distancia de 0.75 m de la ventana, ya que coincide con el
foco de la lente.

      Si colocamos la misma lente ahora a una distancia de 0.75 m de la entrada, con
un foco id´entico al anterior; el resultado ser´a la ﬁgura 6.3 donde ahora la energ´ıa se
concentra a la distancia de 3 m de la entrada.
6.1. ANA´LISIS DEL ´INDICE DE REFRACCIO´N                                      61

(a) Intensidad                             (b) vista cenital

Figura 6.1: Propagaci´on de la luz para una entrada rectangular

(a) Intensidad                             (b) vista cenital

Figura 6.2: Propagaci´on con entrada rectangular y lente convergente en z = 0
62 CAP´ITULO 6. PROPAGACIO´N CON ´INDICE DE REFRACCIO´N VARIABLE

(a) Intensidad  (b) vista cenital

Figura 6.3: Propagaci´on con entrada rectangular y lente convergente en z = 0.75 m

6.2 Resultados

Cuando m´as densa es la sustancia por la que avanza la luz, menor es el esparcimiento
lateral [1]. Y esto es aplicable en la mayor parte de la atm´osfera baja. Lo que suce-
de en esta regi´on atmosf´erica es que el movimiento t´ermico del aire da lugar a unas
ﬂuctuaciones de densidad r´apidamente cambiantes a escala local. Estas ﬂuctuaciones
moment´aneas y bastante aleatorias provocan que haya m´as mol´eculas en unos sitios
que otros. Ocasionando con esto ﬂuctuaciones en el ´ındice de refracci´on. Generalmente
las condiciones que existen en un punto de la atm´osfera no existen en otro, debido a
que la atm´osfera es completamente inhomog´enea. La u´nica situaci´on para la cual nos-
otros podr´ıamos desarrollar un modelo para la atm´osfera es para el caso de turbulencia
isotr´opica homog´enea [10].

      Para poder realizar la simulaci´on a trav´es de la atm´osfera se requiere utilizar un
modelo de las ﬂuctuaciones del ´ındice de refracci´on para cada paso de la propagaci´on,
el cual se realiz´o de acuerdo a la ecuaci´on 3.22.

      Tomando el principio de cambio de fase producido por el ´ındice de refracci´on, y
la distribuci´on en la atm´osfera del mismo. Podemos llevar a cabo una simulacio´n en
donde en cada etapa de la propagaci´on sea como una lente cuyo ´ındice en el plano x, y
sea turbulento con variables aleatorias que tienen distribuci´on Gaussiana, tambi´en la
varianza pudiese cambiar a lo largo de la propagaci´on.

      Las lentes que simulan las ﬂuctuaciones del ´ındice de refracci´on en la atm´osfera
fueron generadas a partir de ruido blanco Gaussiano, ﬁltrado de acuerdo a la ecuaci´on
3.22. Y posteriormente aplicando la transformada de Fourier inversa nos da las ﬂuc-
tuaciones requeridas del ´ındice de refracci´on. En cada intervalo se multiplicara´ el haz
6.2. RESULTADOS  63

por la transmitancia de la lente cuyo ´ındice de refracci´on se obtuvo de la forma antes
mencionada. La varianza de las ﬂuctuaciones es controlada por la potencia del ruido
Gaussiano.

      En las presentes simulaciones con ´ındice variable se utiliz´o una longitud de onda
λ = 750 nm, que puede se f´acilmente producido por el laser semiconductor GaAs/GaAlAs.
Primeramente observemos el comportamiento para un haz Gaussiano. Recordemos que
en el cap´ıtulo anterior mostramos en la ﬁgura 5.4la propagaci´on para de un haz Gaussia-
no en condiciones de vac´ıo. Y pudimos observar como se manten´ıa claramente su forma
inicial con su respectiva atenuacio´n y ensanchamiento en su forma Gaussiana. Ahora
veamos como se propaga a trav´es de condiciones atmosf´ericas. En la ﬁgura 6.4 vemos
las ﬂuctuaciones que presenta el patr´on de intensidad de haz y podemos darnos cuenta
como pierde su forma Gaussiana ﬂuctuando de forma sumamente irregular. Veamos
en la ﬁgura 6.5 las secciones transversales a lo largo de la propagaci´on para observar
m´as claramente las ﬂuctuaciones de la intensidad. La varianza de las ﬂuctuaciones del
´ındice de refracci´on se encuentra en el rango de 7.43 × 10−10.

      Ahora propagamos un haz Bessel, cuyos par´ametros son id´enticos a los que se
utilizaron en el capitulo 6 que dieron como resultado las ﬁguras 5.12 y 5.13, es decir, una
ventana de radio R = 3 mm, la longitud de onda λ = 750 nm, un ´angulo θ = 0.0381◦,
los resultados obtenidos para condiciones de vac´ıo mostraron claramente la propiedad
adifraccional de estos haces. Ahora veamos el efectos de las ﬂuctuaciones del ´ındice
de refracci´on para estos haces Bessel. Si la varianza del ´ındice de refracci´on es de
7.45 × 10−16 los resultados obtenidos se muestran en la ﬁgura 6.6, donde los efectos de
las ﬂuctuaciones son muy poco notorios manteni´endose su condici´on adifraccional.

      Para una varianza de 7.45×10−14, el patr´on de intensidad del haz Bessel se muestra
en la ﬁgura 6.7, donde au´n es notoria la caracter´ıstica de no difracci´on del haz. Pero
ya se observan los turbulencia en los patrones de intensidad.

      Si la varianza de las ﬂuctuaciones es de 7.43 × 10−10, la propagaci´on ser´a como
se muestra en la ﬁgura 6.8. A partir de estos valores de varianza en las ﬂuctuaciones
se tiene que la forma adifraccional se pierde. De hecho esta varianza fue la misma que
se utiliz´o para el haz Gaussiano, y se puede ver las ﬂuctuaciones en la intensidad son
64 CAP´ITULO 6. PROPAGACIO´N CON ´INDICE DE REFRACCIO´N VARIABLE

(a) Funcio´n inicial  (b) a 1.5 metros

(c) a 3 metros        (d) a 6 metros

Figura 6.4: Propagaci´on de un haz Gaussiano en un medio turbulento (varianza=
7.45 × 10−16).
6.2. RESULTADOS  65

Figura 6.5: Secci´on transversal del haz Gaussiano durante la propagaci´on a trav´es de
un medio turbulento (varianza=7.43 × 10−10).

grandes y la forma inicial de los haces desaparece. Para tener una mejor perspectiva
de la propagaci´on en las ﬁguras 6.9, 6.10 y 6.11, se muestran los perﬁles transversales
de la propagaci´on del haz Bessel para ﬂuctuaciones del ´ındice de refracci´on con va-
rianza de 7.43 × 10−10, 7.43 × 10−10, 7.43 × 10−10 respectivamente. Vemos claramente
como empieza a afectar las ﬂuctuaciones en la forma inicial del haz, hasta perderse
completamente la caracter´ıstica adifraccional.
66 CAP´ITULO 6. PROPAGACIO´N CON ´INDICE DE REFRACCIO´N VARIABLE

(a) Funci´on inicial  (b) a 1.5 metros

(c) a 3 metros        (d) a 4.5 metros

Figura 6.6: Propagaci´on de un haz Bessel en un medio con ´ındice de refracci´on aleatorio
(varianza= 7.45 × 10−16).
6.2. RESULTADOS                         67

(a) Funcio´n inicial  (b) a 1.5 metros

(c) a 3 metros        (d) a 4.5 metros

Figura 6.7: Propagaci´on de un haz Bessel en un medio con ´ındice de refracci´on aleatorio
(varianza= 7.45 × 10−14).
68 CAP´ITULO 6. PROPAGACIO´N CON ´INDICE DE REFRACCIO´N VARIABLE

(a) Funci´on inicial  (b) a 1.5 metros

(c) a 3 metros        (d) a 4.5 metros

Figura 6.8: Propagaci´on de un haz Bessel en un medio con ´ındice de refracci´on aleatorio
(varianza= 7.43 × 10−10).
6.2. RESULTADOS  69

Figura 6.9: Secci´on transversal del haz Bessel durante la propagaci´on en un medio con
´ındice de refracci´on aleatorio (varianza= 7.45 × 10−16).

Figura 6.10: Secci´on transversal del haz Bessel durante la propagaci´on en un medio
con ´ındice de refracci´on aleatorio (varianza= 7.45 × 10−14).
70 CAP´ITULO 6. PROPAGACIO´N CON ´INDICE DE REFRACCIO´N VARIABLE

Figura 6.11: Secci´on transversal del haz Bessel durante la propagaci´on en un medio
con ´ındice de refracci´on aleatorio (varianza= 7.43 × 10−10).
Cap´ıtulo 7

Conclusiones

El estudio de la propagaci´on de sen˜ales ´opticas a trav´es de la atm´osfera es muy intere-
sante, ya que, las necesidades de grandes anchos de banda son cada vez mayores para
la transmisi´on de informaci´on. Se ve en los sistemas ´opticos inal´ambricos una buena
alternativa para cubrir estos requerimientos de anchos de banda. Los haces adifrac-
cionales han despertado un enorme inter´es, pues ser´ıa id´oneo, poder enviar sen˜ales sin
que estas sufran difracci´on a lo largo de grandes distancias, claro que considerando que
debe existir l´ınea de vista en la transmisi´on.

      Debido a los avances en las capacidades de procesamiento en la computadoras,
los m´etodos de diferencias ﬁnitas, especialmente el de Crank-Nicolson, son lo suﬁcien-
temente conﬁables para encontrar num´ericamente la soluciones a la ecuaci´on de onda,
pudiendo incluso, agregar condiciones turbulentas a la propagaci´on. Como ser´ıa el caso
de una onda que se propaga a trav´es de la atm´osfera.

      Los resultados que se obtuvieron mediante diversas simulaciones, ilustran clara-
mente la propagaci´on ´optica, mostrando claramente que en el vac´ıo los haces adifrac-
cionales mantienen su forma inicial durante cierta distancia, que es determinada prin-
cipalmente por el taman˜o de la ventana. Y en condiciones atmosf´ericas de turbulencia
homog´enea, se pierde la caracter´ıstica adifraccional de estos haces, au´n con pequen˜as
ﬂuctuaciones del ´ındice de refracci´on.

      Modelando las turbulencias mediante lentes delgadas, para la propagaci´on de haces
´opticos, es posible simular algunos fen´omenos presentes en la atm´osfera, tales como:
lluvia, neblina, viento, etc. En este trabajo se consider´o una atm´osfera tranquila, por
lo que queda abierta la posibilidad de continuar realizando simulaciones para diferentes
condiciones atmosf´ericas.

                                                      71
72  CAP´ITULO 7. CONCLUSIONES
Bibliograf´ıa

[1] Eugene Hetch, Optica, Addison Wesley, tercera edicion,1998.

[2] Donald W. Dearholt, Electromagnetic Wave Propagation, Mc Graw-Hill. 1973,

[3] J. C. Gutierrez Vega , M. D. Iturbide Castillo and S. Ch´avez Cerda, Alternative
    Formulation for Invariant Optical Fields: Mathieu Beams, Optics Letters, Vol. 25,
    No. 20, octuber 2000, pages 1493-1495. 1995.

[4] J. Durnin and J. J. Miceli Jr , Difraction-Free Beams, Physcal Review Letters, vol.
    58, pages 1499, 1986.

[5] J. Durnin, Exact solutions for nondiﬀracting beams. I. The scalar theory, Physcal
    Review Letters, vol. 58, pages 1499, 1986.

[6] Cardama, Jofre, Rius, Romeu y Blanch, Antenas, Alfaomega,1999.

[7] Lawrence R. S. and John W. Strohbehn, A Survey of Clear-Air Propagation Propa-
    gation Eﬀects Relevant to Optical Communications, Proceedings of the IEEE, vol.
    58, No. 8, Oct. 1970, pp. 1523-1545.

[8] Karp Sherman , Rober M. Gagliardi, Larry B. Stotts, Optical Channels (Fibers,
    Clouds, Water, and the Atmosphere), Plenum Press. 1973.

[9] Strohbehn J. W., Line-of-Sight Wave Propagation Through the Turbulent Atmosp-
    here, Proceedings of the IEEE, vol. 56, No. 8, August 1968, pages 1301-1318.

[10] Fante R. L., Electromagnetic Beam Propagation in Turbulent Media, Proceedings
    of the IEEE, vol. 63, No. 12, December 1975, pages 1669-1975.

[11] David A. de Wolf Waves in Turbulent Air: A Phenomenological Model, Procee-
    dings of the IEEE, vol. 62, No. 11, November 1974, pages 1523-1529.

[12] Hodara H., Light Wave Propagation Through the Atmosphere, Proceedings of the
    IEEE, vol. 54, No. 3, March 1966, pages 368-375.

                                                      73
74  BIBLIOGRAF´IA

[13] C. Pozrikidis , Numerical Computation in Science and Engineering, Oxford Uni-
    versiti Press, 1998.

[14] Bontoux Thierry, Yoshinori Kato, Masahiro Nakatsuka, Three-Dimensional Laser
    Simulation Code On a Desktop Personal Computer: Nonlinear Propagation and
    Fresnel Distribution, Optics Letters, Vol. 25, No. 20, octuber 2000, pages 1493-
    1495. 1995.
Vita

      Jos´e Ad´an Hern´andez Nolasco

Direcci´on permanente: Av. Ju´arez #315
                              Col. Centro C.P. 86500
                              C´ardenas, Tabasco
                              M´exico.
                              jaherno@hotmail.com

La presente tesis fue tipograﬁada con LATEX1 por Jos´e Ad´an Hern´andez Nolasco.

    1El paquete de macros, ITESMtesis.sty, utilizado en el formateo de esta tesis fue escrito por el
Dr. Horacio Mart´ınez Alfaro <hma@campus.mty.itesm.mx>, Profesor Asociado del Centro de Inteli-
gencia Artiﬁcial del Instituto Tecnolo´gico y de Estudios Superiores de Monterrey, Campus Monterrey.

                                                      75
