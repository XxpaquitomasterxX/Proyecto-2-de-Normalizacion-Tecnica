"""Genera FV-00.tex: plano general de ubicación (base: lámina E01 as-built)."""
X0, Y0 = 15.0, 280.0          # esquina superior izquierda de la imagen en la lámina (mm)
PT0X, PT0Y = 30.0, 218.0      # origen del recorte en coordenadas de E01 (pt)
K = 225.0 / 2058.0            # mm de lámina por pt de E01


def S(px, py):
    return (X0 + (px - PT0X) * K, Y0 - (py - PT0Y) * K)

o = []; A = o.append
A(r"""\documentclass[border=0pt]{standalone}
\newcommand{\revlamina}{4}
\input{lamina_comun.tex}
\begin{document}
\begin{tikzpicture}[x=1mm,y=1mm]
\marco""")
A(r"\node[anchor=north west,inner sep=0pt] at (%.2f,%.2f) {\includegraphics[width=225mm]{fv00_base.png}};" % (X0, Y0))
A(r"\draw[line width=0.4pt] (%.2f,%.2f) rectangle ++(225,-173.2);" % (X0, Y0))
A(r"\begin{scope}[shift={(%.2f,%.2f)},rotate=-10]" % (X0 + 211, Y0 - 158))
A(r"\filldraw[fill=white,draw=black,line width=0.4pt] (0,0) circle (6);")
A(r"\fill[black] (0,5.2) -- (-2.2,-3.8) -- (0,-2.2) -- cycle; \draw[black,line width=0.4pt,fill=white] (0,5.2) -- (2.2,-3.8) -- (0,-2.2) -- cycle;")
A(r"\node[font=\fontsize{8}{9}\selectfont\bfseries] at (0,8.2) {N};")
A(r"\end{scope}")

# marcadores con rótulo
items = [
    # (pt_x, pt_y, label_x_mm, label_y_mm, texto, color)
    (454, 1060, 40, 268, 'Edificio CAA-TEC: arreglo FV de 20,88 kWp en la cubierta (FV-01)', 'inv1'),
    (553, 1108, 40, 128, 'Cuarto eléctrico (TS-01, ATS, TP) y equipos FV en la fachada sur (FV-02)', 'nuevo'),
    (653, 1056, 115, 250, 'Generador Kohler existente (E07: J100U-IV, 100 kW)', 'exist'),
    (560, 1181, 40, 118, 'Malla de tierra existente, registros G-01 a G-05 ($\\le$ 5 $\\Omega$)', 'inv2'),
    (566, 1146, 120, 138, 'CRE-01: llegada de la acometida de 480 V', 'exist'),
    (1217, 990, 120, 155, 'Acometida 480 V: 1\\#4/0 Cu por fase, $\\approx$100 m, en ductos PVC', 'dc'),
    (1680, 975, 150, 238, 'Transformador ICE N.\\textsuperscript{o} 119688, 750 kVA, 34,5 kV/480Y/277 V', 'nuevo'),
    (1748, 990, 150, 228, 'Nicho: interruptor 200 A/3P 480 V y medición ICE (supuesta)', 'exist'),
]
for n, (px, py, lx, ly, t, col) in enumerate(items, 1):
    x, y = S(px, py)
    A(r"\draw[%s,line width=0.4pt] (%.2f,%.2f) -- (%.2f,%.2f);" % (col, x, y, lx, ly))
    A(r"\filldraw[%s,draw=black,line width=0.3pt] (%.2f,%.2f) circle (1.1);" % (col, x, y))
    A(r"\node[anchor=west,draw=%s,fill=white,line width=0.4pt,inner sep=1.2pt,font=\fontsize{6}{7}\selectfont] at (%.2f,%.2f) {\textbf{%d} \ %s};" % (col, lx, ly, n, t))

A(r"\node[anchor=north west,font=\fontsize{10}{12}\selectfont\bfseries] at (15,100) {PLANO GENERAL DE UBICACIÓN -- CAMPUS SEDE CENTRAL UTN, VILLA BONITA DE ALAJUELA};")
A(r"\node[anchor=north west,font=\fontsize{7}{8}\selectfont,align=left] at (15,94) {Base: lámina E01 ``Planta de distribución de canalización y red eléctrica'' (as-built TEC, escala original 1:200), reducida sin escala exacta.\\Orientación: norte real aproximado según la flecha (nota 7). En FV-01 y FV-02 se usa el norte de proyecto (deducido de A02), girado $\approx$30° respecto al real.};")
# escala gráfica: 1:200 -> 5 mm por metro en E01 = 14,17 pt/m -> mm de lámina
mm_m = (72 / 25.4) * 5 / 1.0 * K   # (pt por metro en E01) * K
A(r"\begin{scope}[shift={(15,80)}]")
for i in range(5):
    A(r"\fill[%s] (%.2f,0) rectangle ++(%.2f,1.6);" % ('black' if i % 2 == 0 else 'white', i * 10 * mm_m, 10 * mm_m))
A(r"\draw[line width=0.3pt] (0,0) rectangle (%.2f,1.6);" % (50 * mm_m))
for i in range(6):
    A(r"\node[font=\fontsize{5}{6}\selectfont,anchor=north] at (%.2f,-0.3) {%d};" % (i * 10 * mm_m, i * 10))
A(r"\node[font=\fontsize{5}{6}\selectfont,anchor=west] at (%.2f,0.8) {m (aprox.)};" % (50 * mm_m + 1))
A(r"\end{scope}")

# columna derecha
A(r"""\node[anchor=north west,font=\fontsize{9}{11}\selectfont\bfseries] at (252,284) {DATOS DEL EMPLAZAMIENTO};
\node[anchor=north west,font=\fontsize{6.2}{7.6}\selectfont] at (252,277) {%
\setlength{\tabcolsep}{2pt}\begin{tabular}{@{}p{38mm}p{112mm}@{}}
Provincia / cantón & Alajuela / Alajuela (Central)\\
Ubicación & Sede Central UTN, Villa Bonita; el TEC la ubica en Desamparados de Alajuela ($\approx$960 msnm)\\
Coordenadas & 10,0057\,°N; 84,2164\,°O (GPS de las fotografías del 5/10/2026, $\pm$10 m)\\
Propietario / catastro & Universidad Técnica Nacional; A-652521-2000; folio real 2-363445-000\\
Usuario / uso & TEC -- Centro Académico de Alajuela; académico y administrativo\\
Distribuidora & ICE; transformador de pedestal N.\textsuperscript{o} 119688, 750 kVA, 34,5 kV/480Y/277 V\\
Servicio del edificio & 480 V trifásico desde el nicho del transformador; TS-01 480$\Delta$/208Y-120 V en el cuarto eléctrico\\
Respaldo & ATS de 400 A + generador; UPS de 20 kVA para circuitos TRU\\
Sistema FV & 20,88 kWp DC / 20 kW AC; autoconsumo con inyección de excedentes (Ley 10086)\\
\end{tabular}};
\node[anchor=north west,font=\fontsize{9}{11}\selectfont\bfseries] at (252,205) {ÍNDICE DE LÁMINAS};
\node[anchor=north west,font=\fontsize{6.2}{7.6}\selectfont] at (252,198) {%
\setlength{\tabcolsep}{2pt}\begin{tabular}{@{}ll@{}}
\textbf{FV-00} & Plano general de ubicación (esta lámina)\\
\textbf{FV-01} & Planta de cubierta: distribución del arreglo, pasillos, exclusiones y ruta DC\\
\textbf{FV-02} & Planta parcial nivel 1 y elevación: inversores, tableros y desconectadores\\
\textbf{FV-03} & Diagrama unifilar completo e interconexión\\
\textbf{FV-04} & Puesta a tierra, medios de desconexión y rotulación\\
\end{tabular}};
\node[anchor=north west,font=\fontsize{9}{11}\selectfont\bfseries] at (252,160) {NOTAS};
\node[anchor=north west,font=\fontsize{6}{7.4}\selectfont,align=left,text width=152mm] at (252,154) {%
1. Las posiciones de los elementos se transcriben de E01 (as-built). La lámina no tiene escala exacta: usar las cotas de FV-01 y FV-02.\\
2. El número del transformador del ICE (119688) y su capacidad se tomaron del rótulo de E01. Se supone que el abonado del servicio es el TEC, con tarifa T-CS (sección 5.8 del documento).\\
3. El punto de interconexión FV está dentro del edificio, en el alimentador TS-01 $\rightarrow$ ATS (lado normal). No se modifica la acometida ni el equipo del ICE.\\
4. E01 rotula el generador como GR-01 de 55 kVA y E07 lo indica como Kohler J100U-IV de 100 kW. En sitio se confirmó un grupo Kohler en cabina; se adopta el dato de E07, el unifilar de diseño. Su capacidad no influye en el sistema FV, que queda del lado normal del ATS.\\
5. La imagen satelital (sección 5.1 del documento) y el registro fotográfico (Anexo D) confirman que el edificio está girado unos 30° y que la cubierta cae hacia el ENE (azimut real de unos 60°). Los árboles cercanos tienen la copa cerca de la altura del alero.\\
6. Medición del ICE: ni los planos ni el cuarto eléctrico muestran el medidor. La acometida del CAA se agregó al nicho existente del transformador (E01); se adopta como supuesto de diseño una medición indirecta (TC) en 480 V en ese nicho, que el ICE sustituye por un medidor bidireccional (FV-03).\\
7. La flecha indica el norte real aproximado ($\pm$10°), obtenido al superponer la imagen satelital (bordes de la cubierta a 60° y 150°) con el contorno del edificio en E01.};""")
A(r"\cajetin{FV-00}{Plano general de ubicación del sistema FV,}{acometida, transformador ICE y equipos principales}{Sin escala (base E01 1:200)}{1 de 5}")
A(r"""\end{tikzpicture}
\end{document}""")
open('FV-00.tex', 'w').write("\n".join(o))
print('ok', mm_m)
