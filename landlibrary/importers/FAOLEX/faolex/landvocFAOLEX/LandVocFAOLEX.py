#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os

class LandVocFAOLEX(object):
    
    def _input_path(self, basepath, filename):
        return os.path.abspath(os.path.join(basepath, filename))

    def load_faolex_landvoc_concepts(self, filename):
        #keyword - one or multiple concepts
        relations = {}
        with open(filename) as file:
            for line in file:
                faolex_concept = line.strip().split(";")[0]
                landvoc_concepts = map(str.strip, line.strip().split(";",1)[1].strip('"').split(";"))
                landvoc_concepts = map(unicode, landvoc_concepts)
                relations[faolex_concept] = landvoc_concepts
        return relations
    
    def __init__(self):
        basepath = os.path.dirname(__file__)        
        self.faolex_related=self.load_faolex_landvoc_concepts(self._input_path(basepath, "faolex-relations.csv"))

###############################################################################

    def get_faolex_related(self):
        return self.faolex_related

    def get_concepts_faolex_related(self, potential_concepts):
        flatten = lambda l: [item for sublist in l for item in sublist]
        return flatten([self.get_faolex_related()[x] for x in potential_concepts if x in self.get_faolex_related().keys()])