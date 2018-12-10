from rdflib import Graph
import time
g = Graph()

themesIds=["7340", "7341", "7342",]
  
for themeId in themesIds:
    url = "https://landportal.org/taxonomy_term/"+str(themeId)+".rdf"    
    g.parse(url)
    print len(g)

# save to file
timestr = time.strftime("%Y%m%d-%H%M%S")
filename_output = timestr+"-oacs.rdf"
g.serialize(destination=filename_output, format='xml')
    
