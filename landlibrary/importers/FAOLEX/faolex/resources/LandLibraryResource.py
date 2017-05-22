import utils
import collections

class LandLibraryResource(object):
    def set_title(self, title):
        self.title = title

    def set_subtitle(self, subtitle_longtitle, subtitle_originaltitle):
        if subtitle_longtitle is not None:
            self.subtitle = subtitle_longtitle
        else:
            self.subtitle = subtitle_originaltitle

    def set_date(self, dateOfText, dateOfOriginalText):
        if dateOfText is not None:
            self.date = dateOfText
        else:
            self.date = dateOfOriginalText
            
    def set_description(self, description):
        self.description = description

    def set_implementedBy(self, text):
        self.implementedBy = text

    def set_implement(self, text):
        self.implement = text

    def set_amendedBy(self, text):
        self.amendedBy = text

    def set_amends(self, text):
        self.amends = text

    def set_repealedBy(self, text):
        self.repealedBy = text

    def set_repeals(self, text):
        self.repeals = text
        
    def set_full_description(self):
        self.full_description = self.description
        self.full_description += "\n"
        self.full_description += self.implementedBy
        self.full_description += self.implement
        self.full_description += self.amendedBy
        self.full_description += self.amends
        self.full_description += self.repealedBy
        self.full_description += self.repeals

    def set_author(self, author):
        self.author = author
    
    def set_publisher(self, publisher):
        self.publisher = publisher

    def set_resource_url(self, linksToFullText):
        self.resource_url = "http://extwprlegs1.fao.org/docs/pdf/"+linksToFullText

    def set_original_url(self, faolexId):
        self.original_url = "http://www.fao.org/faolex/results/details/en/c/"+faolexId

    def set_id(self, id):
        self.id = id

    def set_number_pages(self, number_pages):
        self.number_pages = number_pages

    def set_license(self, license):
        self.license = license

    def set_copyright_details(self, copyright_details):
        self.copyright_details = copyright_details

    def set_type(self, type):
        self.type =  {
            'C': "Constitution",
            'P': "National Policies",
            'L': "Legislation",
            'R': "Regulations",
            'A': "International Conventions or Treaties",
            'M': "Other"
        }[type]

    def set_metadata_language(self, metadata_language):
        self.metadata_language = metadata_language


    def set_language(self, gsaentity_google_language, documentLanguage_en):
        if len(documentLanguage_en) == 1:
            language = documentLanguage_en[0]
        elif (gsaentity_google_language in documentLanguage_en):
            language = gsaentity_google_language
        else:
            language = gsaentity_google_language #some corner cases
        self.language = utils.getISO639_1code(language)

    def set_data_provider(self, data_provider):
        self.data_provider = data_provider

    def set_geographical_focus(self, countries, regions):
        regions_cleaned = list(flatten(filter(None, [utils.getUNM49code(region) for region in regions])))
        countries_cleaned = [x for x in countries if x != "EUR"]
        self.geographical_focus = countries_cleaned+regions_cleaned

    def set_overarching_categories(self, overarching_categories):
        self.overarching_categories = overarching_categories

    def set_concepts(self, potential_concepts, landvoc):
        direct_mapping = landvoc.get_concepts_direct(potential_concepts)
        related_mapping = landvoc.get_concepts_faolex_related(potential_concepts)
        self.concepts = set(direct_mapping+related_mapping)

    def _get_list_for_csv(self, list):
        return u";".join(list)
    
    def _get_string_csv(self, str):
        return str.replace("\"", "\"\"") #duplicate_double_quotes
        
    def set_related_website(self, related_website):
        self.related_website = related_website

    def set_serialImprint(self, serialImprint):
        self.serialImprint = serialImprint

    def as_csv_line(self):
        xstr = lambda s: s or u""
        return ";".join((u'"{}"'.format(xstr(item))) for item in [self.id, self._get_string_csv(self.title),self._get_string_csv(self.full_description),self.author,"",self.publisher,self.data_provider, self.date, self.language, self._get_list_for_csv(self.concepts),"",self._get_list_for_csv(self.overarching_categories), self._get_list_for_csv(self.geographical_focus),self.type, self.original_url, self.resource_url,"", self.license, self.copyright_details, self.number_pages])+'\n'
        
    def __repr__(self):
        return self.id

    def __str__(self):
        return unicode(self.id).encode('utf-8')

def flatten(l):
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, basestring):
            for sub in flatten(el):
                yield sub
        else:
            yield el
