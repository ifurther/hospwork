import scrapy


class CychSpider(scrapy.Spider):
    name = "cych"
    allowed_domains = ["www.cych.org.tw"]
    start_urls = ["https://www.cych.org.tw/hr2.aspx"]

    def parse(self, response):
        pass
