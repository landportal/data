#!/usr/bin/python
# -*- coding: UTF-8 -*-
import glob
import xmltodict
import itertools
import utils
import landvoc
import time
from resources.LandLibraryResource import LandLibraryResource
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
import io


LANDVOC = landvoc.LandVoc()
llrs=set()
set_to_get=set()
list_to_get=list()

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

def create_llr_from_AGRIS_XML(agris_xml_entry):
    llr = LandLibraryResource()
    global set_to_get

    #ID. Only one.
    internal_id = agris_xml_entry["@ags:ARN"]
    llr.set_id(u"AGRIS:"+internal_id)

    #Language
    if "dc:language" in agris_xml_entry:
        langs = agris_xml_entry["dc:language"]
        langs_cleared = set()
        for lang in langs:
            langs_cleared.add(utils.getISO639_1code(lang))
            langs_cleared.add(utils.getISO639_1code_from_ISO639_3code(lang))
        langs_cleared = set(filter(None,langs_cleared))
        llr.set_language(langs_cleared)

    #title. One
    #dc:title. Could be more tan one
    titles = agris_xml_entry["dc:title"]
    if isinstance(titles,basestring):
        llr.set_title(titles)
    else:
        # 2 titles: one in English other in othe lang
        # 2 titles: both in English
        # 3 titles: corner case.
        en_title=u""
        other_title=u""
        for title in titles:
            if detect(title)=="en":
                if not en_title:
                    en_title = title
                else:
                    en_title = en_title + title
            else:
                if not other_title:
                    other_title=title
                else: #corner case
                    en_title = title
        llr.set_title(en_title)
        llr.set_subtitle(other_title)

    #subtitle
    for potential_subtitle in agris_xml_entry["dc:title"]:
        if "dcterms:alternative" in potential_subtitle:
            llr.set_subtitle(potential_subtitle["dcterms:alternative"])

    # description
    final_description = ""
    if "dc:description" in agris_xml_entry:
        for k,v in agris_xml_entry["dc:description"].iteritems():
            if k == "dcterms:abstract":
                if isinstance(v, basestring):
                    final_description = v
                else:
                    # more than one description
                    for description in v:
                        try:
                            if detect(description)=="en": # English description on top
                                final_description = description + u"\n" + final_description
                            else:
                                final_description = final_description + u"\n" + description
                        except LangDetectException:
                                final_description = final_description + u"\n" + description

    llr.set_description(final_description)

    #author. One or more
    authors = []
    if "dc:creator" in agris_xml_entry and "ags:creatorPersonal" in agris_xml_entry["dc:creator"]:
        authors = [author.replace(u"  ", u" ").replace(u"  ", u" ") for author in agris_xml_entry["dc:creator"]["ags:creatorPersonal"]]
        llr.set_authors(authors)

    #corporate_authors. Could be more than one
    corporate_authors = []
    if "dc:creator" in agris_xml_entry and "ags:creatorCorporate" in agris_xml_entry["dc:creator"]:
        corporate_authors = agris_xml_entry["dc:creator"]["ags:creatorCorporate"]
        corporate_authors_flat = list(set([item for sublist in [curate_corporate_author(corporate_author) for corporate_author in corporate_authors] for item in sublist]))
        llr.set_corporate_authors(list(set(corporate_authors_flat)))        

    #publishers. One or more (and more could be in the same item or in a different one
    publishers = []
    if "dc:publisher" in agris_xml_entry and "ags:publisherName" in agris_xml_entry["dc:publisher"]:
        publishers = agris_xml_entry["dc:publisher"]["ags:publisherName"]
        publishers_flat = list(set([item for sublist in [curate_publisher_white_list(publisher) for publisher in publishers] for item in sublist]))
        #remove blacklisted
        publishers_flat = filter(None,[curate_publisher_black_list(publisher) for publisher in publishers_flat])
        llr.set_publishers(list(set(publishers_flat)))


    #type. Only one
    # dc:type. 0..1
    dc_type = None
    if "dc:type" in agris_xml_entry:
        dc_type = agris_xml_entry["dc:type"]
    llr.set_type(utils.getLLR_type(dc_type))

    #number of pages. Only one
    dcterms_extent = None
    if ("dc:format" in agris_xml_entry) and ("dcterms:extent" in agris_xml_entry["dc:format"]):
        dcterms_extent = agris_xml_entry["dc:format"]["dcterms:extent"]

    ags_citationNumber_number_pages = None
    if ("ags:citation" in agris_xml_entry) and ("ags:citationNumber" in agris_xml_entry["ags:citation"]):
        ags_citationNumber = agris_xml_entry["ags:citation"]["ags:citationNumber"]
        ags_citationNumber_number_pages = [x for x in ags_citationNumber if ("pp." in x and x!="pp. .")]
        if ags_citationNumber_number_pages:
            ags_citationNumber_number_pages = ags_citationNumber_number_pages[0]

    pages = None
    if dcterms_extent:
        pages = unicode(utils.clean_extent(dcterms_extent))
    elif ags_citationNumber_number_pages:
        pages = unicode(utils.clean_ags_citationNumber(ags_citationNumber_number_pages))
    
    if pages and utils.is_valid_pages(pages):
        llr.set_number_pages(pages)

    #date.
    if ("dc:date" in agris_xml_entry) and ("dcterms:dateIssued" in agris_xml_entry["dc:date"]):
        issued = agris_xml_entry["dc:date"]["dcterms:dateIssued"]
        llr.set_date(utils.clean_date(issued))


    #original url. Only one
    original_url = "http://agris.fao.org/agris-search/search.do?recordID="+internal_id
    llr.set_original_url(original_url)


    #resource url. Only one
    resource_url = None
    for identifier in agris_xml_entry["dc:identifier"]:
        if identifier["@scheme"]=="dcterms:URI":
            resource_url = identifier["#text"]
        if (not resource_url) and (identifier["@scheme"]=="ags:DOI"): # Happens 3 times
            resource_url = "http://doi.org/"+identifier["#text"]

    if resource_url:
        llr.set_resource_url(resource_url)

    #License
    #dc:rights
    #(AGS) rightsStatement
    #(AGS) TermsOfUse
    #llr.set_license()

    #Copyright details
    #dc:rights
    #(AGS) rightsStatement
    #(AGS) TermsOfUse
    #llr.set_copyright_details()


    #data provider
    llr.set_data_provider(u"AGRIS")

    #image
    #llr.set_image("")

    #keywords
    potential_dc_subjects = []
    potential_agrovoc_subjects = []
    if "dc:subject" in agris_xml_entry:
        potential_dc_subjects = [subject for subject in agris_xml_entry["dc:subject"] if isinstance(subject, basestring)]

        dc_subjects_complex = [subject for subject in agris_xml_entry["dc:subject"] if not isinstance(subject, basestring)]
        for subjectsThesaurus in dc_subjects_complex:
            for subjectThesaurus in subjectsThesaurus["ags:subjectThesaurus"]:
                if "ags:AGROVOC" == subjectThesaurus["@scheme"]:
                    potential_agrovoc_subjects.append(subjectThesaurus["#text"])

    dc_subjects = LANDVOC.get_concepts_direct(potential_dc_subjects)
    agrovoc_subjects = LANDVOC.get_concepts_direct_from_uris(potential_agrovoc_subjects)

    concepts = set(dc_subjects+agrovoc_subjects)
    themes=LANDVOC.get_fixed_themes(concepts)
    oacs=LANDVOC.get_fixed_oacs(concepts)

#     #geographical focus. list
    places_from_title = set(utils.getPlaceET_fromText_NLTK(llr.get_title())) | set(utils.getPlaceET_fromText_GeoText(llr.get_title())) 
    places_from_description = set(utils.getPlaceET_fromText_NLTK(llr.get_description())) | set(utils.getPlaceET_fromText_GeoText(llr.get_description())) 

    countries_from_subjects = set(utils.flatten(filter(None,[utils.getISO3166_1code(k) for k in potential_dc_subjects])))
    regions_from_subjects = set(utils.flatten(filter(None,[utils.getUNM49code(k) for k in potential_dc_subjects])))
    countries_from_agrovoc = set(utils.flatten(filter(None,[utils.getISO3166_1code_fromAGROVOC_URI(uri) for uri in potential_agrovoc_subjects])))
    regions_from_agrovoc = set(utils.flatten(filter(None,[utils.getUNM49code_fromAGROVOC_URI(uri) for uri in potential_agrovoc_subjects])))

#     if len(countries_from_subjects) != len(countries_from_agrovoc):
#         print "DISTINTO"
#         print llr.get_id()
#         print countries_from_subjects
#         print countries_from_agrovoc
#         print "-----------------"
#
#     if len(regions_from_subjects) != len(regions_from_agrovoc):
#         print llr.get_id()
#         print "DISTINTO"
#         print regions_from_subjects
#         print regions_from_agrovoc
#         print "-----------------"
    geographical_focus_codes = countries_from_subjects | regions_from_subjects | countries_from_agrovoc | regions_from_agrovoc | places_from_title | places_from_description
    #geographical_focus_codes = countries_from_subjects | regions_from_subjects | countries_from_agrovoc | regions_from_agrovoc | places_from_title
    #geographical_focus_codes = countries_from_subjects | regions_from_subjects | countries_from_agrovoc | regions_from_agrovoc
    
    llr.set_geographical_focus(geographical_focus_codes)

    llr.set_concepts(concepts);
    llr.set_themes(themes);
    llr.set_overarching_categories(oacs);

    return llr

def curate_corporate_author(corporate_author):
    clean_corporate_authors = set()
    dict_pattern = {"Land Tenure Center" : u"Land Tenure Center, University of Wisconsin-Madison",
                    "Latvia Univ. of Agriculture" : u"Latvia University of Agriculture",
                    "Slovak University of Agriculture" : u"Slovak University of Agriculture",
                    "Technical University in Zvolen" : u"Technical University in Zvolen",
                    "American Agricultural Economics Association": u"American Agricultural Economics Association",
                    "Canadian Institute of Resources Law": u"Canadian Institute of Resources Law - University of Calgary",
                    "Central Arizona Project": u"Central Arizona Project",
                    u"Centro Agronómico Tropical de Investigación y Enseñanza": u"Tropical Agricultural Research and Higher Education Center",
                    "United States;Forest Service": u"United States Department of Agriculture - Forest service",
                    "International Union of Forestry Research Organizations": u"International Union of Forestry Research Organizations",
                    u"Colegio de Geógrafos": u"Colegio de Geógrafos",
                    "Committee on Indian Affairs.;Senate.;United States.;Congress.;United States" : u"United States Senate Committee on Indian Affairs",
                    "Congress.;Committee on Resources.;United States": u"United States House Committee on Natural Resources",
                    "University of Wisconsin--Madison": u"University of Wisconsin-Madison",
                    "Dept. of Agriculture.;Economic Research Service.;United States": u"U.S. Department of Agriculture",
                    "Dept. of Agriculture.;United States": u"U.S. Department of Agriculture",
                    "Environmental and Water Resources Institute": u"Environmental and Water Resources Institute",
                    "Estonian Univ. of Life Sciences": u"Estonian University of Life Sciences",
                    "Latvia University of Agriculture": u"Latvia University of Agriculture",
                    "Fondo Nacional de Investigaciones Agropecuarias": u"Fondo Nacional de Investigaciones Agropecuarias",
                    "IFAMR": u"International Food and Agribusiness Management Review",
                    "IFAMA": u"International Food and Agribusiness Management Association",
                    "International Institute for Environment and Development": u"International Institute for Environment and Development",
                    "Tanzania Natural Resource Forum": u"Tanzania Natural Resource Forum",
                    "IUCN": u"International Union for Conservation of Nature",
                    "Kenya Agricultural Research Institute": u"KALRO Food Crops Research Institute",
                    "Land Tenure Center, University of Wisconsin-Madison": u"Land Tenure Center, University of Wisconsin-Madison",
                    "NGO Forum on Cambodia": u"The NGO Forum on Cambodia",
                    "United States.;Forest Service": u"United States Department of Agriculture - Forest service",
                    "United States;Forest Service": u"United States Department of Agriculture - Forest service",
                    "United States;Committee on Indian Affairs": u"United States Senate Committee on Indian Affairs",
                    "GEMAS": u"The Geological Surveys of Europe",
                    "University of California": u"University of California",
                    "University of Wisconsin--Madison": u"University of Wisconsin-Madison",

    }

    for pattern, curated_corporate_author in dict_pattern.iteritems():
        if pattern in corporate_author:
            clean_corporate_authors.add(curated_corporate_author)
    if not clean_corporate_authors: # in case there is NO pattern match, add the initial publisher
        clean_corporate_authors.add(corporate_author)
    return list(clean_corporate_authors)


def curate_publisher_black_list(publisher):
    blacklist = ["[sn]"]
    if not publisher in blacklist:
        return publisher


def curate_publisher_white_list(publisher):
    clean_publishers = set()
    dict_pattern = {"Elsevier" : u"Elsevier",
                    "Springer" : u"Springer",
                    "Wiley" : u"John Wiley & Sons, Inc.",
                    "Blackwell" : u"Wiley-Blackwell",
                    "WILEY" : u"John Wiley & Sons, Inc.",
                    "Taylor & Francis" : u"Taylor & Francis Group",
                    "John Wiley & Sons" : u"John Wiley & Sons, Inc.",
                    "Kluwer" : u"Kluwer Academic Publishers",
                    "LLU" : u"Latvia University of Agriculture",
                    "Oxford Univ" : u"Oxford University Press",
                    "Routledge" : u"Routledge",
                    "U.S. G.P.O." : u"United States Government Publishing Office",
                    "Laval" : u"Université Laval",
                    "Island Press" : u"Island Press",
                    u"Latvijas Lauksaimniecības universitāte"  : u"Latvia University of Agriculture",
                    "CABI" : u"Centre for Agriculture and Bioscience International",
                    "CSIRO Publishing" : u"CSIRO Publishing", # PENDING TO CREATE
                    "De Gruyter" : u"De Gruyter",  # PENDING TO CREATE
                    "International Society for Horticultural Science" : u"International Society for Horticultural Science", # PENDING TO CREATE
                    "Italian Society of Silviculture and Forest Ecology" : u"Italian Society of Silviculture and Forest Ecology", # PENDING TO CREATE
                    "Land Tenure Center, University of Wisconsin" : u"Land Tenure Center, University of Wisconsin-Madison",
                    "Weed Science Society of America" : u"Weed Science Society of America",
                    "MARDI" : u"Malaysia Agricultural Research and Development Institute",
                    "Forest Products Society" : u"Forest Products Society",
                    "United States Dept. of Agriculture, Forest Service" : u"United States Department of Agriculture - Forest service",
                    "U.S. Dept. of Agriculture, Forest Service" : u"United States Department of Agriculture - Forest service",
                    "Forest Service, U.S. Dept. of Agriculture" : u"United States Department of Agriculture - Forest service",
                    "COSCIENCE" : u"Ecoscience Journal",
                    "Academic Press": u"Academic Press Books",
                    "Agri-overseas" : u"Agri‐Overseas",
                    u"Akadémiai Kiadó": u"Akadémiai Kiadó",
                    "Akademiai Kiado": u"Akadémiai Kiadó",
                    "Allerton Press": u"Allerton Press, Inc.",
                    "American Agricultural Economics Association": u"Agricultural & Applied Economics Association",
                    "American Midland Naturalist": u"American Midland Naturalist Journal",
                    "Association for Tropical Biology": u"Association for Tropical Biology and Conservation",
                    "Universiti Islam Antarabangsa Malaysia": u"International Islamic University Malaysia",
                    "Canadian Agricultural Economics and Farm Management Society": u"Canadian Agricultural Economics Society",
                    "Canadian Council of Forest Ministers": u"Canadian Council of Forest Ministers",
                    "Canadian Institute of Forestry.": u"Canadian Institute of Forestry",
                    "Canadian Institute of Resources Law": u"Canadian Institute of Resources Law - University of Calgary",
                    "CEIDA": u"Centro de Extensión Universitaria e Divulgación Ambiental de Galicia",
                    u"Universidad nacional autonoma de México": u"Universidad Nacional Autónoma de México",
                    "Centro Internacional de Agricultura Tropical": u"International Center for Tropical Agriculture",
                    "CIHEAM": u"International Center for Advanced Mediterranean Agronomic Studies",
                    "IMIDA": u"Instituto Murciano de Investigación y Desarrollo Agrario y Alimentario",
                    "SUDOE Interreg IVB (EU-ERDF)": u"Programa Interreg Sudoe",
                    "CIHEAM-IAMZ, Zaragoza (Spain), Ondokuz Mayis University, Samsun (Turkey)": u"International Center for Advanced Mediterranean Agronomic Studies",
                    "CIMMYT": u"International Maize and Wheat Improvement Center",
                    "Edition of Journal of Economy and entrepreneurship": u"Journal of Economy and entrepreneurship",
                    "University of Zagreb": u"University of Zagreb",
                    "Universiti Kebangsaan Malaysia": u"Universiti Kebangsaan Malaysia",
                    "Forest Research Institute Malaysia": u"Forest Research Institute Malaysia",
                    "Global Forest Watch": u"Global Forest Watch",
                    "World Resources Institute": u"World Resources Institute",
                    "Humboldt Field Research Institute": u"Eagle Hill Institute",
                    "International Institute for Environment and Development": u"International Institute for Environment and Development",
                    "Tanzania Natural Resource Forum": u"Tanzania Natural Resource Forum",
                    "Kmetijsko gozdarska zbornica Slovenije": u"Chamber of Agriculture and Forestry of Slovenia",
                    "Malaysia Agricultural Research and Development Institute": u"Malaysian Agricultural Research and Development Institute",
                    "Nordic Council for Wildlife Research (NKV)": u"Nordic Board for Wildlife Research",
                    "NRC Research Press": u"NRC Research Press",
                    "Royal Zoological Society of NSW": u"Royal Zoological Society of New South Wales",
                    "RUFORUM": u"Regional Universities Forum for Capacity Building in Agriculture",
                    "SERIDA": u"Servicio Regional de Investigación y Desarrollo Agroalimentario",
                    "Raptor Research Foundation": u"Raptor Research Foundation",
                    "Society for Range Management": u"Society for Range Management",
                    "Society for the Study of Amphibians and Reptiles": u"Society for the Study of Amphibians and Reptiles",
                    "U.S. Dept. of Agriculture": u"U.S. Department of Agriculture",
                    "United States Government Publishing Office": u"United States Government Publishing Office",
                    "United States, Dept. of Agriculture": u"U.S. Department of Agriculture",
                    "University of Gembloux": u"Gembloux Agro-Bio Tech",
                    "USDA Forest Service": u"United States Department of Agriculture - Forest service",
                    "USDA": u"U.S. Department of Agriculture",
                    "Versita": u"De Gruyter Open",
    }

    if utils.unicode_malformed(publisher):
        publisher = utils.get_unicode_from_unicode_malformed(publisher) #generate str
    for pattern, curated_publisher in dict_pattern.iteritems():
        if pattern in publisher:
            clean_publishers.add(curated_publisher)
    if not clean_publishers: # in case there is NO pattern match, add the initial publisher
        clean_publishers.add(publisher)
    return list(clean_publishers)

"""
Returns True if the source is valid (it is not in the black list
"""
def filtered_resource_by_multiple_fields(agris_resource):
    flag_to_maintain = True
    source_blacklist = ["http://ring.ciard.net/node/10767", "Italy (FAO)",
                        "http://ring.ciard.net/node/10851", "United States of America (The World Bank)",
                        "http://ring.ciard.net/node/11204", "Italy (Bioversity)",
                        "http://ring.ciard.net/node/2754", "Italy (GFAR)",
                        "http://ring.ciard.net/node/19749", "Netherlands (Technical Centre for Agricultural and Rural Coope)",
                        "http://ring.ciard.net/node/19451", "United States of America (Open Knowledge Repository, OKR)",
                        "http://ring.ciard.net/node/10695", "Indonesia (CIFOR)",
                        "http://ring.ciard.net/node/19685", "United States of America (International Food Policy Research I)",
                        "http://ring.ciard.net/node/10885", "United States of America (IFPRI)",
                        ]
    publisher_corporate_author_blacklist = ["FAO", "Food and Agriculture Organization",
                           "ILRI", "International Livestock Research Institute",
                           "IWMI", "International Water Management Institute",
                           "IIMI", "International Irrigation Management Institute",
                           "CIFOR", "Center for International Forestry Research",
                           "World Bank",
                           ]

    type_blacklist = ["Numerical data", "Other", "Non-Conventional"]

    uri_blacklist = ["http://hdl.handle.net/10568/", "http://hdl.handle.net/10986/"]


    if ("dc:type" not in agris_resource):
        flag_to_maintain = False
    elif agris_resource["dc:type"] in type_blacklist:
        flag_to_maintain = False

    # remove the ones without title
    if (flag_to_maintain) and ("dc:title" not in agris_resource):
        flag_to_maintain = False

    # removes the one without external link
    if ("dc:identifier" not in agris_resource):
        flag_to_maintain = False
    else:
        for identifier in agris_resource["dc:identifier"]:
            if identifier["@scheme"]=="dcterms:URI":
                resource_url = identifier["#text"]
                if any(uri_blacklisted in resource_url for uri_blacklisted in uri_blacklist):
                    flag_to_maintain = False

    if (flag_to_maintain) and ("dc:source" in agris_resource):
        for source in agris_resource["dc:source"]:
            if source in source_blacklist:
                flag_to_maintain = False

    if (flag_to_maintain) and ("dc:publisher" in agris_resource) and ("ags:publisherName" in agris_resource["dc:publisher"]):
        for publisher in agris_resource["dc:publisher"]["ags:publisherName"]:
            if any(publisher_blacklisted in publisher for publisher_blacklisted in publisher_corporate_author_blacklist):
                flag_to_maintain = False

    if (flag_to_maintain) and ("dc:creator" in agris_resource) and ("ags:creatorCorporate" in agris_resource["dc:creator"]):
        for creator in agris_resource["dc:creator"]["ags:creatorCorporate"]:
            if any(publisher_blacklisted in creator for publisher_blacklisted in publisher_corporate_author_blacklist):
                flag_to_maintain = False

    return flag_to_maintain

def process_agris_resource(agris_resource):
    all_resources.add(agris_resource["@ags:ARN"]) #debug
    if filtered_resource_by_multiple_fields(agris_resource):
        selected_resources.add(agris_resource["@ags:ARN"])
        llrs.add(create_llr_from_AGRIS_XML(agris_resource))
        #process_agris_subject(agris_resource)


def process_agris_subject(agris_resource):
    subject="dc:publisher"
    sub_subject="ags:publisherName"
    if subject in agris_resource:
        subject_value= agris_resource[subject][sub_subject]
        #print subject_value
        if isinstance(subject_value, list):
            for v in subject_value:
                subjects_set.add(v)
        else:
            subjects_set.add(agris_resource[subject][sub_subject])

def from_ags_to_json(filename):
    with io.open(filename, encoding='utf-8') as fd:
        doc = xmltodict.parse(fd.read(), force_list={'ags:resource': True, 'dc:subject': True, 'ags:subjectThesaurus': True, 'ags:subjectClassification': True, 'dc:identifier': True, 'dc:language': True, 'ags:citationNumber': True, 'ags:creatorPersonal': True, 'ags:creatorCorporate': True, 'ags:publisherName': True})
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

def generate_csv(llrs, filename):
    with io.open(filename,'w', encoding='utf-8-sig') as csv_file: #UTF-8 BOM
        #csv_file.write((u'\ufeff').encode('utf8')) #BOM
        headers = u"ID;Title;Subtitle;Abstract/Description;Authors;Corporate authors;Publishers;Data provider;Publicaton date (YYYY/MM);Language;Related concepts;Themes;Overarching Categories;Geographical focus;Resource types;Link to the original website;Link to the publication;Thumbnail;License;Copyright details;Pages\n"
        csv_file.write(headers)

        for llr in llrs:
            if (not llr.get_description()) and (not llr.get_concepts()):
                pass # No description and not LandVoc concepts
            else:
                csv_file.write(llr.as_csv_line())
        csv_file.close()

agris_files = glob.glob("agris-search-results/*.xml")
#top5 = itertools.islice(agris_files, 3)
selected_resources = set()
all_resources = set()
subjects_set = set()
for agris_file in agris_files:
    print "----------------"
    print agris_file
    process_agris_xml_file(agris_file)
    print "ALL-Land-related resources="+str(len(all_resources))
    print "FILTERED-Land-related resources="+str(len(selected_resources))
    print "LLRS="+str(len(llrs))
    print "----------------"
print set_to_get
print list_to_get
for item in list_to_get:
    print item
# for item in set_to_get:
#     if not utils.getISO639_1code(lang):
#         if not utils.getISO639_1code_from_ISO639_3code(lang):
#             print lang
#              "----------------"

timestr = time.strftime("%Y%m%d-%H%M%S")
filename_output = timestr+"-agris.csv"
generate_csv(llrs, filename_output)


#print "Len subjects_set="+str(len(subjects_set))
#utils.save_set_in_file("publishers-agris.csv", subjects_set)
#     target_filename=str(year)+"-agris-harvested.json"
#     with open(target_filename, 'w') as target:
#         print "Opening the file="+target_filename
#         for resource in resources:
#             target.write(json.dumps(resource.get_resource())+",")
#         print "Closed the file="+target_filename


