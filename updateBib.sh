#! /bin/bash

cp /home/alastair/thesis/flinders-thesis/honoursThesis.bib /home/alastair/thesis/flinders-thesis/honoursThesis.bib_old
cp /mnt/d/alastair/Documents/Uni/OneDrive\ -\ Flinders/Year\ 4/Semester\ 2/Honours/Reference/honours\ thesis.txt /home/alastair/thesis/flinders-thesis/honoursThesis.bib

python3 /home/alastair/thesis/flinders-thesis/bib_parser.py /home/alastair/thesis/flinders-thesis/honoursThesis.bib