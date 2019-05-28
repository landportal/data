import requests
import json
from fileinput import filename

def retrieve():

    endpoint = "https://api.fao.org/api/gsa/1.0.0"
    #TODO extract to a variable
    retrieve_list = {
        "common lands" : "http://aims.fao.org/aos/agrovoc/c_1782", 
        "deforestation" : "http://aims.fao.org/aos/agrovoc/c_15590", 
        "desertification" : "http://aims.fao.org/aos/agrovoc/c_2204", 
        "dryland management" : "http://aims.fao.org/aos/agrovoc/c_9000036", 
        "farmland" : "http://aims.fao.org/aos/agrovoc/c_2808", 
        "forest conservation" : "http://aims.fao.org/aos/agrovoc/c_1374158672853", 
        "forest degradation" : "http://aims.fao.org/aos/agrovoc/c_331593", 
        "forest grazing" : "http://aims.fao.org/aos/agrovoc/c_3046", 
        "forest land" : "http://aims.fao.org/aos/agrovoc/c_24843", 
        "forest land use" : "http://aims.fao.org/aos/agrovoc/c_1374157828575", 
        "forest resources" : "http://aims.fao.org/aos/agrovoc/c_3050", 
        "geographical information systems" : "http://aims.fao.org/aos/agrovoc/c_35131", 
        "grassland management" : "http://aims.fao.org/aos/agrovoc/c_3364", 
        "housing" : "http://aims.fao.org/aos/agrovoc/c_3678", 
        "indigenous tenure systems" : "http://aims.fao.org/aos/agrovoc/c_9000081", 
        "individual land property" : "http://aims.fao.org/aos/agrovoc/c_9000082", 
        "land" : "http://aims.fao.org/aos/agrovoc/c_4172", 
        "land access" : "http://aims.fao.org/aos/agrovoc/c_9000090", 
        "land administration" : "http://aims.fao.org/aos/agrovoc/c_9000091", 
        "land classification" : "http://aims.fao.org/aos/agrovoc/c_15991", 
        "land cover" : "http://aims.fao.org/aos/agrovoc/c_37897", 
        "land cover mapping" : "http://aims.fao.org/aos/agrovoc/c_9000094", 
        "land degradation" : "http://aims.fao.org/aos/agrovoc/c_34823", 
        "land improvement" : "http://aims.fao.org/aos/agrovoc/c_28717", 
        "land management" : "http://aims.fao.org/aos/agrovoc/c_24866", 
        "land markets" : "http://aims.fao.org/aos/agrovoc/c_4175", 
        "land ownership" : "http://aims.fao.org/aos/agrovoc/c_28718", 
        "land policies" : "http://aims.fao.org/aos/agrovoc/c_195", 
        "land productivity" : "http://aims.fao.org/aos/agrovoc/c_4176", 
        "land reform" : "http://aims.fao.org/aos/agrovoc/c_4178", 
        "land registration" : "http://aims.fao.org/aos/agrovoc/c_9000098", 
        "land resources" : "http://aims.fao.org/aos/agrovoc/c_4179", 
        "land rights" : "http://aims.fao.org/aos/agrovoc/c_37898", 
        "land suitability" : "http://aims.fao.org/aos/agrovoc/c_15992", 
        "land tax" : "http://aims.fao.org/aos/agrovoc/c_4180", 
        "land tenure" : "http://aims.fao.org/aos/agrovoc/c_12069", 
        "land transfers" : "http://aims.fao.org/aos/agrovoc/c_4181", 
        "land use" : "http://aims.fao.org/aos/agrovoc/c_4182", 
        "land use mapping" : "http://aims.fao.org/aos/agrovoc/c_9000100", 
        "land use planning" : "http://aims.fao.org/aos/agrovoc/c_37899", 
        "landowners" : "http://aims.fao.org/aos/agrovoc/c_4184", 
        "multiple land use" : "http://aims.fao.org/aos/agrovoc/c_28734", 
        "natural resources" : "http://aims.fao.org/aos/agrovoc/c_5091", 
        "natural resources management" : "http://aims.fao.org/aos/agrovoc/c_9000115", 
        "pastoral society" : "http://aims.fao.org/aos/agrovoc/c_28741", 
        "pastoralism" : "http://aims.fao.org/aos/agrovoc/c_16144", 
        "private ownership" : "http://aims.fao.org/aos/agrovoc/c_6192", 
        "property rights" : "http://aims.fao.org/aos/agrovoc/c_37942", 
        "public ownership" : "http://aims.fao.org/aos/agrovoc/c_6350", 
        "rangelands" : "http://aims.fao.org/aos/agrovoc/c_6448", 
        "reforestation" : "http://aims.fao.org/aos/agrovoc/c_13802", 
        "resource management" : "http://aims.fao.org/aos/agrovoc/c_6524", 
        "right of access" : "http://aims.fao.org/aos/agrovoc/c_6604", 
        "soil degradation" : "http://aims.fao.org/aos/agrovoc/c_7168", 
        "soil management" : "http://aims.fao.org/aos/agrovoc/c_7176", 
        "spatial database" : "http://aims.fao.org/aos/agrovoc/c_9000154", 
        "sustainable forest management" : "http://aims.fao.org/aos/agrovoc/c_331342", 
        "sustainable land management" : "http://aims.fao.org/aos/agrovoc/c_36580", 
        "tenure" : "http://aims.fao.org/aos/agrovoc/c_7669", 
        "urban agriculture" : "http://aims.fao.org/aos/agrovoc/c_35707", 
        "urban areas" : "http://aims.fao.org/aos/agrovoc/c_8085", 
        "urban planning" : "http://aims.fao.org/aos/agrovoc/c_37948", 
        "urbanization" : "http://aims.fao.org/aos/agrovoc/c_8088", 
        "valuation" : "http://aims.fao.org/aos/agrovoc/c_8152", 
        "water management" : "http://aims.fao.org/aos/agrovoc/c_8320", 
        "water resources" : "http://aims.fao.org/aos/agrovoc/c_8325", 
        "water rights" : "http://aims.fao.org/aos/agrovoc/c_16062", 
    }
    stats={}
    for agrovoc_label, agrovoc_uri in retrieve_list.iteritems():
        print agrovoc_label
        next=0
        all_results = []
        year_start=1850
        year_end=2016
        agrovoc_uri_enconded = "http%3A%252F%252Faims%252Efao%252Eorg%252Faos%252Fagrovoc%252F" + str.replace(agrovoc_uri,"http://aims.fao.org/aos/agrovoc/","")
        
        # problems with the encode of the agrovoc urlagrovoc_uri_enconded
        next_relative_url = "/search?client=docrep&output=xml_no_dtd&site=faodocrep&partialfields=&requiredfields=(agrovoc_id%3A"+ agrovoc_uri_enconded +").docRepCollection%3Adocuments&filter=0&q=+inmeta%3Ayear%3A"+str(year_start)+".."+str(year_end)+"&proxystylesheet=xml_to_json&getfields=*&dnavs=&start=0&apikey=c335a12f-a850-4816-aed5-51ab7f723f12&ulang=en&language=en&sort=meta%3Ayear%3AD%3ASD%3AY"
        while (next_relative_url):
            response = requests.get(endpoint+next_relative_url, headers={"Accept":"application/json","Authorization" : "Bearer 8ce6f29360faa9ee4fcf29b749d455e"})
            data = response.json()
            stats[agrovoc_label] = 0
            if 'current_page' in data['pagination']:
                current_page = data['pagination']['current_page']
            else: #no results for that concept
                next_relative_url = None
                continue
            stats[agrovoc_label] = data['GSP']['RES']['M'] 
            next+=10
            if ('NB' in data['GSP']['RES'] and 'NU' in data['GSP']['RES'] ['NB']):
                next_relative_url = "/search?client=docrep&output=xml_no_dtd&site=faodocrep&partialfields=&requiredfields=(agrovoc_id%3A"+agrovoc_uri_enconded+").docRepCollection%3Adocuments&filter=0&q=+inmeta%3Ayear%3A"+str(year_start)+".."+str(year_end)+"&proxystylesheet=xml_to_json&getfields=*&dnavs=&start="+str(next)+"&apikey=c335a12f-a850-4816-aed5-51ab7f723f12&ulang=en&language=en&sort=meta%3Ayear%3AD%3ASD%3AY"
            else:
                next_relative_url = None
            #save the results in a file
            filename="results-"+agrovoc_label+"-"+current_page+".json"
            with open(filename, 'w') as outfile:
                json.dump(data, outfile)
                print("written file="+filename)

            #concat the results
            partial_results = data['GSP']['RES'] ['results']
            all_results =all_results + partial_results

        with open("all-results+"+agrovoc_label+".json", 'w') as outfile:
            json.dump(all_results, outfile)
            print("written file ALL -"+agrovoc_label+"- results")
    print stats


def retrieve_stats():

    endpoint = "https://api.fao.org/api/gsa/1.0.0"
    retrieve_list = {
        "common lands" : "http://aims.fao.org/aos/agrovoc/c_1782", 
        "deforestation" : "http://aims.fao.org/aos/agrovoc/c_15590", 
        "desertification" : "http://aims.fao.org/aos/agrovoc/c_2204", 
        "dryland management" : "http://aims.fao.org/aos/agrovoc/c_9000036", 
        "farmland" : "http://aims.fao.org/aos/agrovoc/c_2808", 
        "forest conservation" : "http://aims.fao.org/aos/agrovoc/c_1374158672853", 
        "forest degradation" : "http://aims.fao.org/aos/agrovoc/c_331593", 
        "forest grazing" : "http://aims.fao.org/aos/agrovoc/c_3046", 
        "forest land" : "http://aims.fao.org/aos/agrovoc/c_24843", 
        "forest land use" : "http://aims.fao.org/aos/agrovoc/c_1374157828575", 
        "forest resources" : "http://aims.fao.org/aos/agrovoc/c_3050", 
        "geographical information systems" : "http://aims.fao.org/aos/agrovoc/c_35131", 
        "grassland management" : "http://aims.fao.org/aos/agrovoc/c_3364", 
        "housing" : "http://aims.fao.org/aos/agrovoc/c_3678", 
        "indigenous tenure systems" : "http://aims.fao.org/aos/agrovoc/c_9000081", 
        "individual land property" : "http://aims.fao.org/aos/agrovoc/c_9000082", 
        "land" : "http://aims.fao.org/aos/agrovoc/c_4172", 
        "land access" : "http://aims.fao.org/aos/agrovoc/c_9000090", 
        "land administration" : "http://aims.fao.org/aos/agrovoc/c_9000091", 
        "land classification" : "http://aims.fao.org/aos/agrovoc/c_15991", 
        "land cover" : "http://aims.fao.org/aos/agrovoc/c_37897", 
        "land cover mapping" : "http://aims.fao.org/aos/agrovoc/c_9000094", 
        "land degradation" : "http://aims.fao.org/aos/agrovoc/c_34823", 
        "land improvement" : "http://aims.fao.org/aos/agrovoc/c_28717", 
        "land management" : "http://aims.fao.org/aos/agrovoc/c_24866", 
        "land markets" : "http://aims.fao.org/aos/agrovoc/c_4175", 
        "land ownership" : "http://aims.fao.org/aos/agrovoc/c_28718", 
        "land policies" : "http://aims.fao.org/aos/agrovoc/c_195", 
        "land productivity" : "http://aims.fao.org/aos/agrovoc/c_4176", 
        "land reform" : "http://aims.fao.org/aos/agrovoc/c_4178", 
        "land registration" : "http://aims.fao.org/aos/agrovoc/c_9000098", 
        "land resources" : "http://aims.fao.org/aos/agrovoc/c_4179", 
        "land rights" : "http://aims.fao.org/aos/agrovoc/c_37898", 
        "land suitability" : "http://aims.fao.org/aos/agrovoc/c_15992", 
        "land tax" : "http://aims.fao.org/aos/agrovoc/c_4180", 
        "land tenure" : "http://aims.fao.org/aos/agrovoc/c_12069", 
        "land transfers" : "http://aims.fao.org/aos/agrovoc/c_4181", 
        "land use" : "http://aims.fao.org/aos/agrovoc/c_4182", 
        "land use mapping" : "http://aims.fao.org/aos/agrovoc/c_9000100", 
        "land use planning" : "http://aims.fao.org/aos/agrovoc/c_37899", 
        "landowners" : "http://aims.fao.org/aos/agrovoc/c_4184", 
        "multiple land use" : "http://aims.fao.org/aos/agrovoc/c_28734", 
        "natural resources" : "http://aims.fao.org/aos/agrovoc/c_5091", 
        "natural resources management" : "http://aims.fao.org/aos/agrovoc/c_9000115", 
        "pastoral society" : "http://aims.fao.org/aos/agrovoc/c_28741", 
        "pastoralism" : "http://aims.fao.org/aos/agrovoc/c_16144", 
        "private ownership" : "http://aims.fao.org/aos/agrovoc/c_6192", 
        "property rights" : "http://aims.fao.org/aos/agrovoc/c_37942", 
        "public ownership" : "http://aims.fao.org/aos/agrovoc/c_6350", 
        "rangelands" : "http://aims.fao.org/aos/agrovoc/c_6448", 
        "reforestation" : "http://aims.fao.org/aos/agrovoc/c_13802", 
        "resource management" : "http://aims.fao.org/aos/agrovoc/c_6524", 
        "right of access" : "http://aims.fao.org/aos/agrovoc/c_6604", 
        "soil degradation" : "http://aims.fao.org/aos/agrovoc/c_7168", 
        "soil management" : "http://aims.fao.org/aos/agrovoc/c_7176", 
        "spatial database" : "http://aims.fao.org/aos/agrovoc/c_9000154", 
        "sustainable forest management" : "http://aims.fao.org/aos/agrovoc/c_331342", 
        "sustainable land management" : "http://aims.fao.org/aos/agrovoc/c_36580", 
        "tenure" : "http://aims.fao.org/aos/agrovoc/c_7669", 
        "urban agriculture" : "http://aims.fao.org/aos/agrovoc/c_35707", 
        "urban areas" : "http://aims.fao.org/aos/agrovoc/c_8085", 
        "urban planning" : "http://aims.fao.org/aos/agrovoc/c_37948", 
        "urbanization" : "http://aims.fao.org/aos/agrovoc/c_8088", 
        "valuation" : "http://aims.fao.org/aos/agrovoc/c_8152", 
        "water management" : "http://aims.fao.org/aos/agrovoc/c_8320", 
        "water resources" : "http://aims.fao.org/aos/agrovoc/c_8325", 
        "water rights" : "http://aims.fao.org/aos/agrovoc/c_16062", 
    }

    stats={}
    for agrovoc_label, agrovoc_uri in retrieve_list.iteritems():
        agrovoc_uri_enconded = "http%3A%252F%252Faims%252Efao%252Eorg%252Faos%252Fagrovoc%252F" + str.replace(agrovoc_uri,"http://aims.fao.org/aos/agrovoc/","")
        
        # problems with the encode of the agrovoc urlagrovoc_uri_enconded
        next_relative_url = "/search?client=docrep&output=xml_no_dtd&site=faodocrep&partialfields=&requiredfields=(agrovoc_id%3A"+ agrovoc_uri_enconded +").docRepCollection%3Adocuments&filter=0&q=&proxystylesheet=xml_to_json&getfields=*&dnavs=&start=0&apikey=c335a12f-a850-4816-aed5-51ab7f723f12&ulang=en&language=en&sort=meta%3Ayear%3AD%3ASD%3AY"
        response = requests.get(endpoint+next_relative_url, headers={"Accept":"application/json","Authorization" : "Bearer 8ce6f29360faa9ee4fcf29b749d455e"})
        data = response.json()
        stats[agrovoc_label] = 0
        if 'current_page' in data['pagination']:
            current_page = data['pagination']['current_page']
        else: #no results for that concept
            next_relative_url = None
            continue
        stats[agrovoc_label] = data['GSP']['RES']['M']
        print agrovoc_label + ";" + str(data['GSP']['RES']['M'])  
    print stats

#retrieve_stats()
#for k,v in {'land use planning': u'53', 'natural resources management': u'343', 'land productivity': u'22', 'right of access': u'81', 'land classification': u'39', 'forest land use': u'75', 'pastoral society': u'14', 'land administration': u'51', 'geographical information systems': u'46', 'land registration': u'29', 'forest degradation': u'63', 'land cover mapping': u'20', 'land resources': u'106', 'forest conservation': u'60', 'dryland management': u'44', 'urbanization': u'49', 'farmland': u'25', 'land suitability': u'22', 'water resources': u'269', 'land cover': u'20', 'desertification': u'69', 'individual land property': u'90', 'sustainable forest management': u'552', 'landowners': u'31', 'land tax': u'25', 'urban planning': u'17', 'forest grazing': u'27', 'forest resources': u'763', 'reforestation': u'147', 'land transfers': u'28', 'pastoralism': u'32', 'land degradation': u'68', 'sustainable land management': u'85', 'spatial database': u'11', 'private ownership': u'39', 'land rights': u'128', 'resource management': u'568', 'soil management': u'316', 'deforestation': u'207', 'land improvement': u'18', 'property rights': u'95', 'rangelands': u'80', 'forest land': u'240', 'land tenure': u'403', 'valuation': u'16', 'urban areas': u'92', 'multiple land use': u'20', 'land access': u'100', 'land policies': u'117', 'land': u'57', 'public ownership': u'34', 'natural resources': u'277', 'common lands': u'30', 'water management': u'314', 'housing': u'67', 'land use': u'383', 'soil degradation': u'99', 'water rights': u'33', 'land management': u'136', 'land markets': u'35', 'indigenous tenure systems': u'86', 'tenure': u'465', 'grassland management': u'54', 'land reform': u'117', 'land use mapping': u'28', 'urban agriculture': u'32', 'land ownership': u'212'}.iteritems():
#    print k +";"+ str(v)


# initial_retrieve_list = {
#     "agropastoral systems" : "http://aims.fao.org/aos/agrovoc/c_16112",
#     "alienation (land)" : "http://aims.fao.org/aos/agrovoc/c_ceb73ce1",
#     "cadastral administration" : "http://aims.fao.org/aos/agrovoc/c_d774aa00",
#     "cadastral register" : "http://aims.fao.org/aos/agrovoc/c_b4d51db0",
#     "cadastres" : "http://aims.fao.org/aos/agrovoc/c_1177",
#     "capital value (land)" : "http://aims.fao.org/aos/agrovoc/c_a9966ac9",
#     "co-ownership rights" : "http://aims.fao.org/aos/agrovoc/c_599d2e5c",
#     "commons" : "http://aims.fao.org/aos/agrovoc/c_778a14cf",
#     "common property" : "http://aims.fao.org/aos/agrovoc/c_9000022",
#     "community forestry" : "http://aims.fao.org/aos/agrovoc/c_16532",
#     "customary land rights" : "http://aims.fao.org/aos/agrovoc/c_cd44c0b3",
#     "customary tenure" : "http://aims.fao.org/aos/agrovoc/c_56c34d4d",
#     "deforestation" : "http://aims.fao.org/aos/agrovoc/c_15590",
#     "extensive land use" : "http://aims.fao.org/aos/agrovoc/c_36552",
#     "forest land" : "http://aims.fao.org/aos/agrovoc/c_24843",
#     "geographical information systems" : "http://aims.fao.org/aos/agrovoc/c_35131",
#     "grazing land rights" : "http://aims.fao.org/aos/agrovoc/c_97241aeb",
#     "grazing lands" : "http://aims.fao.org/aos/agrovoc/c_3369",
#     "indigenous tenure" : "http://aims.fao.org/aos/agrovoc/c_a291ae58",
#     "indigenous land rights" : "http://aims.fao.org/aos/agrovoc/c_d42b49e7",
#     "indigenous lands" : "http://aims.fao.org/aos/agrovoc/c_86524ff8",
#     "intensive land use" : "http://aims.fao.org/aos/agrovoc/c_36551",
#     "grazing land rights" : "http://aims.fao.org/aos/agrovoc/c_97241aeb",
#     "land access" : "http://aims.fao.org/aos/agrovoc/c_9000090",
#     "land acquisitions" : "http://aims.fao.org/aos/agrovoc/c_89d3dcbb",
#     "land administration" : "http://aims.fao.org/aos/agrovoc/c_9000091",
#     "land area" : "http://aims.fao.org/aos/agrovoc/c_330588",
#     "assignment (land)" : "http://aims.fao.org/aos/agrovoc/c_8c6882ab",
#     "collateral (land)" : "http://aims.fao.org/aos/agrovoc/c_931da360",
#     "land clearing" : "http://aims.fao.org/aos/agrovoc/c_1662",
#     "land concentration" : "http://aims.fao.org/aos/agrovoc/c_8654e90e",
#     "concession (land)" : "http://aims.fao.org/aos/agrovoc/c_357653f9",
#     "land conflicts" : "http://aims.fao.org/aos/agrovoc/c_e236b2b1",
#     "land consolidation" : "http://aims.fao.org/aos/agrovoc/c_4173",
#     "land cover" : "http://aims.fao.org/aos/agrovoc/c_37897",
#     "land cover mapping" : "http://aims.fao.org/aos/agrovoc/c_9000094",
#     "land degradation" : "http://aims.fao.org/aos/agrovoc/c_34823",
#     "land development (urbanization)" : "http://aims.fao.org/aos/agrovoc/c_4174",
#     "Land dispute" : "http://aims.fao.org/aos/agrovoc/c_1ada969a",
#     "land distribution" : "http://aims.fao.org/aos/agrovoc/c_37734",
#     "land diversion" : "http://aims.fao.org/aos/agrovoc/c_28716",
#     "dowry (land)" : "http://aims.fao.org/aos/agrovoc/c_f7cf8606",
#     "land economics" : "http://aims.fao.org/aos/agrovoc/c_25195",
#     "encroachment" : "http://aims.fao.org/aos/agrovoc/c_a245096c",
#     "land environment" : "http://aims.fao.org/aos/agrovoc/c_7ffc9d69",
#     "eviction" : "http://aims.fao.org/aos/agrovoc/c_0b88a82c",
#     "expropriation" : "http://aims.fao.org/aos/agrovoc/c_1798",
#     "land grabs" : "http://aims.fao.org/aos/agrovoc/c_45ce1b52",
#     "land grabbing" : "http://aims.fao.org/aos/agrovoc/c_cc39a497",
#     "land improvement" : "http://aims.fao.org/aos/agrovoc/c_28717",
#     "land information systems" : "http://aims.fao.org/aos/agrovoc/c_9000096",
#     "land inheritance rights" : "http://aims.fao.org/aos/agrovoc/c_70a14ab3",
#     "land investments" : "http://aims.fao.org/aos/agrovoc/c_9a4f48b4",
#     "land law" : "http://aims.fao.org/aos/agrovoc/c_573abb9f",
#     "land loans" : "http://aims.fao.org/aos/agrovoc/c_8b6d895f",
#     "land management" : "http://aims.fao.org/aos/agrovoc/c_24866",
#     "land markets" : "http://aims.fao.org/aos/agrovoc/c_4175",
#     "open access (land)" : "http://aims.fao.org/aos/agrovoc/c_51a39a94",
#     "land policies" : "http://aims.fao.org/aos/agrovoc/c_195",
#     "property rights" : "http://aims.fao.org/aos/agrovoc/c_37942",
#     "land reform" : "http://aims.fao.org/aos/agrovoc/c_4178",
#     "land registration" : "http://aims.fao.org/aos/agrovoc/c_9000098",
#     "land rent" : "http://aims.fao.org/aos/agrovoc/c_7bea427c",
#     "land speculation" : "http://aims.fao.org/aos/agrovoc/c_15d85712",
#     "land suitability" : "http://aims.fao.org/aos/agrovoc/c_15992",
#     "land tax" : "http://aims.fao.org/aos/agrovoc/c_4180",
#     "land tenants" : "http://aims.fao.org/aos/agrovoc/c_330886",
#     "land tenure" : "http://aims.fao.org/aos/agrovoc/c_12069",
#     "land tenure systems" : "http://aims.fao.org/aos/agrovoc/c_66afb052",
#     "land transfers" : "http://aims.fao.org/aos/agrovoc/c_4181",
#     "land use mapping" : "http://aims.fao.org/aos/agrovoc/c_9000100",
#     "land use planning" : "http://aims.fao.org/aos/agrovoc/c_37899",
#     "landlessness" : "http://aims.fao.org/aos/agrovoc/c_24403",
#     "land ownership" : "http://aims.fao.org/aos/agrovoc/c_4184",
#     "negotiated land reform" : "http://aims.fao.org/aos/agrovoc/c_f84a48c4",
#     "pastoral land rights" : "http://aims.fao.org/aos/agrovoc/c_4d6b6100",
#     "pastoral lands" : "http://aims.fao.org/aos/agrovoc/c_8e487587",
#     "priest of the land" : "http://aims.fao.org/aos/agrovoc/c_28f78be5",
#     "marital property rights" : "http://aims.fao.org/aos/agrovoc/c_64d8574a",
#     "rangelands" : "http://aims.fao.org/aos/agrovoc/c_6448",
#     "regularization of illegal occupation" : "http://aims.fao.org/aos/agrovoc/c_3b50d6b6",
#     "right of first occupancy" : "http://aims.fao.org/aos/agrovoc/c_9904d265",
#     "scrublands" : "http://aims.fao.org/aos/agrovoc/c_6887",
#     "security of tenure (land)" : "http://aims.fao.org/aos/agrovoc/c_7fc44e33",
#     "sustainable land management" : "http://aims.fao.org/aos/agrovoc/c_36580",
#     "tenant farmers" : "http://aims.fao.org/aos/agrovoc/c_f73955fb",
#     "title deed" : "http://aims.fao.org/aos/agrovoc/c_b769471e",
#     "Torrens system" : "http://aims.fao.org/aos/agrovoc/c_7017dc39",
#     "unclaimed lands" : "http://aims.fao.org/aos/agrovoc/c_0e0e555b",
#     "water rights" : "http://aims.fao.org/aos/agrovoc/c_16062",
#     "land governance" : "http://aims.fao.org/aos/agrovoc/c_aca7ac6d",
#     "land rights" : "http://aims.fao.org/aos/agrovoc/c_37898",
#     "urbanization" : "http://aims.fao.org/aos/agrovoc/c_8088",
# }

#retrieve()
#retrieve_stats()

def filenames():
    retrieve_list = {
        "common lands" : "http://aims.fao.org/aos/agrovoc/c_1782", 
        "deforestation" : "http://aims.fao.org/aos/agrovoc/c_15590", 
        "desertification" : "http://aims.fao.org/aos/agrovoc/c_2204", 
        "dryland management" : "http://aims.fao.org/aos/agrovoc/c_9000036", 
        "farmland" : "http://aims.fao.org/aos/agrovoc/c_2808", 
        "forest conservation" : "http://aims.fao.org/aos/agrovoc/c_1374158672853", 
        "forest degradation" : "http://aims.fao.org/aos/agrovoc/c_331593", 
        "forest grazing" : "http://aims.fao.org/aos/agrovoc/c_3046", 
        "forest land" : "http://aims.fao.org/aos/agrovoc/c_24843", 
        "forest land use" : "http://aims.fao.org/aos/agrovoc/c_1374157828575", 
        "forest resources" : "http://aims.fao.org/aos/agrovoc/c_3050", 
        "geographical information systems" : "http://aims.fao.org/aos/agrovoc/c_35131", 
        "grassland management" : "http://aims.fao.org/aos/agrovoc/c_3364", 
        "housing" : "http://aims.fao.org/aos/agrovoc/c_3678", 
        "indigenous tenure systems" : "http://aims.fao.org/aos/agrovoc/c_9000081", 
        "individual land property" : "http://aims.fao.org/aos/agrovoc/c_9000082", 
        "land" : "http://aims.fao.org/aos/agrovoc/c_4172", 
        "land access" : "http://aims.fao.org/aos/agrovoc/c_9000090", 
        "land administration" : "http://aims.fao.org/aos/agrovoc/c_9000091", 
        "land classification" : "http://aims.fao.org/aos/agrovoc/c_15991", 
        "land cover" : "http://aims.fao.org/aos/agrovoc/c_37897", 
        "land cover mapping" : "http://aims.fao.org/aos/agrovoc/c_9000094", 
        "land degradation" : "http://aims.fao.org/aos/agrovoc/c_34823", 
        "land improvement" : "http://aims.fao.org/aos/agrovoc/c_28717", 
        "land management" : "http://aims.fao.org/aos/agrovoc/c_24866", 
        "land markets" : "http://aims.fao.org/aos/agrovoc/c_4175", 
        "land ownership" : "http://aims.fao.org/aos/agrovoc/c_28718", 
        "land policies" : "http://aims.fao.org/aos/agrovoc/c_195", 
        "land productivity" : "http://aims.fao.org/aos/agrovoc/c_4176", 
        "land reform" : "http://aims.fao.org/aos/agrovoc/c_4178", 
        "land registration" : "http://aims.fao.org/aos/agrovoc/c_9000098", 
        "land resources" : "http://aims.fao.org/aos/agrovoc/c_4179", 
        "land rights" : "http://aims.fao.org/aos/agrovoc/c_37898", 
        "land suitability" : "http://aims.fao.org/aos/agrovoc/c_15992", 
        "land tax" : "http://aims.fao.org/aos/agrovoc/c_4180", 
        "land tenure" : "http://aims.fao.org/aos/agrovoc/c_12069", 
        "land transfers" : "http://aims.fao.org/aos/agrovoc/c_4181", 
        "land use" : "http://aims.fao.org/aos/agrovoc/c_4182", 
        "land use mapping" : "http://aims.fao.org/aos/agrovoc/c_9000100", 
        "land use planning" : "http://aims.fao.org/aos/agrovoc/c_37899", 
        "landowners" : "http://aims.fao.org/aos/agrovoc/c_4184", 
        "multiple land use" : "http://aims.fao.org/aos/agrovoc/c_28734", 
        "natural resources" : "http://aims.fao.org/aos/agrovoc/c_5091", 
        "natural resources management" : "http://aims.fao.org/aos/agrovoc/c_9000115", 
        "pastoral society" : "http://aims.fao.org/aos/agrovoc/c_28741", 
        "pastoralism" : "http://aims.fao.org/aos/agrovoc/c_16144", 
        "private ownership" : "http://aims.fao.org/aos/agrovoc/c_6192", 
        "property rights" : "http://aims.fao.org/aos/agrovoc/c_37942", 
        "public ownership" : "http://aims.fao.org/aos/agrovoc/c_6350", 
        "rangelands" : "http://aims.fao.org/aos/agrovoc/c_6448", 
        "reforestation" : "http://aims.fao.org/aos/agrovoc/c_13802", 
        "resource management" : "http://aims.fao.org/aos/agrovoc/c_6524", 
        "right of access" : "http://aims.fao.org/aos/agrovoc/c_6604", 
        "soil degradation" : "http://aims.fao.org/aos/agrovoc/c_7168", 
        "soil management" : "http://aims.fao.org/aos/agrovoc/c_7176", 
        "spatial database" : "http://aims.fao.org/aos/agrovoc/c_9000154", 
        "sustainable forest management" : "http://aims.fao.org/aos/agrovoc/c_331342", 
        "sustainable land management" : "http://aims.fao.org/aos/agrovoc/c_36580", 
        "tenure" : "http://aims.fao.org/aos/agrovoc/c_7669", 
        "urban agriculture" : "http://aims.fao.org/aos/agrovoc/c_35707", 
        "urban areas" : "http://aims.fao.org/aos/agrovoc/c_8085", 
        "urban planning" : "http://aims.fao.org/aos/agrovoc/c_37948", 
        "urbanization" : "http://aims.fao.org/aos/agrovoc/c_8088", 
        "valuation" : "http://aims.fao.org/aos/agrovoc/c_8152", 
        "water management" : "http://aims.fao.org/aos/agrovoc/c_8320", 
        "water resources" : "http://aims.fao.org/aos/agrovoc/c_8325", 
        "water rights" : "http://aims.fao.org/aos/agrovoc/c_16062", 
    }
    for agrovoc_label, agrovoc_uri in retrieve_list.iteritems():
        filename="\"results/all-results+"+agrovoc_label+".json\" , "
        print filename

filenames()