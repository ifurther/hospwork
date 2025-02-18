import scrapy
from urllib.parse import urlparse,urlencode,parse_qsl

from hospwork.items import HospworkItem

from hospwork.tool.web import get_base_web_data,get_work_page
from hospwork.tool.job import findjoboriginzation,findjobtype,clean_unused_str
from hospwork.tool.time import clean_date

class VghtcSpider(scrapy.Spider):
    name = "vghtc"
    allowed_domains = ["www.vghtc.gov.tw"]
    start_urls = ["https://www.vghtc.gov.tw/Module/RecruitMent?WebMenuID=9d005e46-411b-46fc-b438-e0bd561eba78&page=2"]

    def parse(self, response):
        item = HospworkItem()

        url_query = dict(parse_qsl(urlparse(response.request.url).query))

        next_page = response.xpath("//div[@id='content']/div//div[@class='pager']/a/@href").getall()[-1].replace("#list",'')
        if next_page and next_page != "javascript:void(0)":
            next_page_urlparse = urlparse(next_page)
            next_query = dict(parse_qsl(next_page_urlparse.query))
            url_query.update(next_query)
            yield scrapy.Request(
                response.urljoin(next_page_urlparse._replace(query=urlencode(url_query)).geturl()),
                callback=self.parse
            )   
