#!/usr/bin/python
# -*- coding: UTF-8 -*-
from __future__ import print_function
import json

with open('results-agris-stats.json', 'r') as data_file:
    results = json.load(data_file)
    #headers

    year=1975
    while year<2018:
        print(';'+str(year), end='')
        year+=1
    print(';TOTAL')
    for concept, years in results.iteritems():
        print(concept, end='')
        sum=0
        year=1975
        while year<2018:
            print(';', end='')
            if unicode(year) in years:
                result_number = years[unicode(year)]
                print(result_number, end='')
                sum+=result_number
            year+=1
        print(';'+str(sum))