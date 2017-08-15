#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import csv

class LandVoc(object):

    def __init__(self):
        basepath = os.path.dirname(__file__)
        self.concepts_and_fixed_relations, self.uris_to_concepts = self.process_landvoc_file(self._input_path(basepath, "landvoc-and-fixed-relatioships.csv"))

    def get_only_concepts(self):
        return self.concepts_and_fixed_relations.keys()

    def get_concepts(self):
        return self.concepts_and_fixed_relations
    
    def _input_path(self, basepath, filename):
        return os.path.abspath(os.path.join(basepath, filename))

    def process_landvoc_file(self, filename):
        concepts={}
        uris_to_concept={}
        with open(filename) as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            headers = reader.next()
            for row in reader:
                concept_label = row[0]
                concept_uri = row[1]
                uris_to_concept[concept_uri]=concept_label
                concepts[concept_label] = {"themes":set(), "oacs": set()}
                for key, value in zip(headers[2:], row[2:]):
                    if value=="x":
                        if key in ["Access to Land & Tenure Security", "Land Use, Management & Investment", "Land Policy & Legislation"] : #OACS
                            concepts[concept_label]["oacs"].add(key)
                        else: # THEMES
                            concepts[concept_label]["themes"].add(key)
        return concepts, uris_to_concept

    def get_concepts_direct(self, potential_concepts):
        return [x.lower() for x in potential_concepts if x.lower() in map(str.lower, self.get_only_concepts())]

    def get_concepts_direct_from_uris(self, potential_uris):
        return [self.uris_to_concepts[uri] for uri in potential_uris if uri in self.uris_to_concepts.keys()]
    
    def get_fixed_themes(self, selected_concepts):
        themes=set()
        for x in selected_concepts:
            if x in self.get_concepts():
                th = self.get_concepts()[x]["themes"]
                themes |= th
            else:
                print "Warning: unknown concept="+x
        return themes

    def get_fixed_oacs(self, selected_concepts):
        oacs=set()
        for x in selected_concepts:
            if x in self.get_concepts():            
                oa = self.get_concepts()[x]["oacs"]
                oacs |= oa
            else:
                print "Warning: unknown concept="+x
        return oacs
    
#     def generate_list_from_string(self, s):
#         return map(str.strip, filter(None, s.split(';')))
# 
# 
#     def get_landvoc_related(self, source_concepts, scheme):
#         flatten = lambda l: [item for sublist in l for item in sublist]
#         final_result={"concepts_and_fixed_relations": [], "themes": [], "oacs": [] }
#         if source_concepts:
#             tmp_result = [self.relations[scheme][x.lower()] for x in source_concepts if x.lower() in map(str.lower, self.relations[scheme].keys())]
#             for r in tmp_result:
#                 final_result["concepts_and_fixed_relations"].append(r["concepts_and_fixed_relations"])
#                 final_result["themes"].append(r["themes"])
#                 final_result["oacs"].append(r["oacs"])
#             final_result["concepts_and_fixed_relations"] = list(set(flatten(final_result["concepts_and_fixed_relations"])))
#             final_result["themes"] = list(set(flatten(final_result["themes"])))
#             final_result["oacs"] = list(set(flatten(final_result["oacs"])))
#         return final_result
# 
#     

lv = LandVoc()
