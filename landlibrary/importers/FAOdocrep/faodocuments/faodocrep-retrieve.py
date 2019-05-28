import requests
import json
from fileinput import filename

RETRIEVE_LIST = {
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

ENDPOINT = "https://api.fao.org/api/gsa/1.0.0"

def retrieve():

    #TODO extract to a variable
    stats={}
    for agrovoc_label, agrovoc_uri in RETRIEVE_LIST.iteritems():
        print agrovoc_label
        next=0
        all_results = []
        year_start=1850
        year_end=2018
        agrovoc_uri_enconded = "http%3A%252F%252Faims%252Efao%252Eorg%252Faos%252Fagrovoc%252F" + str.replace(agrovoc_uri,"http://aims.fao.org/aos/agrovoc/","")
        
        # problems with the encode of the agrovoc urlagrovoc_uri_enconded
        next_relative_url = "/search?client=docrep&output=xml_no_dtd&site=faodocrep&partialfields=&requiredfields=(agrovoc_id%3A"+ agrovoc_uri_enconded +").docRepCollection%3Adocuments&filter=0&q=+inmeta%3Ayear%3A"+str(year_start)+".."+str(year_end)+"&proxystylesheet=xml_to_json&getfields=*&dnavs=&start=0&apikey=c335a12f-a850-4816-aed5-51ab7f723f12&sort=meta%3Ayear%3AD%3ASD%3AY"
        while (next_relative_url):
            print ENDPOINT+next_relative_url
            response = requests.get(ENDPOINT+next_relative_url, headers={"Accept":"application/json","Authorization" : "Bearer 8ce6f29360faa9ee4fcf29b749d455e"})
            data = response.json()
            stats[agrovoc_label] = 0
            if 'current_page' in data['pagination']:
                current_page = data['pagination']['current_page']
            else: #no results for that concept
                next_relative_url = None
                continue
            stats[agrovoc_label] = data['GSP']['RES']['M'] 
            next+=10
            if ('NB' in data['GSP']['RES'] and 'NU' in data['GSP']['RES']['NB']):
                next_relative_url = "/search?client=docrep&output=xml_no_dtd&site=faodocrep&partialfields=&requiredfields=(agrovoc_id%3A"+agrovoc_uri_enconded+").docRepCollection%3Adocuments&filter=0&q=+inmeta%3Ayear%3A"+str(year_start)+".."+str(year_end)+"&proxystylesheet=xml_to_json&getfields=*&dnavs=&start="+str(next)+"&apikey=c335a12f-a850-4816-aed5-51ab7f723f12&sort=meta%3Ayear%3AD%3ASD%3AY"
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

    stats={}
    for agrovoc_label, agrovoc_uri in RETRIEVE_LIST.iteritems():
        agrovoc_uri_enconded = "http%3A%252F%252Faims%252Efao%252Eorg%252Faos%252Fagrovoc%252F" + str.replace(agrovoc_uri,"http://aims.fao.org/aos/agrovoc/","")
        
        # problems with the encode of the agrovoc urlagrovoc_uri_enconded
        next_relative_url = "/search?client=docrep&output=xml_no_dtd&site=faodocrep&partialfields=&requiredfields=(agrovoc_id%3A"+ agrovoc_uri_enconded +").docRepCollection%3Adocuments&filter=0&q=&proxystylesheet=xml_to_json&getfields=*&dnavs=&start=0&apikey=c335a12f-a850-4816-aed5-51ab7f723f12&ulang=en&language=en&sort=meta%3Ayear%3AD%3ASD%3AY"
        response = requests.get(ENDPOINT+next_relative_url, headers={"Accept":"application/json","Authorization" : "Bearer 8ce6f29360faa9ee4fcf29b749d455e"})
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

retrieve()