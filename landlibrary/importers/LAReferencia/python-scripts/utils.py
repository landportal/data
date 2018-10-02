#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import geograpy
import collections
from geograpy import extraction
from geotext import GeoText
import re
from time import strptime
from llr import utils as llrutils 

#Added from https://gist.github.com/onyxfish/322906#gistcomment-1701799
reload(sys)
sys.setdefaultencoding("utf-8")

def flatten(l):
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, basestring):
            for sub in flatten(el):
                yield sub
        else:
            yield el
            
def getPlaceET_fromText_NLTK(text):
    result = list()
    if not text:
        return filter(None, result)    

    # You can now access all of the places found by the Extractor
    places = geograpy.get_place_context(text=text)    
    for place in (places.countries + places.other): 
        c = llrutils.getISO3166_1code(place)
        if not c:
            c = llrutils.getUNM49code(place)
        result.append(c)
    return filter(None, flatten(result))
    
def getPlaceET_fromText_GeoText(text):
    result = list()
    if not text:
        return filter(None, result)    

    places = GeoText(text)
    
    for place in (places.countries):
        c = llrutils.getISO3166_1code(place)
        if not c:
            c = llrutils.getUNM49code(place)
        result.append(c)
    return filter(None, flatten(result))

def getLPOAC(label):
    return {
        "Economic Growth" : None,
        "Governance, Conflict, and Humanitarian Assistance" : None,
        "Climate Change and Natural Resource Management" : "Land Use, Management & Investment",
        "Food Security" : None,
        "Gender Equality and Women's Empowerment" : "Access to Land & Tenure Security",
        "Responsible Land Based Investment" : "Land Use, Management & Investment",
        "Customary and Community Tenure" : "Access to Land & Tenure Security",
        "Marine Tenure and Coastal Resource Management" : "Land Use, Management & Investment",
        "Sustainable Urbanization" : None
    }.get(label, None)

def getLPTheme(label):
    return {
        "Economic Growth" : "Socio-Economic & Institutional Context",
        "Governance, Conflict, and Humanitarian Assistance" : "Land Conflicts",
        "Climate Change and Natural Resource Management" : "Land, Climate change & Environment",
        "Food Security" : "Land & Food Security",
        "Gender Equality and Women's Empowerment" : "Land & Gender",
        "Responsible Land Based Investment" : "Land & Investments",
        "Customary and Community Tenure" : "Indigenous & Community Land Rights",
        "Marine Tenure and Coastal Resource Management" : None,
        "Sustainable Urbanization" : "Urban Tenure"
    }.get(label, None)

def getLPConcepts(label):
    return {
        "Economic Growth" : ["development", "sustainable development"],
        "Governance, Conflict, and Humanitarian Assistance" : ["land conflicts", "land governance"],
        "Climate Change and Natural Resource Management" : ["climate change", "environment", "natural resources management", "sustainable land management"],
        "Food Security" : ["food security"], 
        "Gender Equality and Women's Empowerment" : ["gender equity in access to land", "women"], 
        "Responsible Land Based Investment" : ["land investments"],
        "Customary and Community Tenure" : ["customary tenure", "customary land rights", "local community", "community land rights"],
        "Marine Tenure and Coastal Resource Management" : ["coastal area", "land management", "sustainable land management", "land tenure systems"],
        "Sustainable Urbanization" : ["urban areas", "land development (urbanization)", "urbanization", "sustainable development"]
    }.get(label, None)

def getPublisher(label):
    label_lower= label.lower()
    if "flacso" in label_lower and ("quito" in label_lower or "ecuador" in label_lower):
        label = "Facultad Latinoamericana de Ciencias Sociales Ecuador"

    if "flacso" in label_lower and ("chile" in label_lower):
        label = "Facultad Latinoamericana de Ciencias Sociales Chile"
    
    if "flacso" in label_lower and ("argentina" in label_lower):
        label = "Facultad Latinoamericana de Ciencias Sociales Argentina"
    
    if "flacso" in label_lower and (u"méxico" in label_lower):
        label = u"Facultad Latinoamericana de Ciencias Sociales México"

    if "Colegio de Postgraduados" in label:
        label = "Colegio de Postgraduados"

    if ("Universidad de Buenos Aires" in label) or (u"Facultad de Ciencias Económicas, UBA" in label):
        label = "Universidad de Buenos Aires"
    
    if "Universidad Austral de Chile" in label:
        label = "Universidad Austral de Chile"
    
    if u"Universidad Andina Simón Bolívar" in label:
        label = u"Universidad Andina Simón Bolívar"
    
    if u"Pontificia Universidad Católica de Chile" in label:
        label = u"Pontificia Universidad Católica de Chile"
    
    if (u"UASLP" in label) or (u"Universidad Autónoma de San Luis Potosí" in label):
        label = u"Universidad Autónoma de San Luis Potosí"
    
    if u"Universidad Católica del Norte" in label:
        label = u"Universidad Católica del Norte"
    
    if u"Universidad del Pacífico" in label:
        label = u"Universidad del Pacífico"
    
    if u"Universidad Nacional de Cuyo" in label:
        label = u"Universidad Nacional de Cuyo"
    
    if u"Universidad del Rosario" in label:
        label = u"Universidad del Rosario"
    
    if u"CAAP" in label:
        label = u"Centro Andino de Acción Popular"

    if u"Universidad Nacional de Quilmes" in label:
        label = u"Universidad Nacional de Quilmes"
    
    if u"EAFIT" in label:
        label = u"Universidad EAFIT"
    
    if u"Universidad del Rosario" in label:
        label = u"Universidad del Rosario"
    
    if (u"Universidad Nacional de la Amazonia Peruana" in label) or (u"Universidad Nacional de la Amazonía Peruana" in label) or (u"Universidad de la Amazonía Peruana" in label):
        label = u"Universidad Nacional de la Amazonía Peruana"
    
    if u"Universidad de Lima" in label:
        label = u"Universidad de Lima"
    
    if u"UAEMEX" in label:
        label = u"Universidad Autónoma del Estado de México"

    if (u"Pontificia Universidad Javeriana" in label) or (u"Facultad de Estudios Ambientales y Rurales" in label):
        label = u"Pontificia Universidad Javeriana"
        
    if u"Universidad Nacional (Costa Rica)" in label:
        label = u"Universidad Nacional de Costa Rica"

    if u"Universidad Sergio Arboleda" in label:
        label = u"Universidad Sergio Arboleda"
        

#CLEAN        
    if u"Maestría en" in label:
        label = None
    elif "Facultad" in label and (u"Facultad Latinoamericana de Ciencias Sociales" not in label):
        label = None
    elif "Escuela de" in label:
        label = None
        
    return {
        "University of Costa Rica" : "Universidad de Costa Rica",
        "Costa Rica University" : "Universidad de Costa Rica",
        "Agenda Ambiental": None,
        u"Perú": None,
        "Humanidades y Ciencias Sociales": None

    }.get(label, label)



# Target: 2011-12-13 (YYYY-MM-DD) (Drupal)

def clean_date (date):
    
    dateArray = date.strip().lower().split("-")
    
    if len(dateArray) == 1: #YYYY
        pattern_YYYY =  re.compile("^[0-9]{4}$") #YYYY
        if re.search(pattern_YYYY, date):
            date = date+"-12-31"

    if len(dateArray) == 2:
        year = dateArray[0]
        month = dateArray[1]
        if month in ["01","03","05", "07", "08", "10", "12"]:
            date = year+"-"+month+"-31"
        elif month in ["02"]:
            date = year+"-"+month+"-28"
        else:
            date = year+"-"+month+"-30"
            
    if len(dateArray) == 3:
        year = dateArray[0]
        month = dateArray[1]
        day = dateArray[2].split("-")[0]         
        date = year+"-"+month+"-"+day
    
    return date

def getLLR_type(label):
    return {
        "article": "Journal Articles & Books",
        "report": "Reports & Research",
        "masterThesis": "Reports & Research", 
        "doctoralThesis": "Reports & Research"
    }[label]