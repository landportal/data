#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os

class LandVocLANDJOURNAL(object):
    
    def _input_path(self, basepath, filename):
        return os.path.abspath(os.path.join(basepath, filename))

    def load_landjournal_landvoc_concepts(self, filename):
        #keyword - one or multiple concepts
        relations = {}
        with open(filename, encoding="utf-8") as landjournal_file:
            for line in landjournal_file:
                landjournal_concept = line.strip().split(";")[0]
                landvoc_concepts = map(str.strip, line.strip().split(";",1)[1].strip('"').split(";"))
                relations[landjournal_concept] = landvoc_concepts
        return relations
    
    def __init__(self):
        basepath = os.path.dirname(__file__)        
        self.landjournal_related=self.load_landjournal_landvoc_concepts(self._input_path(basepath, "land_journal-relations.csv"))

###############################################################################

    def get_landjournal_related(self):
        return self.landjournal_related

    def get_concepts_landjournal_related(self, potential_concepts):
        flatten = lambda l: [item for sublist in l for item in sublist]
        return flatten([self.get_landjournal_related()[x] for x in potential_concepts if x in self.get_landjournal_related().keys()])