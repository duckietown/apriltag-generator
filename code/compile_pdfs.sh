#!/bin/bash

cd output

for filename in ./*.tex; do
  echo $filename
  pdflatex $filename

  rm ./*.log
  rm ./*.aux
done

cd ..
