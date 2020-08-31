#!/usr/bin/python
# -*- coding: UTF-8 -*-
from RISparser import readris
from landvoc import LandVoc
from llr.LandLibraryResource import LandLibraryResource
from llr import utils as llrutils
import glob

from landvocLANDJOURNAL.LandVocLANDJOURNAL import LandVocLANDJOURNAL
LANDVOC_LANDJOURNAL = LandVocLANDJOURNAL()

LANDVOC = LandVoc()

concepts_list = []
llrs = set()

def curate_RIS_MDI_file(filename):
    write_filename = "new-"+filename
    with open(filename, encoding="utf-8") as bibliography_file:
        new_bibliography_file = open(write_filename, "w", encoding="utf-8")
        content = bibliography_file.readlines()
        record = 0
        for line in content:
            if "TY  - EJOU" in line:
                if record == 0:
                    record = 1
                else:
                    new_bibliography_file.write("ER  - \n\n")
            new_bibliography_file.write(line)
        new_bibliography_file.write("ER  - ") #latest
        new_bibliography_file.close()

    return write_filename

def create_llrs(filename):

    curated_filename = curate_RIS_MDI_file(filename)

    with open(curated_filename, 'r', encoding="utf-8") as bibliography_file:
        # using https://pypi.python.org/pypi/RISparser
        entries = readris(bibliography_file)
        for entry in entries:
            llrs.add(create_llr_from_RIS(entry))

    print("**********************************")
    print("new records (Set)= %d" %(len(llrs)))
    return llrs


def create_llr_from_RIS(ris_entry):
    llr_record = LandLibraryResource()

    #type. Only one
    if ris_entry["type_of_reference"]=="EJOU":
        llr_record.set_types([u"Peer-reviewed publication"])

    #title. Only one
    title = ris_entry["title"]
    llr_record.set_title(title)

    #subtitle

    # description
    description = ris_entry["abstract"]
    llr_record.set_description(description)

    #author. One or more
    authors = ris_entry["authors"]
    llr_record.set_authors(authors)

    #corporate_authors. Could be more than one

    #publishers. One or more (and more could be in the same item or in a different one
    publishers = [u"Land Journal"]
    llr_record.set_publishers(publishers)

    #ID. Only one.
    doi = ris_entry["doi"]
    llr_record.set_id(doi)

    #number of pages. Only one

    #date.
    year = ris_entry["year"] # format (YYYY)
    issue = ris_entry["number"]
    month = issue
    if int(year) < 2019:
        switcher_pre_2019 = {
            "1": "03",
            "2" : "06",
            "3" : "09",
            "4" : "12",
        }
        month = switcher_pre_2019.get(issue, "2")
    publish_date = llrutils.clean_date(year+"-"+month)# format (YYYY-MM-DD)
    llr_record.set_date(publish_date)


    volume = ris_entry["volume"]
    init_page=str(int(doi[-4:]))
    original_url = "http://www.mdpi.com/2073-445X/"+volume+"/"+issue+"/"+init_page+"/"
    resource_url = original_url+"pdf"

    #original url. Only one
    llr_record.set_original_url(original_url)

    #resource url. Only one
    llr_record.set_resource_url(resource_url)


#     #plan B
#     resource_url = "http://dx.doi.org/"+doi
#     resp = requests.head(resource_url)
#     location = resp.headers["Location"]

    #License
    llr_record.set_license(u"Creative Commons Attribution")

    #Copyright details
    copyright_details = u"© "+year+" by the authors; licensee MDPI, Basel, Switzerland. This article is an open access article."
    llr_record.set_copyright_details(copyright_details)

    #data provider
    llr_record.set_data_provider(u"Land Journal")

    #image
    #image_path = "private://feeds/cover-land-v"+volume+"-i"+issue+".png"
    image_url = "https://www.mdpi.com/data/covers/land/cover-land-v"+volume+"-i"+issue+".png"
    llr_record.set_image(image_url)
    #llr_record.set_image("private://feeds/LandJournal-thumbnail.png")

    #keywords
    keywords = ris_entry["keywords"]
    concepts_list.extend(keywords)

    llr_record.set_potential_list(keywords)

    #geographical focus. list
    final_places = set()
    final_places |= set(llrutils.flatten3(filter(None,[llrutils.getISO3166_1code(k) for k in keywords])))
    final_places |= set(llrutils.flatten3(filter(None,[llrutils.getUNM49code(k) for k in keywords])))
    
    #NLTK for geo
    if not final_places:
        final_places |= set(llrutils.getPlaceET_fromText_NLTK(llr_record.get_title())) | set(llrutils.getPlaceET_fromText_GeoText(llr_record.get_title())) 
        final_places |= set(llrutils.getPlaceET_fromText_NLTK(llr_record.get_description())) | set(llrutils.getPlaceET_fromText_GeoText(llr_record.get_description())) 

    final_places = set(filter(None,llrutils.flatten3(final_places)))

    if not final_places:
        final_places.add("001")

    llr_record.set_geographical_focus(final_places)

    concepts = LANDVOC.get_concepts_direct(keywords)
    
    synonyms = LANDVOC.get_concepts_synonymsEN(keywords)

    concepts.extend(synonyms)

    landjournal_mapping = set(LANDVOC_LANDJOURNAL.get_concepts_landjournal_related(keywords))

    #parse the title
    for concept in LANDVOC.parse_get_concepts(title):
        if concept != "land":
            concepts.append(LANDVOC.get_EnglishPrefLabel(concept,lang="en"))
    
    concepts.extend(landjournal_mapping)
    
    if concepts:
        concepts = set(concepts)
    else:
        concepts = set([u"land",u"research"])

    themes=LANDVOC.get_fixed_themes(concepts)

    llr_record.set_concepts(concepts)
    llr_record.set_themes(themes)

    #Language
    langs = [u"en"]
    llr_record.set_languages(langs)

    # Add journal volumen
    subtitle = "Volume "+volume+" Issue "+issue
    llr_record.set_subtitle(subtitle)

    return llr_record

def generate_csv(llrs, filename):
    with open(filename,'w', encoding="utf-8") as csv_file:
        #csv_file.write((u'\ufeff').encode('utf8')) #BOM
        # TODO: change headers
        headers = LandLibraryResource.get_csv_header_line()
        csv_file.write(headers)

        for llr in llrs:
            #print llr.__dict__
            csv_file.write(llr.as_csv_line())
        csv_file.close()


###############################################################################

# llrs = create_llrs('land-v01-i01_20170608.ris')
# generate_csv(llrs, 'land-v01-i01_20170608.csv')
#
# llrs = create_llrs('land-v02-i04_20170608.ris')
# generate_csv(llrs, 'land-v02-i04_20170608.csv')

ris_files = glob.glob("land*.ris")
for ris_file in ris_files:
    print(ris_file)
    create_llrs(ris_file)
    generate_csv(llrs, ris_file+'.csv')
    llrs = set()
    
print(concepts_list)
more_than_one = [{x:concepts_list.count(x)} for x in set(concepts_list) if concepts_list.count(x)>1]
more_than_one_flat = [list(e.keys())[0] for e in more_than_one]
print(more_than_one_flat)

already_in_csv = list()
import csv
with open('landvocLANDJOURNAL\land_journal-relations.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    for row in csv_reader:
        already = row[0]
        already_in_csv.append(already)

for x in more_than_one_flat:
    if x not in already_in_csv and x not in LANDVOC.get_concepts():
        print(x)


