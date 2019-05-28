#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os

class LandVoc(object):
    
    def _input_path(self, basepath, filename):
        return os.path.abspath(os.path.join(basepath, filename))
    def load_landvoc_concepts(self, filename):
        lines = []
        with open(filename) as working_file:
            for line in working_file:
                line = line.strip().split(";")[0] #or someother preprocessing
                lines.append(line)
        return lines

    def load_relations(self, filename):
        #keyword - one or multiple concepts
        relations = {}
        with open(filename) as working_file:
            for line in working_file:
                faolex_concept = line.strip().split(";")[0]
                landvoc_concepts = map(str.strip, line.strip().split(";",1)[1].strip('"').split(";"))
                relations[faolex_concept] =  landvoc_concepts
        return relations
    
    def __init__(self):
        basepath = os.path.dirname(__file__)
        self.concepts=self.load_landvoc_concepts(self._input_path(basepath, "landvoc-label-id.csv"))
        self.faolex_related=self.load_relations(self._input_path(basepath, "faolex-relations.csv"))
        self.concepts_harvest_enhacenment=self.load_relations(self._input_path(basepath, "concepts_harvest_enhacenment.csv"))
        self.themes_harvest_enhacenment=self.load_relations(self._input_path(basepath, "themes_harvest_enhacenment.csv"))
        self.oacs_harvest_enhacenment=self.load_relations(self._input_path(basepath, "oacs_harvest_enhacenment.csv"))

    def get_concepts(self):
        return self.concepts

    def get_faolex_related(self):
        return self.faolex_related

    def get_concepts_harvest_enhacenment(self):
        return self.concepts_harvest_enhacenment

    def get_themes_harvest_enhacenment(self):
        return self.themes_harvest_enhacenment

    def get_oacs_harvest_enhacenment(self):
        return self.oacs_harvest_enhacenment
                
    def get_concepts_direct(self, potential_concepts):
        return [x for x in potential_concepts if x in self.get_concepts()]

    def get_concepts_faolex_related(self, potential_concepts):
        flatten = lambda l: [item for sublist in l for item in sublist]
        return flatten([self.get_faolex_related()[x] for x in potential_concepts if x in self.get_faolex_related().keys()])

    def get_concepts_harvest_enhancement(self, potential_concepts):
        flatten = lambda l: [item for sublist in l for item in sublist]
        return flatten([self.get_concepts_harvest_enhacenment()[x] for x in potential_concepts if x in self.get_concepts_harvest_enhacenment().keys()])

    def get_themes_harvest_enhancement(self, concepts):
        flatten = lambda l: [item for sublist in l for item in sublist]
        return set(filter(None, flatten([self.get_themes_harvest_enhacenment()[x] for x in concepts if x in self.get_themes_harvest_enhacenment().keys()])))

    def get_oacs_harvest_enhancement(self, concepts):
        flatten = lambda l: [item for sublist in l for item in sublist]
        return set(filter(None, flatten([self.get_oacs_harvest_enhacenment()[x] for x in concepts if x in self.get_oacs_harvest_enhacenment().keys()])))
