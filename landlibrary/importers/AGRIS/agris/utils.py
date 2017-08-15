#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import collections
import re
import geograpy
from geograpy import extraction
from geotext import GeoText

#Added from https://gist.github.com/onyxfish/322906#gistcomment-1701799
reload(sys)
sys.setdefaultencoding("utf-8")

def getPlaceET_fromText_NLTK(text):
    result = list()
    if not text:
        return filter(None, result)    

    # You can now access all of the places found by the Extractor
    places = geograpy.get_place_context(text=text)    
    for place in (places.countries + places.other):
        c = getISO3166_1code(place)
        result.append(c)
        r = getUNM49code(place)
        result.append(r)
    return filter(None, flatten(result))
    
def getPlaceET_fromText_GeoText(text):
    result = list()
    if not text:
        return filter(None, result)    

    places = GeoText(text)
    
    for place in (places.countries):
        c = getISO3166_1code(place)
        result.append(c)
        r = getUNM49code(place)
        result.append(r)
    return filter(None, flatten(result))

    
def getUNM49code_fromAGROVOC_URI(uri):
    return{
        "http://aims.fao.org/aos/agrovoc/c_24920" : "001",
        "http://aims.fao.org/aos/agrovoc/c_165" : "002",
        "http://aims.fao.org/aos/agrovoc/c_7253" : "005",
        "http://aims.fao.org/aos/agrovoc/c_5296" : "009",
        "http://aims.fao.org/aos/agrovoc/c_8355" : "011",
        "http://aims.fao.org/aos/agrovoc/c_1434" : "013",
        "http://aims.fao.org/aos/agrovoc/c_2442" : "014",
        "http://aims.fao.org/aos/agrovoc/c_5218" : "015",
        "http://aims.fao.org/aos/agrovoc/c_335" : "019",
        "http://aims.fao.org/aos/agrovoc/c_5219" : "021",
        "http://aims.fao.org/aos/agrovoc/c_1320" : "029",
        "http://aims.fao.org/aos/agrovoc/c_29171" : "030",
        "http://aims.fao.org/aos/agrovoc/c_29172" : "034",
        "http://aims.fao.org/aos/agrovoc/c_29173" : "035",
        "http://aims.fao.org/aos/agrovoc/c_4805" : "057",
        "http://aims.fao.org/aos/agrovoc/c_666" : "142",
        "http://aims.fao.org/aos/agrovoc/c_37864" : "143",
        "http://aims.fao.org/aos/agrovoc/c_29174" : "145",
        "http://aims.fao.org/aos/agrovoc/c_2724" : "150",
        "http://aims.fao.org/aos/agrovoc/c_2448" : "151",
        "http://aims.fao.org/aos/agrovoc/c_8364" : "155",
    }.get(uri, None)


def getUNM49code(label):
    return {
            'AFRICA': "002",
            'ASIA': "142",
            'CARIBBEAN': "029",
            'CENTRAL AFRICA': "017",
            'CENTRAL AMERICA': "013",
            'EAST AFRICA': "014",
            'EAST ASIA': "030",
            'EUROPE': "150",
            'NORTH AMERICA': "021",
            'NORTH AFRICA': "015",
            'SOUTH AMERICA': "005",
            'AFRICA SOUTH OF SAHARA' : "202",
            'SOUTHEAST ASIA': "035",
            'SOUTH AFRICA': "018",
            'SOUTHERN AFRICA': "018",
            'SOUTH ASIA': "034",
            'WEST AFRICA': "011",
            'WEST ASIA': "145",
            'PACIFIC': "009", # Manual map
            'AMAZONIA': None,
            'MIDDLE EAST': '145', #WESTERN ASIA
            "GLOBAL" : "001",
            "AFRICA" : "002",
            "SOUTH AMERICA" : "005",
            "OCEANIA" : "009",
            "WESTERN AFRICA" : "011",
            "CENTRAL AMERICA" : "013",
            "EASTERN AFRICA" : "014",
            "NORTHERN AFRICA" : "015",
            "MIDDLE AFRICA" : "017",
            "SOUTHERN AFRICA" : "018",
            "AMERICAS" : "019",
            "NORTHERN AMERICA" : "021",
            "CARIBBEAN" : "029",
            "EASTERN ASIA" : "030",
            "SOUTHERN ASIA" : "034",
            "SOUTH-EASTERN ASIA" : "035",
            "SOUTHERN EUROPE" : "039",
            "AUSTRALIA AND NEW ZEALAND" : "053",
            "MELANESIA" : "054",
            "MICRONESIA (REGION)" : "057",
            "POLYNESIA" : "061",
            "ASIA" : "142",
            "CENTRAL ASIA" : "143",
            "WESTERN ASIA" : "145",
            "EUROPE" : "150",
            "EASTERN EUROPE" : "151",
            "NORTHERN EUROPE" : "154",
            "WESTERN EUROPE" : "155",
            "SUB-SAHARAN AFRICA" : "202",
            "LATIN AMERICA AND THE CARIBBEAN" : "419",
            "WEST AND CENTRAL AFRICA": ['011','017'],
            "SOUTHERN  AFRICA" : "018",
            u"WEST\xa0AFRICA": '011',
            u'CENTRAL\xa0ASIA': "143",
            u'SOUTHERN\uffa0 AFRICA': "018",
            u'SOUTH EAST ASIA': "035",
            "LATIN AMERICA": ['013', '005'], # Central America    013 +  South America    005 CHECK
            #CHECK
    }.get(label.upper(), None)


def getISO3166_1code_fromAGROVOC_URI(uri):
    return {
        "http://aims.fao.org/aos/agrovoc/c_650" : "ABW",
        "http://aims.fao.org/aos/agrovoc/c_163" : "AFG",
        "http://aims.fao.org/aos/agrovoc/c_417" : "AGO",
        "http://aims.fao.org/aos/agrovoc/c_29189" : "AIA",
        "http://aims.fao.org/aos/agrovoc/c_241" : "ALB",
        "http://aims.fao.org/aos/agrovoc/c_403" : "AND",
        "http://aims.fao.org/aos/agrovoc/c_5143" : "ANT",
        "http://aims.fao.org/aos/agrovoc/c_8067" : "ARE",
        "http://aims.fao.org/aos/agrovoc/c_603" : "ARG",
        "http://aims.fao.org/aos/agrovoc/c_8926" : "ARM",
        "http://aims.fao.org/aos/agrovoc/c_336" : "ASM",
        "http://aims.fao.org/aos/agrovoc/c_471" : "ATA",
        "http://aims.fao.org/aos/agrovoc/c_505" : "ATG",
        "http://aims.fao.org/aos/agrovoc/c_714" : "AUS",
        "http://aims.fao.org/aos/agrovoc/c_718" : "AUT",
        "http://aims.fao.org/aos/agrovoc/c_9026" : "AZE",
        "http://aims.fao.org/aos/agrovoc/c_1159" : "BDI",
        "http://aims.fao.org/aos/agrovoc/c_870" : "BEL",
        "http://aims.fao.org/aos/agrovoc/c_875" : "BEN",
        "http://aims.fao.org/aos/agrovoc/c_8081" : "BFA",
        "http://aims.fao.org/aos/agrovoc/c_810" : "BGD",
        "http://aims.fao.org/aos/agrovoc/c_1145" : "BGR",
        "http://aims.fao.org/aos/agrovoc/c_780" : "BHR",
        "http://aims.fao.org/aos/agrovoc/c_778" : "BHS",
        "http://aims.fao.org/aos/agrovoc/c_33958" : "BIH",
        "http://aims.fao.org/aos/agrovoc/c_33237" : "BLR",
        "http://aims.fao.org/aos/agrovoc/c_871" : "BLZ",
        "http://aims.fao.org/aos/agrovoc/c_884" : "BMU",
        "http://aims.fao.org/aos/agrovoc/c_331403" : "BOL",
        "http://aims.fao.org/aos/agrovoc/c_1070" : "BRA",
        "http://aims.fao.org/aos/agrovoc/c_814" : "BRB",
        "http://aims.fao.org/aos/agrovoc/c_1125" : "BRN",
        "http://aims.fao.org/aos/agrovoc/c_897" : "BTN",
        "http://aims.fao.org/aos/agrovoc/c_1030" : "BWA",
        "http://aims.fao.org/aos/agrovoc/c_1433" : "CAF",
        "http://aims.fao.org/aos/agrovoc/c_1236" : "CAN",
        "http://aims.fao.org/aos/agrovoc/c_7558" : "CHE",
        "http://aims.fao.org/aos/agrovoc/c_1548" : "CHL",
        "http://aims.fao.org/aos/agrovoc/c_1556" : "CHN",
        "http://aims.fao.org/aos/agrovoc/c_4027" : "CIV",
        "http://aims.fao.org/aos/agrovoc/c_1229" : "CMR",
        "http://aims.fao.org/aos/agrovoc/c_8500" : "COD",
        "http://aims.fao.org/aos/agrovoc/c_1811" : "COG",
        "http://aims.fao.org/aos/agrovoc/c_1850" : "COK",
        "http://aims.fao.org/aos/agrovoc/c_1767" : "COL",
        "http://aims.fao.org/aos/agrovoc/c_1790" : "COM",
        "http://aims.fao.org/aos/agrovoc/c_1267" : "CPV",
        "http://aims.fao.org/aos/agrovoc/c_1920" : "CRI",
        "http://aims.fao.org/aos/agrovoc/c_1997" : "CUB",
        "http://aims.fao.org/aos/agrovoc/c_1400" : "CYM",
        "http://aims.fao.org/aos/agrovoc/c_2080" : "CYP",
        "http://aims.fao.org/aos/agrovoc/c_33095" : "CZE",
        "http://aims.fao.org/aos/agrovoc/c_3245" : "DEU",
        "http://aims.fao.org/aos/agrovoc/c_2346" : "DJI",
        "http://aims.fao.org/aos/agrovoc/c_2363" : "DMA",
        "http://aims.fao.org/aos/agrovoc/c_2185" : "DNK",
        "http://aims.fao.org/aos/agrovoc/c_2364" : "DOM",
        "http://aims.fao.org/aos/agrovoc/c_259" : "DZA",
        "http://aims.fao.org/aos/agrovoc/c_2485" : "ECU",
        "http://aims.fao.org/aos/agrovoc/c_2503" : "EGY",
        "http://aims.fao.org/aos/agrovoc/c_34927" : "ERI",
        "http://aims.fao.org/aos/agrovoc/c_7273" : "ESP",
        "http://aims.fao.org/aos/agrovoc/c_10672" : "EST",
        "http://aims.fao.org/aos/agrovoc/c_2676" : "ETH",
        "http://aims.fao.org/aos/agrovoc/c_2905" : "FIN",
        "http://aims.fao.org/aos/agrovoc/c_2895" : "FJI",
        "http://aims.fao.org/aos/agrovoc/c_2783" : "FLK",
        "http://aims.fao.org/aos/agrovoc/c_3081" : "FRA",
        "http://aims.fao.org/aos/agrovoc/c_2811" : "FRO",
        "http://aims.fao.org/aos/agrovoc/c_4805" : "FSM",
        "http://aims.fao.org/aos/agrovoc/c_3161" : "GAB",
        "http://aims.fao.org/aos/agrovoc/c_8068" : "GBR",
        "http://aims.fao.org/aos/agrovoc/c_33250" : "GEO",
        "http://aims.fao.org/aos/agrovoc/c_3253" : "GHA",
        "http://aims.fao.org/aos/agrovoc/c_3257" : "GIB",
        "http://aims.fao.org/aos/agrovoc/c_3423" : "GIN",
        "http://aims.fao.org/aos/agrovoc/c_3406" : "GLP",
        "http://aims.fao.org/aos/agrovoc/c_3177" : "GMB",
        "http://aims.fao.org/aos/agrovoc/c_3427" : "GNB",
        "http://aims.fao.org/aos/agrovoc/c_2627" : "GNQ",
        "http://aims.fao.org/aos/agrovoc/c_3373" : "GRC",
        "http://aims.fao.org/aos/agrovoc/c_3384" : "GRD",
        "http://aims.fao.org/aos/agrovoc/c_3418" : "GTM",
        "http://aims.fao.org/aos/agrovoc/c_3093" : "GUF",
        "http://aims.fao.org/aos/agrovoc/c_3408" : "GUM",
        "http://aims.fao.org/aos/agrovoc/c_3445" : "GUY",
        "http://aims.fao.org/aos/agrovoc/c_3651" : "HND",
        "http://aims.fao.org/aos/agrovoc/c_33969" : "HRV",
        "http://aims.fao.org/aos/agrovoc/c_3472" : "HTI",
        "http://aims.fao.org/aos/agrovoc/c_3695" : "HUN",
        "http://aims.fao.org/aos/agrovoc/c_3840" : "IDN",
        "http://aims.fao.org/aos/agrovoc/c_3825" : "IND",
        "http://aims.fao.org/aos/agrovoc/c_3948" : "IRL",
        "http://aims.fao.org/aos/agrovoc/c_3940" : "IRN",
        "http://aims.fao.org/aos/agrovoc/c_3941" : "IRQ",
        "http://aims.fao.org/aos/agrovoc/c_3785" : "ISL",
        "http://aims.fao.org/aos/agrovoc/c_3972" : "ISR",
        "http://aims.fao.org/aos/agrovoc/c_4026" : "ITA",
        "http://aims.fao.org/aos/agrovoc/c_4035" : "JAM",
        "http://aims.fao.org/aos/agrovoc/c_4053" : "JOR",
        "http://aims.fao.org/aos/agrovoc/c_4039" : "JPN",
        "http://aims.fao.org/aos/agrovoc/c_11952" : "KAZ",
        "http://aims.fao.org/aos/agrovoc/c_4086" : "KEN",
        "http://aims.fao.org/aos/agrovoc/c_33243" : "KGZ",
        "http://aims.fao.org/aos/agrovoc/c_4073" : "KHM",
        "http://aims.fao.org/aos/agrovoc/c_3261" : "KIR",
        "http://aims.fao.org/aos/agrovoc/c_8808" : "KNA",
        "http://aims.fao.org/aos/agrovoc/c_4116" : "KOR",
        "http://aims.fao.org/aos/agrovoc/c_4119" : "KWT",
        "http://aims.fao.org/aos/agrovoc/c_12076" : "LAO",
        "http://aims.fao.org/aos/agrovoc/c_4244" : "LBN",
        "http://aims.fao.org/aos/agrovoc/c_4307" : "LBR",
        "http://aims.fao.org/aos/agrovoc/c_4312" : "LBY",
        "http://aims.fao.org/aos/agrovoc/c_4312" : "LBY",
        "http://aims.fao.org/aos/agrovoc/c_7349" : "LCA",
        "http://aims.fao.org/aos/agrovoc/c_4315" : "LIE",
        "http://aims.fao.org/aos/agrovoc/c_7345" : "LKA",
        "http://aims.fao.org/aos/agrovoc/c_4284" : "LSO",
        "http://aims.fao.org/aos/agrovoc/c_12204" : "LTU",
        "http://aims.fao.org/aos/agrovoc/c_4471" : "LUX",
        "http://aims.fao.org/aos/agrovoc/c_12103" : "LVA",
        "http://aims.fao.org/aos/agrovoc/c_4940" : "MAR",
        "http://aims.fao.org/aos/agrovoc/c_4904" : "MCO",
        "http://aims.fao.org/aos/agrovoc/c_33245" : "MDA",
        "http://aims.fao.org/aos/agrovoc/c_4510" : "MDG",
        "http://aims.fao.org/aos/agrovoc/c_4534" : "MDV",
        "http://aims.fao.org/aos/agrovoc/c_4792" : "MEX",
        "http://aims.fao.org/aos/agrovoc/c_4630" : "MHL",
        "http://aims.fao.org/aos/agrovoc/c_35697" : "MKD",
        "http://aims.fao.org/aos/agrovoc/c_4540" : "MLI",
        "http://aims.fao.org/aos/agrovoc/c_4548" : "MLT",
        "http://aims.fao.org/aos/agrovoc/c_1155" : "MMR",
        "http://aims.fao.org/aos/agrovoc/c_49907" : "MNE",
        "http://aims.fao.org/aos/agrovoc/c_4908" : "MNG",
        "http://aims.fao.org/aos/agrovoc/c_4964" : "MOZ",
        "http://aims.fao.org/aos/agrovoc/c_4660" : "MRT",
        "http://aims.fao.org/aos/agrovoc/c_4927" : "MSR",
        "http://aims.fao.org/aos/agrovoc/c_4635" : "MTQ",
        "http://aims.fao.org/aos/agrovoc/c_4662" : "MUS",
        "http://aims.fao.org/aos/agrovoc/c_4532" : "MWI",
        "http://aims.fao.org/aos/agrovoc/c_4533" : "MYS",
        "http://aims.fao.org/aos/agrovoc/c_5063" : "NAM",
        "http://aims.fao.org/aos/agrovoc/c_5155" : "NCL",
        "http://aims.fao.org/aos/agrovoc/c_5181" : "NER",
        "http://aims.fao.org/aos/agrovoc/c_5182" : "NGA",
        "http://aims.fao.org/aos/agrovoc/c_5171" : "NIC",
        "http://aims.fao.org/aos/agrovoc/c_5202" : "NIU",
        "http://aims.fao.org/aos/agrovoc/c_5142" : "NLD",
        "http://aims.fao.org/aos/agrovoc/c_5234" : "NOR",
        "http://aims.fao.org/aos/agrovoc/c_5124" : "NPL",
        "http://aims.fao.org/aos/agrovoc/c_5093" : "NRU",
        "http://aims.fao.org/aos/agrovoc/c_5164" : "NZL",
        "http://aims.fao.org/aos/agrovoc/c_5345" : "OMN",
        "http://aims.fao.org/aos/agrovoc/c_5504" : "PAK",
        "http://aims.fao.org/aos/agrovoc/c_5524" : "PAN",
        "http://aims.fao.org/aos/agrovoc/c_5725" : "PER",
        "http://aims.fao.org/aos/agrovoc/c_5783" : "PHL",
        "http://aims.fao.org/aos/agrovoc/c_33221" : "PLW",
        "http://aims.fao.org/aos/agrovoc/c_5555" : "PNG",
        "http://aims.fao.org/aos/agrovoc/c_6055" : "POL",
        "http://aims.fao.org/aos/agrovoc/c_6362" : "PRI",
        "http://aims.fao.org/aos/agrovoc/c_4115" : "PRK",
        "http://aims.fao.org/aos/agrovoc/c_6124" : "PRT",
        "http://aims.fao.org/aos/agrovoc/c_5560" : "PRY",
        "http://aims.fao.org/aos/agrovoc/c_3094" : "PYF",
        "http://aims.fao.org/aos/agrovoc/c_6395" : "QAT",
        "http://aims.fao.org/aos/agrovoc/c_6543" : "REU",
        "http://aims.fao.org/aos/agrovoc/c_6637" : "ROU",
        "http://aims.fao.org/aos/agrovoc/c_33240" : "RUS",
        "http://aims.fao.org/aos/agrovoc/c_6717" : "RWA",
        "http://aims.fao.org/aos/agrovoc/c_6822" : "SAU",
        "http://aims.fao.org/aos/agrovoc/c_37896" : "SCG",
        "http://aims.fao.org/aos/agrovoc/c_7497" : "SDN",
        "http://aims.fao.org/aos/agrovoc/c_6970" : "SEN",
        "http://aims.fao.org/aos/agrovoc/c_7077" : "SGP",
        "http://aims.fao.org/aos/agrovoc/c_7347" : "SHN",
        "http://aims.fao.org/aos/agrovoc/c_7230" : "SLB",
        "http://aims.fao.org/aos/agrovoc/c_7057" : "SLE",
        "http://aims.fao.org/aos/agrovoc/c_2508" : "SLV",
        "http://aims.fao.org/aos/agrovoc/c_6778" : "SMR",
        "http://aims.fao.org/aos/agrovoc/c_7237" : "SOM",
        "http://aims.fao.org/aos/agrovoc/c_7351" : "SPM",
        "http://aims.fao.org/aos/agrovoc/c_49909" : "SRB",
        "http://aims.fao.org/aos/agrovoc/c_6790" : "STP",
        "http://aims.fao.org/aos/agrovoc/c_7534" : "SUR",
        "http://aims.fao.org/aos/agrovoc/c_33096" : "SVK",
        "http://aims.fao.org/aos/agrovoc/c_34123" : "SVN",
        "http://aims.fao.org/aos/agrovoc/c_7549" : "SWE",
        "http://aims.fao.org/aos/agrovoc/c_7547" : "SWZ",
        "http://aims.fao.org/aos/agrovoc/c_7017" : "SYC",
        "http://aims.fao.org/aos/agrovoc/c_7576" : "SYR",
        "http://aims.fao.org/aos/agrovoc/c_8018" : "TCA",
        "http://aims.fao.org/aos/agrovoc/c_1487" : "TCD",
        "http://aims.fao.org/aos/agrovoc/c_7801" : "TGO",
        "http://aims.fao.org/aos/agrovoc/c_7701" : "THA",
        "http://aims.fao.org/aos/agrovoc/c_33246" : "TJK",
        "http://aims.fao.org/aos/agrovoc/c_7802" : "TKL",
        "http://aims.fao.org/aos/agrovoc/c_15047" : "TKM",
        "http://aims.fao.org/aos/agrovoc/c_37893" : "TLS",
        "http://aims.fao.org/aos/agrovoc/c_7808" : "TON",
        "http://aims.fao.org/aos/agrovoc/c_7933" : "TTO",
        "http://aims.fao.org/aos/agrovoc/c_8007" : "TUN",
        "http://aims.fao.org/aos/agrovoc/c_8013" : "TUR",
        "http://aims.fao.org/aos/agrovoc/c_8025" : "TUV",
        "http://aims.fao.org/aos/agrovoc/c_7608" : "TZA",
        "http://aims.fao.org/aos/agrovoc/c_8038" : "UGA",
        "http://aims.fao.org/aos/agrovoc/c_15070" : "UKR",
        "http://aims.fao.org/aos/agrovoc/c_8113" : "URY",
        "http://aims.fao.org/aos/agrovoc/c_8114" : "USA",
        "http://aims.fao.org/aos/agrovoc/c_15121" : "UZB",
        "http://aims.fao.org/aos/agrovoc/c_3645" : "VAT",
        "http://aims.fao.org/aos/agrovoc/c_7352" : "VCT",
        "http://aims.fao.org/aos/agrovoc/c_8186" : "VEN",
        "http://aims.fao.org/aos/agrovoc/c_1097" : "VGB",
        "http://aims.fao.org/aos/agrovoc/c_8256" : "VIR",
        "http://aims.fao.org/aos/agrovoc/c_8227" : "VNM",
        "http://aims.fao.org/aos/agrovoc/c_5159" : "VUT",
        "http://aims.fao.org/aos/agrovoc/c_8296" : "WLF",
        "http://aims.fao.org/aos/agrovoc/c_6772" : "WSM",
        "http://aims.fao.org/aos/agrovoc/c_8483" : "YEM",
        "http://aims.fao.org/aos/agrovoc/c_7252" : "ZAF",
        "http://aims.fao.org/aos/agrovoc/c_8501" : "ZMB",
        "http://aims.fao.org/aos/agrovoc/c_8516" : "ZWE",
    }.get(uri, None)
    
def getISO3166_1code(label):
    return {
        "HONDURAS" : "HND",
        "AFRICA": None,
        "ANGOLA": "AGO",
        "BANGLADESH": "BGD",
        "BELIZE": "BLZ",
        "BENIN": "XXX",
        "BHUTAN": "BTN",
        "BOLIVIA": "BOL",
        "BOTSWANA": "BWA",
        "BRAZIL": "BRA",
        "BURKINA FASO": "BFA",
        "CAMBODIA": "KHM",
        "CAMEROON": "CMR",
        "CANADA": "CAN",
        "CENTRAL AFRICAN REPUBLIC": "CAF",
        "CHILE": "CHL",
        "CHINA": "CHN",
        "COLOMBIA": "COL",
        "CONGO, DR": "COD",
        "COSTA RICA": "CRI",
        "COTE D'IVOIRE": "CIV",
        "CUBA": "CUB",
        "DOMINICAN REPUBLIC": "DOM",
        "ECUADOR": "ECU",
        "EL SALVADOR": "SLV",
        "ETHIOPIA": "ETH",
        "GHANA": "GHA",
        "GUATEMALA": "GTM",
        "HAITI": "HTI",
        "HONDURAS": "HND",
        "INDIA": "IND",
        "INDONESIA": "IDN",
        "KENYA": "KEN",
        "KOREA, DPR": "PRK",
        "LAOS": "LAO",
        "MADAGASCAR": "MDG",
        "MALAWI": "MWI",
        "MALAYSIA": "MYS",
        "MALI": "MLI",
        "MEXICO": "MEX",
        "MOZAMBIQUE": "MOZ",
        "MYANMAR": "MMR",
        "NAMIBIA": "NAM",
        "NEPAL": "NPL",
        "NEW ZEALAND": "NZL",
        "NICARAGUA": "NIC",
        "NIGER": "NER",
        "NIGERIA": "NGA",
        "PAKISTAN": "PAK",
        "PANAMA": "PAN",
        "PAPUA NEW GUINEA": "PNG",
        "PARAGUAY": "PRY",
        "PERU": "PER",
        "PHILIPPINES": "PHL",
        "RWANDA": "RWA",
        "SENEGAL": "SEN",
        "SOLOMON ISLANDS": "SLB",
        "SOUTH AFRICA": "ZAF",
        "SRI LANKA": "LKA",
        "SUDAN": "SDN",
        "SWAZILAND": "SWZ",
        "TAJIKISTAN": "TJK",
        "TANZANIA": "TZA",
        "THAILAND": "THA",
        "TIBET": None,
        "UGANDA": "UGA",
        "URUGUAY": "URY",
        "VENEZUELA": "VEN",
        "VIETNAM": "VNM",
        "ZAMBIA": "XMB",
        "ZIMBABWE": "ZWE",
        "ARUBA" : "ABW",
        "AFGHANISTAN" : "AFG",
        "ANGOLA" : "AGO",
        "ANGUILLA" : "AIA",
        "ÅLAND ISLANDS" : "ALA",
        "ALBANIA" : "ALB",
        "ANDORRA" : "AND",
        "UNITED ARAB EMIRATES" : "ARE",
        "ARGENTINA" : "ARG",
        "ARMENIA" : "ARM",
        "AMERICAN SAMOA" : "ASM",
        "ANTARCTICA" : "ATA",
        "FRENCH SOUTHERN TERRITORIES" : "ATF",
        "ANTIGUA AND BARBUDA" : "ATG",
        "AUSTRALIA" : "AUS",
        "AUSTRIA" : "AUT",
        "AZERBAIJAN" : "AZE",
        "BURUNDI" : "BDI",
        "BELGIUM" : "BEL",
        "BENIN" : "BEN",
        "BONAIRE, SINT EUSTATIUS AND SABA" : "BES",
        "BURKINA FASO" : "BFA",
        "BANGLADESH" : "BGD",
        "BULGARIA" : "BGR",
        "BAHRAIN" : "BHR",
        "BAHAMAS" : "BHS",
        "BOSNIA AND HERZEGOVINA" : "BIH",
        "SAINT BARTHÉLEMY" : "BLM",
        "BELARUS" : "BLR",
        "BELIZE" : "BLZ",
        "BERMUDA" : "BMU",
        "BOLIVIA, PLURINATIONAL STATE OF" : "BOL",
        "BRAZIL" : "BRA",
        "BARBADOS" : "BRB",
        "BRUNEI DARUSSALAM" : "BRN",
        "BHUTAN" : "BTN",
        "BOUVET ISLAND" : "BVT",
        "BOTSWANA" : "BWA",
        "CENTRAL AFRICAN REPUBLIC" : "CAF",
        "CANADA" : "CAN",
        "COCOS (KEELING) ISLANDS" : "CCK",
        "SWITZERLAND" : "CHE",
        "CHILE" : "CHL",
        "CHINA" : "CHN",
        u"CÔTE D'IVOIRE" : "CIV",
        "CAMEROON" : "CMR",
        "CONGO, THE DEMOCRATIC REPUBLIC OF THE" : "COD",
        "CONGO" : "COG",
        "COOK ISLANDS" : "COK",
        "COLOMBIA" : "COL",
        "COMOROS" : "COM",
        "CABO VERDE" : "CPV",
        "CAPE VERDE" : "CPV",
        "COSTA RICA" : "CRI",
        "CUBA" : "CUB",
        "CURAÇAO" : "CUW",
        "CHRISTMAS ISLAND" : "CXR",
        "CAYMAN ISLANDS" : "CYM",
        "CYPRUS" : "CYP",
        "CZECHIA" : "CZE",
        "GERMANY" : "DEU",
        "DJIBOUTI" : "DJI",
        "DOMINICA" : "DMA",
        "DENMARK" : "DNK",
        "DOMINICAN REPUBLIC" : "DOM",
        "ALGERIA" : "DZA",
        "ECUADOR" : "ECU",
        "EGYPT" : "EGY",
        "ERITREA" : "ERI",
        "WESTERN SAHARA" : "ESH",
        "SPAIN" : "ESP",
        "ESTONIA" : "EST",
        "ETHIOPIA" : "ETH",
        "FINLAND" : "FIN",
        "FIJI" : "FJI",
        "FALKLAND ISLANDS (MALVINAS)" : "FLK",
        "FRANCE" : "FRA",
        "FAROE ISLANDS" : "FRO",
        "MICRONESIA, FEDERATED STATES OF" : "FSM",
        "GABON" : "GAB",
        "UNITED KINGDOM" : "GBR",
        "GEORGIA" : "GEO",
        "GUERNSEY" : "GGY",
        "GHANA" : "GHA",
        "GIBRALTAR" : "GIB",
        "GUINEA" : "GIN",
        "GUADELOUPE" : "GLP",
        "GAMBIA" : "GMB",
        "GUINEA-BISSAU" : "GNB",
        "EQUATORIAL GUINEA" : "GNQ",
        "GREECE" : "GRC",
        "GRENADA" : "GRD",
        "GREENLAND" : "GRL",
        "GUATEMALA" : "GTM",
        "FRENCH GUIANA" : "GUF",
        "GUAM" : "GUM",
        "GUYANA" : "GUY",
        "HONG KONG" : "HKG",
        "HEARD ISLAND AND MCDONALD ISLANDS" : "HMD",
        "HONDURAS" : "HND",
        "CROATIA" : "HRV",
        "HAITI" : "HTI",
        "HUNGARY" : "HUN",
        "INDONESIA" : "IDN",
        "ISLE OF MAN" : "IMN",
        "INDIA" : "IND",
        "BRITISH INDIAN OCEAN TERRITORY" : "IOT",
        "IRELAND" : "IRL",
        "IRAN, ISLAMIC REPUBLIC OF" : "IRN",
        "IRAQ" : "IRQ",
        "ICELAND" : "ISL",
        "ISRAEL" : "ISR",
        "ITALY" : "ITA",
        "JAMAICA" : "JAM",
        "JERSEY" : "JEY",
        "JORDAN" : "JOR",
        "JAPAN" : "JPN",
        "KAZAKHSTAN" : "KAZ",
        "KENYA" : "KEN",
        "KYRGYZSTAN" : "KGZ",
        "CAMBODIA" : "KHM",
        "KIRIBATI" : "KIR",
        "SAINT KITTS AND NEVIS" : "KNA",
        "KOREA, REPUBLIC OF" : "KOR",
        "KUWAIT" : "KWT",
        "LAO PEOPLE'S DEMOCRATIC REPUBLIC" : "LAO",
        "LEBANON" : "LBN",
        "LIBERIA" : "LBR",
        "LIBYA" : "LBY",
        "SAINT LUCIA" : "LCA",
        "LIECHTENSTEIN" : "LIE",
        "SRI LANKA" : "LKA",
        "LESOTHO" : "LSO",
        "LITHUANIA" : "LTU",
        "LUXEMBOURG" : "LUX",
        "LATVIA" : "LVA",
        "MACAO" : "MAC",
        "SAINT MARTIN (FRENCH PART)" : "MAF",
        "MOROCCO" : "MAR",
        "MONACO" : "MCO",
        "MOLDOVA, REPUBLIC OF" : "MDA",
        "MADAGASCAR" : "MDG",
        "MALDIVES" : "MDV",
        "MEXICO" : "MEX",
        "MARSHALL ISLANDS" : "MHL",
        "MACEDONIA, REPUBLIC OF" : "MKD",
        "MALI" : "MLI",
        "MALTA" : "MLT",
        "MYANMAR" : "MMR",
        "MONTENEGRO" : "MNE",
        "MONGOLIA" : "MNG",
        "NORTHERN MARIANA ISLANDS" : "MNP",
        "MOZAMBIQUE" : "MOZ",
        "MAURITANIA" : "MRT",
        "MONTSERRAT" : "MSR",
        "MARTINIQUE" : "MTQ",
        "MAURITIUS" : "MUS",
        "MALAWI" : "MWI",
        "MALAYSIA" : "MYS",
        "MAYOTTE" : "MYT",
        "NAMIBIA" : "NAM",
        "NEW CALEDONIA" : "NCL",
        "NIGER" : "NER",
        "NORFOLK ISLAND" : "NFK",
        "NIGERIA" : "NGA",
        "NICARAGUA" : "NIC",
        "NIUE" : "NIU",
        "NETHERLANDS" : "NLD",
        "NORWAY" : "NOR",
        "NEPAL" : "NPL",
        "NAURU" : "NRU",
        "NEW ZEALAND" : "NZL",
        "OMAN" : "OMN",
        "PAKISTAN" : "PAK",
        "PANAMA" : "PAN",
        "PITCAIRN" : "PCN",
        "PERU" : "PER",
        "PHILIPPINES" : "PHL",
        "PALAU" : "PLW",
        "PAPUA NEW GUINEA" : "PNG",
        "POLAND" : "POL",
        "PUERTO RICO" : "PRI",
        "KOREA, DEMOCRATIC PEOPLE'S REPUBLIC OF" : "PRK",
        "PORTUGAL" : "PRT",
        "PARAGUAY" : "PRY",
        "PALESTINE, STATE OF" : "PSE",
        "FRENCH POLYNESIA" : "PYF",
        "QATAR" : "QAT",
        "RÉUNION" : "REU",
        "ROMANIA" : "ROU",
        "RUSSIAN FEDERATION" : "RUS",
        "RWANDA" : "RWA",
        "SAUDI ARABIA" : "SAU",
        "SUDAN" : "SDN",
        "SENEGAL" : "SEN",
        "SINGAPORE" : "SGP",
        "SOUTH GEORGIA AND THE SOUTH SANDWICH ISLANDS" : "SGS",
        "SAINT HELENA, ASCENSION AND TRISTAN DA CUNHA" : "SHN",
        "SVALBARD AND JAN MAYEN" : "SJM",
        "SOLOMON ISLANDS" : "SLB",
        "SIERRA LEONE" : "SLE",
        "EL SALVADOR" : "SLV",
        "SAN MARINO" : "SMR",
        "SOMALIA" : "SOM",
        "SAINT PIERRE AND MIQUELON" : "SPM",
        "SERBIA" : "SRB",
        "SOUTH SUDAN" : "SSD",
        "SAO TOME AND PRINCIPE" : "STP",
        "SURINAME" : "SUR",
        "SLOVAKIA" : "SVK",
        "SLOVENIA" : "SVN",
        "SWEDEN" : "SWE",
        "SWAZILAND" : "SWZ",
        "SINT MAARTEN (DUTCH PART)" : "SXM",
        "SEYCHELLES" : "SYC",
        "SYRIAN ARAB REPUBLIC" : "SYR",
        "TURKS AND CAICOS ISLANDS" : "TCA",
        "CHAD" : "TCD",
        "TOGO" : "TGO",
        "THAILAND" : "THA",
        "TAJIKISTAN" : "TJK",
        "TOKELAU" : "TKL",
        "TURKMENISTAN" : "TKM",
        "TIMOR-LESTE" : "TLS",
        "TONGA" : "TON",
        "TRINIDAD AND TOBAGO" : "TTO",
        "TUNISIA" : "TUN",
        "TURKEY" : "TUR",
        "TUVALU" : "TUV",
        "TAIWAN, PROVINCE OF CHINA" : "TWN",
        "TANZANIA, UNITED REPUBLIC OF" : "TZA",
        "UGANDA" : "UGA",
        "UKRAINE" : "UKR",
        "UNITED STATES MINOR OUTLYING ISLANDS" : "UMI",
        "URUGUAY" : "URY",
        "UNITED STATES" : "USA",
        "UZBEKISTAN" : "UZB",
        "HOLY SEE (VATICAN CITY STATE)" : "VAT",
        "SAINT VINCENT AND THE GRENADINES" : "VCT",
        "VENEZUELA, BOLIVARIAN REPUBLIC OF" : "VEN",
        "VIRGIN ISLANDS, BRITISH" : "VGB",
        "VIRGIN ISLANDS, U.S." : "VIR",
        "VIET NAM" : "VNM",
        "VANUATU" : "VUT",
        "WALLIS AND FUTUNA" : "WLF",
        "SAMOA" : "WSM",
        "YEMEN" : "YEM",
        "SOUTH AFRICA" : "ZAF",
        "ZAMBIA" : "ZMB",
        "ZIMBABWE" : "ZWE",
        "BOLIVIA" : "BOL",
        "MOLDOVA" : "MDA",
        "TAIWAN" : "TWN",
        "TANZANIA" : "TZA",
        "VENEZUELA" : "VEN",
        "VIETNAM" : "VNM",
        "ISLAMIC REPUBLIC OF AFGHANISTAN" : "AFG",
        "REPUBLIC OF ANGOLA" : "AGO",
        "REPUBLIC OF ALBANIA" : "ALB",
        "PRINCIPALITY OF ANDORRA" : "AND",
        "ARGENTINE REPUBLIC" : "ARG",
        "REPUBLIC OF ARMENIA" : "ARM",
        "REPUBLIC OF AUSTRIA" : "AUT",
        "REPUBLIC OF AZERBAIJAN" : "AZE",
        "REPUBLIC OF BURUNDI" : "BDI",
        "KINGDOM OF BELGIUM" : "BEL",
        "REPUBLIC OF BENIN" : "BEN",
        "BONAIRE, SINT EUSTATIUS AND SABA" : "BES",
        "PEOPLE'S REPUBLIC OF BANGLADESH" : "BGD",
        "REPUBLIC OF BULGARIA" : "BGR",
        "KINGDOM OF BAHRAIN" : "BHR",
        "COMMONWEALTH OF THE BAHAMAS" : "BHS",
        "REPUBLIC OF BOSNIA AND HERZEGOVINA" : "BIH",
        "REPUBLIC OF BELARUS" : "BLR",
        "PLURINATIONAL STATE OF BOLIVIA" : "BOL",
        "FEDERATIVE REPUBLIC OF BRAZIL" : "BRA",
        "KINGDOM OF BHUTAN" : "BTN",
        "REPUBLIC OF BOTSWANA" : "BWA",
        "SWISS CONFEDERATION" : "CHE",
        "REPUBLIC OF CHILE" : "CHL",
        "PEOPLE'S REPUBLIC OF CHINA" : "CHN",
        "REPUBLIC OF CÔTE D'IVOIRE" : "CIV",
        "REPUBLIC OF CAMEROON" : "CMR",
        "REPUBLIC OF THE CONGO" : "COG",
        "REPUBLIC OF COLOMBIA" : "COL",
        "UNION OF THE COMOROS" : "COM",
        "REPUBLIC OF CABO VERDE" : "CPV",
        "REPUBLIC OF COSTA RICA" : "CRI",
        "REPUBLIC OF CUBA" : "CUB",
        "CURAÇAO" : "CUW",
        "REPUBLIC OF CYPRUS" : "CYP",
        "CZECH REPUBLIC" : "CZE",
        "FEDERAL REPUBLIC OF GERMANY" : "DEU",
        "REPUBLIC OF DJIBOUTI" : "DJI",
        "COMMONWEALTH OF DOMINICA" : "DMA",
        "KINGDOM OF DENMARK" : "DNK",
        "PEOPLE'S DEMOCRATIC REPUBLIC OF ALGERIA" : "DZA",
        "REPUBLIC OF ECUADOR" : "ECU",
        "ARAB REPUBLIC OF EGYPT" : "EGY",
        "THE STATE OF ERITREA" : "ERI",
        "KINGDOM OF SPAIN" : "ESP",
        "REPUBLIC OF ESTONIA" : "EST",
        "FEDERAL DEMOCRATIC REPUBLIC OF ETHIOPIA" : "ETH",
        "REPUBLIC OF FINLAND" : "FIN",
        "REPUBLIC OF FIJI" : "FJI",
        "FRENCH REPUBLIC" : "FRA",
        "FEDERATED STATES OF MICRONESIA" : "FSM",
        "GABONESE REPUBLIC" : "GAB",
        "UNITED KINGDOM OF GREAT BRITAIN AND NORTHERN IRELAND" : "GBR",
        "REPUBLIC OF GHANA" : "GHA",
        "REPUBLIC OF GUINEA" : "GIN",
        "ISLAMIC REPUBLIC OF THE GAMBIA" : "GMB",
        "REPUBLIC OF GUINEA-BISSAU" : "GNB",
        "REPUBLIC OF EQUATORIAL GUINEA" : "GNQ",
        "HELLENIC REPUBLIC" : "GRC",
        "REPUBLIC OF GUATEMALA" : "GTM",
        "REPUBLIC OF GUYANA" : "GUY",
        "HONG KONG SPECIAL ADMINISTRATIVE REGION OF CHINA" : "HKG",
        "REPUBLIC OF HONDURAS" : "HND",
        "REPUBLIC OF CROATIA" : "HRV",
        "REPUBLIC OF HAITI" : "HTI",
        "HUNGARY" : "HUN",
        "REPUBLIC OF INDONESIA" : "IDN",
        "REPUBLIC OF INDIA" : "IND",
        "ISLAMIC REPUBLIC OF IRAN" : "IRN",
        "REPUBLIC OF IRAQ" : "IRQ",
        "REPUBLIC OF ICELAND" : "ISL",
        "STATE OF ISRAEL" : "ISR",
        "ITALIAN REPUBLIC" : "ITA",
        "HASHEMITE KINGDOM OF JORDAN" : "JOR",
        "REPUBLIC OF KAZAKHSTAN" : "KAZ",
        "REPUBLIC OF KENYA" : "KEN",
        "KYRGYZ REPUBLIC" : "KGZ",
        "KINGDOM OF CAMBODIA" : "KHM",
        "REPUBLIC OF KIRIBATI" : "KIR",
        "STATE OF KUWAIT" : "KWT",
        "LEBANESE REPUBLIC" : "LBN",
        "REPUBLIC OF LIBERIA" : "LBR",
        "LIBYA" : "LBY",
        "PRINCIPALITY OF LIECHTENSTEIN" : "LIE",
        "DEMOCRATIC SOCIALIST REPUBLIC OF SRI LANKA" : "LKA",
        "KINGDOM OF LESOTHO" : "LSO",
        "REPUBLIC OF LITHUANIA" : "LTU",
        "GRAND DUCHY OF LUXEMBOURG" : "LUX",
        "REPUBLIC OF LATVIA" : "LVA",
        "MACAO SPECIAL ADMINISTRATIVE REGION OF CHINA" : "MAC",
        "KINGDOM OF MOROCCO" : "MAR",
        "PRINCIPALITY OF MONACO" : "MCO",
        "REPUBLIC OF MOLDOVA" : "MDA",
        "REPUBLIC OF MADAGASCAR" : "MDG",
        "REPUBLIC OF MALDIVES" : "MDV",
        "UNITED MEXICAN STATES" : "MEX",
        "REPUBLIC OF THE MARSHALL ISLANDS" : "MHL",
        "THE FORMER YUGOSLAV REPUBLIC OF MACEDONIA" : "MKD",
        "REPUBLIC OF MALI" : "MLI",
        "REPUBLIC OF MALTA" : "MLT",
        "REPUBLIC OF MYANMAR" : "MMR",
        "MONTENEGRO" : "MNE",
        "COMMONWEALTH OF THE NORTHERN MARIANA ISLANDS" : "MNP",
        "REPUBLIC OF MOZAMBIQUE" : "MOZ",
        "ISLAMIC REPUBLIC OF MAURITANIA" : "MRT",
        "REPUBLIC OF MAURITIUS" : "MUS",
        "REPUBLIC OF MALAWI" : "MWI",
        "REPUBLIC OF NAMIBIA" : "NAM",
        "REPUBLIC OF THE NIGER" : "NER",
        "FEDERAL REPUBLIC OF NIGERIA" : "NGA",
        "REPUBLIC OF NICARAGUA" : "NIC",
        "NIUE" : "NIU",
        "KINGDOM OF THE NETHERLANDS" : "NLD",
        "KINGDOM OF NORWAY" : "NOR",
        "FEDERAL DEMOCRATIC REPUBLIC OF NEPAL" : "NPL",
        "REPUBLIC OF NAURU" : "NRU",
        "SULTANATE OF OMAN" : "OMN",
        "ISLAMIC REPUBLIC OF PAKISTAN" : "PAK",
        "REPUBLIC OF PANAMA" : "PAN",
        "REPUBLIC OF PERU" : "PER",
        "REPUBLIC OF THE PHILIPPINES" : "PHL",
        "REPUBLIC OF PALAU" : "PLW",
        "INDEPENDENT STATE OF PAPUA NEW GUINEA" : "PNG",
        "REPUBLIC OF POLAND" : "POL",
        "DEMOCRATIC PEOPLE'S REPUBLIC OF KOREA" : "PRK",
        "PORTUGUESE REPUBLIC" : "PRT",
        "REPUBLIC OF PARAGUAY" : "PRY",
        "THE STATE OF PALESTINE" : "PSE",
        "STATE OF QATAR" : "QAT",
        "RWANDESE REPUBLIC" : "RWA",
        "KINGDOM OF SAUDI ARABIA" : "SAU",
        "REPUBLIC OF THE SUDAN" : "SDN",
        "REPUBLIC OF SENEGAL" : "SEN",
        "REPUBLIC OF SINGAPORE" : "SGP",
        "REPUBLIC OF SIERRA LEONE" : "SLE",
        "REPUBLIC OF EL SALVADOR" : "SLV",
        "REPUBLIC OF SAN MARINO" : "SMR",
        "FEDERAL REPUBLIC OF SOMALIA" : "SOM",
        "REPUBLIC OF SERBIA" : "SRB",
        "REPUBLIC OF SOUTH SUDAN" : "SSD",
        "DEMOCRATIC REPUBLIC OF SAO TOME AND PRINCIPE" : "STP",
        "REPUBLIC OF SURINAME" : "SUR",
        "SLOVAK REPUBLIC" : "SVK",
        "REPUBLIC OF SLOVENIA" : "SVN",
        "KINGDOM OF SWEDEN" : "SWE",
        "KINGDOM OF SWAZILAND" : "SWZ",
        "SINT MAARTEN (DUTCH PART)" : "SXM",
        "REPUBLIC OF SEYCHELLES" : "SYC",
        "REPUBLIC OF CHAD" : "TCD",
        "TOGOLESE REPUBLIC" : "TGO",
        "KINGDOM OF THAILAND" : "THA",
        "REPUBLIC OF TAJIKISTAN" : "TJK",
        "DEMOCRATIC REPUBLIC OF TIMOR-LESTE" : "TLS",
        "KINGDOM OF TONGA" : "TON",
        "REPUBLIC OF TRINIDAD AND TOBAGO" : "TTO",
        "REPUBLIC OF TUNISIA" : "TUN",
        "REPUBLIC OF TURKEY" : "TUR",
        "TAIWAN, PROVINCE OF CHINA" : "TWN",
        "UNITED REPUBLIC OF TANZANIA" : "TZA",
        "REPUBLIC OF UGANDA" : "UGA",
        "EASTERN REPUBLIC OF URUGUAY" : "URY",
        "UNITED STATES OF AMERICA" : "USA",
        "REPUBLIC OF UZBEKISTAN" : "UZB",
        "BOLIVARIAN REPUBLIC OF VENEZUELA" : "VEN",
        "BRITISH VIRGIN ISLANDS" : "VGB",
        "VIRGIN ISLANDS OF THE UNITED STATES" : "VIR",
        "SOCIALIST REPUBLIC OF VIET NAM" : "VNM",
        "REPUBLIC OF VANUATU" : "VUT",
        "INDEPENDENT STATE OF SAMOA" : "WSM",
        "REPUBLIC OF YEMEN" : "YEM",
        "REPUBLIC OF SOUTH AFRICA" : "ZAF",
        "REPUBLIC OF ZAMBIA" : "ZMB",
        "REPUBLIC OF ZIMBABWE" : "ZWE",
        "BOLIVIA (PLURINATIONAL STATE OF)" : "BOL",
        "BRUNEI" : "BRN",
        "BURKINA" : "BFA",
        "BURMA" : "MMR",
        "DEMOCRATIC REPUBLIC OF CONGO": "COD",
        "DEMOCRATIC REPUBLIC OF THE CONGO": "COD",
        "EAST TIMOR": "TLS",
        "HOLY SEE": "VAT",
        "IRAN": "IRN",
        "IRAN (ISLAMIC REPUBLIC OF)": "IRN",
        "IVORY COAST": "CIV",
        "KOREA": "KOR",
        "LAOS": "LAO",
        "MACEDONIA": "MKD",
        "MICRONESIA": "FSM",
        "MICRONESIA (FEDERATED STATES OF)": "FSM",
        "REPUBLIC OF KOREA": "KOR",
        "KOREA, REPUBLIC": "KOR",
        "SOUTH KOREA": "KOR",
        "SYRIA": "SYR",
        "THE FORMER YUGOSLAV REPUBLIC OF MACEDONIA": "MKD",
        "VATICAN CITY": "VAT",
        "VENEZUELA (BOLIVARIAN REPUBLIC OF)": "VEN",
        "GLOBAL": "001", # World area UN M49
        "USA": "USA",
        "PALESTINE" : "PSE",
        "RUSSIA": "RUS",
        "ZAIRE": None
    }.get(label.upper(), None)

# potential new langs!!!!
# lit, lt, Lithuanian
# lav, lv, Latvian
# ron, ro, Romanian
# fin, fi, Finnish
# tha, th, Thai
# kat, ka, Georgian
# nep, ne, Nepali
# hbs, sh, Serbo-Croatian
# glg, gl, Galician
# mao, mi, Māori
# cat, ca, Catalan
# nde, nd, Northern Ndebele
# ben, bn, Bengali
# hin, hi, Hindi
# est, et, Estonian
# sna, sn, Shona
# may, ms, Malay
# pan, pa, (Eastern) Punjabi
# heb, he, Hebrew (modern)
# mal, ml, Malayalam
# afr, af, Afrikaans
# lat, la, Latin

#Langs: set(['ru', 'fr', 'en', 'nl', None, 'pt', 'sr', 'de', 'tr', 'hu', 'lv', 'pl', 'sk', 'th', 'cs', 'ro', 'es'])

########## REAL NEW LANGS: LV, TH, RO

# NOT mapped
# eth - Ethiopian Sign Language
# gmh - Middle High German (ca. 1050-1500)
# tag - Tagoi
# mul - Multiple languages
# und - Undetermined
# Es9 [wrong]
# En. [wrong] = Maybe English


def getISO639_1code_from_ISO639_3code(code):
    return {
        "aze" : "az",
        "lit" : "lt",
        "fin" : "fi",
        "tur" : "tr",
        "srp" : "sr",
        "kat" : "ka",
        "alb" : "sq",
        "khm" : "km",
        "ind" : "id",
        "scc" : "sr", # The ISO 639-2/T code srp deprecated the ISO 639-2/B code scc
        "nob" : "no", # Norsk bokmål. Covered by macrolanguage [no/nor]
        "nep" : "ne", # Nepali
        "hbs" : "sh", # Serbo-Croatian. http://www-01.sil.org/iso639-3/documentation.asp?id=hbs
        "glg" : "gl", # Galician
        "mao" : "mi", # Māori
        "cat" : "ca", # Catalan
        "nde" : "nd", # Northern Ndebele
        "ben" : "bn", # Bengali
        "hin" : "hi", # Hindi
        "est" : "et", # Estonian
        "sna" : "sn", # Shona
        "may" : "ms", # Malay
        "pan" : "pa", # (Eastern) Punjabi
        "heb" : "he", # Hebrew (modern)
        "mal" : "ml", # Malayalam
        "afr" : "af", # Afrikaans
        "lat" : "la", # Latin
    }.get(code, None)


def getISO639_1code(label):
    return {
        "Albanian" : "sq",
        "Arabic" : "ar",
        "Azerbaijani" : "az",
        "Bosnian" : "bs",
        "Bulgarian" : "bg",
        "Catalan" : "ca",
        "Chinese" : "zh",
        "Chineset" : "zh",
        "Croatian" : "hr",
        "Czech" : "cs",
        "Danish" : "da",
        "Dutch" : "nl",
        "English" : "en",
        "Farsi" : "fa",
        "French" : "fr",
        "German" : "de",
        "Greek" : "el",
        "Hungarian" : "hu",
        "Indonesian" : "id",
        "Italian" : "it",
        "Japanese": "ja",
        "Korean": "ko",
        "Latvian": "lv",
        "Macedonian" : "mk",
        "Montenegrin" : "sr",
        "Norwegian" : "no",
        "Polish" : "pl",
        "Portuguese" : "pt",
        "Russian" : "ru",
        "Romanian": "ro",
        "Serbian" : "sr",
        "Serbo-Croatian" : "sh",
        "Slovak" : "sk",
        "Slovenian" : "sl",
        "Spanish" : "es",
        "Swedish" : "sv",
        "Thai" : "th",
        "Turkish" : "tr",
        "Ukrainian" : "uk",
    }.get(label, None)


def getLLR_type(label):
    return {
        "Conference" : "Conference Papers & Reports",
        "Bibliography" : "Journal Articles & Books",
        "Lit. Review" : "Journal Articles & Books",
        "Book" : "Journal Articles & Books",
        "Web site": "Multimedia",
        "Journal Article": "Journal Articles & Books",
        "Summary": "Policy Papers & Briefs",
        "Report": "Reports & Research",
        "Working Paper": "Policy Papers & Briefs",
        "Thesis": "Journal Articles & Books",
        "Handbook/Manual": "Manuals & Guidelines",
        "Maps or Atlases" : "Maps",
    }.get(label, None)


# dev_contries = ["Algeria", "Egypt", "Libya", "Mauritania", "Morocco", "Sudan", "Tunisia", "Angola", "Botswana", "Lesotho", "Malawi", "Mauritius", "Mozambique", "Namibia", "South Africa", "Zambia", "Zimbabwe", "Brunei Darussalam", "China", "Hong Kong", "Indonesia", "Malaysia", "Myanmar", "Papua New Guinea", "Philippines", "Republic of Korea", "Singapore", "Thailand", "Viet Nam", "Barbados", "Cuba", "Dominican Republic", "Guyana", "Haiti", "Jamaica", "Trinidad and Tobago", "Cameroon", "Central African Republic", "Chad", "Congo", "Equatorial Guinea", "Gabon", "Sao Tome and Principe", "Costa Rica", "El Salvador", "Guatemala", "Honduras", "Mexico", "Nicaragua", "Panama", "Benin", "Burkina Faso", "Cabo Verde", "Gambia", "Ghana", "Guinea", "Guinea-Bissau", "Liberia", "Mali", "Niger", "Nigeria", "Senegal", "Sierra Leone", "Togo", "Bangladesh", "India", "Iran (Islamic Republic of)", "Nepal", "Pakistan", "Sri Lanka", "Burundi", "Comoros", "Democratic Republic of the Congo", "Djibouti", "Eritrea", "Ethiopia", "Kenya", "Madagascar", "Rwanda", "Somalia", "Uganda", "United Republic of Tanzania", "Argentina", "Bolivia (Plurinational State of)", "Brazil", "Chile", "Colombia", "Ecuador", "Paraguay", "Peru", "Uruguay", "Venezuela (Bolivarian Republic of)", "Bahrain", "Iraq", "Israel", "Jordan", "Kuwait", "Lebanon", "Oman", "Qatar", "Saudi Arabia", "Syria", "Turkey", "United Arab Emirates", "Yemen", "COTE D'IVOIRE"]
# for c in dev_contries:
#     print "<http://data.landportal.info/geo/"+getISO3166_1code(c.upper())+">"

harvest_dict = {
    "access to land" : "http://aims.fao.org/aos/agrovoc/c_9000090",
    "agrarian law" : "http://aims.fao.org/aos/agrovoc/c_28633",
    "agrarian reform" : "http://aims.fao.org/aos/agrovoc/c_196",
    "agrarian structure of land" : "http://aims.fao.org/aos/agrovoc/c_7193",
    "agricultural land management" : "http://aims.fao.org/aos/agrovoc/c_4bd6790a",
    "agricultural landscape" : "http://aims.fao.org/aos/agrovoc/c_37277",
    "agroforestry systems" : "http://aims.fao.org/aos/agrovoc/c_330982",
    "agropastoralism" : "http://aims.fao.org/aos/agrovoc/c_16112",
    "alienated land" : "http://aims.fao.org/aos/agrovoc/c_ceb73ce1",
    "alienation of land" : "http://aims.fao.org/aos/agrovoc/c_ceb73ce1",
    "animal husbandry" : "http://aims.fao.org/aos/agrovoc/c_8532",
    "aquaculture" : "http://aims.fao.org/aos/agrovoc/c_550",
    "cadastral administration of land" : "http://aims.fao.org/aos/agrovoc/c_d774aa00",
    "cadastre administration" : "http://aims.fao.org/aos/agrovoc/c_d774aa00",
    "capital value of land" : "http://aims.fao.org/aos/agrovoc/c_a9966ac9",
    "cedaw" : "http://aims.fao.org/aos/agrovoc/c_958edb9d",
    "cedaw land" : "http://aims.fao.org/aos/agrovoc/c_958edb9d",
    "common land" : "http://aims.fao.org/aos/agrovoc/c_778a14cf",
    "common law on land" : "http://aims.fao.org/aos/agrovoc/c_1783",
    "common rights" : "http://aims.fao.org/aos/agrovoc/c_de048871",
    "communal land ownership" : "http://aims.fao.org/aos/agrovoc/c_9024771d",
    "communal territory" : "http://aims.fao.org/aos/agrovoc/c_41b77c02",
    "community forestry" : "http://aims.fao.org/aos/agrovoc/c_16532",
    "conflict of interest" : "http://aims.fao.org/aos/agrovoc/c_854e9e62",
    "contract farming" : "http://aims.fao.org/aos/agrovoc/c_1839",
    "co-ownership rights" : "http://aims.fao.org/aos/agrovoc/c_599d2e5c",
    "customary land rights" : "http://aims.fao.org/aos/agrovoc/c_cd44c0b3",
    "customary law" : "http://aims.fao.org/aos/agrovoc/c_10222",
    "customary law on land" : "http://aims.fao.org/aos/agrovoc/c_10222",
    "customary rights" : "http://aims.fao.org/aos/agrovoc/c_cd44c0b3",
    "deforestation" : "http://aims.fao.org/aos/agrovoc/c_15590",
    "development agencies" : "http://aims.fao.org/aos/agrovoc/c_2224",
    "eminent domain" : "http://aims.fao.org/aos/agrovoc/c_c208d7f3",
    "encroached land" : "http://aims.fao.org/aos/agrovoc/c_a245096c",
    "extensive land use" : "http://aims.fao.org/aos/agrovoc/c_36552",
    "farm tenancy" : "http://aims.fao.org/aos/agrovoc/c_dec8141f",
    "farmers associations" : "http://aims.fao.org/aos/agrovoc/c_2806",
    "farmers organizations" : "http://aims.fao.org/aos/agrovoc/c_37175",
    "forest law" : "http://aims.fao.org/aos/agrovoc/c_8c59c597",
    "geographical information systems" : "http://aims.fao.org/aos/agrovoc/c_35131",
    "grazing land rights" : "http://aims.fao.org/aos/agrovoc/c_97241aeb",
    "grazing lands" : "http://aims.fao.org/aos/agrovoc/c_3369",
    "grazing rights" : "http://aims.fao.org/aos/agrovoc/c_97241aeb",
    "indigenous land tenure" : "http://aims.fao.org/aos/agrovoc/c_a291ae58",
    "indigenous lands" : "http://aims.fao.org/aos/agrovoc/c_86524ff8",
    "intensive land use" : "http://aims.fao.org/aos/agrovoc/c_36551",
    "land access" : "http://aims.fao.org/aos/agrovoc/c_9000090",
    "land acquisition" : "http://aims.fao.org/aos/agrovoc/c_89d3dcbb",
    "land administration" : "http://aims.fao.org/aos/agrovoc/c_9000091",
    "land alienation" : "http://aims.fao.org/aos/agrovoc/c_ceb73ce1",
    "land area" : "http://aims.fao.org/aos/agrovoc/c_330588",
    "land assignment" : "http://aims.fao.org/aos/agrovoc/c_8c6882ab",
    "land based collateral" : "http://aims.fao.org/aos/agrovoc/c_931da360",
    "land cadastre" : "http://aims.fao.org/aos/agrovoc/c_1177",
    "land clearing" : "http://aims.fao.org/aos/agrovoc/c_1662",
    "land collective ownership" : "http://aims.fao.org/aos/agrovoc/c_29157",
    "land concentration" : "http://aims.fao.org/aos/agrovoc/c_8654e90e",
    "land concession" : "http://aims.fao.org/aos/agrovoc/c_357653f9",
    "land conflicts" : "http://aims.fao.org/aos/agrovoc/c_e236b2b1",
    "land consolidation" : "http://aims.fao.org/aos/agrovoc/c_4173",
    "land cover" : "http://aims.fao.org/aos/agrovoc/c_37897",
    "land cover mapping" : "http://aims.fao.org/aos/agrovoc/c_9000094",
    "land decentralization" : "http://aims.fao.org/aos/agrovoc/c_2143",
    "land degradation" : "http://aims.fao.org/aos/agrovoc/c_34823",
    "land development" : "http://aims.fao.org/aos/agrovoc/c_331049",
    "land dispute" : "http://aims.fao.org/aos/agrovoc/c_1ada969a",
    "land distribution" : "http://aims.fao.org/aos/agrovoc/c_37734",
    "land diversion" : "http://aims.fao.org/aos/agrovoc/c_28716",
    "land dowry " : "http://aims.fao.org/aos/agrovoc/c_f7cf8606",
    "land economics" : "http://aims.fao.org/aos/agrovoc/c_25195",
    "land eminent domain" : "http://aims.fao.org/aos/agrovoc/c_c208d7f3",
    "land encroachment" : "http://aims.fao.org/aos/agrovoc/c_a245096c",
    "land environment" : "http://aims.fao.org/aos/agrovoc/c_7ffc9d69",
    "land eviction" : "http://aims.fao.org/aos/agrovoc/c_0b88a82c",
    "land expropriation" : "http://aims.fao.org/aos/agrovoc/c_1798",
    "land geomatics" : "http://aims.fao.org/aos/agrovoc/c_92332",
    "land grab" : "http://aims.fao.org/aos/agrovoc/c_cc39a497",
    "land grabbing" : "http://aims.fao.org/aos/agrovoc/c_cc39a497",
    "land green belts" : "http://aims.fao.org/aos/agrovoc/c_37720",
    "land improvement" : "http://aims.fao.org/aos/agrovoc/c_28717",
    "land information systems" : "http://aims.fao.org/aos/agrovoc/c_9000096",
    "land inheritance rights" : "http://aims.fao.org/aos/agrovoc/c_70a14ab3",
    "land investments" : "http://aims.fao.org/aos/agrovoc/c_9a4f48b4",
    "land law" : "http://aims.fao.org/aos/agrovoc/c_573abb9f",
    "land loans" : "http://aims.fao.org/aos/agrovoc/c_8b6d895f",
    "land management" : "http://aims.fao.org/aos/agrovoc/c_24866",
    "land management rights" : "http://aims.fao.org/aos/agrovoc/c_862db225",
    "land map scale" : "http://aims.fao.org/aos/agrovoc/c_128d5eb6",
    "land markets" : "http://aims.fao.org/aos/agrovoc/c_4175",
    "land occupation" : "http://aims.fao.org/aos/agrovoc/c_9044ce39",
    "land of local community" : "http://aims.fao.org/aos/agrovoc/c_45cd8441",
    "land of non indigenous peoples" : "http://aims.fao.org/aos/agrovoc/c_28e0dafa",
    "land open access" : "http://aims.fao.org/aos/agrovoc/c_51a39a94",
    "land ownership" : "http://aims.fao.org/aos/agrovoc/c_28718",
    "land perimeter" : "http://aims.fao.org/aos/agrovoc/c_db4161cb",
    "land policies" : "http://aims.fao.org/aos/agrovoc/c_195",
    "land prescription" : "http://aims.fao.org/aos/agrovoc/c_f86e1a09",
    "land property rights" : "http://aims.fao.org/aos/agrovoc/c_37942",
    "land reform" : "http://aims.fao.org/aos/agrovoc/c_4178",
    "land reforms" : "http://aims.fao.org/aos/agrovoc/c_bb4738d4",
    "land registration" : "http://aims.fao.org/aos/agrovoc/c_9000098",
    "land rent" : "http://aims.fao.org/aos/agrovoc/c_7bea427c",
    "land rights in divorce" : "http://aims.fao.org/aos/agrovoc/c_b3372020",
    "land rights of orphans" : "http://aims.fao.org/aos/agrovoc/c_e5f9b786",
    "land rural planning" : "http://aims.fao.org/aos/agrovoc/c_6704",
    "land speculation" : "http://aims.fao.org/aos/agrovoc/c_15d85712",
    "land suitability" : "http://aims.fao.org/aos/agrovoc/c_15992",
    "land surveyors" : "http://aims.fao.org/aos/agrovoc/c_26e30c73",
    "land tax" : "http://aims.fao.org/aos/agrovoc/c_4180",
    "land tenant" : "http://aims.fao.org/aos/agrovoc/c_330886",
    "land tenant's rights" : "http://aims.fao.org/aos/agrovoc/c_28775",
    "land tenure" : "http://aims.fao.org/aos/agrovoc/c_12069",
    "land tenure system" : "http://aims.fao.org/aos/agrovoc/c_66afb052",
    "land territory" : "http://aims.fao.org/aos/agrovoc/c_a9e7dd7f",
    "land transfers" : "http://aims.fao.org/aos/agrovoc/c_4181",
    "land use mapping" : "http://aims.fao.org/aos/agrovoc/c_9000100",
    "land use planning" : "http://aims.fao.org/aos/agrovoc/c_37899",
    "land use rights" : "http://aims.fao.org/aos/agrovoc/c_945c9e82",
    "landlessness" : "http://aims.fao.org/aos/agrovoc/c_24403",
    "landowners" : "http://aims.fao.org/aos/agrovoc/c_4184",
    "latifundium" : "http://aims.fao.org/aos/agrovoc/c_9c0e84b3",
    "lineage" : "http://aims.fao.org/aos/agrovoc/c_29225",
    "lineage land" : "http://aims.fao.org/aos/agrovoc/c_d08b21b6",
    "marital property rights" : "http://aims.fao.org/aos/agrovoc/c_64d8574a",
    "marital property rights about land" : "http://aims.fao.org/aos/agrovoc/c_64d8574a",
    "matrilineal land" : "http://aims.fao.org/aos/agrovoc/c_a0982198",
    "nature reserves" : "http://aims.fao.org/aos/agrovoc/c_16141",
    "negotiated land reform" : "http://aims.fao.org/aos/agrovoc/c_f84a48c4",
    "notary" : "http://aims.fao.org/aos/agrovoc/c_72efbdb8",
    "pastoral land rights" : "http://aims.fao.org/aos/agrovoc/c_4d6b6100",
    "pastoral lands" : "http://aims.fao.org/aos/agrovoc/c_8e487587",
    "patrilineal land" : "http://aims.fao.org/aos/agrovoc/c_85dfd05c",
    "prescriptive property" : "http://aims.fao.org/aos/agrovoc/c_f86e1a09",
    "prescriptive rights" : "http://aims.fao.org/aos/agrovoc/c_f86e1a09",
    "priest of the land" : "http://aims.fao.org/aos/agrovoc/c_28f78be5",
    "private ownership of land" : "http://aims.fao.org/aos/agrovoc/c_6192",
    "property law about land" : "http://aims.fao.org/aos/agrovoc/c_da192f3f",
    "protected land areas" : "http://aims.fao.org/aos/agrovoc/c_37952",
    "public ownership of land" : "http://aims.fao.org/aos/agrovoc/c_6350",
    "rangelands" : "http://aims.fao.org/aos/agrovoc/c_6448",
    "regularization of land ownership" : "http://aims.fao.org/aos/agrovoc/c_d190bc52",
    "right of access" : "http://aims.fao.org/aos/agrovoc/c_6604",
    "right of first occupancy" : "http://aims.fao.org/aos/agrovoc/c_9904d265",
    "right of land access" : "http://aims.fao.org/aos/agrovoc/c_6604",
    "right of land clearance" : "http://aims.fao.org/aos/agrovoc/c_62487b4a",
    "rural areas" : "http://aims.fao.org/aos/agrovoc/c_6699",
    "rural land use planning" : "http://aims.fao.org/aos/agrovoc/c_6704",
    "rural population" : "http://aims.fao.org/aos/agrovoc/c_6705",
    "sacred woods" : "http://aims.fao.org/aos/agrovoc/c_c0a7f4fb",
    "scrublands" : "http://aims.fao.org/aos/agrovoc/c_6887",
    "security of land tenure" : "http://aims.fao.org/aos/agrovoc/c_7fc44e33",
    "security of tenure" : "http://aims.fao.org/aos/agrovoc/c_7fc44e33",
    "state property" : "http://aims.fao.org/aos/agrovoc/c_22d01a32",
    "statute law" : "http://aims.fao.org/aos/agrovoc/c_86cb818a",
    "suburban agriculture" : "http://aims.fao.org/aos/agrovoc/c_18389",
    "sustainable land management" : "http://aims.fao.org/aos/agrovoc/c_36580",
    "tenant farmer" : "http://aims.fao.org/aos/agrovoc/c_f73955fb",
    "title deed" : "http://aims.fao.org/aos/agrovoc/c_b769471e",
    "torrens cadastral system " : "http://aims.fao.org/aos/agrovoc/c_7017dc39",
    "torrens system" : "http://aims.fao.org/aos/agrovoc/c_7017dc39",
    "unclaimed lands" : "http://aims.fao.org/aos/agrovoc/c_0e0e555b",
    "urban areas" : "http://aims.fao.org/aos/agrovoc/c_8085",
    "urban land development" : "http://aims.fao.org/aos/agrovoc/c_4174",
    "water management" : "http://aims.fao.org/aos/agrovoc/c_8320",
    "water rights" : "http://aims.fao.org/aos/agrovoc/c_16062",
    "willing seller" : "http://aims.fao.org/aos/agrovoc/c_88c1b116",
    "zoning" : "http://aims.fao.org/aos/agrovoc/c_36936",
}

def flatten(l):
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, basestring):
            for sub in flatten(el):
                yield sub
        else:
            yield el

def save_set_in_file(filename, set_to_save):
    with open(filename, 'w') as target:
        print "Opening the file="+filename
        for item in set_to_save:
            target.write(item.encode('utf8')+"\n")
        print "Closed the file="+filename

def getmonthNumber(monthLabel):
    return {
        "jan" : "01",
        "ene" : "01",
        "feb" : "02",
        "mar" : "03",
        "apr" : "04",
        "abr" : "04",
        "may" : "05",
        "jun" : "06",
        "jul" : "07",
        "aug" : "08",
        "ago" : "08",
        "sep" : "09",
        "oct" : "10",
        "nov" : "11",
        "dec" : "12",
        "dic" : "12",
    }.get(monthLabel, None)

# concepts_query = ["agrarian law" , "agrarian reform" , "agrarian structure of land" , "agricultural land management" , "agricultural landscape" , "agropastoralism" , "alienation of land"  , "land alienation" , "cadastral administration" , "capital value of land" , "cadastre administration" , "cedaw land" , "common land" , "common law on land" , "common rights" , "communal land ownership" , "communal territory" , "community forestry" , "contract farming" , "cedaw" , "customary land rights" , "customary rights" , "customary law on land" , "extensive land use" , "farm tenancy" , "forest law" , "customary law" , "grazing land rights" , "grazing lands" , "indigenous land tenure" , "indigenous lands" , "intensive land use" , "grazing rights" , "land access" , "land acquisition" , "land administration" , "land area" , "land assignment" , "land based collateral" , "land cadastre" , "land clearing" , "land collective ownership" , "land concentration" , "land concession" , "access to land" , "land conflicts" , "land consolidation" , "land cover" , "land cover mapping" , "land decentralization" , "land degradation" , "land development" , "land dispute" , "land distribution" , "land diversion" , "land dowry " , "land economics" , "land eminent domain" , "eminent domain" , "land encroachment" , "land environment" , "land eviction" , "land expropriation" , "land geomatics" , "encroached land" , "land grabbing" , "land green belts" , "land improvement" , "land information systems" , "land grab" , "land inheritance rights" , "land investments" , "land law" , "land loans" , "land management" , "land management rights" , "land map scale" , "land markets" , "land occupation" , "land of local community" , "land of non indigenous peoples" , "land open access" , "land perimeter" , "land policies" , "land prescription" , "land property rights" , "land reform" , "land reforms" , "land registration" , "land rent" , "land rights in divorce" , "land rights of orphans" , "prescriptive rights" , "prescriptive property" , "rural planning" , "land speculation" , "land suitability" , "land surveyors" , "land tax" , "land tenant" , "land tenure" , "land tenure system" , "land territory" , "land transfers" , "land use mapping" , "land use planning" , "land use rights" , "willing seller" , "landlessness" , "land use planning" , "landowners" , "latifundium" , "lineage" , "lineage land" , "land ownership" , "marital property rights about land" , "matrilineal land" , "negotiated land reform" , "pastoral land" , "patrilineal land" , "priest of the land" , "marital property rights" , "private ownership of land" , "property law about land" , "protected land areas" , "public ownership of land" , "rangelands" , "land ownership" , "land access" , "land clearance" , "right of first occupancy" , "rural areas" , "rural population" , "sacred woods" , "scrublands" , "right of access" , "security of land tenure" , "security of tenure" , "state property" , "statute law" , "suburban agriculture" , "sustainable land management" , "tenant farmer" , "title deed" , "torrens cadastral system " , "torrens system" , "unclaimed lands" , "urban areas" , "urban land development" , "water rights" , "zoning"]
#
# for x in harvest_dict.keys():
#     if x not in concepts_query:
#         print x

def clean_extent (extent):
    pattern_dddp =  re.compile("^[0-9]{1,3}p\.$")
    if re.search(pattern_dddp,extent):
        extent = extent.replace("p.","") # remove the first month
        return extent

    pattern_dddsp =  re.compile("^[0-9]{1,3} p\.$")
    if re.search(pattern_dddsp,extent):
        extent = extent.replace(" p.","") # remove the first month
        return extent

    pattern_dddspages =  re.compile("^[0-9]{1,3} pages\.$")
    if re.search(pattern_dddspages,extent):
        extent = extent.replace(" pages.","") # remove the first month
        return extent

    pattern_rrrcsdddpp =  re.compile("^[xvi]{1,3}, [0-9]{1,3}p\.$")
    if re.search(pattern_rrrcsdddpp,extent):
        extent = extent.split(",")[1].replace("p.","").strip() # remove the first month
        return extent

    return extent

def clean_ags_citationNumber(pages):
    pattern_pp =  re.compile("^pp\. ")
    if re.search(pattern_pp, pages):
        pages = pages.replace("pp. ","")
    pages = pages.replace(".","")
    return pages
        
def is_valid_pages(pages):
    pattern_pages =  re.compile("^[0-9\-]+$")
    if re.search(pattern_pages, pages):
        return True
    else:
        return False

def clean_date (date):
    date = re.sub('[\[\]]', '', date)
    pattern_mmm_mmmYYYY =  re.compile("^[a-z]{3}\-[a-z]{3}[0-9]{4}$")
    if re.search(pattern_mmm_mmmYYYY,date):
        date = date[4:] # remove the first month

    pattern_YYYY_YYYY =  re.compile("^[0-9]{4}[\-/][0-9]{4}$") # 2020/2021
    if re.search(pattern_YYYY_YYYY,date):
        date = date[:4] # get the first year

    pattern_MM_YYYY =  re.compile("^[0-9]{2}/[0-9]{4}$") # 12/2033
    if re.search(pattern_MM_YYYY,date):
        month=date[:2]
        year=date[3:]
        date=year+"-"+month

    if len(date)==5: # 2011- => 2012
        date=date[:-1]

    pattern_mmmYYYY =  re.compile("^[a-z]{3}[0-9]{4}$") #mmm2033
    if re.search(pattern_mmmYYYY,date):
        month=date[:3]
        month= getmonthNumber(month)
        year=date[3:]
        if month:
            date=year+"-"+month

    pattern_YYYY_M =  re.compile("^[0-9]{4}\-[0-9]$")
    if re.search(pattern_YYYY_M,date):
        date = date[:5]+"0"+date[5:]

    pattern_YYYY_MM_D =  re.compile("^[0-9]{4}\-[0-9]{2}\-[0-9]$")
    if re.search(pattern_YYYY_MM_D,date):
        date = date[:8]+"0"+date[8:]

    pattern_YYYY_M_D =  re.compile("^[0-9]{4}\-[0-9]\-[0-9]$")
    if re.search(pattern_YYYY_M_D,date):
        date = date[:5]+"0"+date[5:7]+"0"+date[7:]


    pattern_YYYY =  re.compile("^[0-9]{4}$") #YYYY
    if re.search(pattern_YYYY, date):
        date = date+"-12-31"

    pattern_YYYY_MM =  re.compile("^[0-9]{4}\-[0-9]{2}$")
    if re.search(pattern_YYYY_MM,date):
        date = date+"-31"

    pattern_YYYY_MM_DD =  re.compile("^[0-9]{4}\-[0-9]{2}\-[0-9]{2}$")
    if not re.search(pattern_YYYY_MM_DD, date):
        date = {
            "19uu" : None,
            "1dic2006" : "2016-12-01",
            "inv2010-2011" : "2010-12-31",
        }.get(date, None)
    
    return date

def unicode_malformed (unicode_s):
    if u"\xc3" in unicode_s :
        return True
    else:
        return False

def get_unicode_from_unicode_malformed (unicode_s):
    return ''.join(map(lambda x: chr(ord(x)),unicode_s)).decode('utf8')