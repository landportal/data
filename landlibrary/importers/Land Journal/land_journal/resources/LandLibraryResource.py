import utils
import collections

class LandLibraryResource(object):
    def __init__(self):
        self.id = u""
        self.title = u""
        self.subtitle = None
        self.description = u""
        self.authors = list()
        self.corporate_authors = list()
        self.publishers = list()
        self.date = u""
        self.number_pages = None
        self.data_provider = u""
        self.language =u""
        self.concepts = list()
        self.themes = list()
        self.overarching_categories = list()
        self.geographical_focus = list()
        self.type = u""
        self.original_url = u""
        self.resource_url = u""
        self.image = u""
        self.license = u""
        self.copyright_details = u""
        
        
    def set_title(self, title):
        self.title = title
    
    def get_title(self):
        return self.title
    
    def set_subtitle(self, subtitle):
        self.subtitle = subtitle

    def get_subtitle(self):
        return self.subtitle

    def set_date(self, date):
        self.date = date
            
    def get_date(self):
        return self.date

    def set_description(self, description):
        self.description = description

    def get_description(self):
        return self.description
        
    def set_authors(self, authors):
        self.authors = authors

    def get_authors(self):
        return self.authors
        
    def set_corporate_authors(self, corporate_authors):
        self.corporate_authors = corporate_authors
        
    def get_corporate_authors(self):
        return self.corporate_authors

    def set_publishers(self, publishers):
        self.publishers = publishers

    def get_publishers(self):
        return self.publishers

    def set_image(self, image):
        self.image = image
        
    def get_image(self):
        return self.image

    def set_resource_url(self, resource_url):
        self.resource_url = resource_url
        
    def get_resource_url(self):
        return self.resource_url

    def set_original_url(self, original_url):
        self.original_url = original_url

    def get_original_url(self):
        return self.original_url

    def set_id(self, id):
        self.id = id

    def get_id(self):
        return self.id

    def set_number_pages(self, number_pages):
        self.number_pages = number_pages

    def get_number_pages(self):
        return self.number_pages

    def set_license(self, license):
        self.license = license

    def get_license(self):
        return self.license

    def set_copyright_details(self, copyright_details):
        self.copyright_details = copyright_details

    def get_copyright_details(self):
        return self.copyright_details

    def set_type(self, type):
        self.type = type

    def get_type(self):
        return self.type

    def set_metadata_language(self, metadata_language):
        self.metadata_language = metadata_language

    def get_metadata_language(self):
        return self.metadata_language

    def set_language(self, lang):
        self.language = lang

    def get_language(self):
        return self.language

    def set_data_provider(self, data_provider):
        self.data_provider = data_provider

    def get_data_provider(self):
        return self.data_provider

    def set_geographical_focus(self, countries, regions):
        self.geographical_focus = countries | regions

    def get_geographical_focus(self):
        return self.geographical_focus
    
    def set_overarching_categories(self, overarching_categories):
        self.overarching_categories = overarching_categories

    def get_overarching_categories(self):
        return self.overarching_categories

    def set_themes(self, themes):
        self.themes = themes

    def get_themes(self):
        return self.themes

    def set_concepts(self, concepts):
        self.concepts = concepts

    def get_concepts(self):
        return self.concepts

    def _get_list_for_csv(self, l, c=u";"):
        """
         Args:
        l (list): The list.
        c (char): The separator char. ';' by default
        """
        return (c).join(l).decode("utf-8")

    def _get_string_csv(self, s):
        if s:
            return s.replace("\"", "\"\"") #duplicate_double_quotes
        else:
            return None

    def as_csv_line(self):
        xstr = lambda s: s or u""
        return  u";".join((u'"{}"'.format(xstr(item))) for item in [self.get_id(), self._get_string_csv(self.get_title()), self._get_string_csv(self.get_subtitle()),self._get_string_csv(self.get_description()),self._get_list_for_csv(self.get_authors(),"\n"),self._get_list_for_csv(self.get_corporate_authors()),self._get_list_for_csv(self.get_publishers()),self.get_data_provider(), self.get_date(), self.get_language(), self._get_list_for_csv(self.get_concepts()),self._get_list_for_csv(self.get_themes()),self._get_list_for_csv(self.get_overarching_categories()), self._get_list_for_csv(self.get_geographical_focus()),self.get_type(), self.get_original_url(), self.get_resource_url(),self.get_image(), self.get_license(), self.get_copyright_details(), self.get_number_pages()])+'\n'
        
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
