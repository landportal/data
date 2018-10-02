import requests
import json
import harvest_lists

# 1) Get labels in different languages
# 2) Get stats for each label
# 3) Get stats for the whole bunch (duplicates + filter out)
# Combination of languages (land)

def retrieve_by_concept(harvest_concept, with_land=False): 
    page = 1 #(first page is 1)
    limit = 100
    endpoint = "http://www.lareferencia.info/vufind/api/v1/search?"
    returned_fields = "&field[]=rawData&field[]=accessRestrictions&field[]=containerStartPage&field[]=urls&field[]=id&field[]=title&field[]=subTitle&field[]=languages&field[]=summary&field[]=formats&field[]=publicationDates&field[]=primaryAuthors&field[]=secondaryAuthors&field[]=corporateAuthors&field[]=publishers&field[]=subjects&"
    if with_land:
        subjects = "&join=AND&lookfor0[]="+"\"tierra\""+"&type0[]=Subject&lookfor0[]=\""+harvest_concept+"\"&type0[]=Subject&bool0[]=AND"
    else:
        subjects = "lookfor=\""+harvest_concept+"\"&type=Subject"
    url_getCount = endpoint+returned_fields+subjects+"&limit=0"
    resultCount = requests.get(url_getCount, headers={"Accept":"application/json"}).json()["resultCount"]
    print harvest_concept +";"+str(resultCount)
    
    while ((page-1)*limit < resultCount):
        url = endpoint+returned_fields+subjects+"&limit="+str(limit)+"&page="+str(page)
        response = requests.get(url, headers={"Accept":"application/json"})
        data = response.json()["records"]
        #save the results in a file
        folder="results"
        if with_land:
            filename="results-tierra+"+harvest_concept+"-"+str(page)+".json"
        else:
            filename="results-"+harvest_concept+"-"+str(page)+".json"

        with open(folder+"/"+filename, 'w') as outfile:
            json.dump(data, outfile, indent=4)
            print("written file="+"results/"+filename)       
        page+=1 #next page
        
#     for record in data["records"]:
#         print record["id"]
#         print record["rawData"]
#         #print record["title"]
#         #if "subTitle" in record: print record["subTitle"] 
#         #if "summary" in record: print record["summary"]
#         #if "publicationDates" in record: print record["publicationDates"]
#         #if "formats" in record: print record["formats"] 
#         #if "primaryAuthors" in record: print record["primaryAuthors"] 
#         #if "secondaryAuthors" in record: print record["secondaryAuthors"] 
#         #if "corporateAuthors" in record: print record["corporateAuthors"]
#         lareferencia_url = "http://www.lareferencia.info/vufind/Record/"+record["id"]
#                
#         #if "containerStartPage" in record: print record["containerStartPage"] 
#         if "accessRestrictions" in record: print record["accessRestrictions"] 
#         
#         #if "subjects" in record: print record["subjects"] 
#         #if "publishers" in record: print record["publishers"] 
#         #if "urls" in record: print record["urls"] 
#         
#         #print record["languages"]


def retrieve_stats(harvest_concept,with_land=False):
    endpoint = "http://www.lareferencia.info/vufind/api/v1/search?limit=0&"
    if with_land:
        url = endpoint+"join=AND&lookfor0[]=\"tierra\"&type0[]=Subject&lookfor0[]=\""+harvest_concept+"\"&type0[]=Subject&bool0[]=AND"
    else:
        url = endpoint+"lookfor=\""+harvest_concept+"\"&type=Subject"

    response = requests.get(url, headers={"Accept":"application/json"})
    data = response.json()
    total_count = data['resultCount']
    if with_land:
        print "tierra+"+harvest_concept+";"+str(total_count)
    else:
        print harvest_concept+";"+str(total_count)
    return total_count

# total=0
# for harvest_concept in harvest_lists.HARVEST_LIST_LAREFERENCIA:
#     total+=retrieve_stats(harvest_concept)
# print "TOTAL="+str(total)
# print "------------------------"
#  
# total=0
# for harvest_concept in harvest_lists.HARVEST_LIST_WITH_LAND_LAREFERENCIA:
#     total+=retrieve_stats(harvest_concept, with_land=True)
# print "TOTAL="+str(total)
# print "------------------------"


for harvest_concept in harvest_lists.HARVEST_LIST_LAREFERENCIA:
    retrieve_by_concept(harvest_concept)

for harvest_concept in harvest_lists.HARVEST_LIST_WITH_LAND_LAREFERENCIA:
    retrieve_by_concept(harvest_concept, with_land=True)
