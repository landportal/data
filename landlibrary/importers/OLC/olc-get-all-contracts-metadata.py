import urllib, json
from sets import Set

url = "http://rc-api-stage.elasticbeanstalk.com/api/contracts?category=olc&per_page=500"
response = urllib.urlopen(url) 
html=response.read() 
data = json.loads(html)

#with open('20170113-contracts.json') as data_file:    
#    data = json.load(data_file)
results = data['results']
resultSet = Set([])
i = 0
for record in results:
	i = i + 1
	id = record['id']
	if (id):
		print "%i - Contract #%s" %(i,id)
        resultSet.add(id)

print "Total %d" %i
print "**********************************"

contracts=[]
for rs in sorted(resultSet):
	contract_metadata_url = "http://rc-api-stage.elasticbeanstalk.com/api/contract/"+str(rs)+"/metadata"
	response = urllib.urlopen(contract_metadata_url) 
	html=response.read() 
	data = json.loads(html)
	contracts.append(data)
	print "Retrieved contract #%s" %rs
with open('contracts-metadata.json', 'w') as outfile:
    json.dump(contracts, outfile)