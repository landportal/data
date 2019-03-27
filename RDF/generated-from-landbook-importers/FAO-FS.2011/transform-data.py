#!/usr/bin/python
# -*- coding: utf-8 -*-

import inspect
import os
import sys

# prefer local copy to the one which is installed
# hack from http://stackoverflow.com/a/6098238/280539
_top_level_path = os.path.realpath(os.path.abspath(os.path.join(
    os.path.split(inspect.getfile(inspect.currentframe()))[0],
    ".."
)))
if _top_level_path not in sys.path:
    sys.path.insert(0, _top_level_path)
# end of hack

from SPARQLWrapper import SPARQLWrapper, RDFXML

indicators = [   
    "<http://data.landportal.info/indicator/FAO-21015-6121>",
    "<http://data.landportal.info/indicator/FAO-21017-6124>",
    "<http://data.landportal.info/indicator/FAO-21018-6125>",
    "<http://data.landportal.info/indicator/FAO-21022-6121>",
    "<http://data.landportal.info/indicator/FAO-21024-6121>",
    "<http://data.landportal.info/indicator/FAO-21027-6121>",
    "<http://data.landportal.info/indicator/FAO-21028-6121>",
    "<http://data.landportal.info/indicator/FAO-21029-6125>",
    "<http://data.landportal.info/indicator/FAO-21036-6121>",
    "<http://data.landportal.info/indicator/FAO-21037-6121>",
    "<http://data.landportal.info/indicator/FAO-21038-6121>",
    "<http://data.landportal.info/indicator/FAO-21039-6121>"
]
sparql = SPARQLWrapper("https://landportal.org/sparql")

# in the new structure, it is needed that the dataset URL and the observation URL 
# update using the new dataset ID = FAO-FS.2011

for indicator in indicators:
    sparql.setQuery("""
    CONSTRUCT   {
        ?newObs ?p ?o .
        ?newObs qb:dataSet <http://data.landportal.info/dataset/FAO-FS.2011> .
        ?time ?tp ?to .
        ?end ?ep ?eo .
        ?beginning ?bp ?bo .
        ?timedescription ?tdp ?tdo .

    }
    FROM <http://data.landportal.info> 
    WHERE {
        ?obs a qb:Observation ;
             qb:dataSet ?dataset ;
             cex:ref-indicator ?indicator ;
             cex:ref-time ?time;
             ?p ?o .

        ?time ?tp ?to ;
             time:hasBeginning ?beginning ;
             time:hasEnd ?end .

        OPTIONAL {
            ?time time:hasDateTimeDescription ?timedescription .
            ?timedescription ?tdp ?tdo .
        }

        ?end ?ep ?eo .
        ?beginning ?bp ?bo .

        VALUES ?dataset { <http://data.landportal.info/dataset/FAO-FS> } .
        VALUES ?indicator { """+indicator+"""} .

        BIND (URI(CONCAT ("http://data.landportal.info/dataset/FAO-FS.2011",
                         STRAFTER (STR(?obs),"FAO-FS")))
             AS ?newObs)
        
        FILTER (?p != qb:dataSet) # removed dataset triple
    }""")

    sparql.setReturnFormat(RDFXML)
    results = sparql.query()
    results.convert().serialize(destination=indicator.replace("<http://data.landportal.info/indicator/","").replace(">","")+".rdf", format='xml')
    print indicator
