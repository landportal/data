import glob
import xmltodict, json
import harvest_lists

class AgrisResource(object):

    def __init__(self, id, resource):
        self.id = id
        self.resource = resource

    def __key(self):
        return (self.id)

    def __eq__(x, y):
        return isinstance(y, x.__class__) and x.__key() == y.__key()

    def __hash__(self):
        return hash(self.__key())

    def get_resource(self):
        return self.resource

def is_harvest_label(label):
    return (label.lower() in harvest_lists.FINAL_HARVEST_LIST.keys())

def is_harvest_uri(uri):
    return (uri in harvest_lists.FINAL_HARVEST_LIST.values())

def process_agris_resource(agris_resource):
    if ("dc:subject" in agris_resource) and (agris_resource["dc:subject"]):
        # could be 0, 1 or more dc:subject
        dc_subjects = filter(None,agris_resource["dc:subject"])
        for dc_subject in dc_subjects:
            if ("ags:subjectThesaurus" in dc_subject) and (dc_subject["ags:subjectThesaurus"]):
                for subject in dc_subject["ags:subjectThesaurus"]:
                        scheme = subject["@scheme"] if "@scheme" in subject else ""
                        if (scheme == "ags:AGROVOC"):
                            if ("@xml:lang" in subject) and (subject["@xml:lang"]):
                                label = (subject["#text"] if "#text" in subject else "")
                                lang = subject["@xml:lang"]
                                if (lang=="en"):
                                    if is_harvest_label(label):
                                        print label #text
                                        d = dict(agris_resource)
                                        resources.add(AgrisResource(agris_resource["@ags:ARN"], agris_resource))
                                    else:
                                        not_selected_agrovoc.add(label)
                                else:
                                    pass #in other language
                            else:
                                uri=subject["#text"]
                                if is_harvest_uri(uri): #uri
                                    print uri #uri
                                    resources.add(AgrisResource(agris_resource["@ags:ARN"], agris_resource))
                                else:
                                    not_selected_agrovoc.add(uri)
                                #<ags:subjectThesaurus scheme="ags:AGROVOC">http://aims.fao.org/aos/agrovoc/c_27465</ags:subjectThesaurus>

#         if ("ags:subjectClassification" in dc_subject) and (dc_subject["ags:subjectClassification"]):
#             for subject in dc_subject["ags:subjectClassification"]:



    #<ags:subjectThesaurus xml:lang="en" scheme="ags:AGROVOC"><![CDATA[hygiene]]></ags:subjectThesaurus>

def from_ags_to_json(filename):
    with open(filename) as fd:
        doc = xmltodict.parse(fd.read(), force_list={'ags:resource': True, 'dc:subject': True, 'ags:subjectThesaurus': True, 'ags:subjectClassification': True})
        return doc
        #return json.dumps(doc) # '{"e": {"a": ["text", "text"]}}'

counter = 0

def process_agris_xml_file(filename):
    json_content = from_ags_to_json(filename)
    for resource in json_content['ags:resources']["ags:resource"]:
        global counter
        counter+=1
        if (counter%100000 ==0):
            print "Analyzing resource #"+str(counter)
        process_agris_resource(resource)

#     if isinstance(json_content['ags:resources']["ags:resource"],dict):
#         #only one item in the resources
#         process_agris_resource(['ags:resources']["ags:resource"])
#         print "ONLY ONE"
#     else:
#         for resource in json_content['ags:resources']["ags:resource"]:
#             process_agris_resource(resource)

not_selected_agrovoc = set()
#read_files = glob.glob("d:\Downloads\work\agris\XML_Output\*\*\*.xml")
files ={}
year=2016
while year<2018:
    files[year] = glob.glob("d:\Downloads\XML_Output\\"+str(year)+"\*\*.xml")
    year+=1
for year, read_files in files.iteritems():
    resources = set()
    print "Analyzing year="+str(year)
    for f in read_files:
        process_agris_xml_file(f)
    print "----------------"
    print "Land-related resources="+str(len(resources))

    target_filename=str(year)+"-agris-harvested.json"
    with open(target_filename, 'w') as target:
        print "Opening the file="+target_filename
        for resource in resources:
            target.write(json.dumps(resource.get_resource())+",")
        print "Closed the file="+target_filename

