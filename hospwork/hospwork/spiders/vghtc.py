import scrapy


class VghtcSpider(scrapy.Spider):
    name = "vghtc"
    allowed_domains = ["www.vghtc.gov.tw"]
    start_urls = ["https://www.vghtc.gov.tw"]

    def parse(self, response):
        pass
