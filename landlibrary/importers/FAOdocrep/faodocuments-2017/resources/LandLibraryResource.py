class LandLibraryResource(object):
    def set_title(self, title):
        self.title = title

    def set_subtitle(self, subtitle_longtitle=None, subtitle_originaltitle=None):
        if subtitle_longtitle is not None:
            self.subtitle = subtitle_longtitle
        else:
            self.subtitle = subtitle_originaltitle

    def set_date(self, dateOfText=None, dateOfOriginalText=None):
        if dateOfText is not None:
            self.date = dateOfText
        else:
            self.date = dateOfOriginalText
            
    def set_description(self, description):
        self.description = description

    def set_author(self, author):
        self.author = author

    def generate_author(self, possible_authors):
        author = set()
        for possible in possible_authors:
            if possible and unicode(possible).lower() !="fao":
                author.add(possible)       
        return "\n".join(unicode(e) for e in author)

    def generate_organizations(self, possible_orgs):
        orgs = set()
        orgs.add(u"Food and Agriculture Organization of the United Nations (FAO)")
        for possible in possible_orgs:
            if possible in ["Regional Office for Africa", "Regional Office for the Near East", "Regional Office for Europe", "Regional Office for Latin America and the Caribbean", "Regional Office for Asia and the Pacific"]:
                orgs.add(possible)
        return orgs
    
    def set_corporate_authors(self, corporate_authors):
        self.corporate_authors = corporate_authors

    def set_publishers(self, publishers):
        self.publishers = publishers

    def set_resource_url(self, resource_url):
        self.resource_url = resource_url

    def set_original_url(self, original_url):
        self.original_url = original_url

    def set_id(self, id):
        self.id = id

    def set_number_pages(self, number_pages):
        self.number_pages = number_pages

    def set_license(self, license):
        self.license = license

    def set_copyright_details(self, copyright_details):
        self.copyright_details = copyright_details

    def set_type(self, type):
        self.type = {
            'Article' : 'Journal Articles & Books' ,
            'Book' : 'Journal Articles & Books' ,
            'Bulletin' : 'Policy Papers & Briefs' ,
            'Document' : 'Reports & Research',
            'Meeting' : 'Reports & Research', 
            'Mixed Material' : 'Policy Papers & Briefs',
            'Periodical' : 'Journal Articles & Books',
            'Project' : 'Policy Papers & Briefs',
            'Reports' : 'Reports & Research', 
            'Serials' : 'Journal Articles & Books',
            None: 'Other',
        }[type]

    def set_metadata_language(self, metadata_language):
        self.metadata_language = metadata_language


    def set_languages(self, languages):
        self.languages = languages

    def set_data_provider(self, data_provider):
        self.data_provider = data_provider

    def set_geographical_focus(self, countries=None, regions=None):
        self.geographical_focus = countries | regions

    def set_overarching_categories(self, overarching_categories):
        self.overarching_categories = overarching_categories

    def set_themes(self, themes):
        self.themes = themes
        
    def set_concepts(self, potential_concepts, landvoc):
        direct_mapping = landvoc.get_concepts_direct(potential_concepts)
        related_mapping = landvoc.get_concepts_faolex_related(potential_concepts)
        concepts_harvest_enhancement = landvoc.get_concepts_harvest_enhancement(potential_concepts)
        self.concepts = set(direct_mapping+related_mapping+concepts_harvest_enhancement)

    def _get_list_for_csv(self, l):
        return u";".join(l)
    
    def _get_string_csv(self, s):
        return s.replace("\"", "\"\"") #duplicate_double_quotes
        
    def set_related_website(self, related_website):
        self.related_website = related_website

    def set_serialImprint(self, serialImprint):
        self.serialImprint = serialImprint

    def set_thumbnail(self, thumbnail):
        self.thumbnail = thumbnail

    def as_csv_line(self):
        xstr = lambda s: s or u""
        return ";".join((u'"{}"'.format(xstr(item))) for item in [self.id, self._get_string_csv(self.title),self._get_string_csv(self.description),self.author,self._get_list_for_csv(self.corporate_authors),self._get_list_for_csv(self.publishers),self.data_provider, self.date, self._get_list_for_csv(self.languages), self._get_list_for_csv(self.concepts),self._get_list_for_csv(self.themes),self._get_list_for_csv(self.overarching_categories), self._get_list_for_csv(self.geographical_focus),self.type, self.original_url, self.resource_url,self.thumbnail, self.license, self.copyright_details, self.number_pages])+'\n'
        
    def __repr__(self):
        return self.id

    def __str__(self):
        return unicode(self.id).encode('utf-8')

