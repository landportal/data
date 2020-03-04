#!/usr/bin/python
# -*- coding: UTF-8 -*-
import utils
import collections

class Project(object):
    def __init__(self):

        self.title = u""
        self.acronym = u""
        self.description = u""
        self.image = u""

        self.geographical_focus = list()
        self.themes = list()
        self.concepts = list()

        self.id = u""
        self.start_date = u""
        self.end_date = u""

        self.budget_currency = u""
        self.budget_value = u""
        self.budget_value_USD = u""

        self.website = u""
        self.contact_info = u""
        self.staff = list()

        
        self.donors = list()
        self.implementers = list()

        self.data_provider = u""
        
        
    def get_id(self):
        return self.id

    def set_title(self, title):
        self.title = title
    
    def get_title(self):
        return self.title
    
    def set_acronym(self, acronym):
        self.acronym = acronym

    def get_acronym(self):
        return self.acronym

    def set_description(self, description):
        self.description = description

    def get_description(self):
        return self.description
        
    def set_image(self, image):
        self.image = image
        
    def get_image(self):
        return self.image

    def set_geographical_focus(self, codes):
        self.geographical_focus = codes

    def get_geographical_focus(self):
        return self.geographical_focus

    def set_themes(self, project_themes):
        self.themes = project_themes

    def get_themes(self):
        return self.themes

    def set_concepts(self, concepts):
        self.concepts = concepts

    def get_concepts(self):
        return self.concepts

    def set_id(self, i_id):
        self.id = i_id

    def set_start_date(self, start_date):
        self.start_date = start_date
            
    def get_start_date(self):
        return self.start_date

    def set_end_date(self, end_date):
        self.end_date = end_date
            
    def get_end_date(self):
        return self.end_date

    def set_budget_currency(self, budget_currency):
        self.budget_currency = budget_currency

    def get_budget_currency(self):
        return self.budget_currency

    def set_budget_value(self, budget_value):
        self.budget_value = budget_value

    def get_budget_value(self):
        return self.budget_value

    def set_budget_value_USD(self, budget_value_USD):
        self.budget_value_USD = budget_value_USD

    def get_budget_value_USD(self):
        return self.budget_value_USD

    def set_website(self, website):
        self.website = website
        
    def get_website(self):
        return self.website

    def set_contact_info(self, contact_info):
        self.contact_info = contact_info

    def get_contact_info(self):
        return self.contact_info
    
    def set_staff(self, staff):
        self.staff = staff

    def get_staff(self):
        return self.staff
    
    def set_donors(self, donors):
        self.donors = donors

    def get_donors(self):
        return self.donors    

    def set_implementers(self, implementers):
        self.implementers = implementers

    def get_implementers(self):
        return self.implementers
        
    def set_data_provider(self, data_provider):
        self.data_provider = data_provider

    def get_data_provider(self):
        return self.data_provider

    
    def _get_list_for_csv(self, l, c=u";"):
        """
         Args:
        l (list): The list.
        c (char): The separator char. ';' by default
        """
        return (c).join(l)

    def _get_string_csv(self, s):
        if s:
            return s.replace("\"", "\"\"") #duplicate_double_quotes
        else:
            return None

    def as_csv_line(self):
        xstr = lambda s: s or u""
        return  u";".join((u'"{}"'.format(xstr(item))) for item in [self.get_id(), 
                                                                    self._get_string_csv(self.get_title()),
                                                                    self._get_string_csv(self.get_description()),
                                                                    self._get_string_csv(self.get_acronym()),
                                                                    self.get_image(), 
                                                                    self._get_list_for_csv(self.get_geographical_focus()),
                                                                    self._get_list_for_csv(self.get_concepts()),
                                                                    self._get_list_for_csv(self.get_themes()),
                                                                    self.get_start_date(), 
                                                                    self.get_end_date(), 
                                                                    self.get_budget_currency(), 
                                                                    self.get_budget_value(), 
                                                                    self.get_budget_value_USD(), 
                                                                    self.get_website(), 
                                                                    self.get_contact_info(), 
                                                                    self._get_list_for_csv(self.get_staff()),
                                                                    self._get_list_for_csv(self.get_donors()),
                                                                    self._get_list_for_csv(self.get_implementers()),
                                                                    self.get_data_provider()]) + u'\n'

    @staticmethod
    def get_csv_headers():
        return u"ID;Title;Description;Acronym;Image;Geographical focus;Related concepts;Themes;Start date;End date;Budget Currency;Budget value;Budget value USD;website;Contact info;Staff;Donors;Implementers;Data provider\n"

    def __repr__(self):
        return self.id

    def __str__(self):
        return unicode(self.id).encode('utf-8')

    def __eq__(self, other): 
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return (not self.__eq__(other))

    def __hash__(self):
        return hash(self.__repr__())
    
def flatten(l):
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, basestring):
            for sub in flatten(el):
                yield sub
        else:
            yield el
