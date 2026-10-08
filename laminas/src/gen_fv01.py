"""Genera FV-01.tex: planta de cubierta con el arreglo FV (redibujo vectorial de A04).

Coordenadas en metros: X crece del alero del eje A hacia el eje M/N (Sur -> Norte),
Y crece del alero alto (eje 03) hacia el alero bajo (eje 17) (Oeste -> Este).
Las posiciones de ejes y losas se obtuvieron de la lámina A04 (PDF vectorial):
56,7 pt/m, origen en la esquina exterior del alero (eje A / eje 03).
"""
ESC = 8.0          # mm por metro -> 1:125
OX, OY = 45.2, 232.0

LETRAS = [('A', .23), ('B', 1.29), ('C', 2.31), ("C'", 2.86), ("C''", 3.39), ('D', 3.99),
          ('E', 5.48), ('E1', 6.08), ('F', 6.61), ('G', 7.57), ('H', 8.04), ('I', 9.01),
          ('J', 9.54), ('K', 10.58), ('L', 12.98), ('M', 13.88), ('N', 16.74)]
NUMS = [('01', -2.98), ('02', -1.27), ('03', -.21), ('04', .99), ('05', 2.19), ('06', 3.17),
        ("06'", 4.43), ('07', 4.97), ('08', 6.84), ('09', 7.88), ('10', 8.48), ("10'", 9.08),
        ('11', 10.67), ('12', 11.20), ('13', 12.84), ('14', 13.72), ('15', 15.10), ('16', 16.90),
        ('17', 19.40)]
W, L = 15.05, 18.0
MW, ML, GAP = 1.134, 2.278, 0.025
XA, YA = 2.32, 4.20
XB = XA + 9 * MW + 8 * GAP
YB = YA + 4 * ML + 3 * GAP
YBJ = 16.10          # bajante DC en el alero del eje A
XDC = 1.95           # ruta DC entre la huella del eje B y el arreglo

o = []
A = o.append
A(r"""\documentclass[border=0pt]{standalone}
\newcommand{\revlamina}{3}
\input{lamina_comun.tex}
\begin{document}
\begin{tikzpicture}[x=1mm,y=1mm]
\marco
%% ===================== PLANTA =====================
\begin{scope}[shift={(%.2f,%.2f)},x=%.3fmm,y=-%.3fmm]""" % (OX, OY, ESC, ESC))

# ejes
for t, x in LETRAS:
    A(r"\draw[exist!60,line width=0.15pt,dash pattern=on 4pt off 1pt on 0.6pt off 1pt] (%.2f,-5.0) -- (%.2f,21.4);" % (x, x))
    for y in (-5.5, 21.9):
        A(r"\node[circle,draw=exist,line width=0.3pt,minimum size=3.6mm,inner sep=0pt,font=\fontsize{5}{5}\selectfont] at (%.2f,%.2f) {%s};" % (x, y, t.replace("'", "$'$")))
for t, y in NUMS:
    A(r"\draw[exist!60,line width=0.15pt,dash pattern=on 4pt off 1pt on 0.6pt off 1pt] (-1.85,%.2f) -- (19.55,%.2f);" % (y, y))
    for x in (-2.35, 20.07):
        A(r"\node[circle,draw=exist,line width=0.3pt,minimum size=3.6mm,inner sep=0pt,font=\fontsize{5}{5}\selectfont] at (%.2f,%.2f) {%s};" % (x, y, t.replace("'", "$'$")))

# losas y elementos existentes
losas = [(1, 2.38, -2.93, 5.41, 0.93), (2, 5.50, -0.30, 10.66, 0.93), (3, 5.79, -1.28, 8.03, -0.31),
         (4, 15.05, 13.70, 16.80, 16.90), (5, 7.74, 16.60, 9.53, 19.40), (6, 1.29, 18.00, 5.56, 19.40)]
for n, x1, y1, x2, y2 in losas:
    A(r"\fill[losa!35] (%.2f,%.2f) rectangle (%.2f,%.2f);" % (x1, y1, x2, y2))
    A(r"\draw[losa!80!black,line width=0.35pt,pattern=north east lines,pattern color=losa!90!black] (%.2f,%.2f) rectangle (%.2f,%.2f);" % (x1, y1, x2, y2))
# unidades condensadoras (símbolo)
for (x, y) in [(2.75, -2.5), (4.2, -2.5), (2.75, -1.1), (4.2, -1.1), (5.9, 0.15), (7.2, 0.15), (8.5, 0.15), (9.75, 0.15)]:
    A(r"\draw[exist,fill=white,line width=0.3pt] (%.2f,%.2f) rectangle ++(0.85,0.55); \draw[exist,line width=0.2pt] (%.2f,%.2f) circle (0.18);" % (x, y, x + 0.42, y + 0.27))
# pasarela de acceso
A(r"\draw[exist,line width=0.35pt,pattern=crosshatch,pattern color=yellow!60!black] (1.40,0.00) rectangle (2.20,2.45);")

# cubierta: costillas SSP380 y contorno
x = 0.19
while x < W:
    ytop = 0.0
    ybot = 16.6 if 7.34 < x < 9.82 else L
    A(r"\draw[exist!35,line width=0.12pt] (%.2f,%.2f) -- (%.2f,%.2f);" % (x, ytop, x, ybot))
    x += 0.38
A(r"\draw[black,line width=0.9pt] (0,0) -- (%.2f,0) -- (%.2f,%.2f) -- (9.82,%.2f) -- (9.82,16.60) -- (7.34,16.60) -- (7.34,%.2f) -- (0,%.2f) -- cycle;" % (W, W, L, L, L, L))

# huellas de mantenimiento existentes (A04)
hu = [((0.30, 3.15), (2.35, 3.15)), ((0.30, 3.15), (0.30, 6.73)), ((0.30, 6.73), (1.29, 6.73)),
      ((1.29, 6.73), (1.29, 17.86)), ((5.40, 1.00), (13.80, 1.00)), ((13.80, 1.00), (13.80, 13.75)),
      ((5.40, 16.87), (7.34, 16.87)), ((9.82, 16.87), (14.60, 16.87))]
for (a, b) in hu:
    A(r"\draw[nfpa!70,line width=1.6pt] (%.2f,%.2f) -- (%.2f,%.2f); \draw[white,line width=0.9pt] (%.2f,%.2f) -- (%.2f,%.2f);" % (a + b + a + b))

# pasillo perimetral NFPA 1 (1,2 m)
A(r"\fill[nfpa,opacity=0.13,even odd rule] (0,0) rectangle (%.2f,%.2f) (1.2,1.2) rectangle (%.2f,%.2f);" % (W, L, W - 1.2, L - 1.2))
A(r"\draw[nfpa,line width=0.5pt] (1.2,1.2) rectangle (%.2f,%.2f);" % (W - 1.2, L - 1.2))
# zona interior de viento (a = 1,5 m)
A(r"\draw[viento,line width=0.5pt,dash pattern=on 3pt off 1.5pt] (1.5,1.5) rectangle (%.2f,%.2f);" % (W - 1.5, L - 1.5))
# franja de sombra/servicio de condensadoras
A(r"\fill[pattern=north west lines,pattern color=sombra] (2.38,0.96) rectangle (10.66,%.2f);" % YA)
A(r"\draw[sombra,line width=0.5pt] (2.38,0.96) rectangle (10.66,%.2f);" % YA)

# arreglo FV
mid = 0
for r in range(4):
    col = 'inv1' if r < 2 else 'inv2'
    for c in range(9):
        mid += 1
        x = XA + c * (MW + GAP); y = YA + r * (ML + GAP)
        A(r"\filldraw[fill=%s!22,draw=%s,line width=0.45pt] (%.3f,%.3f) rectangle ++(%.3f,%.3f);" % (col, col, x, y, MW, ML))
        A(r"\draw[%s!70,line width=0.15pt] (%.3f,%.3f) -- ++(%.3f,0);" % (col, x + 0.08, y + ML / 2, MW - 0.16))
        A(r"\fill[%s] (%.3f,%.3f) rectangle ++(0.30,0.22);" % (col, x + MW / 2 - 0.15, y + ML - 0.36))
        A(r"\node[font=\fontsize{4.6}{5}\selectfont,text=%s!80!black] at (%.3f,%.3f) {M%02d};" % (col, x + MW / 2, y + 0.55, mid))
    yc = YA + r * (ML + GAP) + ML / 2
    A(r"\node[anchor=west,font=\fontsize{6.5}{7}\selectfont\bfseries,text=%s] at (%.2f,%.2f) {S%d};" % (col, XB + 0.12, yc - 0.25, r + 1))
    # remate del string hacia la ruta DC
    A(r"\draw[dc,line width=0.9pt] (%.3f,%.3f) -- (%.2f,%.3f);" % (XA, yc, XDC, yc))

# ruta DC y bajante
A(r"\draw[dc,line width=1.6pt] (%.2f,%.2f) -- (%.2f,%.2f) -- (0.00,%.2f);" % (XDC, YA + ML / 2, XDC, YBJ, YBJ))
A(r"\filldraw[dc,draw=black,line width=0.3pt] (0,%.2f) circle (0.32);" % YBJ)
A(r"\draw[black,line width=0.5pt,-{Latex[length=1.6mm]}] (-0.32,%.2f) -- (-1.30,%.2f);" % (YBJ, YBJ))

# pendiente
A(r"\draw[black,line width=0.6pt,-{Latex[length=2.2mm]}] (11.0,14.3) -- (11.0,16.0);")
A(r"\node[anchor=west,font=\fontsize{6.5}{7}\selectfont\bfseries] at (11.15,15.1) {15\,\%};")
A(r"\node[anchor=west,font=\fontsize{4.6}{5}\selectfont] at (11.15,15.65) {cae al ENE (az. $\approx$60°)};")

# cotas
def cota_h(x1, x2, y, t, above=True):
    A(r"\draw[black,line width=0.25pt,{Bar[width=1.6mm]Latex[length=1.2mm]}-{Latex[length=1.2mm]Bar[width=1.6mm]}] (%.3f,%.2f) -- (%.3f,%.2f);" % (x1, y, x2, y))
    A(r"\node[font=\fontsize{5.5}{6}\selectfont,fill=white,inner sep=0.6pt] at (%.3f,%.2f) {%s};" % ((x1 + x2) / 2, y - 0.45 if above else y + 0.45, t))


def cota_v(x, y1, y2, t):
    A(r"\draw[black,line width=0.25pt,{Bar[width=1.6mm]Latex[length=1.2mm]}-{Latex[length=1.2mm]Bar[width=1.6mm]}] (%.2f,%.3f) -- (%.2f,%.3f);" % (x, y1, x, y2))
    A(r"\node[font=\fontsize{5.5}{6}\selectfont,fill=white,inner sep=0.6pt,rotate=90] at (%.2f,%.3f) {%s};" % (x - 0.45, (y1 + y2) / 2, t))

f = lambda v: ('%.2f' % v).replace('.', ',')
cota_h(0, XA, 20.55, f(XA)); cota_h(XA, XB, 20.55, f(XB - XA)); cota_h(XB, W, 20.55, f(W - XB))
cota_v(18.75, 0, 0.96, ''); cota_v(18.75, 0.96, YA, f(YA - 0.96)); cota_v(18.75, YA, YB, f(YB - YA)); cota_v(18.75, YB, L, f(L - YB))
A(r"\node[font=\fontsize{5}{6}\selectfont,anchor=west] at (18.85,0.48) {0,96};")
# cotas de pasillo y zona de borde (lado norte, a media altura)
A(r"\draw[nfpa,line width=0.25pt,{Bar[width=1.4mm]Latex[length=1mm]}-{Latex[length=1mm]Bar[width=1.4mm]}] (%.2f,11.9) -- (%.2f,11.9);" % (W - 1.2, W))
A(r"\node[font=\fontsize{4.6}{5}\selectfont,text=nfpa,anchor=south] at (%.2f,11.85) {1,20};" % (W - 0.6))
A(r"\draw[viento,line width=0.25pt,{Bar[width=1.4mm]Latex[length=1mm]}-{Latex[length=1mm]Bar[width=1.4mm]}] (%.2f,12.6) -- (%.2f,12.6);" % (W - 1.5, W))
A(r"\node[font=\fontsize{4.6}{5}\selectfont,text=viento,anchor=north] at (%.2f,12.65) {a = 1,50};" % (W - 0.75))

# marcadores de referencia
refs = [((3.90, -1.90), 1), ((8.30, 0.42), 2), ((6.90, -0.80), 3), ((15.92, 15.30), 4), ((8.63, 18.80), 5),
        ((3.40, 18.70), 6), ((1.80, 1.60), 7), ((0.75, 10.60), 8), ((6.50, 2.55), 9), ((-0.75, 17.05), 10),
        ((14.30, 7.20), 11), ((XDC - 0.55, 11.00), 12)]
for (x, y), n in refs:
    A(r"\refm{(%.2f,%.2f)}{%d}" % (x, y, n))

# norte
A(r"""\begin{scope}[shift={(17.6,-3.4)}]
\draw[line width=0.5pt] (0,0) circle (1.0);
\fill[black] (1.25,0) -- (-0.6,0.42) -- (-0.25,0) -- (-0.6,-0.42) -- cycle;
\node[font=\fontsize{7}{8}\selectfont\bfseries] at (1.95,0) {N};
\draw[line width=0.6pt,-{Latex[length=1.6mm]},gray] (0,0) -- ({1.55*cos(30)},{1.55*sin(30)});
\node[font=\fontsize{4.6}{5}\selectfont,gray,anchor=west] at ({1.6*cos(30)},{1.6*sin(30)+0.15}) {N real ($\approx$30°)};
\end{scope}""")
A(r"\end{scope}")

# títulos de la planta
A(r"\node[anchor=north west,font=\fontsize{10}{12}\selectfont\bfseries] at (22,30) {PLANTA DE CUBIERTA -- DISTRIBUCIÓN DEL ARREGLO FOTOVOLTAICO};")
A(r"\node[anchor=north west,font=\fontsize{7}{8}\selectfont] at (22,24.5) {Escala 1:125 (A3). Cotas en metros. Redibujo vectorial a partir de la lámina A04 (as-built, TEC, mayo 2025) y S10.};")
A(r"\draw[line width=0.3pt] (22,25.5) -- (225,25.5);")
# escala gráfica 0-5 m
A(r"\begin{scope}[shift={(150,15.5)}]")
for i in range(5):
    A(r"\fill[%s] (%.1f,0) rectangle ++(8,1.6);" % ('black' if i % 2 == 0 else 'white', i * 8))
A(r"\draw[line width=0.3pt] (0,0) rectangle (40,1.6);")
for i in range(6):
    A(r"\node[font=\fontsize{5}{6}\selectfont,anchor=north] at (%d,-0.3) {%d};" % (i * 8, i))
A(r"\node[font=\fontsize{5}{6}\selectfont,anchor=west] at (41,0.8) {m};")
A(r"\end{scope}")

# ===================== COLUMNA DERECHA =====================
A(r"""\node[anchor=north west,font=\fontsize{9}{11}\selectfont\bfseries] at (252,284) {LEYENDA};
\begin{scope}[shift={(252,276)}]
\filldraw[fill=inv1!22,draw=inv1,line width=0.45pt] (0,0) rectangle (6,-4); \fill[inv1] (2.4,-3.6) rectangle (3.6,-3.0);
\node[anchor=west,font=\fontsize{6}{7}\selectfont,align=left] at (8,-2) {Módulo CS6W-580TB-AG con optimizador S650B (\rule{2mm}{1.5mm}), strings S1--S2 $\rightarrow$ INV-1};
\filldraw[fill=inv2!22,draw=inv2,line width=0.45pt] (0,-6) rectangle (6,-10);
\node[anchor=west,font=\fontsize{6}{7}\selectfont] at (8,-8) {Módulo CS6W-580TB-AG + S650B, strings S3--S4 $\rightarrow$ INV-2};
\fill[nfpa,opacity=0.13] (0,-12) rectangle (6,-16); \draw[nfpa,line width=0.5pt] (0,-12) rectangle (6,-16);
\node[anchor=west,font=\fontsize{6}{7}\selectfont] at (8,-14) {Pasillo perimetral de 1,20 m libre (NFPA 1:2012 \S 11.12, RNPCI)};
\draw[viento,line width=0.5pt,dash pattern=on 3pt off 1.5pt] (0,-20) -- (6,-20);
\node[anchor=west,font=\fontsize{6}{7}\selectfont] at (8,-20) {Límite de zona de borde de viento, $a$ = 1,50 m (CFIA 2023)};
\fill[pattern=north west lines,pattern color=sombra] (0,-22) rectangle (6,-26); \draw[sombra,line width=0.5pt] (0,-22) rectangle (6,-26);
\node[anchor=west,font=\fontsize{6}{7}\selectfont] at (8,-24) {Franja libre por sombra de condensadoras y servicio de A/C};
\fill[losa!35] (0,-28) rectangle (6,-32); \draw[losa!80!black,pattern=north east lines,pattern color=losa!90!black] (0,-28) rectangle (6,-32);
\node[anchor=west,font=\fontsize{6}{7}\selectfont] at (8,-30) {Losa de concreto existente (excluida del montaje)};
\draw[exist,fill=white,line width=0.3pt] (0.5,-34) rectangle (5.5,-37.5); \draw[exist,line width=0.2pt] (3,-35.75) circle (1);
\node[anchor=west,font=\fontsize{6}{7}\selectfont] at (8,-35.8) {Unidad condensadora existente (símbolo, láminas M1--M04)};
\draw[nfpa!70,line width=1.6pt] (0,-41) -- (6,-41); \draw[white,line width=0.9pt] (0,-41) -- (6,-41);
\node[anchor=west,font=\fontsize{6}{7}\selectfont] at (8,-41) {Huella de mantenimiento existente (A04)};
\draw[exist,pattern=crosshatch,pattern color=yellow!60!black] (0,-43.5) rectangle (6,-47);
\node[anchor=west,font=\fontsize{6}{7}\selectfont] at (8,-45.2) {Pasarela de acceso a losas de A/C (existente)};
\draw[dc,line width=1.6pt] (0,-50) -- (6,-50);
\node[anchor=west,font=\fontsize{6}{7}\selectfont] at (8,-50) {Canalización DC: 2 $\times$ EMT 3/4'' sobre soportes S-5! (sin perforar)};
\filldraw[dc,draw=black,line width=0.3pt] (3,-54.5) circle (1.6);
\node[anchor=west,font=\fontsize{6}{7}\selectfont] at (8,-54.5) {BJ-DC: bajante por fachada sur (eje A) hacia equipos de FV-02};
\draw[exist!60,line width=0.3pt,dash pattern=on 4pt off 1pt on 0.6pt off 1pt] (0,-59) -- (6,-59);
\node[anchor=west,font=\fontsize{6}{7}\selectfont] at (8,-59) {Eje estructural / arquitectónico};
\end{scope}""")

A(r"""\node[anchor=north west,font=\fontsize{9}{11}\selectfont\bfseries] at (252,214) {REFERENCIAS};
\node[anchor=north west,font=\fontsize{5.8}{7.4}\selectfont,align=left,text width=72mm] at (252,208) {%
\textbf{1, 2} Losas de condensadoras de A/C (ejes 01--04)\\
\textbf{3} Losa de concreto (ejes 02--03)\\
\textbf{4} Losa sobre ducto de escalera (eje N)\\
\textbf{5} Losa sobre ducto del ascensor (G--J)\\
\textbf{6} Losa de concreto bajo el alero (B--D)\\
\textbf{7} Pasarela de acceso a losas de A/C\\
\textbf{8} Huella de mantenimiento existente\\
\textbf{9} Franja libre de 3,24 m por sombra\\
\textbf{10} Bajante DC BJ-DC (ver FV-02)\\
\textbf{11} Zona interior de viento\\
\textbf{12} Ruta DC por costado sur del arreglo};
\node[anchor=north west,font=\fontsize{9}{11}\selectfont\bfseries] at (330,214) {CONFIGURACIÓN};
\node[anchor=north west,font=\fontsize{5.8}{7}\selectfont] at (330,208) {%
\setlength{\tabcolsep}{2.2pt}\begin{tabular}{@{}llllr@{}}
\textbf{String} & \textbf{Módulos} & \textbf{Optim.} & \textbf{Inv.} & \textbf{kWp}\\\hline
S1 & M01--M09 & O01--O09 & INV-1 & 5,22\\
S2 & M10--M18 & O10--O18 & INV-1 & 5,22\\
S3 & M19--M27 & O19--O27 & INV-2 & 5,22\\
S4 & M28--M36 & O28--O36 & INV-2 & 5,22\\\hline
\textbf{Total} & 36 & 36 & 2 & \textbf{20,88}\\
\end{tabular}};
\node[anchor=north west,font=\fontsize{9}{11}\selectfont\bfseries] at (330,182) {DETALLE MÓDULO (1:50)};
\begin{scope}[shift={(338,118)}]
\foreach \x in {-3,1.5,6,10.5,15,19.5,24,28.5} {\draw[exist!50,line width=0.2pt] (\x,-3) -- (\x,49);}
\filldraw[fill=inv1!18,draw=inv1,line width=0.6pt] (0,0) rectangle (22.68,45.56);
\draw[inv1!70,line width=0.2pt] (1.5,22.78) -- (21.2,22.78);
\draw[dc,line width=0.5pt,dash pattern=on 1.5pt off 1pt] (8.5,36) rectangle (14.2,40);
\foreach \x in {6,15} {\fill[black] (\x-0.9,-0.9) rectangle (\x+0.9,0.9); \fill[black] (\x-0.9,44.66) rectangle (\x+0.9,46.46);}
\draw[line width=0.25pt,{Bar[width=1.4mm]Latex[length=1mm]}-{Latex[length=1mm]Bar[width=1.4mm]}] (-6,0) -- (-6,45.56);
\node[rotate=90,font=\fontsize{5.2}{6}\selectfont,fill=white,inner sep=0.5pt] at (-6,22.78) {2278};
\draw[line width=0.25pt,{Bar[width=1.4mm]Latex[length=1mm]}-{Latex[length=1mm]Bar[width=1.4mm]}] (0,-5.5) -- (22.68,-5.5);
\node[font=\fontsize{5.2}{6}\selectfont,fill=white,inner sep=0.5pt] at (11.34,-5.5) {1134};
\draw[line width=0.2pt] (14.2,38) -- (31,38); \node[anchor=west,font=\fontsize{5.2}{6.2}\selectfont,align=left] at (31,38) {Optimizador S650B\\(en el marco, dorso)};
\draw[line width=0.2pt] (15.9,46.46) -- (31,48); \node[anchor=west,font=\fontsize{5.2}{6.2}\selectfont,align=left] at (31,48) {Abrazadera S-5-U + PVKIT 2.0\\(sobre costilla, sin perforar)};
\draw[line width=0.2pt] (28.5,10) -- (31,10); \node[anchor=west,font=\fontsize{5.2}{6.2}\selectfont,align=left] at (31,10) {Costilla de la lámina SSP380\\(paralela a la pendiente)};
\node[anchor=west,font=\fontsize{5.2}{6.2}\selectfont,align=left] at (31,24) {CS6W-580TB-AG, 31,6 kg\\juntas entre módulos 25 mm};
\end{scope}""")

A(r"""\node[anchor=north west,font=\fontsize{9}{11}\selectfont\bfseries] at (252,108) {NOTAS};
\node[anchor=north west,font=\fontsize{5.8}{7.2}\selectfont,align=left,text width=152mm] at (252,102) {%
1. Cubierta SOLCON SSP380 de junta alzada (HG \#24 + 1,5'' poliisocianurato), pendiente 15\,\% (8,53°), cae hacia el eje 17. Dimensiones según A04: 15,05 m (A--M) $\times$ 18,00 m (03--17); S10 da 17,80 m entre ejes estructurales.\\
2. Norte de proyecto (flecha negra) deducido de las fachadas de A02 (eje A = Sur, eje N = Norte). La imagen satelital y los rumbos del registro fotográfico del 5/10/2026 muestran que el norte real (flecha gris) está girado $\approx$30°: la cubierta cae hacia el ENE, azimut real $\approx$60°, que es el caso de cálculo (sección 10.1).\\
3. Montaje coplanar sin rieles S-5! PVKIT 2.0 (EdgeGrab en las líneas extremas, MidGrab compartido en las 3 interiores) sobre abrazaderas S-5-U (supuesto de diseño para costilla vertical, calibre HG 24); sin perforaciones en la cubierta. 5 líneas de apoyo $\times$ 18 abrazaderas = 90; separación de costillas supuesta de 0,38 m (perfil SSP380). Unión de marcos con orejeta listada UL 2703 y Cu estañado \#10 (FV-04).\\
4. El arreglo queda fuera del pasillo perimetral de 1,20 m (NFPA 1 \S 11.12) y de las zonas de borde de viento ($a$ = 1,50 m), y respeta huellas, pasarela y losas existentes.\\
5. Apagado rápido a nivel de módulo (SolarEdge PVRSS, NEC 690.12): 1 V por optimizador; iniciador = desconectador IFV (FV-02).\\
6. Canalización DC en EMT continua y unida a tierra (NEC 690.31, 690.43); rótulo ``CIRCUITO DC SOLAR FV'' a no más de 3 m (690.31(D)(2)). El cruce del pasillo perimetral y de la huella se hace con protector de paso a ras, pintado y rotulado.\\
7. Posiciones de losas y huellas transcritas de A04; las condensadoras se representan en forma simbólica.\\
8. La capacidad estructural de cerchas, clavadores y clips no está certificada: requiere dictamen de ingeniero estructural (CFIA).};""")

A(r"\cajetin{FV-01}{Planta de cubierta: distribución del arreglo FV,}{pasillos, exclusiones y ruta DC}{1:125}{2 de 5}")
A(r"""\end{tikzpicture}
\end{document}""")
open('FV-01.tex', 'w').write("\n".join(o))
print('ok', XB, YB)
