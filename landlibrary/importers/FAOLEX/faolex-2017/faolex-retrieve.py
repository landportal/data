def retrieve():
    endpoint = "https://api.fao.org/api/gsa/1.0.0"
    #typeOfTextCodes = ['C','P','L','R','A','M']
    typeOfTextCodes = ['C','P','A','M']
    #C = Constitutions
    #P = Policies
    #L = Legislations
    #R = Regulation
    # A = International Agreements
    #M = Miscellaneous
    for typeOfTextCode in typeOfTextCodes:
        next=0
        all_results = []
        year=1986
        next_relative_url = "/search?client=faolex&output=xml_no_dtd&site=faolex_collection&partialfields=&requiredfields=(subjectSelectionCode%3ALA).(typeOfTextCode%3A"+typeOfTextCode+")&filter=0&q=+inmeta%3AallYear%3A"+year+".."+year+"&proxystylesheet=xml_to_json&getfields=*&dnavs=&start=0&apikey=4b025441-7e81-4b5d-a2c5-b43f7ca991e9&ulang=en&language=en&sort=meta%3Ayear%3AD%3ASD%3AY"
        while (next_relative_url):
            response = requests.get(endpoint+next_relative_url, headers={"Accept":"application/json","Authorization" : "Bearer 8ce6f29360faa9ee4fcf29b749d455e"})
            data = response.json()
            current_page = data['pagination']['current_page']
            next+=10
            if ('NU' in data['GSP']['RES'] ['NB']):
                next_relative_url ="/search?client=faolex&output=xml_no_dtd&site=faolex_collection&partialfields=&requiredfields=(subjectSelectionCode%3ALA).(typeOfTextCode%3A"+typeOfTextCode+")&filter=0&q=&proxystylesheet=xml_to_json&getfields=*&dnavs=&start="+str(next)+"&apikey=4b025441-7e81-4b5d-a2c5-b43f7ca991e9&ulang=en&language=en&sort=meta%3Ayear%3AD%3ASD%3AY"
            else:
                next_relative_url = None
            #save the results in a file
            filename="results-"+typeOfTextCode+"-"+year+".json"
            with open(filename, 'w') as outfile:
                json.dump(data, outfile)
                print("written file="+filename)

            #concat the results
            partial_results = data['GSP']['RES'] ['results']
            all_results =all_results + partial_results

        with open("all-results+"+typeOfTextCode+"+"+year+".json", 'w') as outfile:
            json.dump(all_results, outfile)
            print("written file ALL -"+typeOfTextCode+"- results")


def retrieve_by_year(typeOfTextCode, init_year, end_year):
    endpoint = "https://api.fao.org/api/gsa/1.0.0"
    #typeOfTextCode = 'L'
    #C = Constitutions
    #P = Policies
    #L = Legislations
    #R = Regulation
    # A = International Agreements
    #M = Miscellaneous
    all_results = []
    year = init_year

    while (year!=end_year):
        next=0
        all_results_by_year = []
        next_relative_url = "/search?client=faolex&output=xml_no_dtd&site=faolex_collection&partialfields=&requiredfields=(subjectSelectionCode%3ALA).(typeOfTextCode%3A"+typeOfTextCode+")&filter=0&q=+inmeta%3AallYear%3A"+str(year)+".."+str(year)+"&proxystylesheet=xml_to_json&getfields=*&dnavs=&start=0&apikey=4b025441-7e81-4b5d-a2c5-b43f7ca991e9&ulang=en&language=en&sort=meta%3Ayear%3AD%3ASD%3AY"
        while (next_relative_url):
            response = requests.get(endpoint+next_relative_url, headers={"Accept":"application/json","Authorization" : "Bearer 8ce6f29360faa9ee4fcf29b749d455e"})
            data = response.json()
            if (data['pagination']):
                current_page = data['pagination']['current_page']
            else:
                break
            next+=10
            if ('NB' in data['GSP']['RES'] and 'NU' in data['GSP']['RES']['NB']):
                next_relative_url ="/search?client=faolex&output=xml_no_dtd&site=faolex_collection&partialfields=&requiredfields=(subjectSelectionCode%3ALA).(typeOfTextCode%3A"+typeOfTextCode+")&filter=0&q=+inmeta%3AallYear%3A"+str(year)+".."+str(year)+"&proxystylesheet=xml_to_json&getfields=*&dnavs=&start="+str(next)+"&apikey=4b025441-7e81-4b5d-a2c5-b43f7ca991e9&ulang=en&language=en&sort=meta%3Ayear%3AD%3ASD%3AY"
            else:
                next_relative_url = None
            #save the results in a file
            filename="results-"+typeOfTextCode+"-"+current_page+"-"+str(year)+".json"
            with open(filename, 'w') as outfile:
                json.dump(data, outfile)
                print("written file="+filename)

            #concat the results
            partial_results = data['GSP']['RES'] ['results']
            all_results_by_year =all_results_by_year + partial_results
        filename_year = "all-results+"+typeOfTextCode+"+"+str(year)+".json"
        with open(filename_year, 'w') as outfile:
            json.dump(all_results_by_year, outfile)
            print("WRITTEN:"+ filename_year)

        all_results = all_results + all_results_by_year
        year+=1

    filename_all = "all-results+"+typeOfTextCode+"+"+str(init_year)+"+"+str(end_year)+".json"
    with open(filename_all, 'w') as outfile:
        json.dump(all_results, outfile)
        print("written " + filename_all)

