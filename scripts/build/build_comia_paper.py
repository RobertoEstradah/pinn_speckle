"""
Genera paper/paper_comia_roberto_hernandez_estrada.zip
Adapta el paper original (biblatex/XeLaTeX) al formato LNCS/COMIA
(pdfLaTeX + BibTeX + splncs04).

Uso:
    python scripts/build_comia_paper.py

Requisitos:
    paper/paper_maestria_roberto_hernandez_estrada.zip
    master_supporting_docs/supporting_papers/LaTeX2e+Proceedings+Templates+download.zip
"""
import zipfile, re, os, shutil

# ── Rutas ──────────────────────────────────────────────────────────────────
PAPER_ZIP = r'D:\Tesis_Maestria\paper\paper_maestria_roberto_hernandez_estrada.zip'
TPL_ZIP   = (r'D:\Tesis_Maestria\master_supporting_docs\supporting_papers'
             r'\LaTeX2e+Proceedings+Templates+download.zip')
BUILD_DIR = r'D:\Tesis_Maestria\paper\comia_build'
OUT_ZIP   = r'D:\Tesis_Maestria\paper\paper_comia_roberto_hernandez_estrada.zip'

# ── Mapa \citet{key} → "Autor et al.~\cite{key}" ──────────────────────────
CITET_MAP = {
    'Raissi2019_PINNs':          'Raissi et al.',
    'Sitzmann2020_SIREN':        'Sitzmann et al.',
    'Karniadakis2021_review':    'Karniadakis et al.',
    'Cuomo2022_review':          'Cuomo et al.',
    'Schoder2024_PINN_acoustics':'Schoder y Kraxberger',
    'Wang2021_failurePINNs':     'Wang et al.',
    'Thuerey2021_PBDL':          'Thuerey et al.',
    'Baydin2018_autodiff':       'Baydin et al.',
    'Chen2020_nanoptics':        'Chen et al.',
    'Fang2020_scattering':       'Fang y Zhan',
    'Jin2014_FEM':               'Jin',
    'Mckay1979_LHS':             'McKay et al.',
    'Goodman2007_Speckle':       'Goodman',
}

# ── Contenido embebido de main.tex (LNCS) ─────────────────────────────────
MAIN_TEX = r"""% ============================================================
%  Simulacion acelerada de speckle optico — Version COMIA/LNCS
%  Roberto Hernandez Estrada | UJAT — DACYTI | Jun 2026
%
%  Compilar en Overleaf: compilador pdfLaTeX.
%  Bibliografia: BibTeX + splncs04.bst
% ============================================================
\documentclass[runningheads]{llncs}

% --- Codificacion y babel ---
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage[spanish,es-tabla]{babel}

% --- Graficas ---
\usepackage{graphicx}
\graphicspath{{figures/}}

% --- Matematicas ---
\usepackage{amsmath, amssymb, amsfonts, mathtools}
\DeclareMathOperator*{\argmin}{arg\,min}

% --- Tablas ---
\usepackage{booktabs}
\usepackage{array}
\usepackage[flushleft]{threeparttable}

% --- Tipografia ---
\usepackage{microtype}
\usepackage{float}
\usepackage{subcaption}
\usepackage{xurl}

% --- Hyperref (penultimo) ---
\usepackage[hidelinks]{hyperref}

% --- Cleveref (ultimo) ---
\usepackage[nameinlink,spanish]{cleveref}
\crefname{section}{secci\'{o}n}{secciones}
\Crefname{section}{Secci\'{o}n}{Secciones}
\crefname{table}{tabla}{tablas}
\Crefname{table}{Tabla}{Tablas}
\crefname{figure}{figura}{figuras}
\Crefname{figure}{Figura}{Figuras}
\crefname{equation}{ecuaci\'{o}n}{ecuaciones}
\Crefname{equation}{Ecuaci\'{o}n}{Ecuaciones}

% ============================================================
\begin{document}
% ============================================================

\title{Simulaci\'{o}n acelerada de speckle \'{o}ptico mediante
       Redes Neuronales Informadas por F\'{i}sica con activaci\'{o}n
       sinusoidal%
       \thanks{Este trabajo forma parte de la tesis de maestr\'{i}a
               del primer autor, desarrollada en el programa de
               Maestr\'{i}a en Ciencias de la Computaci\'{o}n de la
               Universidad Ju\'{a}rez Aut\'{o}noma de Tabasco (UJAT),
               bajo la direcci\'{o}n del
               Dr.~Jos\'{e} Ad\'{a}n Hern\'{a}ndez Nolasco.}}

\titlerunning{PINN-SIREN para simulaci\'{o}n de speckle \'{o}ptico}

\author{Roberto Hern\'{a}ndez Estrada\inst{1} \and
        Jos\'{e} Ad\'{a}n Hern\'{a}ndez Nolasco\inst{1}}

\authorrunning{R. Hern\'{a}ndez Estrada y
               J.\,A. Hern\'{a}ndez Nolasco}

\institute{Divisi\'{o}n Acad\'{e}mica de Ciencias y
           Tecnolog\'{i}as de la Informaci\'{o}n (DACYTI),\\
           Universidad Ju\'{a}rez Aut\'{o}noma de Tabasco (UJAT),\\
           Villahermosa, Tabasco, M\'{e}xico\\
           \email{robertohernandezestrd@gmail.com}}

\maketitle

% ====== Abstract en ingles (requerido por LNCS) ======
\begin{abstract}
Physics-Informed Neural Networks with sinusoidal activation functions
(SIREN-PINNs) are applied to solve the 2D scalar Helmholtz equation
as a mesh-free surrogate for optical speckle simulation.
The proposed SIREN architecture ($5\times128$, $\omega_0=1.0$) achieves
relative $L^2$ errors of $0.006\,\%$ (1D) and $0.171\,\%$ (2D) against
analytical solutions, outperforming the state of the art by factors of
$\times\!415$ and $\times\!11.2$, respectively.
A two-phase Adam\,+\,L-BFGS optimization strategy and Latin Hypercube
Sampling (LHS) are key to convergence and accuracy.
Multi-seed validation ($\mathrm{SEED}\in\{42,123,777\}$) confirms
statistical robustness with an inter-seed $L^2$ variance of $13\,\%$
(relative).
These results establish SIREN-PINNs as a precise and stable solver for
the scalar Helmholtz equation, laying the foundation for physically
accurate optical speckle generation.

\keywords{Physics-Informed Neural Networks \and SIREN \and
          Helmholtz equation \and optical speckle \and
          Latin Hypercube Sampling}
\end{abstract}

% ====== Resumen en espanol ======
\section*{Resumen}
\noindent
Se presenta una implementaci\'{o}n de Redes Neuronales Informadas por
F\'{i}sica con activaci\'{o}n sinusoidal (PINN-SIREN) para la
resoluci\'{o}n de la ecuaci\'{o}n de Helmholtz bidimensional con campo
el\'{e}ctrico complejo, en un paradigma libre de malla
(\textit{mesh-free}) orientado a la simulaci\'{o}n acelerada de
fen\'{o}menos \'{o}pticos.
La arquitectura SIREN propuesta ($5\times128$ neuronas, $\omega_0=1.0$)
alcanza errores $L^2$ de $0.006\,\%$ en el caso 1D y $0.171\,\%$ en el
caso 2D respecto a soluciones anal\'{i}ticas, superando al estado del
arte en factores de $\times\!415$ y $\times\!11.2$, respectivamente.
La validaci\'{o}n multi-semilla ($\mathrm{SEED}\in\{42,123,777\}$)
confirma la robustez estad\'{i}stica del m\'{e}todo.
La generaci\'{o}n de patrones de speckle con condici\'{o}n de frontera
de fase aleatoria $\phi(x)\sim\mathcal{U}(0,2\pi)$ constituye el
siguiente paso planificado de esta investigaci\'{o}n.

\noindent\textbf{Palabras clave:} Redes Neuronales Informadas por
F\'{i}sica, SIREN, ecuaci\'{o}n de Helmholtz, speckle \'{o}ptico,
activaci\'{o}n sinusoidal, muestreo por hip\'{e}rcubo latino.

% ============================================================
% Cuerpo del articulo
% ============================================================
\input{sections/01_introduccion}
\input{sections/02_marco_teorico}
\input{sections/03_metodologia}
\input{sections/04_resultados}
\input{sections/05_conclusiones}

% ============================================================
% Bibliografia
% ============================================================
\bibliographystyle{splncs04}
\bibliography{references}

\end{document}
"""

# ── Función de conversión de citas ─────────────────────────────────────────

def adapt_citations(content):
    """Convierte comandos biblatex a BibTeX estándar."""
    bs = '\\'
    for key, author in CITET_MAP.items():
        old = bs + 'citet{' + key + '}'
        new = author + '~' + bs + 'cite{' + key + '}'
        content = content.replace(old, new)
    # \citep{...} -> \cite{...}
    content = content.replace(bs + 'citep{', bs + 'cite{')
    # naked \ref{sec:conclusiones} -> \cref
    content = content.replace(bs + 'ref{sec:conclusiones}',
                               bs + 'cref{sec:conclusiones}')
    return content


# ── Pipeline principal ─────────────────────────────────────────────────────

def main():
    # 1. Preparar directorio de construcción
    if os.path.exists(BUILD_DIR):
        shutil.rmtree(BUILD_DIR)
    os.makedirs(os.path.join(BUILD_DIR, 'figures'))
    os.makedirs(os.path.join(BUILD_DIR, 'sections'))

    # 2. llncs.cls + splncs04.bst desde plantilla LNCS
    with zipfile.ZipFile(TPL_ZIP) as z:
        for fn in ['llncs.cls', 'splncs04.bst']:
            with open(os.path.join(BUILD_DIR, fn), 'wb') as f:
                f.write(z.read(fn))
    print('Plantilla LNCS extraída (llncs.cls, splncs04.bst)')

    # 3. Figuras desde paper original
    with zipfile.ZipFile(PAPER_ZIP) as z:
        for fn in z.namelist():
            if fn.startswith('figures/') and fn.endswith('.png'):
                out = os.path.join(BUILD_DIR, 'figures', os.path.basename(fn))
                with open(out, 'wb') as f:
                    f.write(z.read(fn))
    print('Figuras copiadas')

    # 4. references.bib sin modificar
    with zipfile.ZipFile(PAPER_ZIP) as z:
        with open(os.path.join(BUILD_DIR, 'references.bib'), 'wb') as f:
            f.write(z.read('references.bib'))
    print('references.bib copiado')

    # 5. main.tex embebido
    with open(os.path.join(BUILD_DIR, 'main.tex'), 'w', encoding='utf-8') as f:
        f.write(MAIN_TEX)
    print('main.tex escrito')

    # 6. Secciones con citas adaptadas
    with zipfile.ZipFile(PAPER_ZIP) as z:
        for sec in ['01_introduccion', '02_marco_teorico', '03_metodologia',
                    '04_resultados', '05_conclusiones']:
            raw = z.read(f'sections/{sec}.tex').decode('utf-8')
            adapted = adapt_citations(raw)
            out = os.path.join(BUILD_DIR, 'sections', f'{sec}.tex')
            with open(out, 'w', encoding='utf-8') as f:
                f.write(adapted)
            n_citet = raw.count('\\citet{')
            n_citep = raw.count('\\citep{')
            print(f'  {sec}: {n_citet} \\citet + {n_citep} \\citep -> \\cite')
    print('Secciones adaptadas')

    # 7. Crear ZIP final
    if os.path.exists(OUT_ZIP):
        os.remove(OUT_ZIP)
    with zipfile.ZipFile(OUT_ZIP, 'w', zipfile.ZIP_DEFLATED) as zout:
        for root, _, files in os.walk(BUILD_DIR):
            for fn in files:
                filepath = os.path.join(root, fn)
                arcname  = os.path.relpath(filepath, BUILD_DIR).replace('\\', '/')
                zout.write(filepath, arcname)

    size_kb = os.path.getsize(OUT_ZIP) / 1024
    print(f'\nZIP final: {OUT_ZIP}')
    print(f'Tamaño  : {size_kb:.1f} KB')
    print('\nContenido:')
    with zipfile.ZipFile(OUT_ZIP) as z:
        for fn in sorted(z.namelist()):
            print(f'  {fn}')


if __name__ == '__main__':
    main()
