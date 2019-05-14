#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging
import json
from sets import Set
import landvoc
from resources.LandLibraryResource import LandLibraryResource
import utils

def _(s, language):
    spanishStrings = {'Implemented by: ': 'Implementado por: ',
                      'Implements: ' : 'Implementa: ',
                      'Amended by: ' : 'Enmendado por: ',
                      'Amends: ' : 'Enmienda: ',
                      'Repealed by: ' : 'Revocado por: ',
                      'Repeals: ' : 'Revoca: ',
    }
    frenchStrings = {'Implemented by: ': 'Mis en oeuvre par: ',
                     'Implements: ' : 'Met en oeuvre: ',
                     'Amended by: ' : u'Modifié par: ',
                     'Amends: ' : u'Modifie: ',
                     'Repealed by: ' : u'Abrogé par: ',
                     'Repeals: ' : u'Abroge: ',
    }

    if language == 'E':
        return s
    if language == 'S':
        return spanishStrings[s]
    if language == 'F':
        return frenchStrings[s]

def get_faolexId_from_SPARQL():
    with open('sparql-faolex.json') as sparql_faolex:
        sparql_faolex_returned = json.load(sparql_faolex)
        sparql_results = sparql_faolex_returned['results']['bindings']

    resultSparqlSet = Set()

    for sparql_result in sparql_results:
        faolexId = sparql_result['id']['value']
        resultSparqlSet.add(faolexId)
    return resultSparqlSet

def cat_json(outfile, infiles):
    file(outfile, "w")\
        .write("[%s]" % (",".join([mangle(file(f).read()) for f in infiles])))

def mangle(s):
    return s.strip()[1:-1]

def get_only_new_records(documents_already_ingested):
    #infiles = ['results/all-results+C.json','results/all-results+P.json','results/all-results+L+1800+1985.json', 'results/all-results+L+1986+2016.json','results/all-results+R+1800+1985.json', 'results/all-results+R+1986+2016.json','results/all-results+A.json','results/all-results+M.json']
    #cat_json("ALL.json", infiles)
    with open('ALL.json') as data_file:
        results = json.load(data_file)

    resultDict= {}
    for result in results:
        faolexId_object = next((x for x in result['R']['mts'] if x['MT']['N']=='faolexId'), None)
        faolexId = faolexId_object ['MT']['V']
        if (faolexId not in documents_already_ingested):
            resultDict[faolexId] = result
        else:
            logging.debug('%s not added. Already in the SPARQL' %(faolexId))
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
    i=0
    for key, value in resultDict.iteritems():
        llr = LandLibraryResource()

        #repealed_object = next((x for x in value['R']['mts'] if x['MT']['N']=='repealed'), None)
        #if repealed_object is not None:
        #    continue

        #title. Only one
        title = get_value_metatag(value, 'titleOfText')
        llr.set_title(title)

        #subtitle. 1st longTitle, 2nd original title, 3rd None
        subtitle_longtitle = get_value_metatag(value, 'longTitleOfText')
        subtitle_originaltitle = get_value_metatag(value, 'originalTitleOfText')
        llr.set_subtitle(subtitle_longtitle, subtitle_originaltitle)

        # compound, because it can be splitted in several abstracts (present in 98 records)
        description = "".join([x['MT']['V'] for x in value['R']['mts'] if x['MT']['N']=='abstract'])
        llr.set_description(description)

        #author. Only one
        author = get_value_metatag(value, 'Author')
        llr.set_author(author)

        #type. Only one
        type = get_value_metatag(value, 'typeOfTextCode')
        llr.set_type(type)

        #metadata language. Only one
        metadata_language = get_value_metatag(value, 'recordLanguage')
        llr.set_metadata_language(metadata_language)

        #resource_url. Only one
        linksToFullText = get_value_metatag(value, 'linksToFullText')
        llr.set_resource_url(linksToFullText)

        #ID. Only one
        faolexId = get_value_metatag(value, 'faolexId')
        llr.set_id(faolexId)

        #original url. Only one
        llr.set_original_url(faolexId)

        #number of pages. Only one
        page_count = get_value_metatag(value, 'page count')
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
        llr.set_data_provider(u"FAO Legal Office")

        #date.
        dateOfText = get_value_metatag(value, 'dateOfText')
        dateOfOriginalText = get_value_metatag(value, 'dateOfOriginalText')
        llr.set_date(dateOfText,dateOfOriginalText)

        #geographical focus. list
        country_ISO3_list = get_values_metatag(value, 'country_ISO3')
        geographicalArea_en_list = get_values_metatag(value, 'geographicalArea_en')
        llr.set_geographical_focus(country_ISO3_list, geographicalArea_en_list)

        #Overarching categories
        llr.set_overarching_categories([u"Land Policy & Legislation"])

        #landvoc concepts
        #keywordCode_list = [x['MT']['V'] for x in value['R']['mts'] if x['MT']['N']=='keywordCode']
        keyword_list = get_values_metatag(value, 'keyword_en')
        llr.set_concepts(keyword_list, lv);

        #related website. Only one
        relatedWebSite = get_value_metatag(value, 'relatedWebSite')
        llr.set_related_website(relatedWebSite)
        
        publisher = utils.get_publisher(relatedWebSite)
        llr.set_publisher(publisher)

        #Serial imprint (Source in the website). Only one
        serialImprint = get_value_metatag(value, 'serialImprint')
        llr.set_serialImprint(serialImprint)

        #language. Only one
        gsaentity_google_language = get_value_metatag(value, 'gsaentity_google_language')

        #Could be more than one value
        documentLanguage_en = get_values_metatag(value, 'documentLanguage_en')
        llr.set_language(gsaentity_google_language, documentLanguage_en)

        #implementedBy = get_values_metatag(value, 'implementedBy') 
        implementedByTitle = get_values_metatag(value, 'implementedByTitle')
        implementedByDate = get_values_metatag(value, 'implementedByDate')
        llr.set_implementedBy(generate_aditional_text(implementedByTitle, implementedByDate, "Implemented by: ", llr.metadata_language))

            
        #implement = get_values_metatag(value, 'implement')
        implementTitle = get_values_metatag(value, 'implementTitle')
        implementDate = get_values_metatag(value, 'implementDate')
        llr.set_implement(generate_aditional_text(implementTitle, implementDate, "Implements: ", llr.metadata_language))

        #amendedBy = get_values_metatag(value, 'amendedBy')
        amendedByTitle = get_values_metatag(value, 'amendedByTitle')
        amendedByDate = get_values_metatag(value, 'amendedByDate')
        llr.set_amendedBy(generate_aditional_text(amendedByTitle, amendedByDate, "Amended by: ", llr.metadata_language))

        #amends = get_values_metatag(value, 'amends')
        amendsTitle = get_values_metatag(value, 'amendsTitle')
        amendsDate = get_values_metatag(value, 'amendsDate')
        llr.set_amends(generate_aditional_text(amendsTitle, amendsDate, "Amends: ", llr.metadata_language))
        
        #repealedBy = get_values_metatag(value, 'repealedBy')
        repealedByTitle = get_values_metatag(value, 'repealedByTitle')
        repealedByDate = get_values_metatag(value, 'repealedByDate')
        llr.set_repealedBy(generate_aditional_text(repealedByTitle, repealedByDate, "Repealed by: ", llr.metadata_language))
        
        #repeals = get_values_metatag(value, 'repeals')
        repealsTitle = get_values_metatag(value, 'repealsTitle')
        repealsDate = get_values_metatag(value, 'repealsDate')
        llr.set_repeals(generate_aditional_text(repealsTitle, repealsDate, "Repeals: ", llr.metadata_language))
        
        llr.set_full_description()

        llrs.append(llr)

    print "**********************************"
    print "new records without repealed (Set)= %d" %(len(llrs))
    return llrs

def generate_csv(llrs):
    with open('faolex.csv','w') as file:
        file.write((u'\ufeff').encode('utf8')) #BOM
        headers = u"ID;Title;Abstract/Description;Authors;Corporate authors;Publishers;Data provider;Publicaton date (YYYY/MM);Language;Related concepts;Themes;Overarching Categories;Geographical focus;Resource types;Link to the original website;Link to the publication;Thumbnail;License;Copyright details;Pages\n"
        file.write(headers.encode('utf8'))
        for llr in llrs:
            file.write(llr.as_csv_line().encode('utf8'))
        file.close()

###############################################################################

def generate_stats(resultDict):

    years=[]
    types=[]

    for key, value in resultDict.iteritems():
        #title. Only one
        year = get_value_metatag(value, 'year')
        years.append(year)
        
        type = get_value_metatag(value, 'typeOfTextCode')
        types.append(type)

    for y in sorted(set(years)):
        print str(y)+"-"+str(years.count(y))

    for t in sorted(set(types)):
        print str(t)+"-"+str(types.count(t))

        
###############################################################################

#retrieve()
#retrieve_by_year('L', 1800, 1985)
#retrieve_by_year('L', 1986, 2016)
#retrieve_by_year('R', 1800, 1985)
#retrieve_by_year('R', 1986, 2016)

documents_already_ingested = get_faolexId_from_SPARQL()
new_records = get_only_new_records(documents_already_ingested)
llrs = create_llrs(new_records)
#generate_stats(new_records)
generate_csv(llrs)
