%
% Este archivo se realiza modificando algunos fragmentos de
% la clase standard article. Requiere esta clase para ser
% empleado.
%
% Autor : Luis Sierra
% A pedido de : la organizacion del CLEI 2002
% Requiere : LaTeX2e y la clase estandar article
% modificaciones posteriores para cleiej: H�ctor Cancela

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{cleiej}[2011/01/25, para CLEIej - basado en clei.cls 2002/06/21 Desarrollado para el CLEI 2002]

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Opciones de la clase
% resumen : propia de esta clase
% leqno, fleqn, openbib, final, draft : como en article
%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% booleana resumen: empleada para realizar el newpage de la 
% primer carilla
%
\newif\if@resumen
\@resumenfalse
\DeclareOption{resumen}{%
      \@resumentrue%
   }

\DeclareOption{leqno}{%
      \PassOptionsToClass{\CurrentOption}{article}%
   }
\DeclareOption{fleqn}{%
      \PassOptionsToClass{\CurrentOption}{article}%
   }
\DeclareOption{openbib}{%
      \PassOptionsToClass{\CurrentOption}{article}%
   }
\DeclareOption{final}{%
      \PassOptionsToClass{\CurrentOption}{article}%
   }
\DeclareOption{draft}{%
      \PassOptionsToClass{\CurrentOption}{article}%
   }
\DeclareOption*{%
   \PackageWarning{clei}{Opci\'on desconocida `\CurrentOption'}%
}
\ProcessOptions\relax

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% REQUERIMIENTO 2 : a4paper
% REQUERIMIENTO 3 : 10pt
% REQUERIMIENTO 3.3 : onecolumn
\LoadClass[10pt,a4paper,oneside,notitlepage,onecolumn]{article}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% REQUERIMIENTO 2 : margenes
% para impresora sin duplex
%
\setlength{\evensidemargin}{-0.04cm}
\setlength{\oddsidemargin}{-0.04cm}
\setlength{\textwidth}{16.5cm}
\setlength\@tempdima{-0.54cm}
%\addtolength\@tempdima{-\topmargin}
\addtolength\@tempdima{-\headheight}
\addtolength\@tempdima{-\headsep}
\addtolength\topmargin{\@tempdima}
\setlength{\textheight}{25.2cm}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% REQUERIMIENTO : acerca del titulo 
%
\renewcommand\maketitle{\par
  \begingroup
    \renewcommand\thefootnote{\@fnsymbol\c@footnote}%
    \def\@makefnmark{\rlap{\@textsuperscript{\normalfont\@thefnmark}}}%
    \long\def\@makefntext##1{\parindent 1em\noindent
            \hb@xt@1.8em{%
                \hss\@textsuperscript{\normalfont\@thefnmark}}##1}%
      \newpage
      \global\@topnum\z@   % Prevents figures from going at top of page.
      \@maketitle
      \@thanks % REQUERIMIENTO 2: numeracion
%    \thispagestyle{empty}\@thanks % REQUERIMIENTO 2: numeracion
  \endgroup
  \setcounter{footnote}{0}%
  \global\let\thanks\relax
  \global\let\maketitle\relax
  \global\let\@maketitle\relax
  \global\let\@thanks\@empty
  \global\let\@author\@empty
  \global\let\@date\@empty
  \global\let\@title\@empty
  \global\let\title\relax
  \global\let\author\relax
  \global\let\date\relax
%  \global\let\and\relax
}
\def\@maketitle{%
  \newpage
  \null
  \vskip 2em%
  \begin{center}%
  \let \footnote \thanks
    % REQUERIMIENTO 3.1 : fuente del titulo
    {\bfseries \fontsize{16}{20} \selectfont \@title \par}%
    \vskip 1.5em%
    {\large   % REQUERIMIENTO 3.1 : tamanio del autor
      \lineskip .5em%
      \begin{tabular}[t]{c}%
        \@author
      \end{tabular}\par}%
    \vskip 1em%
    {\large \@date}%
  \end{center}%
  \par
  \vskip 1.5em}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% REQUERIMIENTO caratula
%    sin fecha y \and modificado
\date{}
\renewcommand{\and}{ \\[1pc] and \\[1pc]}%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% REQUERIMIENTO cabezales
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{} % clear all header and footer fields
\fancyfoot[CO]{\footnotesize \thepage}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% REQUERIMIENTO 3.2 abstract y keywords
%  
\renewenvironment{abstract}{%
        \begin{center}%
	  \begin{minipage}{13.5cm}%
        \begin{center}%
 {\bfseries Abstract \vspace{-.5em}\vspace{\z@}}%
             
         \end{center}%
        }%
      {\end{minipage}%
         \end{center}%
      }
\newenvironment{resumen}{%
        \begin{center}%
          {\bfseries Resumen\vspace{-.5em}\vspace{\z@}}%
        \end{center}%
        }
      {}
\if@resumen
   \newenvironment{keywords}{%
      \par \vspace{1pc} \noindent \textbf{Keywords: }%
      }%
      {}
\else
   \newenvironment{keywords}{%
      \par \vspace{1pc} \noindent \textbf{Keywords: }%
      }%
      {\newpage}
\fi
\newenvironment{palabrasclaves}{%
   \par \vspace{1pc} \noindent \textbf{Palabras claves: }%
   }%
   {\newpage}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% REQUERIMIENTO 3.4 bibliografia
%  
\bibliographystyle{IEEEtran}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% REQUERIMIENTO 4 secciones
%  
\renewcommand\section{\@startsection {section}{1}{\z@}%
                                   {-3.5ex \@plus -1ex \@minus -.2ex}%
                                   {2.3ex \@plus.2ex}%
                                   {\normalfont\large\bfseries}}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% REQUERIMIENTO 4.1 subsecciones
%  
\renewcommand\subsection{\@startsection{subsection}{2}{\z@}%
                                     {-3.25ex\@plus -1ex \@minus -.2ex}%
                                     {1.5ex \@plus .2ex}%
                                     {\normalfont\bfseries}}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% REQUERIMIENTO 4.1.1 subsubsecciones
%  
\renewcommand\subsubsection{\@startsection{subsubsection}{3}{\z@}%
                                     {-3.25ex\@plus -1ex \@minus -.2ex}%
                                     {1.5ex \@plus .2ex}%
                                     {\normalfont\itshape}}


