#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging
import json
from sets import Set
import landvoc
from llr.LandLibraryResource import LandLibraryResource
import llr.utils as llrutils
import utils
from landvocFAOLEX.LandVocFAOLEX import LandVocFAOLEX
import io
import time

LANDVOC = landvoc.LandVoc()
LANDVOCFAOLEX = LandVocFAOLEX()

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

def get_only_new_records(documents_already_ingested):
    #infiles = ['results/all-results+C.json','results/all-results+P.json','results/all-results+L+1800+1985.json', 'results/all-results+L+1986+2016.json','results/all-results+R+1800+1985.json', 'results/all-results+R+1986+2016.json','results/all-results+A.json','results/all-results+M.json']
    #cat_json("ALL.json", infiles)
    with open('ALL-1800+2018.json') as data_file:
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

def get_only_old_records(documents_already_ingested):
    with open('ALL-1800+2018.json') as data_file:
        results = json.load(data_file)

    resultDict= {}
    for result in results:
        faolexId_object = next((x for x in result['R']['mts'] if x['MT']['N']=='faolexId'), None)
        faolexId = faolexId_object ['MT']['V']
        if (faolexId in documents_already_ingested):
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
        if subtitle_longtitle is not None:
            llr.set_subtitle(subtitle_longtitle)
        else:
            llr.set_subtitle(subtitle_originaltitle)

        # compound, because it can be splitted in several abstracts (present in 98 records)
        description = "".join([x['MT']['V'] for x in value['R']['mts'] if x['MT']['N']=='abstract'])
        #llr.set_description(description)

        #author. Only one
        authors = get_value_metatag(value, 'Author')
        if authors:
            llr.set_authors([authors])

        #type. Only one
        type_original = get_value_metatag(value, 'typeOfTextCode')
        types_lp = utils.getLLR_types(type_original)
        llr.set_types(types_lp)

        #metadata language. Only one
        metadata_language = get_value_metatag(value, 'recordLanguage')        
        llr.set_metadata_language(metadata_language)

        #resource_url. Only one
        linksToFullText = get_value_metatag(value, 'linksToFullText')
        resource_url = "http://extwprlegs1.fao.org/docs/pdf/"+linksToFullText
        llr.set_resource_url(resource_url)

        #ID. Only one
        faolexId = get_value_metatag(value, 'faolexId')
        llr.set_id(faolexId)

        #original url. Only one
        original_url = "http://www.fao.org/faolex/results/details/en/c/"+faolexId
        llr.set_original_url(original_url)

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
        if dateOfText is not None:
            llr.set_date(dateOfText)
        else:
            llr.set_date(dateOfOriginalText)

        #geographical focus. list
        country_ISO3_list = get_values_metatag(value, 'country_ISO3')
        geographicalArea_en_list = get_values_metatag(value, 'geographicalArea_en')
        
        countries_cleaned = set([x for x in country_ISO3_list if x != "EUR"])
        regions_cleaned = set(llrutils.flatten(filter(None, [utils.getUNM49code(region) for region in geographicalArea_en_list])))
        
        llr.set_geographical_focus(countries_cleaned, regions_cleaned)

        #landvoc concepts
        #keywordCode_list = [x['MT']['V'] for x in value['R']['mts'] if x['MT']['N']=='keywordCode']
        potential_concepts = get_values_metatag(value, 'keyword_en')
        direct_mapping = list()#LANDVOC.get_concepts_direct(potential_concepts)
        related_mapping = LANDVOCFAOLEX.get_concepts_faolex_related(potential_concepts)
        concepts = set(direct_mapping+related_mapping)
        concepts = filter(None,concepts)
        llr.set_concepts(concepts);

        
        themes = LANDVOC.get_fixed_themes(concepts)
        oacs = LANDVOC.get_fixed_oacs(concepts) | set([u"Land Policy & Legislation"])
        
        #Overarching categories
        llr.set_overarching_categories(oacs)
        
        #Themes
        llr.set_themes(themes)

        #related website. Only one
        relatedWebSite = get_value_metatag(value, 'relatedWebSite')
        #llr.set_related_website(relatedWebSite)
        
        if relatedWebSite:
            publishers = utils.get_publisher(relatedWebSite)
            if publishers:
                llr.set_publishers([publishers])

        #Serial imprint (Source in the website). Only one
        serialImprint = get_value_metatag(value, 'serialImprint')
        #llr.set_serialImprint(serialImprint)

        #language. Only one
        gsaentity_google_language = get_value_metatag(value, 'gsaentity_google_language')

        #Could be more than one value
        documentLanguage_en = get_values_metatag(value, 'documentLanguage_en')
        if len(documentLanguage_en) == 1:
            language = documentLanguage_en[0]
        elif (gsaentity_google_language in documentLanguage_en):
            language = gsaentity_google_language
        else:
            language = gsaentity_google_language #some corner cases
        language = llrutils.getISO639_1code(language)
        llr.set_languages([language])

        #implementedBy = get_values_metatag(value, 'implementedBy') 
        implementedByTitle = get_values_metatag(value, 'implementedByTitle')
        implementedByDate = get_values_metatag(value, 'implementedByDate')
        implementedBy = generate_aditional_text(implementedByTitle, implementedByDate, "Implemented by: ", llr.metadata_language)

            
        #implement = get_values_metatag(value, 'implement')
        implementTitle = get_values_metatag(value, 'implementTitle')
        implementDate = get_values_metatag(value, 'implementDate')
        implement = generate_aditional_text(implementTitle, implementDate, "Implements: ", llr.metadata_language)

        #amendedBy = get_values_metatag(value, 'amendedBy')
        amendedByTitle = get_values_metatag(value, 'amendedByTitle')
        amendedByDate = get_values_metatag(value, 'amendedByDate')
        amendedBy = generate_aditional_text(amendedByTitle, amendedByDate, "Amended by: ", llr.metadata_language)

        #amends = get_values_metatag(value, 'amends')
        amendsTitle = get_values_metatag(value, 'amendsTitle')
        amendsDate = get_values_metatag(value, 'amendsDate')
        amends = generate_aditional_text(amendsTitle, amendsDate, "Amends: ", llr.metadata_language)
        
        #repealedBy = get_values_metatag(value, 'repealedBy')
        repealedByTitle = get_values_metatag(value, 'repealedByTitle')
        repealedByDate = get_values_metatag(value, 'repealedByDate')
        repealedBy = generate_aditional_text(repealedByTitle, repealedByDate, "Repealed by: ", llr.metadata_language)
        
        #repeals = get_values_metatag(value, 'repeals')
        repealsTitle = get_values_metatag(value, 'repealsTitle')
        repealsDate = get_values_metatag(value, 'repealsDate')
        repeals = generate_aditional_text(repealsTitle, repealsDate, "Repeals: ", llr.metadata_language)
        
        
        full_description = description
        full_description += "\n"
        full_description += implementedBy
        full_description += implement
        full_description += amendedBy
        full_description += amends
        full_description += repealedBy
        full_description += repeals

        llr.set_description(full_description)

        llrs.append(llr)

    print "**********************************"
    print "new records without repealed (Set)= %d" %(len(llrs))
    return llrs

def generate_csv(llrs, filename_output):
    with io.open(filename_output,'w', encoding='utf-8-sig') as csv_file: #UTF-8 BOM
        headers = LandLibraryResource.get_csv_header_line()
        csv_file.write(headers)
        for llr in llrs:
            csv_file.write(llr.as_csv_line())
        csv_file.close()

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

documents_already_ingested = get_faolexId_from_SPARQL()
new_records = get_only_new_records(documents_already_ingested)
llrs = create_llrs(new_records)
#old_records = get_only_old_records(documents_already_ingested)
#llrs = create_llrs(old_records)
#generate_stats(new_records)
timestr = time.strftime("%Y%m%d-%H%M%S")
filename_output = timestr+"-FAOLEX-processed.csv"
generate_csv(llrs, filename_output)
