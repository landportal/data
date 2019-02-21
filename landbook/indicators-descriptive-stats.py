from SPARQLWrapper import SPARQLWrapper, JSON
from cmath import sqrt
import datetime


def statsReview(indicator, indicatorLabel):
    date = now = datetime.datetime.now().strftime("%Y-%m-%d")

    sparql = SPARQLWrapper("https://landportal.org/sparql")
    sparql.setQuery("""
    PREFIX cex: <http://purl.org/weso/ontology/computex#>

	SELECT 
	(year(min(?dateTime)) AS ?minYear)
	(year(max(?dateTime)) AS ?maxYear)
	(?count)
	(COUNT(DISTINCT(year(?dateTime))) AS ?nYears)
	(COUNT(DISTINCT ?country) AS ?nCountryWithValue)
	(MIN(?value) AS ?minValue)
	(MAX(?value) AS ?maxValue)
	(?mean)
	
	FROM <http://data.landportal.info>
	
	WHERE {
	?obs cex:ref-indicator <"""+indicator+"""> ;
		 cex:value ?value ;
		 cex:ref-area ?country ;
		 cex:ref-time ?time .
	?time time:hasBeginning ?timeValue .
	?timeValue time:inXSDDateTime ?dateTime .
	{  
		SELECT (AVG(?value) as ?mean) (COUNT(?value) as ?count)
		FROM <http://data.landportal.info>
		WHERE {
		 ?obs cex:ref-indicator <"""+indicator+"""> ;
		   cex:value ?value .
		}
	}
	}
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    for result in results["results"]["bindings"]:
        minYear = result["minYear"]["value"]
        maxYear = result["maxYear"]["value"]
        #unit = result["unit"]["value"]
        count = result["count"]["value"]
        nYears = result["nYears"]["value"]
        nCountryWithValue = result["nCountryWithValue"]["value"]
        minValue = (result["minValue"]["value"]).replace('.', ',')
        maxValue = (result["maxValue"]["value"]).replace('.', ',')
        mean = (result["mean"]["value"]).replace('.', ',')
        perMissingValue = (str((1-(float(count))/(float(nYears)*float(nCountryWithValue)))*100)).replace('.', ',')
        indicatorID = indicator.replace("http://data.landportal.info/indicator/", "")
        """
        print "INDICATOR: "+ indicatorID
        print "MIN YEAR: "+ minYear
        print "MAX YEAR: " + maxYear
        #print "UNIT: " + unit
        print "COUNT (number observations): "+ count
        print "NUMBER YEARS: " + nYears
        print "TOTAL COUNTRIES: " + nCountryWithValue
        print "MISSING VALUES (%)" + perMissingValue
        print "MIN VALUE: "+ minValue
        print "MAX VALUE: "+ maxValue
        print "MEAN: "+ mean
        print "---------------------------------------"
        """        
		# CSV: "INDICATOR - MIN - MAX - MEAN - COUNT - VARIANCE - STANDARD DEVIATION"
		# COUNT = Number of observations
		# NUMBER YEARS = NUMBER OF YEARS WITH AT LEAST ONE VALUE
		# NUMBER COUNTRIES = NUMBER OF COUNTRIES WITH AT LEAST ONE VALUE
        print date + ";" + indicatorID + ";" + indicatorLabel + ";" + minYear + ";" + maxYear + ";" + count + ";" + nYears + ";" + nCountryWithValue + ";" + perMissingValue + ";" + minValue + ";" + maxValue + ";" + mean + ";"


def getIndicators():
    sparql = SPARQLWrapper("https://landportal.org/sparql")
    
    sparql_get_indicators = """
    PREFIX cex: <http://purl.org/weso/ontology/computex#>
    
    SELECT DISTINCT ?indicatorURL ?indicatorLabel
    FROM <http://indicators.landportal.info>
    WHERE {
       ?indicatorURL a cex:Indicator ;
	                 rdfs:label ?indicatorLabel .
    } ORDER BY ?indicatorURL
    """
    sparql.setQuery(sparql_get_indicators)
    
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    indicators = []
    for result in results["results"]["bindings"]:
        indicator = (result["indicatorURL"]["value"], result["indicatorLabel"]["value"])
        #print("-------------------------------------------------------")
        #print("indicatorURL: " + indicatorURL)
        indicators.append(indicator)
    return indicators


# main	
#header 
print "date ; indicator ID; indicator label; minYear ; maxYear; number observations ; number years ; total countries ; missing values ; min value ; max value ; mean ; variance ; standard deviation"

indicators = getIndicators()

for indicator in indicators :
    statsReview(indicator[0], indicator[1])
