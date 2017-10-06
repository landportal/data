import scrapy

class BlogSpider(scrapy.Spider):
    LAST_PAGE = 10
    name = 'blogspider'
    start_urls = ["https://www.land-links.org/usaid-land-projects?fwp_paged=1"]
    page = 2
    def parse(self, response):
        for title in response.css('h2.entry-title'):
            #yield {'title': title.css('a ::text').extract_first()}
            yield {'link': title.css('a::attr("href")').extract_first()}

        print "------------------------------------------------"

        if self.page < (self.LAST_PAGE+1):
            next_page = "https://www.land-links.org/usaid-land-projects?fwp_paged="+str(self.page)
            self.page += 1
            yield response.follow(next_page, self.parse)