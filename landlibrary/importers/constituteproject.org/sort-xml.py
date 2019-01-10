import xml.etree.ElementTree as ET

filename = "FIXME.rdf"
tree = ET.parse(filename)
ET.register_namespace('dct',"http://purl.org/dc/terms/")
ET.register_namespace('bibo',"http://purl.org/ontology/bibo/")
    
# this element holds the phonebook entries
container = tree.getroot()
data = []
for elem in container:
    key = elem.findtext("{http://purl.org/dc/elements/1.1/}coverage")
    data.append((key, elem))

data.sort()

# insert the last item from each tuple
container[:] = [item[-1] for item in data]

tree.write("ordered-"+filename)
