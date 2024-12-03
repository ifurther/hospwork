import scrapy


class CsmptSpider(scrapy.Spider):
    name = "csmpt"
    allowed_domains = ["www.csmpt.org.tw"]
    start_urls = ["https://www.csmpt.org.tw/news/index.php?type=4"]

    def parse(self, response):
        pass
