import scrapy


class CgumhSpider(scrapy.Spider):
    name = "cgumh"
    allowed_domains = ["www.cgmh.org.tw"]
    start_urls = ["https://www.cgmh.org.tw/tw/Systems/RecruitInfo/3?bulletinType=A&category=Z"]

    def start_requests(self, start_urls):
        response = scrapy.Request(url=start_urls[0])
        urls = response.css("ul.layout__pagination a::attr(href)").getall()[1:-1]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        pass
