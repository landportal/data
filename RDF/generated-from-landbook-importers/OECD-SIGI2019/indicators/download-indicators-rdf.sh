#!/bin/sh
listVar="8572 8573 8574 8575 8576 8577 8578"
for i in $listVar; do
    wget https://landportal.org/taxonomy_term/"$i".rdf
done
