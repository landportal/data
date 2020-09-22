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
        self.languages =u""
        self.concepts = list()
        self.themes = list()
        self.geographical_focus = list()
        self.types = list()
        self.original_url = u""
        self.resource_url = u""
        self.image = u""
        self.license = u""
        self.copyright_details = u""
        self.potential_list = list()
        self.internal_id = u""        
        
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

    def set_internal_id(self, internal_id):
        self.internal_id = internal_id
        
    def get_internal_id(self):
        return self.internal_id

    def set_id(self, id_value):
        self.id = id_value

    def get_id(self):
        return self.id

    def set_number_pages(self, number_pages):
        self.number_pages = number_pages

    def get_number_pages(self):
        return self.number_pages

    def set_license(self, license_value):
        self.license = license_value

    def get_license(self):
        return self.license

    def set_copyright_details(self, copyright_details):
        self.copyright_details = copyright_details

    def get_copyright_details(self):
        return self.copyright_details

    def set_types(self, types):
        self.types = types

    def get_types(self):
        return self.types

    def set_metadata_language(self, metadata_language):
        self.metadata_language = metadata_language

    def get_metadata_language(self):
        return self.metadata_language

    def set_languages(self, langs):
        self.languages = langs

    def get_languages(self):
        return self.languages

    def set_data_provider(self, data_provider):
        self.data_provider = data_provider

    def get_data_provider(self):
        return self.data_provider

    def set_geographical_focus(self, countries, regions=None):
        if regions:
            self.geographical_focus = countries | regions
        else:
            self.geographical_focus = countries

    def get_geographical_focus(self):
        return self.geographical_focus

    def set_themes(self, collections):
        self.themes = collections

    def get_themes(self):
        return self.themes

    def set_concepts(self, concepts):
        self.concepts = concepts

    def get_concepts(self):
        return self.concepts

    def set_potential_list(self, potential_list):
        self.potential_list = potential_list

    def get_potential_list(self):
        return self.potential_list

    def _get_list_for_csv(self, l, c=u";"):
        """
         Args:
        l (list): The list.
        c (char): The separator char. ';' by default
        """
        return (c).join(l)#.decode("utf-8")

    def _get_string_csv(self, s):
        if s:
            return s.replace("\"", "\"\"") #duplicate_double_quotes
        else:
            return None

    def as_csv_line(self):
        xstr = lambda s: s or u""
#         print self.get_languages()
#         print self.get_types()
#         print self.get_potential_list()
        return  u";".join((u'"{}"'.format(xstr(item))) for item in [self.get_id(), self._get_string_csv(self.get_title()), self._get_string_csv(self.get_subtitle()),self._get_string_csv(self.get_description()),self._get_list_for_csv(self.get_authors(),"\n"),self._get_list_for_csv(sorted(self.get_corporate_authors())),self._get_list_for_csv(self.get_publishers()),self.get_data_provider(), self.get_date(), self._get_list_for_csv(sorted(self.get_languages())), self._get_list_for_csv(sorted(self.get_concepts())),self._get_list_for_csv(sorted(self.get_themes())), self._get_list_for_csv(sorted(self.get_geographical_focus())), self._get_list_for_csv(sorted(self.get_types())), self.get_original_url(), self.get_resource_url(), self.get_image(), self.get_license(), self.get_copyright_details(), self.get_number_pages(), self._get_list_for_csv(self.get_potential_list()), self.get_internal_id()])+'\n'

    @staticmethod
    def get_csv_header_line():
        headers = u"ID;Title;Subtitle;Abstract/Description;Authors;Corporate authors;Publishers;Data provider;Publication date;Languages;Related concepts;Themes;Geographical focus;Resource types;Link to the original website;Link to the publication;Thumbnail;License;Copyright details;Pages;Potential List;Internal ID;\n"
        return headers  
        
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

