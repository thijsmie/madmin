template = R"""
\documentclass[a4paper]{article}
\usepackage{graphicx}
\usepackage{marvosym}
\usepackage{ifthen}
\usepackage[utf8]{inputenc}

\newcommand{\euro}{\EUR\ }
\newcommand{\ibannetje}{NL19 ABNA 0448 1916 28}

\usepackage[dutch]{babel}
\pagestyle{empty}

\textwidth = 13cm

\date{}

\begin{document}
\flushright
\includegraphics[width=5cm]{olympuslogo} \\

Heyendaalseweg 135\\
6525 AJ\ Nijmegen \\
olympus@science.ru.nl \\
Bank: \ibannetje
\flushleft

\begin{tabular}{l l}
\textit{Vereniging:} & %(vereniging)s \\
\textit{Factuurnummer:} & %(factuurnummer)s  \\
\textit{Factuurdatum:} & %(factuurdatum)s  \\
\textit{Afnamedatum:} & %(afnamedatum)s  \\
\textit{Verantwoordelijke:} & %(verantwoordelijke)s \\
\textit{Speciale saldo:} & %(speciaalsaldo)s \\
\end{tabular}

\vspace{1cm}

\begin{tabular}{p{6cm} c c r r}
\emph{Specificatie} & \emph{Aantal} & \emph{Stukprijs} & \emph{Prijs} \\
\hline
%(factuurregels)s
\hline
{\bf Totaal:} & & & \euro %(totaal).2f \\
\end{tabular}
\vspace{0.3cm}

Na deze factuur bedraagt het borrelsaldo nog \EUR %(borrelsaldo).2f, en het speciale saldo nog \EUR %(speciaalsaldona).2f. Extra borrelsaldo kan overgemaakt worden naar rekeningnummer \ibannetje\ t.n.v. Olympus te Nijmegen.

\vfill

\begin{tabular}{p{14cm}}
\hline
\end{tabular}

\begin{center}
\footnotesize
Olympus - Koepel van studieverenigingen van de Faculteit NWI te Nijmegen\\
Rekeningnummer \ibannetje\ t.n.v. Olympus te Nijmegen
\end{center}
\end{document}
"""
