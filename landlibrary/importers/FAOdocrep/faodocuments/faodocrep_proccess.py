#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
import utils
from llr.LandLibraryResource import LandLibraryResource
import llr.utils as llrutils
import glob
import landvoc
from LandVocFAODOCREP.LandVocFAODOCREP import LandVocFAODOCREP
import io
import time

LANDVOC = landvoc.LandVoc()
LandVocFAODOCREP = LandVocFAODOCREP()

def get_faodocrepId_from_file():
    id_list = set()
    with open("2017-FAODOCREP.csv") as f:
        for row in f:
            id_list.add(row.rstrip().replace("FAODOCREP:",""))
    return id_list
    

def get_records():

    documents_already_ingested = get_faodocrepId_from_file()

    faodocrep_files = glob.glob("results/all-results+*.json")

    resultDict= {}

    for faodocrep_file in faodocrep_files:
        print "----------------"
        print "processing="+faodocrep_file

        with open(faodocrep_file) as data_file:
            results = json.load(data_file)
            for result in results:
                uuid = get_value_metatag(result, 'uuid')
                if uuid not in documents_already_ingested:
                    resultDict[uuid] = result
            print "**********************************"
            print "new records (Set)= %d" %(len(resultDict))
    return resultDict

def get_value_metatag(result, name):
    return next(iter([x['MT']['V'] for x in result['R']['mts'] if x['MT']['N']==name]), None)

def get_values_metatag(result, name):
    return [x['MT']['V'] for x in result['R']['mts'] if x['MT']['N']==name]

def generate_aditional_text(titles, dates, label, lang ):
    xstr = lambda s: s or u""
    text=""
    for title, date in zip(titles, dates):
        text += "\n"+_(label, lang)+title+" ("+xstr(date)+")"
    return text

def create_llrs(resultDict):
    llrs = []
    for key, value in resultDict.iteritems():
        llr = LandLibraryResource()

        #title. Only one
        title = get_value_metatag(value, 'Title')
        llr.set_title(title)

        #subtitle.
        subtitle = get_value_metatag(value, 'subtitle')
        if subtitle:
            llr.set_subtitle(subtitle)
        
        # compound, because it can be splitted in several abstracts (present in 98 records)
        description = "".join([x['MT']['V'] for x in value['R']['mts'] if x['MT']['N']=='abstract'])
        llr.set_description(description)

        #author. Only one
        author_en = get_value_metatag(value, 'author_en')
        author_author = get_value_metatag(value, 'Author')
        personalAuthor_en = get_value_metatag(value, 'personalAuthor_en')
        corporateAuthor_en = get_value_metatag(value, 'corporateAuthor_en')
        department_en = get_value_metatag(value, 'department_en')

        possible_authors = [author_en, author_author, personalAuthor_en, corporateAuthor_en, department_en]
        authors = utils.generate_authors(possible_authors)
        
        llr.set_authors(authors)
        corporate_authors_AND_publishers = utils.generate_organizations(possible_authors)
        llr.set_corporate_authors(corporate_authors_AND_publishers)
        llr.set_publishers(corporate_authors_AND_publishers)

        #type. Only one
        docType = get_value_metatag(value, 'docType')
        docTypes = utils.get_types(docType)
        llr.set_types(docTypes)

        if not description and docType=="Meeting":
            meeting_en = get_value_metatag(value, 'meeting_en')
            meetingDocSymbol = get_value_metatag(value, 'meetingDocSymbol')
            session = get_value_metatag(value, 'session')
            if meeting_en:
                description = description + "Meeting Name: " + meeting_en
            if meetingDocSymbol:
                description = description + "\nMeeting symbol/code: " + meetingDocSymbol
            if session:
                description = description + "\nSession: " + session
            llr.set_description(description)


        #resource_url. Only one
        resource_url = value['R']['U']
        llr.set_resource_url(resource_url)

        #ID. Only one
        uuid = get_value_metatag(value, 'uuid')
        final_id = "FAODOCREP:"+uuid
        llr.set_id(final_id)

        #original url. Only one
        cardURL = get_value_metatag(value, 'cardURL')
        llr.set_original_url(cardURL)


        #metadata language. Only one
        # gsaentity_google_language = get_value_metatag(value, 'gsaentity_google_language') # language of the metadata (label)
        _lang = value['R']['LANG'] # language of the metadata (ISO code)
        llr.set_metadata_language(_lang)
        
        languages = set()
        
        _defaultLanguage = get_value_metatag(value, "defaultLanguage")
        if len(_defaultLanguage) == 2:
            languages.add(_defaultLanguage)
        else:
            languages.add(_lang)  
        #languages of the resource. Could be more than one value
        # defaultLanguage = get_value_metatag(value, 'defaultLanguage') #  language of the metadata (label). Not working for multiple languages
        #allLanguages = get_values_metatag(value, "allLanguages") # languages of the resources (ISO codes)
        #allLanguages = map(unicode.lower, allLanguages)

        #languages |= set(allLanguages)
        languages = filter(lambda x : len(x) ==2 , languages) # filter languages only with 2 letters
        llr.set_languages(languages)

        #number of pages. Only one
        page_count = get_value_metatag(value, 'pages')
        if page_count:
            page_count = page_count.replace(" p.","")
        llr.set_number_pages(page_count)

        #License
        llr.set_license("All rights reserved")

        #Copyright details
        if llr.metadata_language == "S":
            llr.set_copyright_details(u"© FAO. Para garantizar la amplia difusión de su información, la FAO se ha comprometido a poner libremente a disposición de los interesados este contenido y alienta el uso, la reproducción y la difusión de los textos, productos multimedia y datos presentados. Salvo que se indique lo contrario, el contenido se puede copiar, imprimir y descargar con fines de estudio privado, investigación y docencia, y para uso en productos o servicios no comerciales, siempre que se reconozca de forma adecuada a la FAO como fuente y titular de los derechos de autor  y que no se indique o que ello implique en modo alguno que la FAO aprueba los puntos de vista, productos o servicios de los usuarios.")
        elif llr.metadata_language == "F":
            llr.set_copyright_details(u"© FAO. Afin d’assurer une large diffusion de ses informations, la FAO s’attache à donner libre accès à ce contenu et encourage l’utilisation, la reproduction et la diffusion des données, des informations textuelles et des supports multimédia présentés. Sauf indication contraire, le contenu peut être reproduit, imprimé et téléchargé aux fins d’étude privée, de recherches ou d’enseignement ainsi que pour utilisation dans des produits ou services non commerciaux, sous réserve que la FAO soit correctement mentionnée comme source et comme titulaire du droit d’auteur et à condition qu’il ne soit ni déclaré ni sous-entendu en aucune manière que la FAO approuverait les opinions, produits ou services des utilisateurs.")
        else:
            llr.set_copyright_details(u"© FAO. FAO is committed to making its content freely available and encourages the use, reproduction and dissemination of the text, multimedia and data presented. Except where otherwise indicated, content may be copied, printed and downloaded for private study, research and teaching purposes, and for use in non-commercial products or services, provided that appropriate acknowledgement of FAO as the source and copyright holder is given and that FAO's endorsement of users' views, products or services is not stated or implied in any way.")

        #data provider
        llr.set_data_provider(u"Food and Agriculture Organization of the United Nations (FAO)")

        #date.
        publicationDate = str(get_value_metatag(value, 'publicationDate'))
        if publicationDate.startswith("Dec 2012"):
            publicationDate = "12/2012"
        publicationDate = "".join(publicationDate.split()) #remove all whitespaces
        publicationDate = publicationDate.replace("//", "/") #replace duplicated symbol '/'
        publicationDate = publicationDate.translate(None, '[]')
        if len(publicationDate) == 4: #just the year
            publicationDate = ("12/")+publicationDate

        #change order to be YYYY-MM        
        final_date = publicationDate.split("/")[1]+ "-" + publicationDate.split("/")[0]
        
        final_date = llrutils.clean_date(final_date)
        llr.set_date(final_date)

        #geographical focus. list
        gsaentity_Country = get_value_metatag(value, 'gsaentity_Country')
        country_id_list = set(get_values_metatag(value, 'country_en') + (gsaentity_Country.split(',') if gsaentity_Country else list()))
        country_iso_list = set()
        for country in country_id_list:
            country_iso_list.add(utils.getISO3166_1_alpha3_code(country))

        region_en_list = get_values_metatag(value, 'region_en')        
        region_m49_list = set()
        for region in region_en_list:
            region_m49_list.add(utils.getUNM49code(unicode(region).title()))

        llr.set_geographical_focus(country_iso_list, region_m49_list)

        #landvoc concepts
        potential_concepts = get_values_metatag(value, 'agrovoc_en')
        #direct_mapping = LandVocFAODOCREP.get_concepts_direct(potential_concepts)
        direct_mapping = LANDVOC.get_concepts_direct(potential_concepts)
        related_mapping = LandVocFAODOCREP.get_concepts_faolex_related(potential_concepts)
        concepts_harvest_enhancement = LandVocFAODOCREP.get_concepts_harvest_enhancement(potential_concepts)
        concepts = set(direct_mapping+related_mapping+concepts_harvest_enhancement)
        concepts = filter(None,concepts)
        concepts = map(unicode,concepts)

        llr.set_concepts(concepts);
        
#         #Overarching categories
#         oacs = LandVocFAODOCREP.get_oacs_harvest_enhancement(potential_concepts)
#         oacs |= LANDVOC.get_fixed_oacs(concepts)        
#         llr.set_overarching_categories(oacs)

        #Themes
        themes = LandVocFAODOCREP.get_themes_harvest_enhancement(potential_concepts)
        themes |= LANDVOC.get_fixed_themes(concepts)
        llr.set_themes(themes)
        
        #Thumbnail
        thumbnail = get_value_metatag(value, 'thumb200')
        llr.set_image(thumbnail)
        llrs.append(llr)


#     #set of langs
#     print sorted(dates, key=lambda s: s.lower())
# 
#     # stats
#     for item in sorted(set(no_desc), key=lambda s: s.lower()):
#         print "%s;%d" %(item, no_desc.count(item))

    print "**********************************"
    return llrs

def generate_csv(llrs, filename_output):
    with io.open(filename_output,'w', encoding='utf-8-sig') as csv_file: #UTF-8 BOM
        headers = LandLibraryResource.get_csv_header_line()
        csv_file.write(headers)
        for llr in llrs:
            csv_file.write(llr.as_csv_line())
        csv_file.close()

###############################################################################

#create_all_file()
new_records = get_records()
llrs = create_llrs(new_records)

timestr = time.strftime("%Y%m%d-%H%M%S")
filename_output = timestr+"-faodocrep-processed.csv"
generate_csv(llrs, filename_output)
