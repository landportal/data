#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import geograpy
import collections
from geograpy import extraction
from geotext import GeoText

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
        c = getISO3166_1code(place)
        result.append(c)
    return filter(None, flatten(result))
    
def getPlaceET_fromText_GeoText(text):
    result = list()
    if not text:
        return filter(None, result)    

    places = GeoText(text)
    
    for place in (places.countries):
        c = getISO3166_1code(place)
        result.append(c)
    return filter(None, flatten(result))

def getISO3166_1code(label):
    label.upper()
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
        u'C\xf4te d\u2019Ivoire': "CIV",
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
        "ZAIRE": None,
        "KOSOVO": "XKX",
        u"C\xd4TE D\u2019IVOIRE": "CIV",
    }.get(label.upper(), None)

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
