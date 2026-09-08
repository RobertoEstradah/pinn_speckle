# Modelo matemático de difracción en región de Fresnel convergente y divergente de una lente esférica — capítulo de libro (Andrés Zárate et al., 2024)

> Fuente: `AndresZarate_etal_2024_DifraccionLenteEsferica_CapituloLibro.pdf` (convertido con pdftotext desde `master_supporting_docs/supporting_papers/referencias/`)

> Capítulo 7 de *Estudos em Ciências Exatas e da Terra: Desafios, Avanços e Possibilidades II* (Editora Artemis, Curitiba-PR, Brasil, 2024). DOI: 10.37572/EdArt_2711243907. Republicación/versión ampliada del paper de Revista Mexicana de Física 65 (2019) 299-306 (mismos autores originales + 3 coautores nuevos: Marian Cristina Ricárdez Torres, Omar Morales Alejos, Israel Benjamín Sánchez Jiménez). Licencia CC BY-NC-ND 4.0.

---

                              2024 by Editora Artemis
                           Copyright © Editora Artemis
                      Copyright do Texto © 2024 Os autores
                   Copyright da Edição © 2024 Editora Artemis

                            O conteúdo deste livro está licenciado sob uma Licença de Atribuição Creative
                            Commons Atribuição-Não-Comercial NãoDerivativos 4.0 Internacional (CC BY-NC-ND
                            4.0). Direitos para esta edição cedidos à Editora Artemis pelos autores. Permitido o
download da obra e o compartilhamento, desde que sejam atribuídos créditos aos autores, e sem a
possibilidade de alterá-la de nenhuma forma ou utilizá-la para fins comerciais.

A responsabilidade pelo conteúdo dos artigos e seus dados, em sua forma, correção e confiabilidade é
exclusiva dos autores. A Editora Artemis, em seu compromisso de manter e aperfeiçoar a qualidade e
confiabilidade dos trabalhos que publica, conduz a avaliação cega pelos pares de todos manuscritos
publicados, com base em critérios de neutralidade e imparcialidade acadêmica.

Editora Chefe      Profª Drª Antonella Carvalho de Oliveira
Editora Executiva  M.ª Viviane Carvalho Mocellin
Direção de Arte    M.ª Bruna Bejarano
Diagramação        Elisangela Abreu
Organizador        Prof. Dr. Alireza Mohebi Ashtiani
Imagem da Capa     Abstract Style Landscapes /123RF
Bibliotecário      Maurício Amormino Júnior – CRB6/2422

Conselho Editorial

Prof.ª Dr.ª Ada Esther Portero Ricol, Universidad Tecnológica de La Habana “José Antonio Echeverría”, Cuba
Prof. Dr. Adalberto de Paula Paranhos, Universidade Federal de Uberlândia, Brasil
Prof. Dr. Agustín Olmos Cruz, Universidad Autónoma del Estado de México, México
Prof.ª Dr.ª Amanda Ramalho de Freitas Brito, Universidade Federal da Paraíba, Brasil
Prof.ª Dr.ª Ana Clara Monteverde, Universidad de Buenos Aires, Argentina
Prof.a Dr.a Ana Júlia Viamonte, Instituto Superior de Engenharia do Porto (ISEP), Portugal
Prof. Dr. Ángel Mujica Sánchez, Universidad Nacional del Altiplano, Peru
Prof.ª Dr.ª Angela Ester Mallmann Centenaro, Universidade do Estado de Mato Grosso, Brasil
Prof.ª Dr.ª Begoña Blandón González, Universidad de Sevilla, Espanha
Prof.ª Dr.ª Carmen Pimentel, Universidade Federal Rural do Rio de Janeiro, Brasil
Prof.ª Dr.ª Catarina Castro, Universidade Nova de Lisboa, Portugal
Prof.ª Dr.ª Cirila Cervera Delgado, Universidad de Guanajuato, México
Prof.ª Dr.ª Cláudia Neves, Universidade Aberta de Portugal
Prof.ª Dr.ª Cláudia Padovesi Fonseca, Universidade de Brasília-DF, Brasil
Prof. Dr. Cleberton Correia Santos, Universidade Federal da Grande Dourados, Brasil
Prof. Dr. Cristo Ernesto Yáñez León – New Jersey Institute of Technology, Newark, NJ, Estados Unidos
Prof. Dr. David García-Martul, Universidad Rey Juan Carlos de Madrid, Espanha
Prof.ª Dr.ª Deuzimar Costa Serra, Universidade Estadual do Maranhão, Brasil
Prof.ª Dr.ª Dina Maria Martins Ferreira, Universidade Estadual do Ceará, Brasil
Prof.ª Dr.ª Edith Luévano-Hipólito, Universidad Autónoma de Nuevo León, México
Prof.ª Dr.ª Eduarda Maria Rocha Teles de Castro Coelho, Universidade de Trás-os-Montes e Alto Douro, Portugal
Prof. Dr. Eduardo Eugênio Spers, Universidade de São Paulo (USP), Brasil
Prof. Dr. Eloi Martins Senhoras, Universidade Federal de Roraima, Brasil
Prof.ª Dr.ª Elvira Laura Hernández Carballido, Universidad Autónoma del Estado de Hidalgo, México

                                                               Editora Artemis
                                                               Curitiba-PR Brasil
                                                               www.editoraartemis.com.br
                                                               e-mail:publicar@editoraartemis.com.br
Prof.ª Dr.ª Emilas Darlene Carmen Lebus, Universidad Nacional del Nordeste/ Universidad Tecnológica Nacional, Argentina
Prof.ª Dr.ª Erla Mariela Morales Morgado, Universidad de Salamanca, Espanha
Prof. Dr. Ernesto Cristina, Universidad de la República, Uruguay
Prof. Dr. Ernesto Ramírez-Briones, Universidad de Guadalajara, México
Prof. Dr. Fernando Hitt, Université du Québec à Montréal, Canadá
Prof. Dr. Gabriel Díaz Cobos, Universitat de Barcelona, Espanha
Prof.a Dr.a Gabriela Gonçalves, Instituto Superior de Engenharia do Porto (ISEP), Portugal
Prof.ª Dr.ª Galina Gumovskaya – Higher School of Economics, Moscow, Russia
Prof. Dr. Geoffroy Roger Pointer Malpass, Universidade Federal do Triângulo Mineiro, Brasil
Prof.ª Dr.ª Gladys Esther Leoz, Universidad Nacional de San Luis, Argentina
Prof.ª Dr.ª Glória Beatriz Álvarez, Universidad de Buenos Aires, Argentina
Prof. Dr. Gonçalo Poeta Fernandes, Instituto Politécnido da Guarda, Portugal
Prof. Dr. Gustavo Adolfo Juarez, Universidad Nacional de Catamarca, Argentina
Prof. Dr. Guillermo Julián González-Pérez, Universidad de Guadalajara, México
Prof. Dr. Håkan Karlsson, University of Gothenburg, Suécia
Prof.ª Dr.ª Iara Lúcia Tescarollo Dias, Universidade São Francisco, Brasil
Prof.ª Dr.ª Isabel del Rosario Chiyon Carrasco, Universidad de Piura, Peru
Prof.ª Dr.ª Isabel Yohena, Universidad de Buenos Aires, Argentina
Prof. Dr. Ivan Amaro, Universidade do Estado do Rio de Janeiro, Brasil
Prof. Dr. Iván Ramon Sánchez Soto, Universidad del Bío-Bío, Chile
Prof.ª Dr.ª Ivânia Maria Carneiro Vieira, Universidade Federal do Amazonas, Brasil
Prof. Me. Javier Antonio Albornoz, University of Miami and Miami Dade College, Estados Unidos
Prof. Dr. Jesús Montero Martínez, Universidad de Castilla - La Mancha, Espanha
Prof. Dr. João Manuel Pereira Ramalho Serrano, Universidade de Évora, Portugal
Prof. Dr. Joaquim Júlio Almeida Júnior, UniFIMES - Centro Universitário de Mineiros, Brasil
Prof. Dr. Jorge Ernesto Bartolucci, Universidad Nacional Autónoma de México, México
Prof. Dr. José Cortez Godinez, Universidad Autónoma de Baja California, México
Prof. Dr. Juan Carlos Cancino Diaz, Instituto Politécnico Nacional, México
Prof. Dr. Juan Carlos Mosquera Feijoo, Universidad Politécnica de Madrid, Espanha
Prof. Dr. Juan Diego Parra Valencia, Instituto Tecnológico Metropolitano de Medellín, Colômbia
Prof. Dr. Juan Manuel Sánchez-Yáñez, Universidad Michoacana de San Nicolás de Hidalgo, México
Prof. Dr. Juan Porras Pulido, Universidad Nacional Autónoma de México, México
Prof. Dr. Júlio César Ribeiro, Universidade Federal Rural do Rio de Janeiro, Brasil
Prof. Dr. Leinig Antonio Perazolli, Universidade Estadual Paulista (UNESP), Brasil
Prof.ª Dr.ª Lívia do Carmo, Universidade Federal de Goiás, Brasil
Prof.ª Dr.ª Luciane Spanhol Bordignon, Universidade de Passo Fundo, Brasil
Prof. Dr. Luis Fernando González Beltrán, Universidad Nacional Autónoma de México, México
Prof. Dr. Luis Vicente Amador Muñoz, Universidad Pablo de Olavide, Espanha
Prof.ª Dr.ª Macarena Esteban Ibáñez, Universidad Pablo de Olavide, Espanha
Prof. Dr. Manuel Ramiro Rodriguez, Universidad Santiago de Compostela, Espanha
Prof. Dr. Manuel Simões, Faculdade de Engenharia da Universidade do Porto, Portugal
Prof.ª Dr.ª Márcia de Souza Luz Freitas, Universidade Federal de Itajubá, Brasil
Prof. Dr. Marcos Augusto de Lima Nobre, Universidade Estadual Paulista (UNESP), Brasil
Prof. Dr. Marcos Vinicius Meiado, Universidade Federal de Sergipe, Brasil
Prof.ª Dr.ª Mar Garrido Román, Universidad de Granada, Espanha
Prof.ª Dr.ª Margarida Márcia Fernandes Lima, Universidade Federal de Ouro Preto, Brasil
Prof.ª Dr.ª María Alejandra Arecco, Universidad de Buenos Aires, Argentina
Prof.ª Dr.ª Maria Aparecida José de Oliveira, Universidade Federal da Bahia, Brasil
Prof.ª Dr.ª Maria Carmen Pastor, Universitat Jaume I, Espanha

                                                                                                                                  Editora Artemis
                                                                                                                                  Curitiba-PR Brasil
                                                                                                                                  www.editoraartemis.com.br
                                                                                                                                  e-mail:publicar@editoraartemis.com.br
Prof.ª Dr.ª Maria da Luz Vale Dias – Universidade de Coimbra, Portugal
Prof.ª Dr.ª Maria do Céu Caetano, Universidade Nova de Lisboa, Portugal
Prof.ª Dr.ª Maria do Socorro Saraiva Pinheiro, Universidade Federal do Maranhão, Brasil
Prof.ª Dr.ª MªGraça Pereira, Universidade do Minho, Portugal
Prof.ª Dr.ª Maria Gracinda Carvalho Teixeira, Universidade Federal Rural do Rio de Janeiro, Brasil
Prof.ª Dr.ª María Guadalupe Vega-López, Universidad de Guadalajara, México
Prof.ª Dr.ª Maria Lúcia Pato, Instituto Politécnico de Viseu, Portugal
Prof.ª Dr.ª Maritza González Moreno, Universidad Tecnológica de La Habana, Cuba
Prof.ª Dr.ª Mauriceia Silva de Paula Vieira, Universidade Federal de Lavras, Brasil
Prof. Dr. Melchor Gómez Pérez, Universidad del Pais Vasco, Espanha
Prof.ª Dr.ª Ninfa María Rosas-García, Centro de Biotecnología Genómica-Instituto Politécnico Nacional, México
Prof.ª Dr.ª Odara Horta Boscolo, Universidade Federal Fluminense, Brasil
Prof. Dr. Osbaldo Turpo-Gebera, Universidad Nacional de San Agustín de Arequipa, Peru
Prof.ª Dr.ª Patrícia Vasconcelos Almeida, Universidade Federal de Lavras, Brasil
Prof.ª Dr.ª Paula Arcoverde Cavalcanti, Universidade do Estado da Bahia, Brasil
Prof. Dr. Rodrigo Marques de Almeida Guerra, Universidade Federal do Pará, Brasil
Prof. Dr. Saulo Cerqueira de Aguiar Soares, Universidade Federal do Piauí, Brasil
Prof. Dr. Sergio Bitencourt Araújo Barros, Universidade Federal do Piauí, Brasil
Prof. Dr. Sérgio Luiz do Amaral Moretti, Universidade Federal de Uberlândia, Brasil
Prof.ª Dr.ª Silvia Inés del Valle Navarro, Universidad Nacional de Catamarca, Argentina
Prof.ª Dr.ª Solange Kazumi Sakata, Instituto de Pesquisas Energéticas e Nucleares (IPEN)- USP, Brasil
Prof.ª Dr.ª Stanislava Kashtanova, Saint Petersburg State University, Russia
Prof.ª Dr.ª Susana Álvarez Otero – Universidad de Oviedo, Espanha
Prof.ª Dr.ª Teresa Cardoso, Universidade Aberta de Portugal
Prof.ª Dr.ª Teresa Monteiro Seixas, Universidade do Porto, Portugal
Prof. Dr. Valter Machado da Fonseca, Universidade Federal de Viçosa, Brasil
Prof.ª Dr.ª Vanessa Bordin Viera, Universidade Federal de Campina Grande, Brasil
Prof.ª Dr.ª Vera Lúcia Vasilévski dos Santos Araújo, Universidade Tecnológica Federal do Paraná, Brasil
Prof. Dr. Wilson Noé Garcés Aguilar, Corporación Universitaria Autónoma del Cauca, Colômbia
Prof. Dr. Xosé Somoza Medina, Universidad de León, Espanha

                         Dados Internacionais de Catalogação na Publicação (CIP)
                                        (eDOC BRASIL, Belo Horizonte/MG)

                E82 Estudos em Ciências Exatas e da Terra: Desafios, Avanços e
                                Possibilidades II / Organizador Alireza Mohebi Ashtiani. –
                                Curitiba, PR: Artemis, 2024.
                                Formato: PDF
                                Requisitos de sistema: Adobe Acrobat Reader
                                Modo de acesso: World Wide Web
                                Inclui bibliografia
                                Edição bilíngue
                                ISBN 978-65-81701-39-0
                                DOI 10.37572/EdArt_271124390
                                1. Ciências exatas e da terra – Pesquisa – Brasil. I. Ashtiani,

                          Alireza Mohebi.
                                                                                                        CDD 509

                          Elaborado por Maurício Amormino Júnior – CRB6/2422

                                                                                                                                  Editora Artemis
                                                                                                                                  Curitiba-PR Brasil
                                                                                                                                  www.editoraartemis.com.br
                                                                                                                                  e-mail:publicar@editoraartemis.com.br
                                                   INTRODUÇÃO

          A coletânea Estudos em Ciências Exatas e da Terra: Desafios, Avanços e
Possibilidades II reúne contribuições significativas nas áreas de geociências, engenharia e
física, com um foco particular na análise e solução de problemas complexos em diferentes
contextos e regiões do mundo. Os artigos apresentados neste volume abordam desde
questões geológicas e ambientais até modelos matemáticos avançados aplicados a
problemas práticos, evidenciando a diversidade e a riqueza dos desafios contemporâneos
enfrentados por pesquisadores nas Ciências Exatas e da Terra.

          O primeiro artigo, Feições Erosivas em Vargem Alta (Espírito Santo, Brasil),
trata das dinâmicas de erosão no município de Vargem Alta, com um olhar atento aos
processos naturais e suas consequências para o meio ambiente local. Em seguida,
Análise de Estabilidade de Talude no Município de Vargem Alta (ES) oferece uma análise
detalhada sobre a estabilidade de taludes e suas implicações para a segurança das áreas
urbanas e rurais afetadas.

          No artigo Contribuição para o Zoneamento de Risco de Inundações Urbanas
no Município de Lichinga, Província de Niassa, Moçambique, o foco se desloca para a
aplicação de metodologias para o zoneamento de risco de inundações, um tema de
grande importância para o planejamento urbano e a segurança das populações em
regiões vulneráveis.

          No trabalho Paleocanais na Plataforma Continental Interna do Rio Grande:
Evidências de Variações Eustáticas Durante o Quaternário, os autores investigam as
evidências geológicas de mudanças eustáticas, proporcionando uma compreensão mais
profunda dos eventos climáticos e ambientais que marcaram a história do planeta.

          No campo da geografia e da agricultura, Consolidação de Terras Agrícolas (Estudo
de Caso Russo) apresenta um estudo de caso sobre a reorganização da agricultura em
uma região da Rússia, discutindo a viabilidade de práticas de consolidação de terras para
otimizar o uso da terra e aumentar a produção agrícola.

          Seguindo para a física aplicada, o artigo 1D Space-Time Solution of the Species
Diffusion Equation with Double Entry Boundary in Spherical Foods explora soluções
matemáticas para a equação de difusão de espécies, com aplicação no setor alimentício,
focando na modelagem de processos dentro de esferas alimentícias.

          Em seguida, Modelo Matemático de Difracción en Región de Fresnel Convergente
y Divergente de una Lente Esférica apresenta um modelo matemático inovador para a
difração da luz em lentes esféricas, contribuindo para o campo da óptica e suas aplicações.

          Por fim, Caracterización de los Efectos de una Fulguración Solar discute os impactos
de eventos solares extremos, com foco nas implicações para a física espacial e para a
proteção de tecnologias modernas sensíveis, como satélites e sistemas de comunicação.
          Como é possível observar, este volume é uma contribuição valiosa para o avanço
das Ciências Exatas e da Terra, apresentando uma ampla gama de pesquisas que têm
o potencial de influenciar práticas em diversas áreas, desde a mitigação de riscos
ambientais até o desenvolvimento de novas tecnologias e abordagens inovadoras em
várias disciplinas. A variedade de temas e abordagens evidenciam a complexidade dos
desafios que os pesquisadores enfrentam atualmente e reforçam a importância da
colaboração interdisciplinar para o progresso científico.

          Desejo a todos uma proveitosa leitura!

                                                                                         Alireza Mohebi Ashtiani
SUMÁRIO

CAPÍTULO 1........................................................................................................................................ 1
FEIÇÕES EROSIVAS EM VARGEM ALTA (ESPÍRITO SANTO, BRASIL)

     Éder Carlos Moreira
     Leonardo Coelho Fabrino Filho

          https://doi.org/10.37572/EdArt_2711243901

CAPÍTULO 2.................................................................................................................................... 15
ANÁLISE DE ESTABILIDADE DE TALUDE NO MUNICÍPIO DE VARGEM ALTA (ES)

     Éder Carlos Moreira
     Eric José Cerqueira Gonçalves
     Thiago Curty Vimercati

          https://doi.org/10.37572/EdArt_2711243902

CAPÍTULO 3....................................................................................................................................27
CONTRIBUIÇÃO PARA O ZONEAMENTO DE RISCO DE INUNDAÇÕES URBANAS NO
MUNICÍPIO DE LICHINGA, PROVÍNCIA DE NIASSA, MOÇAMBIQUE

     Americo José Fombe
     Gustavo Sobrinho Dgedge

          https://doi.org/10.37572/EdArt_2711243903

CAPÍTULO 4....................................................................................................................................47
PALEOCANAIS NA PLATAFORMA CONTINENTAL INTERNA DO RIO GRANDE:
EVIDÊNCIAS DE VARIAÇÕES EUSTÁTICAS DURANTE O QUATERNÁRIO

     Laurício Corrêa Terra
          https://doi.org/10.37572/EdArt_2711243904

CAPÍTULO 5................................................................................................................................... 56
AGRICULTURAL LAND CONSOLIDATION (RUSSIAN CASE STUDY)

     Alexander Sagaydak
     Anna Sagaydak

          https://doi.org/10.37572/EdArt_2711243905

                                                                                                                                S USMU ÁMRÁIROI O
CAPÍTULO 6................................................................................................................................... 64
1D SPACE-TIME SOLUTION OF THE SPECIES DIFFUSION EQUATION WITH DOUBLE
ENTRY BOUNDARY IN SPHERICAL FOODS

     Juan Ignacio González Pacheco
     Mariela Beatriz Maldonado
     Ariel Fernando Márquez Agüero
     Paula Anabella Giorlando Videla
     Leonel Nicolás Lisanti
     Carla Rocío Zaragoza
     Oscar Daniel Galvez

          https://doi.org/10.37572/EdArt_2711243906

CAPÍTULO 7................................................................................................................................... 85
MODELO MATEMÁTICO DE DIFRACCIÓN EN REGIÓN DE FRESNEL CONVERGENTE
Y DIVERGENTE DE UNA LENTE ESFÉRICA

     Esteban Andrés Zárate
     Quintiliano Angulo Córdova
     Marian Cristina Ricárdez Torres
     Omar Morales Alejos
     Israel Benjamín Sánchez Jiménez
     José Adán Hernández Nolasco

          https://doi.org/10.37572/EdArt_2711243907

CAPÍTULO 8................................................................................................................................. 100
CARACTERIZACIÓN DE LOS EFECTOS DE UNA FULGURACIÓN SOLAR

     Guillermo Daniel Rodriguez
     Ricardo Ezequiel Garcia
     Leonardo José Navarría
     Nicolas Quaglino

          https://doi.org/10.37572/EdArt_2711243908

SOBRE O ORGANIZADOR.........................................................................................................112

ÍNDICE REMISSIVO.................................................................................................................... 113

                                                                                                                                S USMU ÁMRÁIROI O
                                         CAPÍTULO 7

MODELO MATEMÁTICO DE DIFRACCIÓN EN REGIÓN DE
        FRESNEL CONVERGENTE Y DIVERGENTE DE UNA
                                                          LENTE ESFÉRICA

Data de submissão: 09/11/2024                                             Israel Benjamín Sánchez Jiménez
Data de aceite: 18/11/2024                                                                     Universidad Juárez

                               Esteban Andrés Zárate                                       Autónoma de Tabasco
                                     Universidad Juárez                                   División Académica de

                                 Autónoma de Tabasco                                              Ciencias Básicas
                                División Académica de                             Cunduacán Tabasco, México

                                        Ciencias Básicas                      José Adán Hernández Nolasco
                        Cunduacán Tabasco, México                                              Universidad Juárez
        https://orcid.org/0000-0003-3515-5793
                                                                                           Autónoma de Tabasco
                         Quintiliano Angulo Córdova                        División Académica de Ciencias y
                                     Universidad Juárez
                                                                                Tecnologías de la Información
                                 Autónoma de Tabasco                              Cunduacán Tabasco, México
                                División Académica de            https://orcid.org/0000-0003-4671-0350

                                        Ciencias Básicas  RESUMEN: El objetivo de este trabajo fue
                        Cunduacán Tabasco, México         determinar el modelo matemático de difracción
        https://orcid.org/0000-0002-9594-6311             en las regiones de Fresnel convergente y
                                                          divergente de un doblete cementado, utilizando
                   Marian Cristina Ricárdez Torres        el método de propagación del espectro
                                     Universidad Juárez   angular. Se obtuvieron modelos de difracción
                                                          mediante la convolución de transformadas de
                                 Autónoma de Tabasco      Fourier, con una distribución tipo Bessel de la
                                División Académica de     suma de argumentos, asociada a la distribución
                                                          de amplitud del campo de ondas de luz láser
                                        Ciencias Básicas  difractadas por dos aberturas circulares de
                        Cunduacán Tabasco, México         radios diferentes. Los resultados teóricos
                                                          fueron corroborados experimentalmente
                                  Omar Morales Alejos     y mediante simulación computacional. Se
                                     Universidad Juárez   concluyó que la suma de los argumentos
                                                          permite interpretar el patrón de difracción
                                 Autónoma de Tabasco      como franjas de interferencia elípticas con
                                División Académica de     distribución tipo Bessel. Además, el desfase

                                        Ciencias Básicas
                        Cunduacán Tabasco, México

Estudos em Ciências Exatas e da Terra: Desafios, Avanços e Possibilidades II  Capítulo 7  85
que experimentan las ondas difractadas al propagarse desde el plano objeto hasta la región
de Fresnel convergente es de π/4, mientras que, al llegar a la región de Fresnel divergente
del lente doblete cementado usado como lente transformador, el desfase es de 3/4 π.
PALABRAS CLAVE: Difracción. Convolución. Fresnel convergente y divergente.
Simulación computacional.

MATHEMATICAL MODEL OF DIFFRACTION IN CONVERGENT AND DIVERGENT
                              FRESNEL REGION OF A SPHERICAL LENS

ABSTRACT: The objective of this work was to determine the mathematical model
of diffraction in the convergent and divergent Fresnel regions of a cemented doublet,
employing the angular spectrum propagation method. Diffraction models were derived
through the convolution of Fourier transforms, with a Bessel-type distribution of the
sum of arguments, associated with the amplitude distribution of the laser light wave
field diffracted by two circular apertures of differing radii. Theoretical results were
corroborated both experimentally and through computational simulation. It was concluded
that the summation of the arguments enables the interpretation of the diffraction pattern
as elliptical interference fringes with a Bessel-type distribution. Furthermore, the phase
shift experienced by the diffracted waves as they propagate from the object plane to the
convergent Fresnel region is π/4, while upon reaching the divergent Fresnel region of the
cemented doublet lens used as a transforming lens, the phase shift is 3 π/4.
KEYWORDS: Diffraction. Convolution. Convergent and divergent Fresnel. Computational
simulation.

1 INTRODUCCIÓN

          El problema de difracción de luz coherente puede ser interpretado como
el mapeo de la distribución de amplitud del campo óptico en algunas regiones del
espacio, asociado a este problema existe la necesidad de describir la distribución de
amplitud caracterizada por la función de transmitancia t (x, y) asociada a la abertura
u objeto difractor en planos de la región convergente, divergente y focal de una lente
esférica (Martínez et al., 2001). (Sheppard & Hrynevych, 1992) realizaron el estudio
de difracción por una abertura circular, en el que propusieron una generalización a la
teoría de difracción de Fresnel, a través de una aproximación por variación paraboidal
en vez de una variación binominal en los términos de fase en la ecuación. (Quintero
et al., 2006), estudiaron los efectos de difracción e interferencia producidos por una
estructura compuesta de múltiples aberturas circulares idénticas, no reportan análisis
de propagación, ni presentan un modelo matemático de difracción, ya que el trabajo lo
realizaron sin el uso de lente transformadora.

          (Zárate, 2011), realizó el estudio de propagación del campo difractado por dos
aberturas de radios con igual magnitud, su análisis lo realizó hasta la región de Fraunhofer o
de la transformada de Fourier, usando un doblete cementado como lente transformadora.

Estudos em Ciências Exatas e da Terra: Desafios, Avanços e Possibilidades II  Capítulo 7        86
Mientras que (Zárate et al., 2013), realizaron un análisis de propagación hasta el plano de
enfoque o de Fraunhofer de un doblete cementado usado como transformador. además
presentaron imágenes de patrones de difracción generados de forma experimental, en las
cuales no se aprecia la geometría elíptica de las franjas de máxima y mínima intensidad,
sin realizar un análisis de la propagación del campo de difracción hacia las regiones
convergente y divergente de un lente doblete cementado usado como transformador.

          En este trabajo, se reporta el estudio de propagación hasta la región de Fresnel
convergente y divergente, de un lente doblete cementado del campo de difracción
producido, por dos aberturas circulares con radios de diferente magnitud, contenidas
en material laminado, iluminadas con ondas planas. El tratamiento se realizó bajo el
formalismo del método de propagación del espectro angular.

2 MATERIALES Y MÉTODOS

El modelo matemático de difracción fue generado de acuerdo con el arreglo

de la figura 1. Centrando el análisis de propagación del campo difractado por las

dos aberturas (figura 1,4) colocadas en el plano x0 y0, de radios a1 y a2 de diferentes
magnitudes iluminadas con ondas planas monocromáticas de amplitud constante E0. La
función de transmitancia que se le asocia al par de aberturas como objeto difractor es,

                                                     (Goodman, 2005), siendo l1 la distancia a la que
se encuentran desplazadas las aberturas circulares, respecto al origen de coordenadas

del plano objeto x0 y0 ver figura 1, cuyo espesor es lz y r0 en coordenadas polares queda

definido como  .

Figura 1. Procesador de Fourier usado para obtener patrones de difracción. Sobre la figura identificamos a: (1) laser

de He-Ne, (2) filtro espacial, (3) colimador, (4) objeto bajo estudio en plano x0y0, (5) lente transformadora, y (6) plano
de observación xzyz.

Estudos em Ciências Exatas e da Terra: Desafios, Avanços e Possibilidades II  Capítulo 7                                    87
          El campo de ondas monocromáticas difractadas por el objeto o aberturas
circulares desplazadas del origen en la cantidad l1, y distribuidas en el plano x0 y0 está
dado por la ecuación (1).

          (Andrés Zárate et al., 2013) determinaron que la distribución de amplitud del
campo propagado hasta el plano xz yz , en el que se distribuye, se obtiene mediante
la ecuación (2), en la que se ha usado como condición inicial, que el objeto difractor
esté colocado a la distancia d0, la cual es la misma que la longitud focal de la lente
transformadora (d0= fLD), además de considerar el teorema de la transformada de Fourier
del producto de funciones (Gaskill, 1978).

          La transformada de Fourier de la función de transmitancia t0 (x0, y0) en la ecuación
(2) se obtiene usando el teorema de linealidad, escalamiento y desplazamiento (Gaskill,

1978); siendo              la frecuencia espacial definida en el plano de frecuencias

espaciales uv, resultando

          En tanto que la transformada de Fourier de la Función exponencial de la ecuación
(2) es:

          Sustituyendo las ecuaciones (3) y (4) en la ecuación (2) se determina que la
distribución de amplitud del campo difractado queda definida por la siguiente expresión:

Estudos em Ciências Exatas e da Terra: Desafios, Avanços e Possibilidades II  Capítulo 7        88
          Donde el símbolo ⊗ significa la operación matemática de convolución, mientras
que el símbolo ● significa la operación de multiplicación en la ecuación (5) y en ecuaciones
subsecuentes.

3 RESULTADOS TEÓRICOS
          La ecuación (5) establece que, el patrón de difracción GzC(u,v) se ha propagado

hasta la región de Fresnel (convergente) situada en el intervalo de distancia 0<z< fLD,
donde fLD es la distancia focal de la lente transformadora (el cual se interpreta como
un patrón de difracción derecho). Mediante el uso de la propiedad conmutativa de la
convolución y a través de un proceso de integración la ecuación (5) se reescribe para esta
región de Fresnel convergente en la forma dada por la ecuación (6). En esta ecuación, el
desfasamiento que ha sufrido el campo propagado desde el plano x0y0 hasta el plano xzyz
en el intervalo arriba especificado, fue de π/4 el cual se obtiene realizando la integral de
convolución de la ecuación (5) y considerando que fLD -z>0.

          El patrón de difracción propagado hasta la región de Fresnel (divergente) de la
lente transformadora, situada en el intervalo de distancia fLD<z<∞ se interpreta como
un patrón de difracción izquierdo, quedando definido a través de la ecuación (7), el
desfasamiento en esta región fue de 3π/4, mismo que se determina considerando que
z- fLD<0 y realizando la integral de convolución de la ecuación (5).

Estudos em Ciências Exatas e da Terra: Desafios, Avanços e Possibilidades II  Capítulo 7      89
          Las distribuciones de intensidad para las regiones de Fresnel (convergente y
divergente) de la lente transformadora, se determinan respectivamente por las ecuaciones
(8) y (9).

          Usando la expresión (10) para el producto de funciones Bessel

( ) ( ) J1 2πa1ω J1 2πa2ω , (Hayek, 2001; Andrés Zárate, 2011); considerando que los

productos de las funciones Bessel.

Definidos por la suma                                                                     , no

aportan información relevante a la distribución de intensidad por lo cual no se toman en

cuenta y combinando la ecuación (10) con la ecuación (8), se obtiene que la distribución

de intensidad en la región de Fresnel (convergente) de un lente doblete cementado o

transformador es.

Estudos em Ciências Exatas e da Terra: Desafios, Avanços e Possibilidades II  Capítulo 7        90
          La distribución de intensidad en la región de Fresnel (divergente) del doblete
cementado o transformador, se determina considerando que la suma de funciones
Bessel del párrafo anterior, en la ecuación (10) no aporta información relevante, bajo esta
condición la ecuación (9) se reescribe en la forma:

          En la ecuación (11) la distribución del patrón de difracción que se propaga en la
región de Fresnel (convergente) de la lente transformadora, difiere solo en el denominador
de la distribución de intensidad definida con la ecuación (12) del patrón de difracción
izquierdo que se propaga en la región de Fresnel (divergente) de la lente transformadora.
Las ecuaciones (11) y (12) nos permiten afirmar que en las regiones de Fresnel convergente
y divergente del lente doblete cementado usado como transformador, existe un patrón
de difracción elíptico de distribución tipo Bessel con suma de argumentos, que modula
franjas lineales de Young.

4 RESULTADOS EXPERIMENTALES

          Los experimentos se desarrollaron empleando el sistema óptico de la Fig. 2a, el
cual está en relación directa con el esquema de la Fig. 1. El haz de luz de láser de He-Ne
(λ= 632 nm) ampliado y filtrado con objetivo de microscopio 40X y pinhole de 50 μm , fue

Estudos em Ciências Exatas e da Terra: Desafios, Avanços e Possibilidades II  Capítulo 7     91
colimado con lente doblete cementado acromático de 50 cm de distancia focal. Como
objeto difractor, se usaron dos aberturas circulares, su imagen se muestra en la Fig. 2b,
cuyos radios de curvatura son: a1= 1.0 mm y a2= 1.5 mm, respectivamente. Contenidas en
material laminado de plástico con lz = 2.0mm de espesor. Se uso como transformador un
doblete acromático cementado de 25 cm de distancia focal. Las imágenes de cada patrón
de difracción en intensidad se grabaron usando una cámara digital de alta velocidad y
precisión, con sensor CMOS y 18.0 megapíxeles.

                       Figura 2. a) Arreglo experimental, b) Aberturas con radios de diferente magnitud.

a		                                                                           b

          En la región de Fresnel convergente situada en el intervalo de distancia 0<z<fLD
de la lente transformadora, se obtiene la convolución de transformadas de Fourier,
cuantitativamente los podemos relacionar con los valores exactos dados por la ecuación
(11) y se consideran patrones de difracción derechos. La Fig. 3. a, b y d muestran la
distribución de intensidad, de los campos de difracción de convolución grabados a
diferentes distancias, ver Tabla I, en la región de Fresnel convergente del doblete
cementado, puede observarse que el patrón de difracción está formado por franjas
elípticas con distribución tipo Bessel de suma de argumentos modulando franjas de
Young, lo cual se hace más relevante en la imagen de la Fig. 3d.

          Las imágenes de la Fig. 3c y 3e se consideran izquierdas y dan referencia del
grabado de patrones de difracción en distribución de intensidad, en la zona de Fresnel
divergente o de convolución de las transformada de Fourier, situada en el intervalo de
distancias fLD <z<∞ de la lente transformadora; se observa que cada patrón contiene
mínimos y máximos de irradiancia alternados, cuantitativamente se pueden relacionar
con los valores exactos dados por la ecuación (12), además se ve que cada patrón de

Estudos em Ciências Exatas e da Terra: Desafios, Avanços e Possibilidades II  Capítulo 7                  92
difracción está formado por franjas elípticas con distribución tipo Bessel de suma de
argumentos, modulando franjas de Young.

          Las imágenes de la Fig. 3, fueron generadas cuando los centros geométricos de
las aberturas circulares Fig. 2, se orientaron paralelos al eje x0 del plano objeto. Además,
la Fig. 3a, muestra mínimos de irradiancia centrales en cada patrón, se establece que
es más dominante la función de Bessel de orden uno en el producto con la función de
Bessel de orden cero a la distancia z=22cm de propagación. Mientras que a la distancia
de propagación z=23cm y z=24cm, la función de Bessel de orden cero es la dominante en
el producto dando máximos centrales de difracción, ver Figs. 3b y 3d. También se observa
que, conforme se acerca el plano de grabado a la distancia focal de 25cm de la lente
transformadora los máximos centrales en cada patrón se amplifican Fig. 3d. Respecto a
las imágenes de la Fig. 3c y 3e se consideran izquierdas, al ser grabadas en la zona de
Fresnel divergente, en ellas se observa que cada patrón contiene mínimos y máximos de
intensidad alternados en la región central.

             Tabla I. Distancia objeto lente y lente plano de grabado, centros geométricos paralelos al eje x0.

Figura 3. a, b, c, d y e, patrones de difracción obtenidos experimentalmente grabados en la región de Fresnel
convergente y divergente de un doblete cementado.

Estudos em Ciências Exatas e da Terra: Desafios, Avanços e Possibilidades II  Capítulo 7                         93
          La Fig. 4a, 4b muestran la distribución de intensidad, de los campos de difracción
de convolución grabados a diferentes distancias de la lente transformadora ver Tabla
II, cuantitativamente los podemos relacionar con los valores exactos dados por la
ecuación (11) y se consideran derechos, en la región de Fresnel (convergente) del doblete
cementado, puede observarse que el patrón de difracción está formado por franjas
elípticas con distribución tipo Bessel modulando franjas de Young. Las imágenes de la Fig.
4a y 4b, fueron generadas cuando los centros geométricos de las aberturas circulares
figura 2, se orientaron paralelas al eje y0 del plano objeto. La imagen de la Fig. 4a, muestra
un máximo y un mínimo de irradiancia centrales en cada patrón, se establece que en el
patrón superior es más dominante la función de Bessel de orden cero que la función
de Bessel de orden uno, en el producto con la función de Bessel a la distancia z=20cm;
mientras que en el patrón de difracción inferior es dominante la función de Bessel de
orden uno más que la de orden cero en el producto de acuerdo con la ecuación (11). A
la distancia de propagación z=24cm, la función de Bessel de orden cero es la dominante
en el producto generando máximos centrales de difracción ver Fig. 4b. Se observa que
conforme se acerca el plano de grabado a la distancia focal de la lente transformadora
los máximos centrales en cada patrón de difracción se amplifican.

          Mientras que la imagen del patrón de difracción de la Fig. 4c se considera izquierdo
y fue grabada en la zona de Fresnel (divergente) o de convolución de la lente transformadora;
se observa que cada patrón contiene mínimos y máximos de irradiancia alternados en su
parte central, puede distinguir en la figura 4c, que el patrón de difracción está formado por
franjas elípticas con distribución tipo Bessel modulando franjas de Young.

Figura 4. a), b), c) Patrones de difracción obtenidos experimentalmente y grabados en la región de Fresnel
convergente y divergente del lente doblete cementado.

Estudos em Ciências Exatas e da Terra: Desafios, Avanços e Possibilidades II  Capítulo 7                    94
Tabla II. Distancia objeto lente y lente plano de grabado, centros geométricos paralelos al eje y0.

5 SIMULACIÓN

          La simulación computacional permite de una forma visual y práctica validar
los resultados del modelo matemático de difracción, en este caso empleamos el
método numérico “Beam Propagation Method”, que es una herramienta computacional
ampliamente utilizada en óptica, y es una técnica numérica viable para el cálculo de haces
ópticos en propagación libre, con pequeñas o nulas variaciones en el índice de refracción
(Schmidt, 2010).

          El algoritmo se implementó en el software matemático MatLab, para emular
la propagación del haz laser de onda plana con longitud de onda de 632 nm, por dos
aberturas circulares de radios de diferentes magnitudes de a1= 1.0 mm y a2 = 1.5mm
respectivamente, tomadas como objeto difractor. Se construyo una malla de 60×60 mm,
considerando 975 muestras tanto para el eje x, como para el eje y. La distancia entre los
centros de las dos aberturas es de 7 mm.

          Una lente es un objeto de fase, para emular un doblete acromático y cementado,
consideramos un retardo de fase entregado por una lente esférica perfecta convergente
con una longitud focal de 25 cm. El objeto difractor se colocó a la distancia fija d0= 25 cm,
que es equivalente a la distancia focal frontal del doblete cementado. Los diferenciales en
el eje de propagación z son dz = 20 mm.

          Para cada valor diferencial dz se obtuvo una gráfica de intensidad del haz
óptico difractado, guardando las imágenes presentadas en la Fig. 5a, 5b, 5c, 5d y 5e
correspondientes a las mismas distancias z a las que se tomaron las fotografías de la
Fig. 3 en la parte experimental, ver Tabla I, dentro de la zona de Fresnel convergente;
así como las del caso de la zona de Fresnel divergente del doblete cementado; además,
para este caso de simulación también se consideró que los centros geométricos de
las aberturas fueron orientados en el eje x0. Para el caso de los centros geométricos
paralelos al eje y0 se obtuvo una gráfica de intensidad del haz óptico difractado,
guardando las imágenes simuladas, las cuales se muestran en la Fig. 6a, 6b y 6c, y
corresponden a las mismas distancias z a la lente de acuerdo con la Tabla II, a las que se

Estudos em Ciências Exatas e da Terra: Desafios, Avanços e Possibilidades II  Capítulo 7             95
tomaron las imágenes en la etapa experimental, tanto en la zona de Fresnel convergente
y divergente del doblete cementado.

Figura 5. a, b, c, d y e. Gráficas de intensidad de un haz de luz, producidas grabadas mediante simulación
computacional.

Figura 6. a, b y c. Graficas de intensidad de un haz de luz, producidas grabadas mediante simulación computacional.

          En lo que respecta a las imágenes de la Fig. 7a y 7b, ellas fueron producidas y
grabadas de forma experimental en el plano focal, de Fraunhofer o de la transformada de
Fourier, situado a la distancia z=25cm de la lente doblete cementado o transformadora. La
imagen de la Fig. 7a corresponde al patrón de difracción de franjas elípticas, producido
por las dos aberturas circulares cuyos centros de curvatura estuvieron orientados en
el eje x0 del plano objeto, modulando franjas verticales de Young. Por la forma en que la
lente hace converger la información, las franjas elípticas de máxima y mínima intensidad,
quedan orientadas hacia el eje v en el espacio de frecuencias espaciales. La imagen de

Estudos em Ciências Exatas e da Terra: Desafios, Avanços e Possibilidades II  Capítulo 7                             96
la Fig. 7b, muestra el patrón de difracción de transformada de Fourier, producido por el
mismo par de aberturas circulares, con centros de curvatura paralelos ahora hacia el eje
y0 del plano objeto, en este caso las franjas elípticas están orientadas hacia el eje u en el
espacio de frecuencias espaciales, también modulando franjas horizontales de Young.

          En la Fig. 7. c) y d) se muestran los patrones de difracción simulados de
transformada de Fourier, obtenidos en el plano focal o de Fraunhofer de la lente, las
líneas de difracción de Young son bastante claras y bien definidas, y se aprecia su
orientación horizontal y vertical. En tanto que las franjas de Bessel se distribuyen como
las obtenidas de forma experimental ver Fig. 7a y 7b; es decir, las franjas de mínima y de
máxima intensidad son elípticas, como lo predijeron Zárate et al (2013).

Figura 7 a, b. Patrones de difracción de transformada Fourier generados y grabados experimentalmente. Mientras
que los de las figuras c y d, fueron generadas mediante simulación en computadora.

Estudos em Ciências Exatas e da Terra: Desafios, Avanços e Possibilidades II  Capítulo 7                        97
El Teorema de rotación publicado por Bracewell (2002), estableció que: Si una

función f (x, y) es rotada en el plano xy, entonces su transformada de Fourier g(u,v) es

rotada en el plano de frecuencias espaciales uv a través del mismo ángulo y en el mismo

sentido. En base al teorema antes referido basta establecer que la transformada de

Fourier es sensible a rotación, con lo cual se establece que los patrones de difracción

mostrados en las Figs. 7a y 7b no son iguales, es decir, tienen distribución tipo Bessel y

son de geometría elíptica, en el primer patrón de difracción el semieje mayor está en la

dirección del eje de las frecuencias espaciales v, mientras que en el segundo patrón de

difracción el semieje mayor está en la dirección de eje de frecuencias espaciales u, en

base a que las aberturas circulares, ha sufrido una rotación de               respecto del eje x0 en
el plano objeto.

6 CONCLUSIONES

          Los modelos matemáticos de convolución de transformadas de Fourier
ecuaciones (11) y (12), permiten establecer que las funciones de Bessel de orden uno
son las dominantes en los productos para generar los mínimos de la figura 3a; mientras
que las funciones de Bessel de orden cero son dominantes para generar los máximos de
irradiancia central ver Figs. 3b, 3d y 4b. Por lo que se refiere a las Figs. 3c, 3e, 4a y 4c se
observa que a las distancias que se grabaron ver Tablas 1 y 2, se alternan tanto la función
de Bessel de orden uno, como la de orden cero en los productos, para producir de manera
simultánea un mínimo y un máximo de irradiancia centrales.

          Es de importancia documentar el desfase de que sufren las ondas difractadas,
al propagarse desde el plano objeto hasta la zona de Fresnel convergente del doblete
cementado usado como lente transformadora. Mientras que, al propagarse el campo
difractado hasta la zona de Fresnel divergente de la lente transformadora, sufre un desfase
de . Basta recordar que, Zárate et al, (2013) publicaron que el desfase de que sufrió
el campo difractado al propagarse desde el plano objeto hasta el plano en la zona de
Fraunhofer, de enfoque o de la transformada de Fourier de la lente transformadora. Esto
permite concluir que el campo de difracción al propagarse se desfasa de acuerdo con la
zona en el que se desea grabar su distribución de intensidad.

          Se observa de la Figs. 4b y 4c que, conforme esté el plano de grabado o de
Fresnel convergente o divergente, próximas al plano de enfoque o de Fraunhofer, también
conocido como el plano de la transformada de Fourier, los resultados de tipo experimental
mostrados, así como los mostrados en las Figs. 7a y 7b refuerzan, lo publicado por Zárate
et al, (2013) en lo referente a las imágenes de transformada de Fourier, en ellas se hace
evidente la forma elíptica del patrón de difracción.

Estudos em Ciências Exatas e da Terra: Desafios, Avanços e Possibilidades II  Capítulo 7              98
REFERENCIAS BIBLIOGRÁFICAS
Andrés Zárate, E. (2011). Estudio de Patrones de Difracción, en la Evaluación de Aberturas [Tesis de
doctorado]. INAOE.

Andrés Zárate, E., Angulo Córdova, Q., Hernández Nolasco, J. A., Gutiérrez Tepach, G., & Treviño
Palacios, C. G. (2013). Elliptical Bessel-like Diffraction Pattern Produced by Circular Apertures with
Different Radius. Proceedings of SPIE - The International Society for Optical Engineering, 8785, 1-6.

Bracewell, R. N. (2002). The Fourier transform and its applications. McGraw Hill.

Gaskill, J. D. (1978). Linear Systems, Fourier Transforms, and Optics. John Wiley & Sons.

Goodman, J. W. (2005). Introduction to Fourier Optics (3.a ed.). McGraw Hill.

Hayek, S. I. (2001). Advanced mathematica methods in science and engineering. Marcel Dekker.

Martínez-Niconoff, G., Muñoz-Lopez, J., & Méndez-Martínez, E. (2001). Description of phase
singularities and their application to focusing design. Journal of the Optical Society of America. A,
Optics, Image Science, and Vision, 18(9), 2089-2094.

Quintero, O., Barrera, J. F., Henao, R., & Medina, F. F. (2006). Prevailing effects of interference or
diffraction by multiple apertures. Optics Communications, 266(2), 558-561.

Schmidt, J. D. (2010). Numerical simulation of optical wave propagation: With examples in MATLAB.
SPIE PRESS.

Sheppard, C. J. R., & Hrynevych, M. (1992). Diffraction by a circular aperture: A generalization of
Fresnel diffraction theory. JOSA A, 9(2), 274-281.

Estudos em Ciências Exatas e da Terra: Desafios, Avanços e Possibilidades II  Capítulo 7                99
       SOBRE O ORGANIZADOR
                  Alireza Mohebi Ashtiani possui graduação em bacharelado em Matemática,

       Matemática Aplicada, pela Amirkabir University of Technology (Polytechnic of Tehran),
       Teerã/Irã (2003), mestrado em Matemática Aplicada pelo Institute for Advanced Studies
       in Basic Siences (IASBS), Zanjan/Irã (2005) e doutorado em Engenharia Elétrica pela
       Universidade Estadual de Campinas (UNICAMP) na área de Automação (2012). Foi bolsista
       de Pós-doutorado Júnior do CNPq no Instituto de Matemática, Estatística e Computação
       Científica (IMECC/UNICAMP) e bolsista de Pós-doutorado da Fundação de Amparo à
       Pesquisa do Estado de São Paulo (FAPESP) na Faculdade de Ciências Aplicadas da
       Universidade Estadual de Campinas (FCA/UNICAMP). Desde 2013 é docente vinculado
       ao Departamento Acadêmico de Matemática do Campus Londrina da Universidade
       Tecnológica Federal do Paraná (UTFPR), e atualmente, docente permanente do Programa
       de Pós-Graduação em Matemática em Rede Nacional (PROFMAT) da UTFPR, Campus
       Cornélio Procópio.

                                                                                                   Alireza Mohebi Ashtiani
                                                                           http://lattes.cnpq.br/5025709771742662

Estudos em Ciências Exatas e da Terra: Desafios, Avanços e Possibilidades II Sobre o Organizador 112
ÍNDICE REMISSIVO

A
Agricultural land consolidation 56, 57, 58, 59, 61, 62, 63
B
Boundary conditions 64, 65, 69, 70, 72, 74, 80, 81
C
Climatología 100, 102, 109, 110
Convolución 85, 86, 89, 92, 94, 98
D
Danos 15, 16, 27
Deslizamentos 15, 16, 18, 19, 20, 21, 24
Difracción 85, 86, 87, 89, 91, 92, 93, 94, 95, 96, 97, 98, 99
E
Effective diffusivity 65, 66, 67, 69, 79, 82
Espacial 33, 39, 87, 88, 100, 102, 109, 110
F
Feições erosivas 1, 2, 7, 9, 10, 12, 13
Fresnel convergente y divergente 85, 86, 87, 91, 93, 94, 96
Fulguración 100, 102, 104, 106, 109
G
Geotecnia 13, 15, 26
H
Hollow spherical foods 65, 81
I
Inundação urbana 27, 38, 39
Ionosonda 100, 104

Estudos em Ciências Exatas e da Terra: Desafios, Avanços e Possibilidades II  Índice Remissivo  113
L

Land market 56, 57, 60, 61, 62

M

Magnetómetro 100
Mass diffusion 65
Mathematical model 64, 65, 66, 81, 86
Metodologia 7, 17, 27, 31, 36, 37, 50, 65
Movimentos de massa 1, 10, 11, 12, 15, 16, 18, 20, 23, 24

P

Paleocanais 47, 48, 50, 51, 52, 53, 54

Q

Quaternário 47, 48, 50, 52, 53, 54

R

Rent regulation 56
Republic of Kalmykia 56, 61, 63
Riometro 100, 107, 108, 109, 110
Risco 5, 7, 20, 26, 27, 28, 30, 33, 36, 38, 39, 40, 41, 42, 45
Riscos geológicos 15
Russia 56, 57, 58, 59, 62, 63

S

Simulación computacional 85, 86, 95, 96
Sísmica de alta resolução 47
Sol 100

U

Uso e ocupação do solo 1, 10, 11, 36

V

Variações Eustáticas 47, 48, 49, 52, 53, 54

Estudos em Ciências Exatas e da Terra: Desafios, Avanços e Possibilidades II  Índice Remissivo  114
