#!/bin/sh
listVar="8561 8564 8565 8566 8567 8568 8569 8570"
for i in $listVar; do
    wget https://landportal.org/taxonomy_term/"$i".rdf
done
