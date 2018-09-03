from SPARQLWrapper import SPARQLWrapper, JSON
from cmath import sqrt
import datetime

def statsReview(dataset, datasetLabel):
    date = now = datetime.datetime.now().strftime("%Y-%m-%d")

    sparql = SPARQLWrapper("https://landportal.org/sparql")
    sparql.setQuery("""
	PREFIX cex: <http://purl.org/weso/ontology/computex#>
	PREFIX qb: <http://purl.org/linked-data/cube#>

	SELECT 
	(year(min(?dateTime)) AS ?minYear)
	(year(max(?dateTime)) AS ?maxYear)
	(COUNT(DISTINCT(year(?dateTime))) AS ?nYears)
	(COUNT(DISTINCT ?country) AS ?nCountryWithValue)
	(COUNT(?obs) as ?count)
	FROM <http://data.landportal.info>
	
	WHERE {
	?obs qb:dataSet <"""+dataset+"""> ;
		 cex:ref-area ?country ;
		 cex:ref-time ?time .
	?time time:hasBeginning ?timeValue .
	?timeValue time:inXSDDateTime ?dateTime .
	}
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    for result in results["results"]["bindings"]:
        minYear = result["minYear"]["value"]
        maxYear = result["maxYear"]["value"]
        count = result["count"]["value"]
        nYears = result["nYears"]["value"]
        nCountryWithValue = result["nCountryWithValue"]["value"]
        datasetID = dataset.replace("http://data.landportal.info/dataset/", "")
        """
        print "INDICATOR: "+ datasetID
        print "MIN YEAR: "+ minYear
        print "MAX YEAR: " + maxYear
        print "COUNT (number observations): "+ count
        print "NUMBER YEARS: " + nYears
        print "TOTAL COUNTRIES: " + nCountryWithValue
        print "---------------------------------------"
        """        
		# CSV: "INDICATOR - MIN - MAX - MEAN - COUNT - VARIANCE - STANDARD DEVIATION"
		# COUNT = Number of observations
		# NUMBER YEARS = NUMBER OF YEARS WITH AT LEAST ONE VALUE
		# NUMBER COUNTRIES = NUMBER OF COUNTRIES WITH AT LEAST ONE VALUE
        print date + ";" + datasetID + ";" + datasetLabel + ";" + minYear + ";" + maxYear + ";" + count + ";" + nYears + ";" + nCountryWithValue + ";"


def getDatasets():
    sparql = SPARQLWrapper("https://landportal.org/sparql")
    
    sparql_get_datasets = """
    PREFIX cex: <http://purl.org/weso/ontology/computex#>
    PREFIX qb: <http://purl.org/linked-data/cube#>

    SELECT DISTINCT ?dataset ?datasetLabel
    FROM <http://datasets.landportal.info>
    WHERE {
       ?dataset a qb:DataSet ;
                rdfs:label ?datasetLabel .
    } ORDER BY ?dataset
    """
    sparql.setQuery(sparql_get_datasets)
    
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    datasets = []
    for result in results["results"]["bindings"]:
        dataset = (result["dataset"]["value"], result["datasetLabel"]["value"])
        #print("-------------------------------------------------------")
        #print("dataset: " + dataset)
        datasets.append(dataset)
    return datasets


# main	
#header 
print "date ; dataset ID; minYear ; maxYear; number observations ; number years ; total countries ;"

datasets = getDatasets()

for dataset in datasets :
    statsReview(dataset[0], dataset[1])
