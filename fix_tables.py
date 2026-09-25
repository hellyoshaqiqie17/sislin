import re

with open('main.tex', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Fix Table 1: Accidental extra column & width overflow
tab1_pattern = r'\\begin\{table\}\[!t\]\s*\\caption\{Parameter Fisis.*?\\end\{table\}'
new_tab1 = r'''\begin{table}[!t]
\caption{Parameter Fisis dan Kanonik Model ASCPA~\cite{yang2026signal}}
\label{tab:parameters}
\centering
\footnotesize
\begin{tabular}{@{}llcc@{}}
\toprule
\textbf{Param.} & \textbf{Makna Fisis dalam Sistem} & \textbf{Nilai} & \textbf{Satuan} \\
\midrule
$m$ & Massa gerak (piston \& spindel) & $1{,}0$ & $\text{kg}$ \\
$c$ & Redaman viskos film udara & $6{,}0$ & $\text{N}\cdot\text{s/m}$ \\
$k$ & Kekakuan kontak \& pneumatik & $25{,}0$ & $\text{N/m}$ \\
$\omega_n$ & Frekuensi alami tak-teredam & $5{,}0$ & $\text{rad/s}$ \\
$f_n$ & Frekuensi siklis alami & $0{,}796$ & $\text{Hz}$ \\
$\zeta$ & Rasio redaman tak-berdimensi & $0{,}60$ & -- \\
$\omega_d$ & Frekuensi sudut teredam & $4{,}0$ & $\text{rad/s}$ \\
$\sigma$ & Peluruhan eksponensial ($\zeta \omega_n$) & $3{,}0$ & $\text{s}^{-1}$ \\
$K_{dc}$ & Penguatan statis DC ($1/k$) & $0{,}04$ & $\text{m/N}$ \\
$D_p$ & Diameter piston aerostatik & $20{,}0$ & $\text{mm}$ \\
$L_p$ & Panjang piston aerostatik & $30{,}0$ & $\text{mm}$ \\
$h_0$ & Rata-rata tebal film udara & $30{,}0$ & $\mu\text{m}$ \\
$P$ & Tekanan pasokan udara & $0{,}40$ & $\text{MPa}$ \\
\bottomrule
\end{tabular}
\end{table}'''

text, n1 = re.subn(tab1_pattern, lambda m: new_tab1, text, flags=re.DOTALL)
print(f'Table 1 replacements: {n1}')

# 2. Fix Table 2: Width overflow
tab2_pattern = r'\\begin\{table\}\[!t\]\s*\\caption\{Perbandingan Kinerja Dinamis Eksperimental.*?\\end\{table\}'
new_tab2 = r'''\begin{table}[!t]
\caption{Perbandingan Kinerja Dinamis Eksperimental~\cite{yang2026signal}}
\label{tab:actuator_comp}
\centering
\footnotesize
\begin{tabular}{@{}lcccc@{}}
\toprule
\textbf{Aktuator} & \textbf{Waktu (s)} & \textbf{RMSE (N)} & \textbf{IAE (N}\cdot\text{s)} & \textbf{Riak (N)} \\
\midrule
TPA (Tradisional) & $19{,}244$ & $0{,}237$ & $5{,}732$ & $0{,}046$ \\
LFPA (Gesekan Rendah) & $10{,}400$ & $0{,}097$ & $1{,}271$ & $0{,}015$ \\
\textbf{ASCPA (Usulan)} & $\mathbf{6{,}124}$ & $\mathbf{0{,}087}$ & $\mathbf{1{,}060}$ & $\mathbf{0{,}003}$ \\
\bottomrule
\end{tabular}
\end{table}'''

text, n2 = re.subn(tab2_pattern, lambda m: new_tab2, text, flags=re.DOTALL)
print(f'Table 2 replacements: {n2}')

# 3. Fix inline operator L
text = text.replace(
    r'Terapkan operator diferensial linier $\mathcal{L} = m \frac{d^2}{dt^2} + c \frac{d}{dt} + k$ terhadap respons usulan',
    r'Terapkan operator diferensial linier $\mathcal{L}$ terhadap respons usulan'
)

# 4. Embed thebibliography so citations NEVER produce [?]
new_bib = r'''\begin{thebibliography}{10}
\providecommand{\url}[1]{#1}
\csname url@samestyle\endcsname
\providecommand{\newblock}{\relax}
\providecommand{\bibinfo}[2]{#2}
\providecommand{\BIBentrySTDinterwordspacing}{\spaceskip=0pt\relax}
\providecommand{\BIBentryALTinterwordstretchfactor}{4}
\providecommand{\BIBentryALTinterwordspacing}{\spaceskip=\fontdimen2\font plus
\BIBentryALTinterwordstretchfactor\fontdimen3\font minus
  \fontdimen4\font\relax}
\providecommand{\BIBforeignlanguage}[2]{{%
\expandafter\ifx\csname l@#1\endcsname\relax
\typeout{** WARNING: IEEEtran.bst: No hyphenation pattern has been}%
\typeout{** loaded for the language `#1'. Using the pattern for}%
\typeout{** the default language instead.}%
\else
\language=\csname l@#1\endcsname
\fi
#2}}
\providecommand{\BIBdecl}{\relax}
\BIBdecl

\bibitem{yang2026signal}
Z.~Yang, Z.~Li, Y.~Niu, J.~Kou, X.~Shen, Y.~Wang, Z.~Sun, Y.~Ma, and Y.~Shi,
  ``Signal processing and force control for precision machining with grinding
  system integrating an aerostatic suspension compact pneumatic actuator,''
  \emph{Mechanical Systems and Signal Processing}, vol. 251, art. 114229, 2026.

\bibitem{cao2019modeling}
J.~Cao, X.~Zhu, F.~Li, and X.~Jin, ``Modeling and constrained optimal design of
  an ultra-low-friction pneumatic cylinder with air bearing,'' \emph{Advances
  in Mechanical Engineering}, vol.~11, no.~6, pp. 1--14, 2019.

\bibitem{yang2024observer}
Z.~Yang, J.~Kou, Z.~Li, Y.~Ma, W.~Zhao, Y.~Wang, and Y.~Shi, ``Observer-based
  adaptive neural network force tracking control for pneumatic polishing system
  end-effector,'' \emph{IEEE/ASME Transactions on Mechatronics}, vol.~29, no.~4,
  pp. 2741--2752, 2024.

\bibitem{oppenheim1997signals}
A.~V. Oppenheim, A.~S. Willsky, and S.~H. Nawab, \emph{Signals and Systems},
  2nd~ed.\hskip 1em plus 0.5em minus 0.4em\relax Upper Saddle River, NJ, USA:
  Prentice Hall, 1997.

\bibitem{chen2013linear}
C.-T. Chen, \emph{Linear System Theory and Design}, 4th~ed.\hskip 1em plus 0.5em
  minus 0.4em\relax New York, NY, USA: Oxford University Press, 2013.

\bibitem{lathi2018linear}
B.~P. Lathi and R.~A. Green, \emph{Linear Systems and Signals}, 3rd~ed.\hskip
  1em plus 0.5em minus 0.4em\relax Oxford, UK: Oxford University Press, 2018.

\bibitem{ogata2010modern}
K.~Ogata, \emph{Modern Control Engineering}, 5th~ed.\hskip 1em plus 0.5em minus
  0.4em\relax Boston, MA, USA: Prentice Hall, 2010.

\bibitem{yao2015adaptive}
J.~Yao, W.~Deng, and Z.~Jiao, ``Adaptive control of hydraulic actuators with
  {LuGre} model-based friction compensation,'' \emph{IEEE Transactions on
  Industrial Electronics}, vol.~62, no.~10, pp. 6469--6477, 2015.

\end{thebibliography}'''

old_bib = r'''\bibliographystyle{IEEEtran}
\bibliography{references}'''

if old_bib in text:
    text = text.replace(old_bib, new_bib)
    print('Replaced bibliography')
else:
    print('old_bib not found')

with open('main.tex', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated main.tex cleanly!')
