from rdflib import Graph
import time
g = Graph()

themesIds=["7343", "7344", "7345", "7346", "7347", "7348", "7349", "7350", "7351" , "7352", "7508","8472" ]
  
for themeId in themesIds:
    url = "https://landportal.org/taxonomy_term/"+str(themeId)+".rdf"    
    g.parse(url)
    print len(g)

# save to file
timestr = time.strftime("%Y%m%d-%H%M%S")
filename_output = timestr+"-themes.rdf"
g.serialize(destination=filename_output, format='xml')
    
