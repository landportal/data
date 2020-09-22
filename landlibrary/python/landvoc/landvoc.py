#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import csv

class LandVoc(object):

    def __init__(self):
        self.concepts_and_fixed_relations, self.uris_to_concepts = self.process_landvoc_files()
        self.synonymsEn = {}
        for concept_k, concept_v in self.get_concepts().items():
            for syn in concept_v["synonyms_en"]:
                self.synonymsEn[syn] = concept_k


    def get_EnglishPrefLabel(self, label, lang="en"):
        concept = self.getConcept(label, lang)
        if concept:
            return concept["prefLabel_en"]
        else:
            #return unicode(concept)
            return None


    def getConcept(self, label, lang="en"):
        label = label.lower()
        if not self.check_concept(label, lang):
            return None
        for concept in self.concepts_and_fixed_relations.values():
            if "en" == lang and concept["prefLabel_en"].lower() == label:
                return concept
            elif "fr" == lang and concept["prefLabel_fr"].lower() == label:
                return concept
            elif "es" == lang and concept["prefLabel_es"].lower() == label:
                return concept
            elif "pt" == lang and concept["prefLabel_pt"].lower() == label:
                return concept

    def check_concept(self, label, lang="en"):
        label = label.lower()
        if (lang in ["en", "es", "fr", "pt"]) and (label in self.get_prefLabel_of_all_concepts(lang)):
            return True
        else:
            #print "Error in \"%s\""  %(label)
            return False


    def check_theme(self, collection):
        if collection in self.get_themes():
            return True
        else:
            print("Error in \"%s\""  %(collection))
            return False

    
    def get_prefLabel_of_all_concepts(self, lang="en"):
        
        if "en" == lang:
            all_labels_str = [item["prefLabel_en"].lower() for item in self.concepts_and_fixed_relations.values()]
        elif "fr" == lang:
            all_labels_str = [item["prefLabel_fr"].lower() for item in self.concepts_and_fixed_relations.values()]
        elif "es" == lang:
            all_labels_str = [item["prefLabel_es"].lower() for item in self.concepts_and_fixed_relations.values()]
        elif "pt" == lang:
            all_labels_str = [item["prefLabel_pt"].lower() for item in self.concepts_and_fixed_relations.values()]
        
        return all_labels_str

    def get_concepts(self):
        return self.concepts_and_fixed_relations
    
    def _input_path(self, basepath, filename):
        return os.path.abspath(os.path.join(basepath, filename))

    def process_landvoc_files(self):
        basepath = os.path.dirname(__file__)
        filenameFixedRelationships=self._input_path(basepath, "LandVoc-fixed-relationships.csv")
        concepts={}
        uris_to_concept={}
        with open(filenameFixedRelationships) as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            headers = next(reader)
            for row in reader:
                real_label = row[1]
                concept_label = real_label.lower()
                concept_uri = row[0]
                uris_to_concept[concept_uri]=concept_label
                concepts[concept_label] = {"themes":set(), "real_label": real_label, "synonyms": set()}
                for key, value in zip(headers[2:], row[2:]):
                    if value in ["x", "X"]:
                        concepts[concept_label]["themes"].add(key)

        # Process languages
        filenameLanguages=self._input_path(basepath, "LandVoc-concepts-plain.csv")
        with open(filenameLanguages, encoding="utf-8") as langfile:
            reader = csv.reader(langfile, delimiter=',', quotechar='"')
            headers = next(reader)
            for row in reader:
                prefLabel_en = row[0]
                prefLabel_en_lower = prefLabel_en.lower()
                prefLabel_fr = row[1]
                prefLabel_es = row[2]
                prefLabel_pt = row[3]
                concept_uri = row[4]
                uris_to_concept[concept_uri]=prefLabel_en_lower
                #concepts[prefLabel_en_lower] = {"themes":set(), "real_label": prefLabel_en, "uri": concept_uri}
                concepts[prefLabel_en_lower]["prefLabel_en"]=prefLabel_en
                concepts[prefLabel_en_lower]["prefLabel_fr"]=prefLabel_fr
                concepts[prefLabel_en_lower]["prefLabel_es"]=prefLabel_es
                concepts[prefLabel_en_lower]["prefLabel_pt"]=prefLabel_pt

        # Process synonyms
        filenameSynonyms=self._input_path(basepath, "synonyms.csv")
        with open(filenameSynonyms, "r", encoding="utf8") as synfile:
            readerSyn = csv.reader(synfile, delimiter=',', quotechar='"',skipinitialspace=True)
            headers = next(readerSyn)
            for row in readerSyn:
                #uri = row[0] #uri
                prefLabel_en_lower = row[1].lower().strip()
                concepts[prefLabel_en_lower]["synonyms_en"] = [x.strip().lower() for x in row[2].split("|") if x]
                concepts[prefLabel_en_lower]["synonyms_es"] = [x.strip().lower() for x in row[3].split("|") if x]
                concepts[prefLabel_en_lower]["synonyms_fr"] = [x.strip().lower() for x in row[4].split("|") if x]
                concepts[prefLabel_en_lower]["synonyms_pt"] = [x.strip().lower() for x in row[5].split("|") if x]
        return concepts, uris_to_concept

    def getRealLabelFromConceptLabel(self, lower_label):
        real_label = self.concepts_and_fixed_relations[lower_label]["real_label"]
        return real_label

    def get_concepts_direct(self, potential_concepts):
        return [self.getRealLabelFromConceptLabel(x.lower()) for x in potential_concepts if x.lower() in map(str.lower, self.get_prefLabel_of_all_concepts())]

    def get_concepts_synonymsEN(self, labels):
#         result = set()
#         for label in labels:
#             for concept_k, concept_v in self.get_concepts().items():
#                 if label.lower() in concept_v["synonyms_en"]:
#                     result.add(concept_v["prefLabel_en"])
#                     print(label)
#                     print(concept_v)
        return [self.synonymsEn[label] for label in labels if label in self.synonymsEn]


    def get_concepts_direct_from_uris(self, potential_uris):
        return [self.uris_to_concepts[uri] for uri in potential_uris if uri in self.uris_to_concepts.keys()]
    
    def get_fixed_themes(self, selected_concepts):
        themes=set()
        for x in map(str.lower, selected_concepts):
            if x in self.get_concepts():
                th = self.get_concepts()[x]["themes"]
                themes |= th
            else:
                print("Warning (Themes): unknown concept="+x)
        return themes


    #return a list of concepts from a given text
    def parse_get_concepts(self, text):
        """
        This method returns a list of concepts parsed from the text
        @param text: A text string to be parsed.
        @type text: string
        @return: A list of concepts.
        @rtype: list
        """
        retrieved_concepts = []
        text = text.lower()
        for concept_label in self.get_prefLabel_of_all_concepts():
            if concept_label.lower() in text:
                retrieved_concepts.append(self.getRealLabelFromConceptLabel(concept_label))
        return retrieved_concepts


    def get_themes(self):
        return [u"Forest Tenure", u"Indigenous & Community Land Rights", u"Land & Food Security",
                u"Land & Gender", u"Land & Investments", u"Land Conflicts",
                u"Land Stakeholders & Institutions", u"Land, Climate Change & Environment",
                u"Rangelands, Drylands & Pastoralism", u"Socio-Economic & Institutional Context", u"Urban Tenure", 
                u"Forest Landscape Restoration", u"Land in Post-Conflict Settings", u"Land & Corruption"]

lv = LandVoc()
