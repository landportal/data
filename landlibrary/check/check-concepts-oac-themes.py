#from __future__ import print_function
import fileinput

def check(listToCheck, sourceList, type):
   listToCheck = map(str.strip, line.replace('\"','').strip().split(";"))
   listToCheck = filter(None, listToCheck) # Remove empty/blank items
   for itemToCheck in listToCheck:
      if (sourceList.__contains__(itemToCheck.strip()) == False):
        print "Error in \"%s\" for the value \"%s\"" %(type, itemToCheck.strip())


### Load the concepts, oacs and themes ####

concepts = []
for line in fileinput.input('landvoc-label-id.csv'):
   part=line.partition(',')
   label = part[0].strip()
   # Add label to the list
   concepts.append(label)

oacs = []
for line in fileinput.input('landvoc-oacs.txt'):
   oacs.append(line.strip())

themes = []
for line in fileinput.input('landvoc-themes.txt'):
   themes.append(line.strip())

### Start to check the values ###

for line in fileinput.input('ifpri-to-check-concepts.csv'):
	check(line, concepts, "concepts")

for line in fileinput.input('ifpri-to-check-oacs.csv'):
	check(line, oacs, "oacs")

for line in fileinput.input('ifpri-to-check-themes.csv'):
	check(line, themes, "themes")
	
#TODO reading a CSV file
# 1st: 3rd partner source tag
# 2nd: landvoc concept
# 3rd: OA category
# 4th: Theme
"""
for line in fileinput.input('ifpri-to-check.csv'):
   # ';' separator
   part=line.partition(';')
   sourceTag = part[0].strip()
   conceptsToCheck = part[2].strip()
   print conceptsToCheck
   check(line, concepts)
   check(line, oacs)
   check(line, themes)
   
   oacsToCheck = part[4].strip()
   themesToCheck = part[6].strip()
   
   check(conceptsToCheck, concepts)
"""
