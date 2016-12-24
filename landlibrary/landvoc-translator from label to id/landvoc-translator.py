from __future__ import print_function
import fileinput
from sets import Set

landvoc = {}
#with open('regions-iso.csv') as data_file:    
for line in fileinput.input('landvoc-label-id.csv'):
   part=line.partition(',')
   label = part[0].strip()
   id = part[2].strip()
   landvoc[label] = {'id': id}

for line in fileinput.input('ifpri-landvoc-concepts.csv'):
    concepts = map(str.strip, line.replace('\"','').strip().split(";"))
    for concept in concepts:
      if landvoc.has_key(concept.strip()):
		print(landvoc[concept.strip()]['id'], end=";")
      else:
        pass #print (concept.strip())
    print ("")