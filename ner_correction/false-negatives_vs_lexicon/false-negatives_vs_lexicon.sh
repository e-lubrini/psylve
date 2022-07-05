#!/bin/env bash

echo --- OBT labels equal to a FN
fgrep --color -i -x -f psyllo_habitat.txt onto_habitat.txt
echo ---
echo

echo --- OBT labels that contain a FN
fgrep --color -i -w -f psyllo_habitat.txt onto_habitat.txt
echo ---
echo

echo --- OBT labels contained in a FN
fgrep --color -i -w -f onto_habitat.txt psyllo_habitat.txt
echo ---
echo

echo --- Common words between FN and OBT labels
sed -e 's, ,\n,g' onto_habitat.txt | tr '[:upper:]' '[:lower:]' | sort -u >words_onto_habitat.txt
fgrep --color -i -w -f words_onto_habitat.txt psyllo_habitat.txt
echo ---
echo

echo --- Taxo labels equal to a FN
fgrep --color -i -x -f psyllo_taxa.txt onto_taxa.txt
echo ---
echo

echo --- Taxo labels that contain a FN
fgrep --color -i -w -f psyllo_taxa.txt onto_taxa.txt
echo ---
echo

echo --- Uh... Unique FNs please
fgrep --color -i -w -o -f psyllo_taxa.txt onto_taxa.txt | sort -u
echo ---
echo

echo --- Taxo labels contained in a FN
# fgrep --color -i -w -f onto_taxa.txt psyllo_taxa.txt
echo cannot do that
echo ---
echo

echo --- Common words between FN and Taxo labels
sed -e 's, ,\n,g' psyllo_taxa.txt | sed -e '/^$/d' -e '/^T$/d' -e '/^L.$/d' -e '/^W.$/d' -e '/^cf.$/d' | tr '[:upper:]' '[:lower:]' | sort -u >words_psyllo_taxa.txt
fgrep --color -i -w -f words_psyllo_taxa.txt onto_taxa.txt
echo ---
echo

echo --- Uh... Unique words please
fgrep --color -i -w -o -f words_psyllo_taxa.txt onto_taxa.txt | sort -u
echo ---
echo
