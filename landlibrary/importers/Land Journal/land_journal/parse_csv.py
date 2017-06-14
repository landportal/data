#!/usr/bin/python
# -*- coding: UTF-8 -*-
from RISparser import readris
import landvoc
from resources.LandLibraryResource import LandLibraryResource
import utils
import csv


LANDVOC = landvoc.LandVoc()

def update_themes_oacs_csv(filename):
    
    with open(filename, 'rb') as fileR, open("new-"+filename, 'wb') as fileW:
        reader = csv.reader(fileR, delimiter=';', quotechar='"')
        writer = csv.writer(fileW, delimiter=';', quotechar='"')
        headers = reader.next()
        writer.writerow(headers)
        header_related_concepts= "Related concepts"
        header_themes = "Themes"
        header_oacs = "Overarching Categories"
        for row in reader:
            themes = set()
            oacs = set()
            for key, value in zip(headers, row):
                if key==header_related_concepts:
                    l = filter(None, [x.strip() for x in value.split(";")])
                    #clear spaces
                    index_concepts = headers.index(header_related_concepts)
                    row[index_concepts] = ';'.join(l)
                    themes = LANDVOC.get_fixed_themes(l);        
                    oacs = LANDVOC.get_fixed_oacs(l);        

                if key==header_themes:
                    print "--------------------------"
                    current_themes = set(filter(None, [x.strip() for x in value.split(";")]))
                    print current_themes
                    print themes
                    themes |= current_themes
                    index_theme = headers.index(header_themes)
                    row[index_theme] = ';'.join(themes)
                    print ';'.join(themes)
                    print "--------------------------"
                if key==header_oacs:
                    print "--------------------------"
                    current_oacs = set(filter(None, [x.strip() for x in value.split(";")]))
                    print current_oacs
                    print oacs
                    oacs |= current_oacs    
                    index_oacs = headers.index(header_oacs)
                    row[index_oacs] = ';'.join(oacs)
                    print ';'.join(oacs)
                    print "--------------------------"

            writer.writerow(row)
###############################################################################

update_themes_oacs_csv('test.csv')

