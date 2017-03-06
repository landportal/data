import urllib, json
from sets import Set

#url = "https://www.constituteproject.org/service/constitutions"
#response = urllib.urlopen(url) 
#html=response.read() 
#data = json.loads(html)

with open('constitutions.json') as data_file:    
    data = json.load(data_file)
i = 0
for constitution in data:
	i = i + 1
	id = constitution['id']
	title = constitution['title']
	print "<http://www.constituteproject.org/constitution/%s> dct:title \"%s\" ." %(id,title)
	#print "%i - Constitution #%s" %(i,id)

print "Total %d" %i
print "**********************************"
