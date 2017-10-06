import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join
import utils

class Project(scrapy.Item):
    title = scrapy.Field(output_processor=TakeFirst())
    description = scrapy.Field(output_processor=TakeFirst())
    start_date = scrapy.Field(output_processor=TakeFirst())
    end_date = scrapy.Field(output_processor=TakeFirst())
    funding = scrapy.Field(output_processor=TakeFirst())
    countries = scrapy.Field(output_processor=Join(separator=u";"))
    project_url = scrapy.Field(output_processor=TakeFirst())
    donor = scrapy.Field(output_processor=TakeFirst())
    related_overarching_categories = scrapy.Field(output_processor=Join(separator=u";"))
    related_themes = scrapy.Field(output_processor=Join(separator=u";"))
    related_concepts = scrapy.Field(output_processor=Join(separator=u";"))
    
    
class USAIDSpider(scrapy.Spider):
    LAST_PAGE = 10
    name = 'USAIDSpider'
    start_urls = ["https://www.land-links.org/project/property-rights-and-artisanal-diamond-development-ii-cote-divoire/",
    "https://www.land-links.org/project/addressing-biodiversity-social-conflict-in-latin-america/",
    "https://www.land-links.org/project/agriculture-rural-development-support-ukraine/",
    "https://www.land-links.org/project/agroinvest-ukraine/",
    "https://www.land-links.org/project/approach-to-participatory-management-of-natural-resources-central-asia/",
    "https://www.land-links.org/project/arziki-project-niger/",
    "https://www.land-links.org/project/biodiversity-conservation-of-public-lands-in-the-brazilian-amazon/",
    "https://www.land-links.org/project/bolivia-land-titling-program/",
    "https://www.land-links.org/project/building-bridges-to-peace-uganda/",
    "https://www.land-links.org/project/burundi-policy-reform-program/",
    "https://www.land-links.org/project/capacity-building-for-responsible-minerals-trade-democratic-republic-of-congo/",
    "https://www.land-links.org/project/caribbean-open-trade-support-dominica/",
    "https://www.land-links.org/project/conflict-management-and-mitigation-in-rwanda/",
    "https://www.land-links.org/project/cooperative-agreement-with-the-international-real-property-foundation/",
    "https://www.land-links.org/project/economic-growth-hubs-infrastructure-and-competitiveness-philippines/",
    "https://www.land-links.org/project/economic-prosperity-initiative-georgia/",
    "https://www.land-links.org/project/ecuador-sustainable-forests-and-coasts/",
    "https://www.land-links.org/project/egypt-financial-services-project/",
    "https://www.land-links.org/project/enhancing-customary-justice-systems-in-the-mau-forest-kenya/",
    "https://www.land-links.org/project/ethiopia-land-administration-program/",
    "https://www.land-links.org/project/ethiopia-strengthening-land-tenure-and-administration-program/",
    "https://www.land-links.org/project/ethno-environment-corridors-in-the-brazilian-amazon/",
    "https://www.land-links.org/project/evaluation-research-and-communication-global/",
    "https://www.land-links.org/project/feed-the-future-tanzania-land-tenure-assistance-activity/",
    "https://www.land-links.org/project/food-and-enterprise-development-liberia/",
    "https://www.land-links.org/project/food-security-research-program-zambia/",
    "https://www.land-links.org/project/ghana-commercial-agriculture-project/",
    "https://www.land-links.org/project/governance-in-environment-frontiers-brazil/",
    "https://www.land-links.org/project/indonesia-marine-and-climate-support/",
    "https://www.land-links.org/project/integrated-development-and-conservation-in-the-bolivian-amazon-project/",
    "https://www.land-links.org/project/kenya-transition-initiative/",
    "https://www.land-links.org/project/knowledge-management-and-technical-support-services-global/",
    "https://www.land-links.org/project/kosovo-property-rights-program/",
    "https://www.land-links.org/project/kyrgyzstan-land-policy-reform-project/",
    "https://www.land-links.org/project/land-access-for-women-vietnam/",
    "https://www.land-links.org/project/land-administration-and-protection-of-property-sri-lanka/",
    "https://www.land-links.org/project/land-administration-to-nurture-development-ethiopia/",
    "https://www.land-links.org/project/land-and-rural-development-project-colombia/",
    "https://www.land-links.org/project/land-conflict-resolution-project-liberia/",
    "https://www.land-links.org/project/land-governance-support-activity/",
    "https://www.land-links.org/project/land-policy-and-institutional-support-liberia/",
    "https://www.land-links.org/project/land-reform-and-market-development-project-central-asia/",
    "https://www.land-links.org/project/land-reform-in-afghanistan/",
    "https://www.land-links.org/project/land-reform-project-in-tajikistan/",
    "https://www.land-links.org/project/land-rights-and-community-forest-program-liberia/",
    "https://www.land-links.org/project/land-titling-and-economic-restructuring-in-afghanistan/",
    "https://www.land-links.org/project/land-potential-knowledge-system/",
    "https://www.land-links.org/project/legislative-strengthening-and-capacity-building-rwanda/",
    "https://www.land-links.org/project/local-investment-in-national-competitiveness-ukraine/",
    "https://www.land-links.org/project/mas-inversion-para-el-desarrollo-alternativo-sostenible-colombia/",
    "https://www.land-links.org/project/mejora-de-los-procedimientos-catastrales-municipales-paraguay/",
    "https://www.land-links.org/project/mitigating-interethnic-land-conflict-in-colombia/",
    "https://www.land-links.org/project/mobile-application-to-secure-tenure-tanzania/",
    "https://www.land-links.org/project/mobile-applications-secure-tenure-burkina-faso/",
    "https://www.land-links.org/project/national-land-observatory-pilot-burkina-faso/",
    "https://www.land-links.org/project/ongoing-legal-and-regulatory-assistance-angola/",
    "https://www.land-links.org/project/people-rules-and-organizations-supporting-the-protection-of-ecosystem-resources-liberia/",
    "https://www.land-links.org/project/pilot-responsible-land-based-investments/",
    "https://www.land-links.org/project/programme-de-bonne-gouvernance-democractic-republic-of-congo/",
    "https://www.land-links.org/project/promara-kenya/",
    "https://www.land-links.org/project/promoting-peace-and-reconciliation-in-violence-affected-communities-in-colombia/",
    "https://www.land-links.org/project/promoting-peace-through-land-dispute-management-rwanda/",
    "https://www.land-links.org/project/proparque-honduras/",
    "https://www.land-links.org/project/property-rights-artisanal-diamond-development-ii-central-african-republic/",
    "https://www.land-links.org/project/property-rights-and-artisanal-diamond-development-ii-cote-divoire/",
    "https://www.land-links.org/project/property-rights-and-artisanal-diamond-development-ii-guinea/",
    "https://www.land-links.org/project/property-rights-and-artisanal-diamond-development-central-african-republic/",
    "https://www.land-links.org/project/property-rights-and-artisanal-diamond-development-guinea/",
    "https://www.land-links.org/project/property-rights-and-artisanal-diamond-development-liberia/",
    "https://www.land-links.org/project/property-rights-and-natural-resource-management-global/",
    "https://www.land-links.org/project/property-rights-and-resource-governance-global/",
    "https://www.land-links.org/project/redd-readiness-in-brazil/",
    "https://www.land-links.org/project/resilience-and-economic-growth-in-the-sahel-enhanced-resilience/",
    "https://www.land-links.org/project/rift-valley-local-empowerment-for-peace-kenya/",
    "https://www.land-links.org/project/rwanda-hiv-aids-policy-reform-initiative/",
    "https://www.land-links.org/project/rwanda-land-conflict-transformation-project/",
    "https://www.land-links.org/project/rwanda-land-law-project/",
    "https://www.land-links.org/project/rwanda-land-project/",
    "https://www.land-links.org/project/securing-rights-to-land-and-natural-resources-for-biodiversity-and-livelihoods-kenya/",
    "https://www.land-links.org/project/stability-peace-reconciliation-in-northern-uganda/",
    "https://www.land-links.org/project/strengthening-environmental-and-agricultural-research-zambia/",
    "https://www.land-links.org/project/strengthening-property-rights-in-timor-leste/",
    "https://www.land-links.org/project/strengthening-urban-resilience-growth-equity-philippines/",
    "https://www.land-links.org/project/sudan-property-rights-program/",
    "https://www.land-links.org/project/sudan-rural-land-and-governance-project/",
    "https://www.land-links.org/project/support-program-for-economic-and-enterprise-development-mozambique/",
    "https://www.land-links.org/project/supporting-access-to-justice-fostering-peace-and-equity-uganda/",
    "https://www.land-links.org/project/supporting-the-justice-and-security-sector-through-property-rights-in-libya/",
    "https://www.land-links.org/project/sustainable-and-thriving-environments-for-west-african-regional-development-sierra-leone/",
    "https://www.land-links.org/project/tajikistan-land-reform-and-farm-restructuring-project/",
    "https://www.land-links.org/project/tajikistan-land-reform-and-farm-restructuring-project-2/",
    "https://www.land-links.org/project/tanzania-policy-project/",
    "https://www.land-links.org/project/tenure-global-climate-change-burma/",
    "https://www.land-links.org/project/tenure-and-global-climate-change-global/",
    "https://www.land-links.org/project/tenure-global-climate-change-vietnam/",
    "https://www.land-links.org/project/tenure-global-climate-change-zambia/",
    "https://www.land-links.org/project/tierras-land-conflict-resolution-in-el-quiche-guatemala/",
    "https://www.land-links.org/project/voices-in-peace-kenya/"]

    custom_settings = {
      # specifies exported fields and order
      'FEED_EXPORT_FIELDS': ["id", "title", "description", "acronym", "start_date", "end_date", "funding", "project_url", "countries", "donor", "related_overarching_categories", "related_themes", "related_concepts"],
    }
    
    
    def parse(self, response):
        article = response.css('article.hentry')
        l = ItemLoader(item=Project(), response=response)
        title = article.css('h1.entry-title::text').extract_first()
        l.add_value('title', title)

        duration = article.css('div.project-duration::text').extract_first().replace("Project Duration: ", "")
        start_date = duration[:4]
        end_date = duration[8:]
        l.add_value('start_date', start_date)
        l.add_value('end_date', end_date)

        funding = article.css('div.entry-approximate-funding::text').extract_first()
        if funding:
            funding = funding.replace("Approximate", "").replace("Funding:", "").strip().replace(",","").replace("$", "USD ")
            l.add_value('funding', funding)

        description = article.css('div.entry-content').extract_first().replace("<div class=\"entry-content\">\n                        ", "").replace("\n                    </div>","")
        l.add_value("description", description)

        countries = []
        countries_init = article.css('div.entry-related-countries a::text').extract()
        
        countries += [utils.getISO3166_1code(c) for c in countries_init]
        if not countries_init:
            countries += utils.getPlaceET_fromText_GeoText(title)
            countries += utils.getPlaceET_fromText_NLTK(title)
        
        if title.endswith(": Global"):
            countries.append("001") #Global
#         if not countries:
#             print "-----------------------------------------------------------"
#             print title
#             print response.url
        l.add_value("countries", list(set(countries)))


        lp_oacs = []
        lp_themes = []
        lp_concepts = []
        usaid_themes_init = article.css('div.entry-related-issues a::text').extract()
        for usaid_theme_init in usaid_themes_init:
            possible_oac = utils.getLPOAC(usaid_theme_init)
            if possible_oac:
                lp_oacs.append(possible_oac)

            possible_theme = utils.getLPTheme(usaid_theme_init)
            if possible_theme:
                lp_themes.append(possible_theme)

            possible_concepts = utils.getLPConcepts(usaid_theme_init)
            if possible_concepts:
                lp_concepts+=possible_concepts


        l.add_value("related_overarching_categories", list(set(lp_oacs)))
        l.add_value("related_themes", list(set(lp_themes)))
        l.add_value("related_concepts", list(set(lp_concepts)))

        l.add_value("project_url", response.url)

        l.add_value("donor", "USAID")
        #return list()
        return l.load_item()
        