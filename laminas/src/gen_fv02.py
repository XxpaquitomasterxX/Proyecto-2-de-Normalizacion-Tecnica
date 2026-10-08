"""Genera FV-02.tex: equipos FV en fachada sur (eje A) y cuarto eléctrico, nivel 1.

Planta 1:50 sobre la planta arquitectónica A01 (nivel 1, as-built) en coordenadas de ejes
(X: eje A -> N, Y: eje 01 -> 17, metros). Equipos existentes del cuarto eléctrico
transcritos de la lámina E01 (posición aproximada). Elevación de la fachada sur 1:30.
"""
o = []; A = o.append
P_ESC = 20.0                 # mm/m planta (1:50)
P_OX = 20 + 3.0 * P_ESC      # X = -3,0 m en x = 20 mm
P_OY = 282 + 12.6 * P_ESC    # Y = 12,6 m en y = 282 mm
E_ESC = 25.0                 # mm/m elevación (1:40)
E_OX = 25 - 13.45 * E_ESC    # Y = 13,45 m en x = 25 mm
E_OY = 27.0                  # rasante exterior en y = 27 mm

A(r"""\documentclass[border=0pt]{standalone}
\newcommand{\revlamina}{5}
\input{lamina_comun.tex}
\begin{document}
\begin{tikzpicture}[x=1mm,y=1mm]
\marco""")

# ---------------- PLANTA ----------------
A(r"\begin{scope}[shift={(%.2f,%.2f)},x=%.3fmm,y=-%.3fmm]" % (P_OX, P_OY, P_ESC, P_ESC))
A(r"\node[anchor=north west,inner sep=0pt] at (-3.0,12.6) {\includegraphics[width=180mm]{fv02_base.png}};")
A(r"\draw[line width=0.4pt] (-3.0,12.6) rectangle (6.0,19.8);")

def caja(x1, y1, x2, y2, estilo):
    A(r"\draw[%s] (%.2f,%.2f) rectangle (%.2f,%.2f);" % (estilo, x1, y1, x2, y2))

EX = 'draw=exist,fill=exist!25,line width=0.4pt'
existentes = [  # (x1,y1,x2,y2, etiqueta, pos etiqueta, anchor)
    (0.31, 13.90, 0.56, 14.35, 'TM-UPS', (0.62, 14.12), 'west'),
    (0.31, 14.42, 0.61, 15.07, 'TS-01', (0.64, 14.96), 'west'),
    (0.31, 15.12, 0.56, 15.78, 'ATS (TA-GR)', (0.62, 15.45), 'west'),
    (0.31, 15.85, 0.56, 16.60, 'TP', (0.62, 16.22), 'west'),
    (0.75, 16.55, 1.25, 16.78, 'TN1', (1.00, 16.40), 'south'),
    (1.35, 16.55, 1.85, 16.78, 'TI1', (1.60, 16.40), 'south'),
    (1.95, 16.55, 2.45, 16.78, 'TRU1', (2.20, 16.40), 'south'),
    (2.55, 16.55, 3.05, 16.78, 'TD1', (2.80, 16.40), 'south'),
    (3.40, 13.80, 3.95, 14.20, 'PCA/PDI', (3.67, 14.30), 'north'),
]
for x1, y1, x2, y2, t, (lx, ly), an in existentes:
    caja(x1, y1, x2, y2, EX)
    A(r"\node[anchor=%s,font=\fontsize{4.8}{5}\selectfont,text=exist!80!black,inner sep=0.5pt] at (%.2f,%.2f) {%s};" % (an, lx, ly, t))
# UPS con zona de servicio
A(r"\draw[exist,line width=0.4pt,pattern=crosshatch,pattern color=exist!40] (1.05,13.80) rectangle (2.30,14.95);")
A(r"\draw[%s] (1.40,14.05) rectangle (1.95,14.70);" % EX)
A(r"\node[font=\fontsize{4.8}{5}\selectfont,text=exist!80!black] at (1.675,14.375) {UPS};")
# condensadora existente del cuarto eléctrico (exterior, en muro)
A(r"\draw[exist,fill=white,line width=0.4pt] (-0.40,14.85) rectangle (0.17,15.47); \draw[exist,line width=0.3pt] (-0.115,15.16) circle (0.18);")

# equipos nuevos (exterior, muro eje A)
NV = 'draw=nuevo,fill=nuevo!18,line width=0.6pt'
A(r"\draw[draw=inv1,fill=inv1!25,line width=0.6pt] (-0.13,15.65) rectangle (0.17,15.97);")
A(r"\draw[draw=inv2,fill=inv2!25,line width=0.6pt] (-0.13,16.25) rectangle (0.17,16.57);")
caja(0.02, 13.82, 0.17, 14.27, NV)            # TFV
caja(-0.05, 14.37, 0.17, 14.75, NV)           # IFV
caja(0.31, 14.45, 0.51, 15.00, NV + ',pattern=north east lines,pattern color=nuevo')  # CD-FV (en muro, sobre TS-01)
# zonas de trabajo NEC 110.26 (0,90 m)
A(r"\draw[nuevo,line width=0.35pt,dash pattern=on 2pt off 1pt] (-1.03,15.55) rectangle (-0.13,16.67);")
A(r"\draw[nuevo,line width=0.35pt,dash pattern=on 2pt off 1pt] (-0.95,13.75) rectangle (-0.05,14.80);")
A(r"\node[font=\fontsize{4.6}{5}\selectfont,text=nuevo,rotate=90] at (-0.85,16.11) {0,90 m};")
A(r"\node[font=\fontsize{4.6}{5}\selectfont,text=nuevo,rotate=90] at (-0.80,14.28) {0,90 m};")
# bajante DC y canalizaciones
A(r"\filldraw[dc,draw=black,line width=0.3pt] (0.02,16.11) circle (0.07);")
A(r"\draw[dc,line width=1.1pt] (0.02,16.11) -- (0.02,15.97); \draw[dc,line width=1.1pt] (0.02,16.11) -- (0.02,16.25);")
A(r"\draw[black,line width=0.8pt] (0.10,16.57) -- (0.10,16.70) -- (0.24,16.70);")   # (simbólico) salida AC
A(r"\draw[black,line width=0.9pt,dash pattern=on 3pt off 1pt] (0.12,15.65) -- (0.12,14.27);")  # AC INV->TFV (bajo condensadora)
A(r"\draw[nuevo,line width=1.0pt] (0.17,14.56) -- (0.31,14.56);")   # IFV -> CD-FV (pasamuro)
A(r"\draw[violet,line width=0.6pt,dash pattern=on 2pt off 1pt] (0.17,16.45) -- (0.40,16.45) -- (0.40,16.95) -- (1.80,16.95) -- (1.80,17.55);")
A(r"\node[draw=violet,font=\fontsize{4.6}{5}\selectfont,text=violet,fill=white,inner sep=1pt] at (1.80,17.75) {RACK};")

# rótulos de equipos nuevos con líneas de referencia (zona exterior libre)
def callout(px, py, lx, ly, txt, col='nuevo'):
    A(r"\draw[%s,line width=0.3pt] (%.2f,%.2f) -- (%.2f,%.2f);" % (col, px, py, lx, ly))
    A(r"\node[anchor=east,font=\fontsize{5.6}{6.4}\selectfont\bfseries,text=%s,fill=white,inner sep=0.8pt,align=right] at (%.2f,%.2f) {%s};" % (col, lx, ly, txt))
callout(-0.13, 15.81, -1.35, 15.30, 'INV-1', 'inv1')
callout(-0.13, 16.41, -1.35, 16.95, 'INV-2', 'inv2')
callout(0.02, 16.11, -1.35, 16.30, 'BJ-DC', 'dc')
callout(-0.05, 14.56, -1.25, 14.95, 'IFV')
callout(0.02, 14.05, -1.25, 13.40, 'TFV')
callout(0.41, 14.72, 1.15, 13.25, 'CD-FV')
A(r"\node[anchor=north,font=\fontsize{4.6}{5}\selectfont,text=exist!80!black,fill=white,inner sep=0.6pt] at (-0.12,15.50) {UC (exist.)};")
# marcas de corte de la elevación
A(r"\draw[black,line width=0.5pt,-{Latex[length=1.6mm]}] (-1.9,13.65) -- (-1.9,13.95); \draw[black,line width=0.5pt,-{Latex[length=1.6mm]}] (-1.9,16.95) -- (-1.9,16.65);")
A(r"\draw[black,line width=0.3pt,dash pattern=on 4pt off 1pt on 1pt off 1pt] (-1.9,13.65) -- (-1.9,16.95);")
A(r"\node[font=\fontsize{5.5}{6}\selectfont\bfseries,fill=white,inner sep=0.6pt] at (-2.15,13.55) {E1};")
A(r"\node[font=\fontsize{5.5}{6}\selectfont\bfseries,fill=white,inner sep=0.6pt] at (-2.15,17.05) {E1};")
# etiquetas de recintos y norte
A(r"\node[font=\fontsize{5.5}{6}\selectfont\bfseries,fill=white,inner sep=0.8pt] at (-2.1,18.6) {EXTERIOR (fachada sur)};")
A(r"""\begin{scope}[shift={(4.9,18.9)}]
\draw[line width=0.4pt] (0,0) circle (0.42);
\fill[black] (0.55,0) -- (-0.25,0.18) -- (-0.10,0) -- (-0.25,-0.18) -- cycle;
\node[font=\fontsize{6}{7}\selectfont\bfseries] at (0.82,0) {N};
\end{scope}""")
A(r"\end{scope}")
A(r"\node[anchor=north west,font=\fontsize{9}{11}\selectfont\bfseries] at (20,135.5) {PLANTA PARCIAL NIVEL 1 -- FACHADA SUR (EJE A) Y CUARTO ELÉCTRICO};")
A(r"\node[anchor=north west,font=\fontsize{6.5}{7.5}\selectfont] at (20,131) {Escala 1:50 (A3). Base: planta A01 nivel 1 (as-built). Equipos existentes transcritos de E01 (posición aproximada).};")

# ---------------- ELEVACIÓN E1 ----------------
def E(y, h):
    return (E_OX + y * E_ESC, E_OY + h * E_ESC)

def rect(y1, h1, y2, h2, estilo):
    (a, b), (c, d) = E(y1, h1), E(y2, h2)
    A(r"\draw[%s] (%.2f,%.2f) rectangle (%.2f,%.2f);" % (estilo, a, b, c, d))

def txt(y, h, t, extra=''):
    a, b = E(y, h)
    A(r"\node[font=\fontsize{5.2}{6}\selectfont%s] at (%.2f,%.2f) {%s};" % (extra, a, b, t))

# muro y rasante
rect(13.70, 0.0, 16.90, 2.85, 'fill=exist!8,draw=exist,line width=0.5pt')
a, b = E(13.45, 0); c, d = E(17.10, 0)
A(r"\draw[line width=0.8pt] (%.2f,%.2f) -- (%.2f,%.2f);" % (a, b, c, d))
A(r"\fill[pattern=north east lines,pattern color=exist] (%.2f,%.2f) rectangle (%.2f,%.2f);" % (a, b - 3, c, d))
txt(16.55, -0.18, 'Rasante exterior $\\approx$ 192,3 (E01)', ',anchor=north')
txt(13.95, 2.70, 'Muro eje A (continúa hasta el alero, $\\approx$ 7,5 m)', ',anchor=west')
# condensadora existente
rect(14.85, 0.30, 15.47, 0.95, 'draw=exist,fill=white,line width=0.4pt,dash pattern=on 2pt off 1pt')
txt(15.16, 0.62, 'UC exist.', ',text=exist')
# equipos nuevos
rect(13.82, 1.10, 14.27, 1.75, 'draw=nuevo,fill=nuevo!18,line width=0.6pt'); txt(14.045, 1.48, '\\textbf{TFV}', ',text=nuevo')
rect(14.37, 1.05, 14.75, 1.65, 'draw=nuevo,fill=nuevo!18,line width=0.6pt'); txt(14.56, 1.40, '\\textbf{IFV}', ',text=nuevo')
a, b = E(14.70, 1.30); c, d = E(14.83, 1.30)
A(r"\draw[nuevo,line width=1.2pt] (%.2f,%.2f) -- (%.2f,%.2f);" % (a, b, c, d))   # palanca
rect(15.65, 0.90, 15.97, 1.71, 'draw=inv1,fill=inv1!25,line width=0.6pt'); txt(15.81, 1.30, '\\textbf{INV-1}', ',text=inv1,rotate=90')
rect(16.25, 0.90, 16.57, 1.71, 'draw=inv2,fill=inv2!25,line width=0.6pt'); txt(16.41, 1.30, '\\textbf{INV-2}', ',text=inv2,rotate=90')
# DC desde la cubierta
for y in (16.06, 16.14):
    a, b = E(y, 2.85); c, d = E(y, 1.95)
    A(r"\draw[dc,line width=1.3pt] (%.2f,%.2f) -- (%.2f,%.2f);" % (a, b, c, d))
for (y1, y2) in ((16.06, 15.81), (16.14, 16.41)):
    a, b = E(y1, 1.95); c, d = E(y2, 1.95); e, f = E(y2, 1.71)
    A(r"\draw[dc,line width=1.3pt] (%.2f,%.2f) -- (%.2f,%.2f) -- (%.2f,%.2f);" % (a, b, c, d, e, f))
a, b = E(16.10, 2.85)
A(r"\node[anchor=south,font=\fontsize{5.2}{6}\selectfont,text=dc] at (%.2f,%.2f) {2 EMT 3/4'' DC desde BJ-DC (FV-01)};" % (a, b + 0.5))
# AC: INV -> TFV (bajo la condensadora, h = 0,20 m)
pts = [E(15.81, 0.90), E(15.81, 0.20), E(14.10, 0.20), E(14.10, 1.10)]
A(r"\draw[black,line width=1.0pt] " + " -- ".join("(%.2f,%.2f)" % p for p in pts) + ";")
pts = [E(16.41, 0.90), E(16.41, 0.20), E(15.81, 0.20)]
A(r"\draw[black,line width=1.0pt] " + " -- ".join("(%.2f,%.2f)" % p for p in pts) + ";")
txt(14.14, 0.10, 'EMT AC a h = 0,20 m', ',anchor=west')
# TFV -> IFV y pasamuro hacia CD-FV
a, b = E(14.27, 1.30); c, d = E(14.37, 1.30)
A(r"\draw[black,line width=1.0pt] (%.2f,%.2f) -- (%.2f,%.2f);" % (a, b, c, d))
pts = [E(14.56, 1.05), E(14.56, 0.55)]
A(r"\draw[nuevo,line width=1.0pt] (%.2f,%.2f) -- (%.2f,%.2f);" % (pts[0] + pts[1]))
a, b = E(14.56, 0.55)
A(r"\draw[nuevo,line width=0.4pt] (%.2f,%.2f) circle (1.1);" % (a, b))
txt(14.52, 0.78, 'Pasamuro\\\\a CD-FV', ',anchor=east,text=nuevo,align=right')
# líneas de referencia de altura
for h, t in ((2.00, 'Máx. altura de maniobra 2,00 m (NEC 240.24(A), 404.8)'),):
    a, b = E(13.70, h); c, d = E(16.90, h)
    A(r"\draw[nuevo,line width=0.3pt,dash pattern=on 3pt off 1.5pt] (%.2f,%.2f) -- (%.2f,%.2f);" % (a, b, c, d))
    A(r"\node[anchor=south west,font=\fontsize{5}{6}\selectfont,text=nuevo] at (%.2f,%.2f) {%s};" % (a + 1, b, t))
# cotas verticales
def cv(y, h1, h2, t):
    (a, b), (c, d) = E(y, h1), E(y, h2)
    A(r"\draw[line width=0.25pt,{Bar[width=1.4mm]Latex[length=1mm]}-{Latex[length=1mm]Bar[width=1.4mm]}] (%.2f,%.2f) -- (%.2f,%.2f);" % (a, b, c, d))
    A(r"\node[font=\fontsize{5}{6}\selectfont,rotate=90,fill=white,inner sep=0.5pt] at (%.2f,%.2f) {%s};" % (a - 1.8, (b + d) / 2, t))
cv(16.75, 0, 0.90, '0,90'); cv(16.75, 0.90, 1.71, '0,81'); cv(13.60, 0, 2.00, '2,00')
# cota horizontal del tramo
(a, b), (c, d) = E(13.70, -0.55), E(16.90, -0.55)
A(r"\draw[line width=0.25pt,{Bar[width=1.4mm]Latex[length=1mm]}-{Latex[length=1mm]Bar[width=1.4mm]}] (%.2f,%.2f) -- (%.2f,%.2f);" % (a, b, c, d))
A(r"\node[font=\fontsize{5}{6}\selectfont,fill=white,inner sep=0.5pt] at (%.2f,%.2f) {3,18 m (ejes 14--16)};" % ((a + c) / 2, b))
for y, t in ((13.72, '14'), (15.10, '15'), (16.90, '16')):
    a, b = E(y, 2.85)
    A(r"\draw[exist,line width=0.2pt,dash pattern=on 3pt off 1pt on 0.6pt off 1pt] (%.2f,%.2f) -- (%.2f,%.2f);" % (a, b + 1, a, b + 6))
    A(r"\node[circle,draw=exist,minimum size=3.6mm,inner sep=0pt,font=\fontsize{5}{5}\selectfont] at (%.2f,%.2f) {%s};" % (a, b + 8, t))
A(r"\node[anchor=north west,font=\fontsize{9}{11}\selectfont\bfseries] at (20,122) {ELEVACIÓN E1 -- FACHADA SUR (vista desde el exterior)};")
A(r"\node[anchor=north west,font=\fontsize{6.5}{7.5}\selectfont,align=left] at (20,117.5) {Escala 1:40. Alturas desde la rasante exterior. Cotas en metros.};")

# cuadro de equipos (bajo el título de la elevación)
A(r"""\node[anchor=north west,font=\fontsize{5.3}{6.4}\selectfont] at (128,108) {%
\setlength{\tabcolsep}{2pt}\begin{tabular}{@{}lll@{}}
\textbf{ID} & \textbf{Equipo / modelo} & \textbf{Montaje}\\\hline
INV-1/2 & SolarEdge SE10KUS, 208Y/120 V, NEMA 3R & h 0,90--1,71 m\\
 & 808 $\times$ 317 $\times$ 300 mm, 35,5 kg & exterior\\
TFV & Square D NQ 3$\phi$ 4h, barras 100 A, & h 1,10--1,75 m\\
 & 2 $\times$ QOB335 + SPD tipo 2, gab. NEMA 3R & exterior\\
IFV & Square D HU363RB, 100 A, 600 V, sin & h 1,05--1,65 m\\
 & fusibles, corte visible, con candado & exterior\\
CD-FV & Bloque UL 1953 + interruptor 70 A/3P & muro interior\\
 & (PowerPact HDL36070) + TC del medidor & junto a TS-01\\
IS-TS01 & Interruptor 400 A/3P PowerPact LAL36400, & muro interior,\\
 & gab. NEMA 1, a $\le$ 3 m de TS-01 & junto a CD-FV\\
BJ-DC & 2 $\times$ EMT 3/4'' con PV Wire \#10 & fachada\\\hline
\end{tabular}};""")

# ---------------- COLUMNA DERECHA ----------------
A(r"""\node[anchor=north west,font=\fontsize{9}{11}\selectfont\bfseries] at (252,284) {LEYENDA};
\begin{scope}[shift={(252,276)}]
\filldraw[fill=inv1!25,draw=inv1,line width=0.6pt] (0,0) rectangle (6,-3.5);
\node[anchor=west,font=\fontsize{6}{7}\selectfont] at (8,-1.75) {Inversor INV-1 / INV-2 (SolarEdge SE10KUS), nuevo};
\filldraw[fill=nuevo!18,draw=nuevo,line width=0.6pt] (0,-5.5) rectangle (6,-9);
\node[anchor=west,font=\fontsize{6}{7}\selectfont] at (8,-7.25) {Tablero / desconectador / derivación nuevo (TFV, IFV, CD-FV)};
\filldraw[fill=exist!25,draw=exist,line width=0.4pt] (0,-11) rectangle (6,-14.5);
\node[anchor=west,font=\fontsize{6}{7}\selectfont] at (8,-12.75) {Equipo existente (E01, posición aproximada)};
\draw[nuevo,line width=0.35pt,dash pattern=on 2pt off 1pt] (0,-16.5) rectangle (6,-20);
\node[anchor=west,font=\fontsize{6}{7}\selectfont] at (8,-18.25) {Espacio de trabajo libre NEC 110.26 (0,90 m de profundidad)};
\draw[dc,line width=1.3pt] (0,-23) -- (6,-23);
\node[anchor=west,font=\fontsize{6}{7}\selectfont] at (8,-23) {Canalización DC (EMT), desde la cubierta};
\draw[black,line width=1.0pt] (0,-27) -- (6,-27);
\node[anchor=west,font=\fontsize{6}{7}\selectfont] at (8,-27) {Canalización AC (EMT): C-AC1, C-AC2, C-AC3};
\draw[nuevo,line width=1.0pt] (0,-31) -- (6,-31);
\node[anchor=west,font=\fontsize{6}{7}\selectfont] at (8,-31) {Conexión IFV $\rightarrow$ CD-FV a través del muro};
\draw[violet,line width=0.6pt,dash pattern=on 2pt off 1pt] (0,-35) -- (6,-35);
\node[anchor=west,font=\fontsize{6}{7}\selectfont] at (8,-35) {Comunicación UTP Cat6 al rack de DATIC (monitoreo)};
\end{scope}""")

A(r"""\node[anchor=north west,font=\fontsize{9}{11}\selectfont\bfseries] at (252,232) {EQUIPOS EXISTENTES (E01, E07)};
\node[anchor=north west,font=\fontsize{5.8}{7.2}\selectfont,align=left,text width=152mm] at (252,226) {%
\textbf{TS-01 (TX)} Square D EXN112T3H, 112,5 kVA, 480$\Delta$--208Y/120 V, Z = 3,57 \% \quad \textbf{ATS (TA-GR)} Kohler KSS-ACTC-0400S, 400 A\\
\textbf{TP} Square D HCP32688, barras 800 A, principal LA36400 400 A, 42 polos (2--12 libres) \quad \textbf{TM-UPS} Eaton, 100 A, doble tiro\\
\textbf{TN1, TI1, TRU1, TD1} tableros secundarios \quad \textbf{UPS} Ablerex 20 kVA \quad \textbf{UC} condensadora del cuarto eléctrico};""")

A(r"""\node[anchor=north west,font=\fontsize{9}{11}\selectfont\bfseries] at (252,206) {NOTAS};
\node[anchor=north west,font=\fontsize{5.8}{7.2}\selectfont,align=left,text width=152mm] at (252,200) {%
1. Según E01, el muro interior del eje A del cuarto eléctrico ya está ocupado por TM-UPS, TS-01, ATS y TP. Por eso los inversores, el TFV y el IFV se instalan en la cara \textbf{exterior} del mismo muro (fachada sur), bajo el alero, en envolventes NEMA 3R.\\
2. Los circuitos DC nunca entran al edificio: bajan por la fachada (BJ-DC) directamente a los inversores (NEC 690.31).\\
3. A la salida de TS-01 se instala el interruptor secundario IS-TS01 (400 A/3P, a $\le$ 3 m, NEC 240.21(C)(2)); aguas abajo, la derivación al alimentador protegido IS-TS01 $\rightarrow$ ATS se hace dentro de CD-FV (bloque UL 1953) y termina, a menos de 3 m, en un interruptor de 70 A/3P (NEC 240.21(B)(1), 705.12(B)(2)). IS-TS01 se monta en el muro interior junto a CD-FV, con manija a $\le$ 2,00 m y el espacio de trabajo de NEC 110.26.\\
4. El IFV es el desconectador del sistema FV y el iniciador del apagado rápido. Es accesible desde el exterior para el ICE y Bomberos, tiene corte visible y se puede bloquear con candado (NEC 690.12(C), 690.13, 705.20).\\
5. Mantener 0,90 m de profundidad libre, 0,76 m de ancho y 2,00 m de altura frente a cada equipo (NEC 110.26). Ninguna manija de operación a más de 2,00 m.\\
6. El cuarto eléctrico está unos 2,3 m por debajo de la rasante exterior (NPT 0+190,00): el pasamuro, a h $\approx$ 0,55 m por fuera (bajo el IFV), llega a unos 2,85 m sobre el piso interior. C-AC4 baja en EMT por el muro interior hasta CD-FV, cuya manija queda a 1,70 m del piso del cuarto ($\le$ 2,00 m, NEC 240.24(A)). Pasamuro sellado con material cortafuego y sello hidráulico exterior.\\
7. La posición de la condensadora existente (UC) y de los equipos interiores se transcribe de E01 y del registro fotográfico del 5/10/2026; los equipos FV quedan a los costados de la UC y no obstruyen su descarga de aire ni su acceso de mantenimiento.\\
8. Generador: se adopta el dato de E07 (Kohler J100U-IV, 100 kW); E01 lo rotula como GR-01 de 55 kVA. No afecta la conexión FV, que queda del lado normal del ATS.};""")

A(r"\cajetin{FV-02}{Ubicación de inversores, tableros y desconectadores:}{planta parcial nivel 1 y elevación de fachada sur}{1:50 / 1:40}{3 de 5}")
A(r"""\end{tikzpicture}
\end{document}""")
open('FV-02.tex', 'w').write("\n".join(o))
print('ok')
