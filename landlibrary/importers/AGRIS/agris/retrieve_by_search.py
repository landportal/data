#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import harvest_lists
# from xml.etree import ElementTree
# import pprint
# 
# results={}
# pp = pprint.PrettyPrinter(indent=4)

def check_max_amount(amount):
    max_amount = 1000
    if amount>= max_amount:
        print "---------------------------"
        print "---------------------------"
        print "-- MAXIMUM SIZE REACHED ---"
        print "---------------------------"
        print "---------------------------"

def retrieve_once(harvest_list, with_land=False):
    for concept in harvest_list:
        print "starting to retrieve concept=" + concept
        year_begin = 1965
        year_end = 2017
        concept_url = concept
        if " " in concept:
            concept_url = "\""+concept+"\""
        if with_land:
            url = "http://agris.fao.org/agris-search/export!exportTopAGAP.action?filterString=+subject:(land)+subject:("+concept_url+")+publicationDate:["+str(year_begin)+" TO "+str(year_end)+"]"
        else:
            url = "http://agris.fao.org/agris-search/export!exportTopAGAP.action?filterString=+subject:("+concept_url+")+publicationDate:["+str(year_begin)+" TO "+str(year_end)+"]"
        response = requests.get(url)
        if response.content != "null":
            filename = "agris-"+concept+".xml"
            if with_land:
                filename = "agris-"+concept+"+land.xml"
            with open(filename, 'w') as data_file:
                data_file.write(response.content)

# ***** For the initial part, in order to know if the number of result is below the threshold (1000) 
#        results[concept]={}
#         total_amount = 0
#         if response.content != "null":
#             tree = ElementTree.fromstring(response.content)
#             total_amount = len(tree)
#         results[concept] = total_amount
#         print "number of resources="+str(total_amount)
#         check_max_amount(total_amount)
        
def retrieve_by_year(harvest_list, with_land=False):
    for concept in harvest_list:
        print "starting to retrieve concept=" + concept
        concept_url = concept
        if " " in concept:
            concept_url = "\""+concept+"\""
#        results[concept]={}
        year = 1975
#        total_amount = 0
        while year<2018:
            if with_land:
                url = "http://agris.fao.org/agris-search/export!exportTopAGAP.action?filterString=+subject:(land)XX+subject:("+concept_url+")+publicationDate:["+str(year)+" TO "+str(year)+"]"
            else:
                url = "http://agris.fao.org/agris-search/export!exportTopAGAP.action?filterString=+subject:("+concept_url+")+publicationDate:["+str(year)+" TO "+str(year)+"]"
            print url
            response = requests.get(url)
            if response.content != "null":
                filename = "agris-"+concept+"-"+str(year)+".xml"
                if with_land:
                    filename = "agris-search-results/agris-"+concept+"+land-"+str(year)+".xml"
                with open(filename, 'w') as data_file:
                    data_file.write(response.content)
# ***** For the initial part, in order to know if the number of result is below the threshold (1000) 
# 
#             intermediate_amount=0
#             if response.content != "null":
#                 tree = ElementTree.fromstring(response.content)
#                 #print url
#                 #print "number of resources="+str(len(tree))
#                 intermediate_amount = len(tree)
#                 results[concept][str(year)] = intermediate_amount
#                 total_amount+=intermediate_amount
#                 check_max_amount(intermediate_amount)
            year+=1
#        print "total amount="+str(total_amount)



#retrieve_once(harvest_lists.HARVEST_LIST_ALL_YEARS.keys(), False)
#retrieve_once(harvest_lists.HARVEST_LIST_WITH_LAND_ALL_YEARS.keys(), True)

#retrieve_by_year(harvest_lists.HARVEST_LIST_YEARLY.keys(), False)
#retrieve_by_year(harvest_lists.HARVEST_LIST_WITH_LAND_YEARLY.keys(), True)
