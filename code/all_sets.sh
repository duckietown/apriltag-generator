#!/bin/bash

LISTS=./data/lists/*

for list in $LISTS
do
  list_file=${list##*/}
  echo "Creating tags for set ${list_file%.*}"
   
  python -W ignore create_tags.py --config set --set_name  ${list_file%.*}
done
