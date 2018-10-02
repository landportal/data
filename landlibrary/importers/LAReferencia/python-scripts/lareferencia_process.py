#!/usr/bin/python
# -*- coding: UTF-8 -*-
import glob
import itertools
import landvoc
import time
import io
import json
from llr.LandLibraryResource import LandLibraryResource
import llr.utils as llrutils
import utils
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

LANDVOC = landvoc.LandVoc()
llrs=set()
formats_set= set()

def create_llr_from_lareferencia_record(lareferencia_record):
    llr = LandLibraryResource()


    #ID. Only one.
    internal_id = lareferencia_record["id"]
    llr.set_id(u"LaReferencia:"+internal_id)
    
    
    #title. One
    title = lareferencia_record["title"]
    llr.set_title(title)

    
    #subtitle. Zero or One
    if "subtitle" in lareferencia_record:
        subtitle = lareferencia_record["subtitle"]
        llr.set_subtitle(subtitle)


    # description. Zero or One
    if "summary" in lareferencia_record:
        description = lareferencia_record["summary"][0]
        if description:
            llr.set_description(description)
    
    #Language. Zero, one or more
    langs_cleared = set()
    if "languages" in lareferencia_record:
        languages = lareferencia_record["languages"]
        
        for lang in languages:
            langs_cleared.add(llrutils.getISO639_1code_from_ISO639_3code(lang))
        langs_cleared = set(filter(None,langs_cleared))
    
    if not langs_cleared:        
        try:
            potential_lang = detect(title.lower())
            if potential_lang in ["es", "pt", "en"]:
                langs_cleared.add(potential_lang)
        except LangDetectException:
            pass
    llr.set_languages(langs_cleared)

    #author. One or more
    authors = lareferencia_record["primaryAuthors"]
    if "secondaryAuthors" in lareferencia_record:
        authors+=lareferencia_record["secondaryAuthors"]
    llr.set_authors(authors)
    

    #corporate_authors. Could be more than one
    if "corporateAuthors" in lareferencia_record:
        llr.set_corporate_authors(lareferencia_record["corporateAuthors"])


    #publishers. Zero, one or more
    if "dc.publisher.none.fl_str_mv" in lareferencia_record["rawData"]:
        llr.set_publishers(filter(None,{utils.getPublisher(pub) for pub in lareferencia_record["rawData"]["dc.publisher.none.fl_str_mv"]}))

    #type. One
    types= set()
    formats = lareferencia_record["formats"]
    types.add(utils.getLLR_type(formats[0]))
    if "dc.type.none.fl_str_mv" in lareferencia_record["rawData"]:
        for f in lareferencia_record["rawData"]["dc.type.none.fl_str_mv"]:
            if f=="Artículos de congreso":
                types.add("Conference Papers & Reports")
            if f=="Articulo evaluado por dos pares" or f=='artículos evaluados por pares'  or f=='Artículo evaluado por pares ciegos y producto de investigación' or f=='Artículo evaluado por pares' or f=="Art?culo revisado por pares" or f=='Artículo revisado por pares':
                types.add("Peer-reviewed publication")
    llr.set_types(list(types))

    #number of pages. Only one
    #If there is a last page, there is an initial page
    if "dc.description.lastpage.pt.fl_txt_mv" in lareferencia_record["rawData"]:
        lastpage = lareferencia_record["rawData"]["dc.description.lastpage.pt.fl_txt_mv"][0]
        initialpage = lareferencia_record["rawData"]["dc.description.initialpage.pt.fl_txt_mv"][0]
        number_pages = int(lastpage) - int(initialpage)
        if number_pages:
            llr.set_number_pages(number_pages)

    #date.
    publicationDates = lareferencia_record["publicationDates"][0]
    best_date = publicationDates
    if "dc.date.none.fl_str_mv" in lareferencia_record["rawData"]:
        for potentialDate in lareferencia_record["rawData"]["dc.date.none.fl_str_mv"]:
            if publicationDates in potentialDate:
                best_date = utils.clean_date(potentialDate.split("T")[0])
    llr.set_date(utils.clean_date(best_date))


    #original url. Only one
    lareferencia_url = "http://www.lareferencia.info/vufind/Record/"+internal_id
    llr.set_original_url(lareferencia_url)


    #resource url. Only one. Remove locahost
    resource_url = None
    if "bitstream.url.fl_str_mv" in lareferencia_record["rawData"]:
        potential_urls = lareferencia_record["rawData"]["bitstream.url.fl_str_mv"]
        if len(potential_urls)==1 and ("://localhost" not in potential_urls[0]):
            resource_url = potential_urls[0]
        else:
            for url in potential_urls:
                if "://localhost" in url:
                    continue
                if url.endswith(".pdf") or url.endswith(".PDF"):
                    resource_url = url
            if not resource_url and ("://localhost" not in url):
                resource_url = potential_urls[0] # arbitray. Take the first one
    elif "url" in lareferencia_record["rawData"]:
        resource_url = lareferencia_record["rawData"]["url"][0]

    llr.set_resource_url(resource_url)

    #License
    license_llr = None
    copyright_details = None
    if "dc.rights.none.fl_str_mv" in lareferencia_record["rawData"]:
        for potential_license in lareferencia_record["rawData"]["dc.rights.none.fl_str_mv"]:
            if not llrutils.checkOpenAccess(potential_license):
                return None # STOP. Return None
            if "info:eu-repo/semantics/openAccess" in potential_license:
                copyright_details = "info:eu-repo/semantics/openAccess : Open Access, this refers to access without restrictions, and without financial incentives. Access to the resource is gained directly, without any obstacles." #From https://wiki.surfnet.nl/display/standards/info-eu-repo/#info-eu-repo-AccessRights    if "rights_invalid_str_mv" in lareferencia_record["rawData"]:
    if "rights_invalid_str_mv" in lareferencia_record["rawData"]:
        for potential_license in lareferencia_record["rawData"]["rights_invalid_str_mv"]:
            if not llrutils.checkOpenAccess(potential_license):
                return None # STOP. Return None
            if "Copyright" in potential_license:
                copyright_details = potential_license
            if "creativecommons.org" in potential_license:
                license_llr = llrutils.getCCLicenseAcronym(potential_license)
            if "info:eu-repo/semantics/openAccess" in potential_license and not copyright_details:
                copyright_details = "info:eu-repo/semantics/openAccess : Open Access, this refers to access without restrictions, and without financial incentives. Access to the resource is gained directly, without any obstacles." #From https://wiki.surfnet.nl/display/standards/info-eu-repo/#info-eu-repo-AccessRights    if "rights_invalid_str_mv" in lareferencia_record["rawData"]:
    if "dc.rights.driver.fl_str_mv" in lareferencia_record["rawData"]:
        for potential_license in lareferencia_record["rawData"]["dc.rights.driver.fl_str_mv"]:
            if not llrutils.checkOpenAccess(potential_license):
                return None # STOP. Return None
            if "Copyright" in potential_license:
                copyright_details = potential_license
            if "creativecommons.org" in potential_license:
                license_llr = llrutils.getCCLicenseAcronym(potential_license)
            if "info:eu-repo/semantics/openAccess" in potential_license and not copyright_details:
                copyright_details = "info:eu-repo/semantics/openAccess : Open Access, this refers to access without restrictions, and without financial incentives. Access to the resource is gained directly, without any obstacles." #From https://wiki.surfnet.nl/display/standards/info-eu-repo/#info-eu-repo-AccessRights    if "rights_invalid_str_mv" in lareferencia_record["rawData"]:
    llr.set_license(license_llr)
    llr.set_copyright_details(copyright_details)

    #data provider
    llr.set_data_provider(u"LA Referencia")

    #image
    #llr.set_image("")

    #keywords
    potential_subjects=set()
    for subject in lareferencia_record["subjects"]:
        potential_subjects.add(LANDVOC.get_EnglishPrefLabel(subject[0],lang="es"))
        potential_subjects.add(LANDVOC.get_EnglishPrefLabel(subject[0],lang="en"))
        potential_subjects.add(LANDVOC.get_EnglishPrefLabel(subject[0],lang="pt"))

    concepts = [unicode(s, "utf-8") for s in filter(None,potential_subjects)]
    themes=LANDVOC.get_fixed_themes(concepts)
    oacs=LANDVOC.get_fixed_oacs(concepts)

    llr.set_concepts(concepts);
    llr.set_themes(themes);
    llr.set_overarching_categories(oacs);

    #geographical focus. list
    countries_focus = set()
    countries_focus |= set(utils.getPlaceET_fromText_NLTK(llr.title)) | set(utils.getPlaceET_fromText_GeoText(llr.title))
    countries_focus |= set(utils.getPlaceET_fromText_NLTK(llr.description)) | set(utils.getPlaceET_fromText_GeoText(llr.description))
    for subject in lareferencia_record["subjects"]:
        countries_focus |= set(utils.getPlaceET_fromText_NLTK(subject[0])) | set(utils.getPlaceET_fromText_GeoText(subject[0]))
    llr.set_geographical_focus(countries_focus, set())
    
    return llr

###################################################################################

def process_lareferencia_record(lareferencia_record):
    record_title = lareferencia_record["title"]
    if record_title not in all_records_title:
        all_records_title.add(record_title) #debug
        # TODO FILTER OUT
        llrs.add(create_llr_from_lareferencia_record(lareferencia_record))


counter = 0

def process_lareferencia_json_file(filename):
    with open(filename) as fd: #usaban io.open por temas de codificacion
        data = json.load(fd)
        for record in data:
            global counter
            counter+=1
            if (counter%100 ==0):
                pass
                #print "Analyzing record #"+str(counter)
            process_lareferencia_record(record)

def generate_csv(llrs, filename):
    with io.open(filename,'w', encoding='utf-8-sig') as csv_file: #UTF-8 BOM
        #csv_file.write((u'\ufeff').encode('utf8')) #BOM
        headers = u"ID;Title;Subtitle;Abstract/Description;Authors;Corporate authors;Publishers;Data provider;Publicaton date (YYYY/MM);Language;Related concepts;Themes;Overarching Categories;Geographical focus;Resource types;Link to the original website;Link to the publication;Thumbnail;License;Copyright details;Pages\n"
        csv_file.write(headers)

        for llr in llrs:
            if (not llr.get_description()) or (len(llr.get_concepts())<1) or (len(llr.get_geographical_focus())<1) or (len(llr.get_concepts())==1 and (llr.get_concepts()[0] in ["assessment", "territory", "land", "poverty", "development"])):
                pass
            else:
                csv_file.write(llr.as_csv_line())
        csv_file.close()





lareferencia_files = glob.glob("results/*.json")
#top5 = itertools.islice(agris_files, 3)
#selected_resources = set()
all_records_title = set()

for lareferencia_file in lareferencia_files:
    #print "----------------"
    print lareferencia_file
    process_lareferencia_json_file(lareferencia_file)
    #print "ALL-Land-related resources="+str(len(all_records_title))
    #print "FILTERED-Land-related resources="+str(len(selected_resources))
    #print "LLRS="+str(len(llrs))
    #print "----------------"
llrs = filter(None,llrs)

timestr = time.strftime("%Y%m%d-%H%M%S")
filename_output = timestr+"-lareferencia.csv"
generate_csv(llrs, filename_output)


