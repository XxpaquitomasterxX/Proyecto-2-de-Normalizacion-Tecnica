#!/usr/bin/env bash
# Regenera las láminas FV-00..FV-04 (A3) y las copia a la carpeta laminas/.
# Requiere: python3, pdflatex (TeX Live con babel-spanish, tikz, siunitx, helvet), pdftoppm (poppler).
set -e
cd "$(dirname "$0")"
python3 gen_fv00.py
python3 gen_fv01.py
python3 gen_fv02.py
# Los diagramas de FV-03 y FV-04 se compilan primero como PDF independientes
pdflatex -interaction=nonstopmode unifilar_fv_sa.tex  >/dev/null
pdflatex -interaction=nonstopmode detalle_tierra_sa.tex >/dev/null
for L in FV-00 FV-01 FV-02 FV-03 FV-04; do
  pdflatex -interaction=nonstopmode "$L.tex" >/dev/null
  mv -f "$L.pdf" ..
  pdftoppm -r 200 -png -singlefile "../$L.pdf" "../$L"
done
rm -f *.aux *.log
echo "Láminas generadas en $(cd .. && pwd)"
