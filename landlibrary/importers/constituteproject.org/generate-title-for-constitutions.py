import urllib, json
from sets import Set
import codecs

#url = "https://www.constituteproject.org/service/constitutions"
#response = urllib.urlopen(url) 
#html=response.read() 
#data = json.loads(html)

with codecs.open('constitutions.json', "r", "utf-8") as data_file:    
    data = json.load(data_file)

prefix = u"@prefix dct: <http://purl.org/dc/terms/> ."
with codecs.open('generated-constitutions-title.ttl',"w", "utf-8") as ttl_file:
    ttl_file.write(prefix+"\n")    
    i = 0
    for constitution in data:
    	i = i + 1
    	id = constitution['id']
    	title = constitution['title']
    	line = u"<http://www.constituteproject.org/constitution/%s> dct:title \"Constitution of %s\" ." %(id,title)
        ttl_file.write(line+u"\n")
        print line
    	#print "%i - Constitution #%s" %(i,id)
    print "Total %d" %i
    print "**********************************"
    ttl_file.close()

