GUION DE PRESENTACION — Segundo Avance de Tesis MCC
Roberto Hernandez Estrada | UJAT — DACYTI | Jun 2026
====================================================

CONTENIDO DEL ZIP
-----------------
  main.tex                    Documento maestro (compilar este)
  latexmkrc                   Configuracion de compilacion
  secciones/01_guion.tex      Guion por diapositiva (16:35 min total)
  secciones/02_tecnico.tex    Explicaciones tecnicas de hiperparametros
  secciones/03_preguntas.tex  15 preguntas y respuestas del comite

COMO COMPILAR
-------------
  Opcion 1 (recomendada):
    latexmk main.tex

  Opcion 2 (manual, 2 pasadas):
    pdflatex main.tex
    pdflatex main.tex

  Opcion 3 (Overleaf):
    - Subir todos los archivos manteniendo la estructura de carpetas
    - El compilador debe ser pdfLaTeX
    - Compilar main.tex

REQUISITOS
----------
  - pdfLaTeX (TeX Live 2022+ o MiKTeX 22+)
  - Paquetes: tcolorbox, booktabs, xcolor, amsmath, babel (spanish)
    (todos incluidos en TeX Live completo / MiKTeX completo)

ESTRUCTURA DEL DOCUMENTO
-------------------------
  Seccion 1: Guion por diapositiva
    - Script exacto para cada slide
    - Tiempo estimado y acumulado
    - Tips de presentacion
    - Tabla resumen de tiempos (total: ~16:35 min, margen: ~3:25 min)

  Seccion 2: Explicaciones tecnicas
    - Justificacion de cada hiperparametro NB01 y NB02
    - Razon del cambio lambda=1.0 -> 0.1
    - Por que Adam + L-BFGS, LHS, omega_0=1.0, etc.

  Seccion 3: 15 preguntas del comite
    - Perfiladas para el comite de DACYTI-UJAT
    - Respuestas de 60-90 segundos cada una
    - Tabla resumen con slide de apoyo para cada pregunta
