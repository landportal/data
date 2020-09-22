#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import collections
import re
import geograpy
from geograpy import extraction
from geotext import GeoText
try:
    # Python 2.6-2.7 
    from HTMLParser import HTMLParser
except ImportError:
    # Python 3
    from html.parser import HTMLParser

#Added from https://gist.github.com/onyxfish/322906#gistcomment-1701799
#reload(sys)
#sys.setdefaultencoding("utf-8")



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
    return filter(None, flatten3(result))
    
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
    return filter(None, flatten3(result))

    
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


def getUNM49code(label_region):
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
            "LATIN AMERICA & CARIBBEAN": "419",
            "SAHEL" : ["SEN", "MRT", "MLI", "BFA", "DZA", "NER", "NGA", "TCD", "SDN", "SSD", "ERI", "CMR", "CAF", "ETH"], # from wikipedia
            "WEST AND CENTRAL AFRICA": ['011','017'],
            "ACP": ["AGO", "ATG", "BLZ", "CPV", "COM", "BHS", "BRB", "BEN", "BWA", "BFA", "BDI", "CMR", "CAF", "TCD", "COG", "COD", "COK", "CIV", "CUB", "DJI", "DMA", "DOM", "ERI", "ETH", "FJI", "GAB", "GMB", "GHA", "GRD", "GIN", "GNB", "GNQ", "GUY", "HTI", "JAM", "KEN", "KIR", "LSO", "LBR", "MDG", "MWI", "MLI", "MHL", "MRT", "MUS", "FSM", "MOZ", "NAM", "NRU", "NER", "NGA", "NIU", "PLW", "PNG", "RWA", "KNA", "LCA", "VCT", "SLB", "WSM", "STP", "SEN", "SYC", "SLE", "SOM", "ZAF", "SDN", "SUR", "SWZ", "TZA", "TLS", "TGO", "TON", "TTO", "TUV", "UGA", "VUT", "ZMB", "ZWE"], # from http://www.acp.int/node/7
            "SOUTHERN  AFRICA" : "018",
            u"WEST\xa0AFRICA": '011',
            u'CENTRAL\xa0ASIA': "143",
            u'SOUTHERN\uffa0 AFRICA': "018",
            u'SOUTH EAST ASIA': "035",
            "LATIN AMERICA": ['013', '005'], # Central America    013 +  South America    005 CHECK    
            "EAST ASIA AND PACIFIC": ['030','009'],
            "THE WORLD REGION": "001",
            "WORLD": "001",
            "EUROPE AND CENTRAL ASIA": ["150","143"],            
            "MIDDLE EAST AND NORTH AFRICA": ["145", "015"],
            "COMMONWEALTH OF INDEPENDENT STATES": ["ARM", "AZE", "BLR", "KAZ", "KGZ", "MDA", "RUS", "TJK", "UZB"], # https://en.wikipedia.org/wiki/Commonwealth_of_Independent_States
            "SOUTHEASTERN EUROPE": ["ALB", "BIH", "BGR", "HRV", "GRC", "XKX", "MKD", "MNE", "ROU", "SRB", "SVN"], #https://en.wikipedia.org/wiki/Southeast_Europe
            "AMERICA": None,
            "PACIFIC ISLANDS": ["061", "057", "054"], #https://en.wikipedia.org/wiki/Pacific_Islands
            "CENTRAL EUROPE": ["AUT", "CZE", "DEU", "HUN", "LIE", "POL", "SVK", "CHE"], #https://en.wikipedia.org/wiki/Central_Europe#States
            "SOUTHERN CONE": ['ARG', 'CHL', 'PRY', 'URY', 'BRA'], #https://en.wikipedia.org/wiki/Southern_Cone
            "BALKANS": ["ALB", "BIH", "BGR", "HRV", "GRC", "XKX", "MKD", "MNE", "ROU", "SRB", "SVN"], #https://en.wikipedia.org/wiki/Balkans#The_Balkans
            "CENTRAL EUROPE": ["AUS", "HRV", "CZE", "DEU", "HUN", "LIE", "POL", "SVK", "SVN", "CHE"], # it is not an element of the UN M49
            "Africa".upper() : "002",
            u"África".upper() : "002", 
            u"América".upper() : "019", 
            u"América Latina".upper() : "419", 
            "Antarctic".upper() : "010", 
            "Antarctic Circumpolar".upper() : "010", 
            "Antarctic Peninsula".upper() : "010" ,
            u"Antártida".upper() : "010",
            "South America".upper() : "005",
            u"Sudamérica".upper() : "005",
            u"Latin America and Caribbean".upper() : "419", 
            u"East Asia and Pacific".upper() : ["030", "009"],
            u"Middle East and North Africa".upper() : ["145", "015"],
            u"Central America and the Caribbean".upper() : ["013", "029"],
            u"Central and Eastern Europe".upper() : ["AUS", "HRV", "CZE", "DEU", "HUN", "LIE", "POL", "SVK", "SVN", "CHE","151"],
            u"Central and South Asia".upper() : ["143", "034"],
            u"East and Southern Africa".upper() : ["014", "018"],
            u"Russia and the Commonwealth of Independent States (CIS)".upper() : ["ARM", "BLR", "KAZ", "KGZ", "MDA", "RUS", "TJK", "TKM", "UKR", "UZB"],
            u"Russia and the Commonwealth of Independent States".upper() : ["ARM", "BLR", "KAZ", "KGZ", "MDA", "RUS", "TJK", "TKM", "UKR", "UZB"],
            u'Sub-Sahara Africa'.upper() : "202"

    }.get(label_region.upper(), None)


def getISO3166_1code(label_country):
    return {
        "HONDURAS" : "HND",
        "AFRICA": None,
        "ANGOLA": "AGO",
        "BANGLADESH": "BGD",
        "BELIZE": "BLZ",
        "BENIN": "BEN",
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
        "BAHAMAS, THE" : "BHS",
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
        "GAMBIA, THE" : "GMB",
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
        "CHINA, HONG KONG SAR": "HKG",
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
        "WEST BANK AND GAZA" : "PSE",
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
        "TAIWAN, CHINA": "TWN",
        "TANZANIA, UNITED REPUBLIC OF" : "TZA",
        "UGANDA" : "UGA",
        "UKRAINE" : "UKR",
        "UNITED STATES MINOR OUTLYING ISLANDS" : "UMI",
        "URUGUAY" : "URY",
        "UNITED STATES" : "USA",
        "UZBEKISTAN" : "UZB",
        "HOLY SEE (VATICAN CITY STATE)" : "VAT",
        "SAINT VINCENT AND THE GRENADINES" : "VCT",
        "ST. VINCENT AND THE GRENADINES": "VCT",
        "VENEZUELA, BOLIVARIAN REPUBLIC OF" : "VEN",
        "VIRGIN ISLANDS, BRITISH" : "VGB",
        "VIRGIN ISLANDS, U.S." : "VIR",
        "VIET NAM" : "VNM",
        "VANUATU" : "VUT",
        "WALLIS AND FUTUNA" : "WLF",
        "SAMOA" : "WSM",
        "YEMEN" : "YEM",
        "YEMEN, REPUBLIC OF": "YEM",
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
        "CONGO, REPUBLIC OF": "COG",
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
        "MACEDONIA, FORMER YUGOSLAV REPUBLIC OF": "MKD",
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
        "STATE OF PALESTINE" : "PSE",
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
        "CONGO, DEMOCRATIC REPUBLIC OF": "COD",
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
        "ZAIRE": None,
        "EGYPT, ARAB REPUBLIC OF": "EGY",
        "KOSOVO": "XKX",
        "BORNEO": ["MYS","BRN", "IDN"],
        "WESTERN AUSTRALIA": "AUS",
        "LAO PDR": "LAO",
        "PERú": "PER",
        "INDONESIAN FORESTS": "IDN",
        "LAO TROPICAL DEFORESTATION": "LAO",
        u"C\xd4TE D\u2019IVOIRE": "CIV",
        "CALAKMUL": "MEX",
        "CAMPECHE": "MEX",
        u"PERÚ": "PER",
        u"PER\xa3": "PER",
        "QUITO": "ECU",
        u"Afganistán".upper(): "AFG",
        u"Amazonía Boliviana".upper() : "BOL", 
        u"Amazonía Ecuatoriana".upper() : "ECU", 
        "Antarctic".upper() : "ATA", 
        "Antarctic Circumpolar".upper() : "ATA", 
        "Antarctic Peninsula".upper() : "ATA" ,
        u"Antártida".upper() : "ATA",
        "Antioquia".upper() : "COL",
        "Ayacucho".upper() : "PER", 
        u"Bahía Blanca".upper() : "ARG", 
        u"Bogotá".upper() : "COL", 
        "Brasil".upper() : "BRA",
        "Buenos Aires".upper() : "ARG", 
        "Buenos Aires Province".upper() : "ARG", 
        "Cali".upper() : "COL",
        "Catamarca".upper() : "ARG", 
        u"Colômbia".upper() : "COL",
        "Colombian".upper() : "COL", 
        u"España".upper() : "ESP",
        "Estados Unidos".upper() : "USA", 
        "Jujuy".upper() : "ARG",
        "La Pampa".upper() : "ARG", 
        "La Rioja Argentina".upper() : "ARG", 
        u"Medellín".upper() : "COL",
        "Mendoza".upper() : "ARG",
        u"México".upper() : "MEX",
        u"Neuquén".upper() : "ARG", 
        "Oaxaca".upper() : "MEX",
        u"Paraná".upper() : "BRA",
        "Patagonia".upper() : "ARG", 
        "Patagonian".upper() : "ARG", 
        u"Perú".upper() : "PER",
        u"República Argentina".upper() : "ARG", 
        u"República Dominicana".upper() : "DOM", 
        "Salta".upper() : "ARG",
        "Chubut".upper() : "ARG",
        "West Bank / Gaza".upper() : "PSE",
        "THE GAMBIA" : "GMB",
        "GAMBIA, THE".upper() : "GMB",
        "Congo, Democratic Republic of the".upper(): "COD",
        "Congo, Republic of the".upper(): "COD"
      
    }.get(label_country.upper(), None)



def get_iso3_code(iso2):
    iso_codes = {'AF':'AFG','AX':'ALA','AL':'ALB','DZ':'DZA','AS':'ASM','AD':'AND','AO':'AGO','AI':'AIA','AQ':'ATA','AG':'ATG','AR':'ARG','AM':'ARM','AW':'ABW','AU':'AUS','AT':'AUT','AZ':'AZE','BS':'BHS','BH':'BHR','BD':'BGD','BB':'BRB','BY':'BLR','BE':'BEL','BZ':'BLZ','BJ':'BEN','BM':'BMU','BT':'BTN','BO':'BOL','BA':'BIH','BW':'BWA','BV':'BVT','BR':'BRA','IO':'IOT','BN':'BRN','BG':'BGR','BF':'BFA','BI':'BDI','KH':'KHM','CM':'CMR','CA':'CAN','CV':'CPV','KY':'CYM','CF':'CAF','TD':'TCD','CL':'CHL','CN':'CHN','CX':'CXR','CC':'CCK','CO':'COL','KM':'COM','CG':'COG','CD':'COD','CK':'COK','CR':'CRI','CI':'CIV','HR':'HRV','CU':'CUB','CY':'CYP','CZ':'CZE','DK':'DNK','DJ':'DJI','DM':'DMA','DO':'DOM','EC':'ECU','EG':'EGY','SV':'SLV','GQ':'GNQ','ER':'ERI','EE':'EST','ET':'ETH','FK':'FLK','FO':'FRO','FJ':'FJI','FI':'FIN','FR':'FRA','GF':'GUF','PF':'PYF','TF':'ATF','GA':'GAB','GM':'GMB','GE':'GEO','DE':'DEU','GH':'GHA','GI':'GIB','GR':'GRC','GL':'GRL','GD':'GRD','GP':'GLP','GU':'GUM','GT':'GTM','GG':'GGY','GN':'GIN','GW':'GNB','GY':'GUY','HT':'HTI','HM':'HMD','VA':'VAT','HN':'HND','HK':'HKG','HU':'HUN','IS':'ISL','IN':'IND','ID':'IDN','IR':'IRN','IQ':'IRQ','IE':'IRL','IM':'IMN','IL':'ISR','IT':'ITA','JM':'JAM','JP':'JPN','JE':'JEY','JO':'JOR','KZ':'KAZ','KE':'KEN','KI':'KIR','KP':'PRK','KR':'KOR','KW':'KWT','KG':'KGZ','LA':'LAO','LV':'LVA','LB':'LBN','LS':'LSO','LR':'LBR','LY':'LBY','LI':'LIE','LT':'LTU','LU':'LUX','MO':'MAC','MK':'MKD','MG':'MDG','MW':'MWI','MY':'MYS','MV':'MDV','ML':'MLI','MT':'MLT','MH':'MHL','MQ':'MTQ','MR':'MRT','MU':'MUS','YT':'MYT','MX':'MEX','FM':'FSM','MD':'MDA','MC':'MCO','MN':'MNG','ME':'MNE','MS':'MSR','MA':'MAR','MZ':'MOZ','MM':'MMR','NA':'NAM','NR':'NRU','NP':'NPL','NL':'NLD','AN':'ANT','NC':'NCL','NZ':'NZL','NI':'NIC','NE':'NER','NG':'NGA','NU':'NIU','NF':'NFK','MP':'MNP','NO':'NOR','OM':'OMN','PK':'PAK','PW':'PLW','PS':'PSE','PA':'PAN','PG':'PNG','PY':'PRY','PE':'PER','PH':'PHL','PN':'PCN','PL':'POL','PT':'PRT','PR':'PRI','QA':'QAT','RE':'REU','RO':'ROU','RU':'RUS','RW':'RWA','BL':'BLM','SH':'SHN','KN':'KNA','LC':'LCA','MF':'MAF','PM':'SPM','VC':'VCT','WS':'WSM','SM':'SMR','ST':'STP','SA':'SAU','SN':'SEN','RS':'SRB','SC':'SYC','SL':'SLE','SG':'SGP','SK':'SVK','SI':'SVN','SB':'SLB','SO':'SOM','ZA':'ZAF','GS':'SGS','ES':'ESP','LK':'LKA','SD':'SDN','SR':'SUR','SJ':'SJM','SZ':'SWZ','SE':'SWE','CH':'CHE','SY':'SYR','TW':'TWN','TJ':'TJK','TZ':'TZA','TH':'THA','TL':'TLS','TG':'TGO','TK':'TKL','TO':'TON','TT':'TTO','TN':'TUN','TR':'TUR','TM':'TKM','TC':'TCA','TV':'TUV','UG':'UGA','UA':'UKR','AE':'ARE','GB':'GBR','US':'USA','UM':'UMI','UY':'URY','UZ':'UZB','VU':'VUT','VE':'VEN','VN':'VNM','VG':'VGB','VI':'VIR','WF':'WLF','EH':'ESH','YE':'YEM','ZM':'ZMB','ZW':'ZWE', 'SS':'SSD'}
    iso3 = iso_codes.get(iso2.upper(),None)
    return iso3

def get_iso2_code(iso3):
    iso_codes = {'AFG':'AF','ALA':'AX','ALB':'AL','DZA':'DZ','ASM':'AS','AND':'AD','AGO':'AO','AIA':'AI','ATA':'AQ','ATG':'AG','ARG':'AR','ARM':'AM','ABW':'AW','AUS':'AU','AUT':'AT','AZE':'AZ','BHS':'BS','BHR':'BH','BGD':'BD','BRB':'BB','BLR':'BY','BEL':'BE','BLZ':'BZ','BEN':'BJ','BMU':'BM','BTN':'BT','BOL':'BO','BIH':'BA','BWA':'BW','BVT':'BV','BRA':'BR','IOT':'IO','BRN':'BN','BGR':'BG','BFA':'BF','BDI':'BI','KHM':'KH','CMR':'CM','CAN':'CA','CPV':'CV','CYM':'KY','CAF':'CF','TCD':'TD','CHL':'CL','CHN':'CN','CXR':'CX','CCK':'CC','COL':'CO','COM':'KM','COG':'CG','COD':'CD','COK':'CK','CRI':'CR','CIV':'CI','HRV':'HR','CUB':'CU','CYP':'CY','CZE':'CZ','DNK':'DK','DJI':'DJ','DMA':'DM','DOM':'DO','ECU':'EC','EGY':'EG','SLV':'SV','GNQ':'GQ','ERI':'ER','EST':'EE','ETH':'ET','FLK':'FK','FRO':'FO','FJI':'FJ','FIN':'FI','FRA':'FR','GUF':'GF','PYF':'PF','ATF':'TF','GAB':'GA','GMB':'GM','GEO':'GE','DEU':'DE','GHA':'GH','GIB':'GI','GRC':'GR','GRL':'GL','GRD':'GD','GLP':'GP','GUM':'GU','GTM':'GT','GGY':'GG','GIN':'GN','GNB':'GW','GUY':'GY','HTI':'HT','HMD':'HM','VAT':'VA','HND':'HN','HKG':'HK','HUN':'HU','ISL':'IS','IND':'IN','IDN':'ID','IRN':'IR','IRQ':'IQ','IRL':'IE','IMN':'IM','ISR':'IL','ITA':'IT','JAM':'JM','JPN':'JP','JEY':'JE','JOR':'JO','KAZ':'KZ','KEN':'KE','KIR':'KI','PRK':'KP','KOR':'KR','KWT':'KW','KGZ':'KG','LAO':'LA','LVA':'LV','LBN':'LB','LSO':'LS','LBR':'LR','LBY':'LY','LIE':'LI','LTU':'LT','LUX':'LU','MAC':'MO','MKD':'MK','MDG':'MG','MWI':'MW','MYS':'MY','MDV':'MV','MLI':'ML','MLT':'MT','MHL':'MH','MTQ':'MQ','MRT':'MR','MUS':'MU','MYT':'YT','MEX':'MX','FSM':'FM','MDA':'MD','MCO':'MC','MNG':'MN','MNE':'ME','MSR':'MS','MAR':'MA','MOZ':'MZ','MMR':'MM','NAM':'NA','NRU':'NR','NPL':'NP','NLD':'NL','ANT':'AN','NCL':'NC','NZL':'NZ','NIC':'NI','NER':'NE','NGA':'NG','NIU':'NU','NFK':'NF','MNP':'MP','NOR':'NO','OMN':'OM','PAK':'PK','PLW':'PW','PSE':'PS','PAN':'PA','PNG':'PG','PRY':'PY','PER':'PE','PHL':'PH','PCN':'PN','POL':'PL','PRT':'PT','PRI':'PR','QAT':'QA','REU':'RE','ROU':'RO','RUS':'RU','RWA':'RW','BLM':'BL','SHN':'SH','KNA':'KN','LCA':'LC','MAF':'MF','SPM':'PM','VCT':'VC','WSM':'WS','SMR':'SM','STP':'ST','SAU':'SA','SEN':'SN','SRB':'RS','SYC':'SC','SLE':'SL','SGP':'SG','SVK':'SK','SVN':'SI','SLB':'SB','SOM':'SO','ZAF':'ZA','SGS':'GS','ESP':'ES','LKA':'LK','SDN':'SD','SUR':'SR','SJM':'SJ','SWZ':'SZ','SWE':'SE','CHE':'CH','SYR':'SY','TWN':'TW','TJK':'TJ','TZA':'TZ','THA':'TH','TLS':'TL','TGO':'TG','TKL':'TK','TON':'TO','TTO':'TT','TUN':'TN','TUR':'TR','TKM':'TM','TCA':'TC','TUV':'TV','UGA':'UG','UKR':'UA','ARE':'AE','GBR':'GB','USA':'US','UMI':'UM','URY':'UY','UZB':'UZ','VUT':'VU','VEN':'VE','VNM':'VN','VGB':'VG','VIR':'VI','WLF':'WF','ESH':'EH','YEM':'YE','ZMB':'ZM','ZWE':'ZW', 'SSD': 'SS'}
    iso2 = iso_codes.get(iso3.upper(),None)
    return iso2

################################################################################
##########################   LANGUAGES   #######################################
################################################################################
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


def getISO639_1code_from_ISO639_3code(code_language):
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
        "eng" : "en",
        "por" : "pt",
        "spa" : "es",
        "fra" : "fr",
        "fre" : "fr",
        "und" : None
    }.get(code_language, None)


def getISO639_1code(label_language):
    return {
        "Albanian" : "sq",
        "Amharic": "am",
        "Arabic" : "ar",
        "Azerbaijani" : "az",
        "Bosnian" : "bs",
        "Bulgarian" : "bg",
        "Cambodian" : "km",
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
        "Georgian" : "ka",
        "German" : "de",
        "Greek" : "el",
        "Hebrew": "he",
        "Hungarian" : "hu",
        "Indonesian" : "id",
        "Italian" : "it",
        "Japanese": "ja",
        "Korean": "ko",
        "Latvian": "lv",
        "Lithuanian": "lt",
        "Macedonian" : "mk",
        "Malay": "ms",        
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
        "EN" : "en",
        "en" : "en",
        "en_US" : "en",
        u"Spanish (Español)": "es",
        u"French (Français)": "fr",
        u"Arabic (العربية)": "ar",
        u"Russian (Русский)": "ru",
        u"中文 (Chinese)": "zh"
    }.get(label_language, None)
    

def getLLR_type(label):
    return {
        None: "Other",
    }[label]

def checkOpenAccess(uri):
    if uri in ["info:eu-repo/semantics/closedAccess", "info:eu-repo/semantics/embargoedAccess", "info:eu-repo/semantics/restrictedAccess"]:
        return False
    else:
        return True

def getLicenseFromText(text):
    return {
            'CC BY 3.0 IGO': "CC-BY",
            'CC BY-NC-ND 3.0 IGO': "CC-BY",
            'Creative Commons Attribution CC BY 3.0 IGO': "CC-BY", 
            'CC BY-NC-ND 3.0 igo': "CC-BY-NC-ND",
            'CC BY-NC-ND 4.0 IGO': "CC-BY-NC-ND",
            'http://creativecommons.org/licenses/by/3.0/igo': "CC-BY",
            'http://creativecommons.org/licenses/by/3.0/igo/': "CC-BY",
            'http://creativecommons.org/licenses/by-nc/3.0/us/': "CC-BY-NC",
            'http://creativecommons.org/licenses/by-nc-nd/3.0/igo': "CC-BY-NC-ND",
            'http://creativecommons.org/licenses/by-nc-nd/3.0/igo/': "CC-BY-NC-ND",
            'http://creativecommons.org/licenses/by-nc-nd/4.0/igo/': "CC-BY-NC-ND",
            'http://creativecommons.org/licenses/by-nc-nd/3.0/us/': "CC-BY-NC-ND",
            'http://creativecommons.org/licenses/by-nc-sa/3.0/us/': "CC-BY-NC-SA",
            u'CC BY-NC': "CC-BY-NC",
            u'CC BY': "CC-BY",
            u'CC BY-NC-ND': "CC-BY-NC-ND",
            u'CC BY-SA': "CC-BY-SA",
            u'CC BY-NC-SA': "CC-BY-NC-SA",
            u"Publisher's own license": None,
            'CC-BY-NC-4.0': "CC-BY-NC",
            'CC-BY-4.0': "CC-BY",
            'CC-BY-NC-ND-4.0': "CC-BY-NC-ND",
            'CC-BY-NC-SA-4.0': "CC-BY-NC-SA",
            'CC-BY-SA-4.0': "CC-BY-SA"
    }.get(text, "REVIEW"+text)

def getCCLicenseAcronymELDIS(licenseText):
    if u'Open - CC - Attribution (CCBY)' in licenseText:
        return "CC-BY"
    elif u'Open - CC - NonCommercial (CC BY-NC)' in licenseText:
        return "CC-BY-NC"
    elif u'Open - CC - NonCommercial-NoDerivs (CC BY-NC-ND)' in licenseText:
        return "CC-BY-NC-ND"
    elif u'Open - CC - NonCommercial-ShareAlike (CC BY-NC-SA)' in licenseText:
        return "CC-BY-NC-SA"
    else: # u'Not Known', u'Not Open', u'Open - Other', u'Open - Creative Commons (CC) - Unspecified'
        return None

def getCCLicenseAcronym(uri):
    if "licenses/by/" in uri:
        return "CC-BY"
    elif "licenses/by-nc/" in uri:
        return "CC-BY-NC"
    elif "licenses/by-nd/" in uri:
        return "CC-BY-ND"
    elif "licenses/by-sa/" in uri:
        return "CC-BY-SA"
    elif "licenses/by-nc-nd/" in uri or "licences/by-nc-nd/" in uri:
        return "CC-BY-NC-ND"
    elif "licenses/by-nc-sa/" in uri or "licences/by-nc-sa/" in uri:
        return "CC-BY-NC-SA"
    elif "publicdomain/zero" in uri:
        return "CC0"
    
    
    else:
        print(uri)
        return None

def flatten(l):
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, basestring):
            for sub in flatten(el):
                yield sub
        else:
            yield el

def flatten3(l):
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten3(el)
        else:
            yield el
# dev_contries = ["Algeria", "Egypt", "Libya", "Mauritania", "Morocco", "Sudan", "Tunisia", "Angola", "Botswana", "Lesotho", "Malawi", "Mauritius", "Mozambique", "Namibia", "South Africa", "Zambia", "Zimbabwe", "Brunei Darussalam", "China", "Hong Kong", "Indonesia", "Malaysia", "Myanmar", "Papua New Guinea", "Philippines", "Republic of Korea", "Singapore", "Thailand", "Viet Nam", "Barbados", "Cuba", "Dominican Republic", "Guyana", "Haiti", "Jamaica", "Trinidad and Tobago", "Cameroon", "Central African Republic", "Chad", "Congo", "Equatorial Guinea", "Gabon", "Sao Tome and Principe", "Costa Rica", "El Salvador", "Guatemala", "Honduras", "Mexico", "Nicaragua", "Panama", "Benin", "Burkina Faso", "Cabo Verde", "Gambia", "Ghana", "Guinea", "Guinea-Bissau", "Liberia", "Mali", "Niger", "Nigeria", "Senegal", "Sierra Leone", "Togo", "Bangladesh", "India", "Iran (Islamic Republic of)", "Nepal", "Pakistan", "Sri Lanka", "Burundi", "Comoros", "Democratic Republic of the Congo", "Djibouti", "Eritrea", "Ethiopia", "Kenya", "Madagascar", "Rwanda", "Somalia", "Uganda", "United Republic of Tanzania", "Argentina", "Bolivia (Plurinational State of)", "Brazil", "Chile", "Colombia", "Ecuador", "Paraguay", "Peru", "Uruguay", "Venezuela (Bolivarian Republic of)", "Bahrain", "Iraq", "Israel", "Jordan", "Kuwait", "Lebanon", "Oman", "Qatar", "Saudi Arabia", "Syria", "Turkey", "United Arab Emirates", "Yemen", "COTE D'IVOIRE"]
# for c in dev_contries:
#     print "<http://data.landportal.info/geo/"+getISO3166_1code(c.upper())+">"

h = HTMLParser()

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)    
    return h.unescape(cleantext)

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

def clean_date (date):
    import datetime
    now = datetime.datetime.now()
    year= now.year
    
    date = date.lower().replace(".","").replace(" ","").replace("june","jun")
    pattern_mmmYYYY =  re.compile("^[a-z]{3}[0-9]{4}$") #mmm2033
    if re.search(pattern_mmmYYYY,date):
        month=date[:3]
        month= getmonthNumber(month)
        year=date[3:]
        if month:
            date=year+"-"+month
    
    pattern_YYYY =  re.compile("^[0-9]{4}$") #YYYY
    if re.search(pattern_YYYY, date):
        if int(date) != year:
            date = date+"-12-31"
        else:
            date = date+"-"+str(now.month)

    pattern_YYYY_M =  re.compile("^[0-9]{4}\-[0-9]$")
    if re.search(pattern_YYYY_M,date):
        date = date[:5]+"0"+date[5:]

    pattern_YYYY_MM =  re.compile("^[0-9]{4}\-[0-9]{2}$")
    if re.search(pattern_YYYY_MM, date):
        month = date[-2:]
        if month in ["01","03","05", "07", "08", "10", "12"]:
            date = date+"-31"
        elif month in ["02"]:
            date = date+"-28"
        else:
            date = date+"-30"
    
    return date

def toUnicode(text):
    try:
        text = unicode(text, 'utf-8')
        return text
    except TypeError:
        return text