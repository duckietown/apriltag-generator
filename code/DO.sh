#!/bin/bash



pdflatex A*.tex

rm *.log
rm A*.tex
rm *.aux
rm *.gz

#mv *.pdf ../pdfs/$1wayint$2.pdf
