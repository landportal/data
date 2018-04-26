#!/usr/bin/python
# -*- coding: UTF-8 -*-
from RISparser import readris
from landvoc import LandVoc
from llr.LandLibraryResource import LandLibraryResource
from llr import utils

LANDVOC = LandVoc()

def curate_RIS_MDI_file(filename):
    write_filename = "new-"+filename
    with open(filename, 'r') as bibliography_file:
        new_bibliography_file = open(write_filename, "w")
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
    
    llrs = set()
    with open(curated_filename, 'r') as bibliography_file:
        # using https://pypi.python.org/pypi/RISparser 
        entries = readris(bibliography_file)
        for entry in entries:
            llrs.add(create_llr_from_RIS(entry))

    print "**********************************"
    print "new records (Set)= %d" %(len(llrs))
    return llrs


def create_llr_from_RIS(ris_entry):
    llr_record = LandLibraryResource()

    #type. Only one
    if ris_entry["type_of_reference"]=="EJOU":
        llr_record.set_type(u"Peer-reviewed publication")

    #title. Only one
    title = ris_entry["title"]
    llr_record.set_title(title.decode('utf-8'))

    #subtitle

    # description
    description = ris_entry["abstract"]
    llr_record.set_description(description.decode('utf-8'))

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
    month = {
        "1": "03",
        "2" : "06",
        "3" : "09",
        "4" : "12",
    }[issue]
    publish_date = year+"-"+month+"-31"# format (YYYY-MM-DD)
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
    llr_record.set_image("private://feeds/LandJournal-thumbnail.png")

    #keywords
    keywords = ris_entry["keywords"]

    #geographical focus. list
    countries = set(utils.flatten(filter(None,[utils.getISO3166_1code(k) for k in keywords])))
    regions = set(utils.flatten(filter(None,[utils.getUNM49code(k) for k in keywords])))
    llr_record.set_geographical_focus(countries, regions)


    concepts = LANDVOC.get_concepts_direct(keywords)
    themes=LANDVOC.get_fixed_themes(concepts)
    oacs=LANDVOC.get_fixed_oacs(concepts)

    llr_record.set_concepts(concepts);
    llr_record.set_themes(themes);
    llr_record.set_overarching_categories(oacs);

    #Language
    lang = u"en"
    llr_record.set_language(lang)
    
    return llr_record

def generate_csv(llrs, filename):
    with open(filename,'w') as csv_file:
        csv_file.write((u'\ufeff').encode('utf8')) #BOM
        headers = u"ID;Title;Subtitle;Abstract/Description;Authors;Corporate authors;Publishers;Data provider;Publicaton date (YYYY/MM);Language;Related concepts;Themes;Overarching Categories;Geographical focus;Resource types;Link to the original website;Link to the publication;Thumbnail;License;Copyright details;Pages\n"
        csv_file.write(headers.encode('utf8'))

        for llr in llrs:
            #print llr.__dict__
            csv_file.write(llr.as_csv_line().encode('utf8'))
        csv_file.close()


###############################################################################

# llrs = create_llrs('land-v01-i01_20170608.ris')
# generate_csv(llrs, 'land-v01-i01_20170608.csv')
# 
# llrs = create_llrs('land-v02-i04_20170608.ris')
# generate_csv(llrs, 'land-v02-i04_20170608.csv')

llrs = create_llrs('land-v07-i01_20180402.ris')
generate_csv(llrs, 'land-v07-i01_20180402.csv')
