# Láminas del sistema FV de 20,88 kWp, Centro Académico de Alajuela (TEC)

Planos del Proyecto No. 2 de EL-4601 Normalización Técnica para Electrónica (ITCR): diseño normativo de una instalación solar fotovoltaica en Costa Rica. Todas las láminas son A3 horizontales (420 × 297 mm), en formato vectorial, con un cajetín común.

| Lámina | Contenido | Escala |
|---|---|---|
| [FV-00](FV-00.pdf) | (Rev. 4: norte real, supuestos de medición y generador) Plano general de ubicación: edificio, cuarto eléctrico, acometida 480 V, transformador ICE N.º 119688 (750 kVA), generador y malla de tierra | Sin escala (base E01 1:200) |
| [FV-01](FV-01.pdf) | (Rev. 3: norte real, azimut 60°, abrazadera S-5-U, rótulo 690.31(D)(2)) Planta de cubierta: 36 módulos CS6W-580TB-AG con S650B, strings S1–S4, pasillo NFPA de 1,20 m, zona de viento a = 1,50 m, exclusiones y ruta DC | 1:125 |
| [FV-02](FV-02.pdf) | (Rev. 5: interruptor secundario IS-TS01 de 400 A junto a TS-01) Planta parcial nivel 1 y elevación de la fachada sur: INV-1/INV-2 (SE10KUS), TFV, IFV, CD-FV y espacios de trabajo NEC 110.26 | 1:50 / 1:40 |
| [FV-03](FV-03.pdf) | (Rev. 6: IS-TS01 de 400 A a la salida de TS-01, derivación sobre alimentador protegido, COM-ICE para el SCADA del ICE, notas de categoría B) Diagrama unifilar completo, desde los módulos hasta la interconexión en el alimentador IS-TS01 → ATS | Sin escala |
| [FV-04](FV-04.pdf) | (Rev. 5: protección de la derivación referida a IS-TS01) Puesta a tierra, medios de desconexión, rotulación, secuencia de emergencia y pruebas IEC 62446-1 | Sin escala |

Hay una versión PNG a 200 dpi de cada lámina (`FV-0x.png`) para previsualizar.

## Estructura

```
laminas/
├── FV-00.pdf … FV-04.pdf     láminas finales
├── FV-00.png … FV-04.png     vistas previas a 200 dpi
└── src/
    ├── build.sh              regenera todas las láminas
    ├── lamina_comun.tex      preámbulo común (A3, fuentes, colores, cajetín, marco)
    ├── gen_fv00.py           genera FV-00.tex
    ├── gen_fv01.py           genera FV-01.tex (coordenadas en metros sobre los ejes de A04)
    ├── gen_fv02.py           genera FV-02.tex (planta 1:50 + elevación 1:40)
    ├── unifilar_fv.tex       diagrama unifilar (TikZ) → unifilar_fv_sa.tex → FV-03
    ├── detalle_tierra.tex    detalle de puesta a tierra (TikZ) → detalle_tierra_sa.tex → FV-04
    ├── FV-03.tex, FV-04.tex  láminas que incluyen los diagramas independientes
    └── fv00_base.png, fv02_base.png   recortes de los planos as-built E01 y A01 que sirven de fondo
```

## Cómo regenerar

Se necesita Python 3, TeX Live (`pdflatex` con `babel-spanish`, `tikz`, `siunitx` y `helvet`) y `pdftoppm` (poppler). En Ubuntu: `sudo apt install texlive-latex-extra texlive-lang-spanish texlive-science poppler-utils`.

```bash
cd laminas/src
./build.sh
```

El script ejecuta los generadores Python, compila primero `unifilar_fv_sa.tex` y `detalle_tierra_sa.tex`, porque FV-03 y FV-04 los incluyen como PDF, compila FV-00…FV-04 y por último mueve los PDF y PNG a `laminas/`.

En el documento principal (`main.tex`), las láminas se insertan con `\includegraphics{laminas/FV-0x.pdf}` en páginas horizontales.

## Fuentes de los planos base

- **A01, A02, A04 y S10:** planos arquitectónicos y estructurales as-built del edificio CAA-TEC (mayo 2025). Se usaron para los ejes, las dimensiones de la cubierta (15,05 × 18,00 m), las losas, las huellas y la pendiente del 15 %.
- **E01:** acometida eléctrica y planta de canalización. De aquí salen la ubicación del cuarto eléctrico, el transformador ICE y la malla de tierra.
- **E07–E09:** diagrama unifilar y tableros. Se usaron para TS-01, ATS, TP y el generador.

## Limitaciones

- Las posiciones de los equipos existentes se transcribieron de los planos as-built y del registro fotográfico del 5/10/2026.
- FV-01 y FV-02 usan el norte de proyecto deducido de las fachadas de A02; el norte real está girado ≈30° (flecha gris en FV-01 y flecha de FV-00, obtenidas con la imagen satelital).
- Los datos que no se pudieron obtener del edificio se cubren con los supuestos de diseño del Cuadro 8 del documento.
- La capacidad estructural de la cubierta no está certificada y requiere el dictamen de un ingeniero estructural incorporado al CFIA.
- Estas láminas son un trabajo académico. No sustituyen planos firmados por un profesional responsable ante el CFIA.
