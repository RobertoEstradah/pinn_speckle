%% --> Identificación de la clase
\NeedsTeXFormat{LaTeX2e}[2009/09/24]
\ProvidesClass{RMTA}[2021/10/11 v0.2]

%% RequiredPackages 
\RequirePackage{amsmath,amssymb,amsthm,amsfonts}
\RequirePackage{parskip}

\RequirePackage{nextpage}
\RequirePackage{booktabs}
\RequirePackage{multirow}


\AtBeginDocument{\urlstyle{rm}}

\RequirePackage{float}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% --- Inicialización
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\newcommand\@tituloESP{}
\newcommand\@titleENG{}
\newcommand\@runningtitle{}
\newcommand\@affiliation{}
\newcommand\@headerauthor{}
\newcommand\@email{}
\newcommand\@resumen{}
\newcommand\@abstract{}
\newcommand\@palabrasc{}
\newcommand\@keywords{}
\newcommand\@MSC{}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\DeclareOption{10pt}{\PassOptionsToClass{10pt,twoside}{article}}



\renewcommand{\baselinestretch}{1.5}

\ExecuteOptions{10pt,twoside}

\ProcessOptions\relax

\LoadClass{article}

\setlength{\parskip}{7.5pt}

\RequirePackage[colorlinks,allcolors=blue,breaklinks]{hyperref}
\usepackage{xurl}

\paperheight= 10.25in 
\paperwidth = 7.25in
\topmargin = -0.51in
\RequirePackage{enumitem}
\RequirePackage{titletoc}
\RequirePackage{titlesec}
\usepackage[T1]{fontenc} % True fonts
\usepackage{ae,aecompl}	 % Enhanced encoding for True Fonts 
\RequirePackage[style=numeric,minbibnames=10,maxbibnames = 20]{biblatex}

\RequirePackage[font={small},labelfont={bf,small}]{caption}

\RequirePackage{fancyhdr}

%%%% Special fields

\newcommand{\headerauthor}[1]{\renewcommand\@headerauthor{#1}}
\newcommand{\tituloESP}[1]{\renewcommand\@tituloESP{#1}}
\newcommand{\titleENG}[1]{\renewcommand\@titleENG{#1}}
\newcommand{\runningtitle}[1]{\renewcommand\@runningtitle{\MakeLowercase{\sc #1}}}
\newcommand{\affiliation}[1]{\renewcommand\@affiliation{#1}}
\newcommand{\email}[1]{\renewcommand\@email{\href{mailto:#1}{#1}}}
\newcommand{\resumen}[1]{\renewcommand\@resumen{\small #1}}
\newcommand{\palabrasc}[1]{\renewcommand\@palabrasc{#1}}
\renewcommand{\abstract}[1]{\renewcommand\@abstract{\small #1}}
\newcommand{\keywords}[1]{\renewcommand\@keywords{#1}}
\newcommand{\MSC}[1]{\renewcommand\@MSC{#1}}


%%% Theorem-like enviroments
\newtheorem{Theorem}{Theorem}
\newtheorem{Lemma}{Lemma}
\newtheorem{Remark}{Remark}
\newtheorem{Proposition}{Proposition}
\newtheorem{Definition}{Definition}

\newtheorem{Teorema}{Teorema}
\newtheorem{Lema}{Lema}
\newtheorem{Observacion}{Observaci\'on}
\newtheorem{Proposicion}{Proposici\'on}
\newtheorem{Definicion}{Definici\'on}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%% Titlepage
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\renewcommand\titlepage{
    \begin{center}
    \ifdefstring{\@LAN}{esp}{
    {\LARGE\sc \@tituloESP \\[1cm] \sc \@titleENG \\} 
    }{
    {\LARGE\sc \@titleENG \\[1cm] \sc \@tituloESP \\} 
    }
    \vspace{5ex}
    {\begin{tabular}[t]{c}%
        \sc\@author \\
        Email: \@email
      \end{tabular}\par}%}
    \vspace{5ex}
    \@affiliation
    \vspace{1ex}
    \hrule
    \end{center}
        
}

\newcommand{\abstractresumen}{
{\setlength{\parskip}{0.3pt}
\small
\ifdefstring{\@LAN}{esp}{
\begin{center} \textbf{Resumen}\end{center}
\begin{quote} \@resumen \end{quote}
\textbf{Palabras clave:} \@palabrasc
\begin{center} \textbf{Abstract}\end{center}
\begin{quote} \@abstract \end{quote}
\textbf{Keywords:} \@keywords
}{
\begin{center} \textbf{Abstract}\end{center}
\begin{quote} \@abstract \end{quote}
\textbf{Keywords:} \@keywords
\begin{center} \textbf{Resumen}\end{center}
\begin{quote} \@resumen \end{quote}
\textbf{Palabras clave:} \@palabrasc
}
}
\\
\\
\textbf{Mathematics Subject Classification:} \@MSC
}

\renewcommand{\thesubsection}{\arabic{section}.\arabic{subsection}} 

\setlength\evensidemargin{\oddsidemargin}


\endinput