#!/usr/bin/python
# -*- coding: UTF-8 -*-
import urllib
import glob
import itertools
from resources.Observation import Observation
import json
import time
import io
import pycountry


def get_iso3_from_iso2(iso2):
    return pycountry.countries.get(alpha_2=iso2).alpha_3

indicators = [
# Key element 1: Ratification of human rights instruments
# MISSING

# Key element 2: Elimination of gender-based discrimination in the Constitution
{"code":"952", "label":"Constitution - Gender-based discrimination"},
{"code":"953", "label":"Constitution - Customary law"},
{"code":"954", "label":"Constitution -  Religious law"},
{"code":"955", "label":"Constitution - Special measures"},
# Key element 3: Recognition of women’s legal capacity
{"code":"956", "label":"Legal capacity - Entering contracts"},
# Key element 4: Gender equality of rights with respect to nationality
{"code":"957", "label":"Nationality - Identity documents"},
{"code":"958", "label":"Nationality - Marriage"},
{"code":"959", "label":"Nationality - Transfer of citizenship to children"},
# Key element 5: Gender equality in property rights
{"code":"960", "label":"Property rights - Gender equality"},
{"code":"961", "label":"Property rights - Default marital property regime"},
{"code":"962", "label":"Property rights - Spousal consent"},
{"code":"963", "label":"Property rights - Joint ownership in consensual unions"},
{"code":"964", "label":"Property rights - Special measures"},
# Key element 6: Gender equality in inheritance
{"code":"965", "label":"Inheritance - User rights to the matrimonial house"},
{"code":"966", "label":"Inheritance - Minimum share of matrimonial property"},
{"code":"967", "label":"Inheritance - Consensual unions"},
{"code":"968", "label":"Inheritance - Equal rights"},
{"code":"969", "label":"Inheritance - Equal share"},
{"code":"970", "label":"Inheritance - Compensation"},
# Key element 7: Gender-equitable implementation, dispute mechanisms and access to justice
{"code":"971", "label":"Decentralisation - Customary institutions"},
{"code":"972", "label":"Decentralisation - Formal institutions"},
{"code":"973", "label":"Justice - Equality before the law"},
{"code":"974", "label":"Justice - Access to formal and/or customary institutions"},
{"code":"975", "label":"Justice - Legal support"},
{"code":"976", "label":"Justice - Gender-specific institutions"},
# Key element 8: Women’s participation in national and local institutions enforcing land legislation
{"code":"977", "label":"Female representation - Land-related institutions"},
{"code":"978", "label":"Female representation - Dispute resolution"},
]
def retrieve():
    for indicator in indicators:
        testfile = urllib.URLopener()
        url =  "http://www.fao.org/gender-landrights-database/legislation-assessment-tool/indicators/get_records_region/en/?&reg=ALL&sta_id="+indicator['code']
        filename = indicator['code'] + " - " + "".join([c for c in indicator['label'] if c.isalpha() or c.isdigit() or c==' ']).rstrip() + ".json"
        testfile.retrieve(url, filename)

def generate_csv(observations, filename):
    with io.open(filename,'a', encoding='utf-8-sig') as csv_file: #UTF-8 BOM
        #csv_file.write((u'\ufeff').encode('utf8')) #BOM
        headers = u"Indicator;Country;Year;Value;Comment\n"
        #csv_file.write(headers)

        for observation in observations:
            csv_file.write(observation.as_csv_line())
        csv_file.close()
        
def getLabelForStage(stage):
    return ". Stage "+stage +" means \""+switch_stage(stage)+"\"."

def switch_stage(stage):
    switcher = {
        "0": "Absence of the indicator in the legal framework",
        "1": "A policy is being developed",
        "1.5": "A policy is in place",
        "2": "A draft legislation is to be submitted for deliberations",
        "3": "The indicator appears in primary law",
        "4": "The indicator appears in multiple legal instruments",
        "N/A": "Not applicable",
    }
    return switcher.get(stage, "Invalid VALUE")

def switch_indicator(indicator):
    switcher = {
        "952": "2.4",
        "953": "2.5",
        "954": "2.6",
        "955": "2.7",
        "956": "3.8",
        "957": "4.9",
        "958": "4.10",
        "959": "4.11",
        "960": "5.12",
        "961": "5.13",
        "962": "5.14",
        "963": "5.15",
        "964": "5.16",
        "965": "6.17",
        "966": "6.18",
        "967": "6.19",
        "968": "6.20",
        "969": "6.21",
        "970": "6.22",
        "971": "7.23",
        "972": "7.24",
        "973": "7.25",
        "974": "7.26",
        "975": "7.27",
        "976": "7.28",
        "977": "8.29",
        "978": "8.30",
    }
    return switcher.get(indicator)
    
def process_fao_lat_file(filename):
    #Read JSON data into the datastore variable
    with open(filename, 'r') as f:
        datastore = json.load(f)

    # Generate Observations
    observations = []
    for obs in datastore:
        if obs['c1'] =="N/A" and obs['c99']=="N/A":
            continue
        observation = Observation()
        observation.set_indicator("LAT."+switch_indicator(filename[8:][:3]))
        observation.set_country(get_iso3_from_iso2(obs['country']))
        observation.set_year("2014") # at the end of the file http://www.fao.org/3/a-i4006e.pdf
        observation.set_value(obs['c1'])
        comment = obs['c99'] + getLabelForStage(obs['c1'].strip())
        observation.set_comment(comment)
        observations.append(observation)
    #timestr = time.strftime("%Y%m%d-%H%M%S")
    #filename_output = timestr+"-fao_lat-"+tmp_indicator_code+".csv"
    filename_output = "FAO-LAT.csv"
    generate_csv(observations, filename_output)

# 1. Retrieve
#retrieve()
# 2. Manually move .json to results/ folder
#
# 3. Read
fao_lat_files = glob.glob("results/*.json")
#top5 = itertools.islice(fao_lat_files, 1)
for fao_lat_file in fao_lat_files:
    print "----------------"
    print fao_lat_file
    process_fao_lat_file(fao_lat_file)

# 4. Manual curation

# exchange value and comment
#957    GTM    2014    No restricción    N/A
#No provision = 0
#956    GHA    2014    No provision    No provision could be located

