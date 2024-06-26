from latex import build_pdf
import os


def tm(c): # brown
    return r'\tm{' + c + r'}'


def tmb(c): # blue
    return r'\tmb{' + c + r'}'


def ntm(c, sub=None):
    if sub is None:
        return r'\ntm{' + c + r'} '
    return r'\ntm{' + c + r'_{' + id(sub) + r'}}'


def id(c):
    txt = ""
    for el in c:
        if el == "^":
            txt += r'\textasciicircum'
        elif el in ["_", "$", "%", "&", "~", "{", "}"]:
            txt += "\\"[0] + el
        elif el in ["<", ">"]:
            txt += "$" + el + "$"
        elif el == "\\"[0]:
            txt += "$\\backslash$"
        else:
            txt += el
    return txt


def tex(c):
    name = type(c).__name__
    txt = str()

    if name == "list":
        for el in c:
            txt += tmb(", ")
            txt += tex(el)
        return tmb("[") + txt[8:] + tmb("]")
    
    elif name == "tuple": # (rule_name, c)
        for el in c:
            txt += tmb(", ")
            txt += tex(el)
        return tmb("(") + txt[8:] + tmb(")")
    
    elif name == "dict":
        for el in c:
            txt += tmb(", ")
            txt += tex(el)
            txt += tmb(":")
            txt += tex(c[el])
        return tmb(r'\{') + txt[8:] + tmb(r'\}')

    elif name == "Var":
        if c.ntm == "G":
            txt = ntm(r'\Gamma', c.id)
        else:
            txt = ntm(c.ntm, c.id)
        return txt
    
    elif name == "ApplyPred":
        return id(c.id) + tm("(") + tex(c.input) + tm("$|$") + tex(c.output) + tm(")")

    elif name == "DefinePred":
        return id(c.id) + tm("(") + tex(c.input) + tm("$|$") + tex(c.output) + tm(")") + tm("`") + r'\begin{python}' + c.code + r'\end{python}' + tm("`")
    
    elif name == "Transition":
        if c.ending:
            return tm(r'$\langle$') + tex(c.c1) + tm(",") + tex(c.s1) + tm(r'$\rangle$') + r' $\to$ ' + tex(c.s2)
        return tm(r'$\langle$') + tex(c.c1) + tm(",") + tex(c.s1) + tm(r'$\rangle$') + r' $\to$ ' + tm(r'$\langle$') + tex(c.c2) + tm(",") + tex(c.s2) + tm(r'$\rangle$')
    
    elif name == "Typing":
        return tex(c.g) + r' $\vdash$ ' + tex(c.c1) + tex(c.r) + tex(c.c2)
    
    elif name == "Program":
        for p in c.lst:
            txt += r'~\\\\'
            txt += tex(p)
            txt += "\n"
        return txt[5:]
    
    elif name == "Block":
        return r'\begin{quote}' + tm(r'\{ \\') + tex(c.p) + tm(r'\\ \}') + r'\end{quote}'
    
    elif name == "Rs":
        for option in c.inneroptions:
            txt += r' $|$'
            for el in option:
                txt += r' '
                if el[0] not in ['/', '"']:
                    txt += ntm(el)
                else:
                    txt += tex(el)
        return id(c.name_id) + r':  ' + ntm(id(c.id)) + r' ::= ' + txt[5:] + r'\\'
    
    elif name == "Ro":
        for el in c.uo:
            txt += r'\\'
            txt += tex(el)
        return r'\osr{' + id(c.name_id) + r'}' + \
            r'{' + txt[2:] +  r'}{' + tex(c.tr) +  r'}\\'

    elif name == "Rt":
        for el in c.ut:
            txt += r'\\'
            txt += tex(el)
        return r'\osr{' + id(c.name_id) + r'}' + \
            r'{' + txt[2:] +  r'}{' + tex(c.ty) +  r'}\\'

    elif name == "Code":
        return tex(c.rsp)
    
    elif name == "Breakpoint":
        return r'\textcolor{red}{B-' + id(c.id) + r'}'
    
    elif name == "int":
        return r'$' + str(c) + r'$'

    else: # str
        if c is None:
            return "None"
        return id(c)


def gen_tex(c):
    context = r'''\makeatletter
\documentclass{article}
\usepackage[a4paper, total={6in, 8in}, margin=0.2in]{geometry}
\usepackage{graphicx} % Required for inserting images
\usepackage{amssymb}
\usepackage{amsbsy}
\usepackage{xcolor}
\usepackage{listings}
\usepackage{multicol}
\usepackage{parskip}
\newcommand{\bound}[1]{\rceil {#1} \lceil}

\definecolor{battleshipgrey}{rgb}{0.52, 0.52, 0.51}

\newcommand{\com}[1]{\textcolor{battleshipgrey}{\hfill\llap{\hspace*{1em}{#1}}}}

\newcommand{\tm}[1]{\textcolor{brown}{#1}}
\newcommand{\tmb}[1]{\textcolor{blue}{#1}}
\newcommand{\ntm}[1]{\colorbox{blue!30}{$#1$}}

\newcommand{\srbegin}[3]{
    \ntm{#1} $\in$ {#2} ::= {#3} % symbol + syntax category + first el of rule
    \snextel
} % syntax rule
\newcommand{\srend}{}
\newcommand{\srel}[1]{{#1} \snextel} % syntax element
\newcommand{\snextel}{\@ifnextchar{\srend}{}{$|$ \srel}}

\newcommand{\osr}[3]{
\begin{tabular}{ c }
 #2 \\
 \hline
 #3
\end{tabular}~{\tiny #1}
}

% https://tex.stackexchange.com/questions/83882/how-to-highlight-python-syntax-in-latex-listings-lstinputlistings-command
% Default fixed font does not support bold face
\DeclareFixedFont{\ttb}{T1}{txtt}{bx}{n}{8} % for bold
\DeclareFixedFont{\ttm}{T1}{txtt}{m}{n}{8}  % for normal

% Custom colors
\definecolor{deepblue}{rgb}{0,0,0.5}
\definecolor{deepred}{rgb}{0.6,0,0}
\definecolor{deepgreen}{rgb}{0,0.5,0}

% Python style for highlighting
\newcommand\pythonstyle{\lstset{
language=Python,
basicstyle=\ttm,
morekeywords={self},              % Add keywords here
keywordstyle=\ttb\color{deepblue},
emph={MyClass,__init__},          % Custom highlighting
emphstyle=\ttb\color{deepred},    % Custom highlighting style
stringstyle=\color{deepgreen},
frame=tb,                         % Any extra options here
showstringspaces=false
}}


% Python environment
\lstnewenvironment{python}[1][]
{
\pythonstyle
\lstset{#1}
}
{}

\title{Semantics}
\author{m.brojek2 }
\date{January 2024}

\begin{document}
''' + tex(c) + r'''
\end{document}
'''
    
    dirname = os.getcwd()
    os.chdir(os.path.join(dirname, "tmp"))

    with open("tmp_convert.tex", "w") as tmp_tex:
        tmp_tex.write(context)

    pdf = build_pdf(context)
    pdf.save_to("tmp_convert.pdf")
    os.chdir(dirname)