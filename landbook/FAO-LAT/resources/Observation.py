#!/usr/bin/python
# -*- coding: UTF-8 -*-
import collections

class Observation(object):
    def __init__(self):        
        self.indicator = u""
        self.country = u""
        self.year = u""
        self.value = u""
        self.comment = u""        
        
    def set_indicator(self, indicator):
        self.indicator = indicator
    
    def get_indicator(self):
        return self.indicator
    
    def set_country(self, country):
        self.country = country
    
    def get_country(self):
        return self.country
    
    def set_year(self, year):
        self.year = year

    def get_year(self):
        return self.year

    def set_value(self, value):
        self.value = value
            
    def get_value(self):
        return self.value

    def set_comment(self, comment):
        self.comment = comment

    def get_comment(self):
        return self.comment
        

    def _get_list_for_csv(self, l, c=u";"):
        """
         Args:
        l (list): The list.
        c (char): The separator char. ';' by default
        """
        return (c).join(l)

    def _get_string_csv(self, s):
        if s:
            return s.replace(u"\"", u"\"\"") #duplicate_double_quotes
        else:
            return None

    def as_csv_line(self):
        xstr = lambda s: s or u""
        return  u";".join((u'"{}"'.format(xstr(item))) for item in [self._get_string_csv(self.get_indicator()), 
                                                                    self._get_string_csv(self.get_country()), 
                                                                    self._get_string_csv(self.get_year()),
                                                                    self._get_string_csv(self.get_value()),
                                                                    self._get_string_csv(self.get_comment())]) + u'\n'
        
    def __repr__(self):
        return self.indicator + " - " + self.country + " - " + self.year + " - " + self.value + " - " + self.comment

    def __str__(self):
        return unicode(self.indicator + self.country + self.year).encode('utf-8')

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
