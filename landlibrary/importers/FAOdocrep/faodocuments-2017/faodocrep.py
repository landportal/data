#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
import utils
import landvoc
from resources.LandLibraryResource import LandLibraryResource

def cat_json(outfile, infiles):
    file(outfile, "w")\
        .write("[%s]" % (",".join([mangle(file(f).read()) for f in infiles if file(f).read()!="[]"])))

def mangle(s):
    return s.strip()[1:-1]

def create_all_file():
    infiles = ["results/all-results+land productivity.json" , "results/all-results+right of access.json" , "results/all-results+land classification.json" , "results/all-results+forest land use.json" , "results/all-results+pastoral society.json" , "results/all-results+land administration.json" , "results/all-results+geographical information systems.json" , "results/all-results+land registration.json" , "results/all-results+urban agriculture.json" , "results/all-results+land ownership.json" , "results/all-results+land resources.json" , "results/all-results+forest conservation.json" , "results/all-results+pastoralism.json" , "results/all-results+urbanization.json" , "results/all-results+land suitability.json" , "results/all-results+water management.json" , "results/all-results+urban planning.json" , "results/all-results+land cover.json" , "results/all-results+desertification.json" , "results/all-results+sustainable forest management.json" , "results/all-results+urban areas.json" , "results/all-results+land tax.json" , "results/all-results+sustainable land management.json" , "results/all-results+forest grazing.json" , "results/all-results+forest resources.json" , "results/all-results+reforestation.json" , "results/all-results+land management.json" , "results/all-results+land markets.json" , "results/all-results+grassland management.json" , "results/all-results+land degradation.json" , "results/all-results+resource management.json" , "results/all-results+tenure.json" , "results/all-results+land use planning.json" , "results/all-results+private ownership.json" , "results/all-results+water resources.json" , "results/all-results+land rights.json" , "results/all-results+multiple land use.json" , "results/all-results+soil management.json" , "results/all-results+deforestation.json" , "results/all-results+land.json" , "results/all-results+rangelands.json" , "results/all-results+property rights.json" , "results/all-results+land transfers.json" , "results/all-results+land tenure.json" , "results/all-results+valuation.json" , "results/all-results+landowners.json" , "results/all-results+land improvement.json" , "results/all-results+land policies.json" , "results/all-results+farmland.json" , "results/all-results+public ownership.json" , "results/all-results+natural resources.json" , "results/all-results+land reform.json" , "results/all-results+common lands.json" , "results/all-results+spatial database.json" , "results/all-results+housing.json" , "results/all-results+land use.json" , "results/all-results+soil degradation.json" , "results/all-results+water rights.json" , "results/all-results+dryland management.json" , "results/all-results+land access.json" , "results/all-results+indigenous tenure systems.json" , "results/all-results+natural resources management.json" , "results/all-results+forest land.json" , "results/all-results+individual land property.json" , "results/all-results+land use mapping.json" , "results/all-results+forest degradation.json" , "results/all-results+land cover mapping.json"]
    cat_json("ALL.json", infiles)

def get_records():
    with open('ALL.json') as data_file:
        results = json.load(data_file)

#     return
#     tags= list()
#     print len(results)
#     for result in results:
#         for x in result['R']['mts']:
#             tags.append(x['MT']['N'])
#     print "**********************************"
#     #set of tags
#     print sorted(set(tags), key=lambda s: s.lower())
#
#     # stats
#     for tag in sorted(set(tags), key=lambda s: s.lower()):
#         print "%s;%d" %(tag, tags.count(tag))


#     uuid= set()
#     for result in results:
#         uuid.add(get_value_metatag(result, 'uuid'))
#     print len(uuid)
#     print "**********************************"

#     for result in results:
#         type = get_value_metatag(result, 'docType_en')
#         if type=="Meeting":
#             print get_value_metatag(result, 'title')
#     return

    resultDict= {}
    for result in results:
        uuid = get_value_metatag(result, 'uuid')
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
    lv = landvoc.LandVoc()
    llrs = []
    for key, value in resultDict.iteritems():
        llr = LandLibraryResource()

        #title. Only one
        title = get_value_metatag(value, 'title')
        llr.set_title(title)

        #subtitle.
        subtitle = get_value_metatag(value, 'subtitle')
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
        author = llr.generate_author(possible_authors)
        llr.set_author(author)

        corporate_authors_AND_publishers = llr.generate_organizations(possible_authors)
        llr.set_corporate_authors(corporate_authors_AND_publishers)
        llr.set_publishers(corporate_authors_AND_publishers)

        #type. Only one
        docType_en = get_value_metatag(value, 'docType_en')
        llr.set_type(docType_en)

        if not description and docType_en=="Meeting":
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
                
        #languages of the resource. Could be more than one value
        # defaultLanguage = get_value_metatag(value, 'defaultLanguage') #  language of the metadata (label). Not working for multiple languages
        allLanguages = get_values_metatag(value, "allLanguages") # languages of the resources (ISO codes)
        llr.set_languages(allLanguages)

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
        agrovoc_en_list = get_values_metatag(value, 'agrovoc_en')
        llr.set_concepts(agrovoc_en_list, lv);
        
        #Overarching categories
        oacs = lv.get_oacs_harvest_enhancement(agrovoc_en_list)
        llr.set_overarching_categories(oacs)

        #Themes
        themes = lv.get_themes_harvest_enhancement(agrovoc_en_list)
        llr.set_themes(themes)
        
        #Thumbnail
        thumbnail = get_value_metatag(value, 'thumb200')
        llr.set_thumbnail(thumbnail)

        llrs.append(llr)


#     #set of langs
#     print sorted(dates, key=lambda s: s.lower())
# 
#     # stats
#     for item in sorted(set(no_desc), key=lambda s: s.lower()):
#         print "%s;%d" %(item, no_desc.count(item))

    print "**********************************"
    return llrs

def generate_csv(llrs):
    with open('faodocrep.csv','w') as csv_file:
        csv_file.write((u'\ufeff').encode('utf8')) #BOM
        headers = u"ID;Title;Abstract/Description;Authors;Corporate authors;Publishers;Data provider;Publicaton date (YYYY/MM);Language;Related concepts;Themes;Overarching Categories;Geographical focus;Resource types;Link to the original website;Link to the publication;Thumbnail;License;Copyright details;Pages\n"
        csv_file.write(headers.encode('utf8'))
        for llr in llrs:
            csv_file.write(llr.as_csv_line().encode('utf8'))
        csv_file.close()

###############################################################################

#create_all_file()
new_records = get_records()
llrs = create_llrs(new_records)
generate_csv(llrs)

