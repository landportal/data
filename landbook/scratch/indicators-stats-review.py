from SPARQLWrapper import SPARQLWrapper, JSON
from cmath import sqrt

def statsReview(indicator):
    sparql = SPARQLWrapper("https://landportal.info/sparql")
    sparql.setQuery("""
    PREFIX cex: <http://purl.org/weso/ontology/computex#>
    SELECT (MIN(?value) AS ?minvalue)  (MAX(?value) AS ?maxvalue) (?mean) (?count) (SUM(((xsd:float(?value - ?mean))*(xsd:float(?value - ?mean))))/(?count - 1) AS ?variance)
    FROM <http://data.landportal.info>
    WHERE {
    ?obs cex:ref-indicator <"""+indicator+"""> ;
         cex:value ?value .
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
        min = result["minvalue"]["value"]
        max = result["maxvalue"]["value"]
        mean = result["mean"]["value"]
        count = result["count"]["value"]
        variance = result["variance"]["value"]
        
        print "INDICATOR: "+ indicator
        print "MIN: "+ min
        print "MAX: "+ max
        print "MEAN: "+ mean
        print "COUNT: "+ count
        print "VARIANCE: "+ variance
        print "STANDARD DEVIATION: "+str(sqrt(float(variance)))
        print "---------------------------------------"
        


def getIndicators():
    sparql = SPARQLWrapper("https://landportal.info/sparql")
    
    sparql_get_indicators = """
    PREFIX cex: <http://purl.org/weso/ontology/computex#>
    
    SELECT DISTINCT ?indicatorURL
    FROM <http://data.landportal.info>
    WHERE {
       ?indicatorURL a cex:Indicator . # ?obs cex:ref-indicator ?indicatorURL .
    } ORDER BY ?indicatorURL
    """
    sparql.setQuery(sparql_get_indicators)
    
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    indicators = []
    for result in results["results"]["bindings"]:
        indicatorURL = result["indicatorURL"]["value"]
        #print("-------------------------------------------------------")
        #print("indicatorURL: " + indicatorURL)
        indicators.append(indicatorURL)
    return indicators
        
indicators = getIndicators()

# main
for indicator in indicators :
    statsReview(indicator)