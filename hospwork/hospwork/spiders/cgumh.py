import scrapy
from urllib.parse import urlparse,urlencode,parse_qsl

class CgumhSpider(scrapy.Spider):
    name = "cgumh"
    allowed_domains = ["www.cgmh.org.tw"]

    start_urls = [
        "https://www.cgmh.org.tw/tw/Systems/RecruitInfo/3?bulletinType=A&category=Z"
        
        ]

    def parse(self, response):
        url_query = dict(parse_qsl(urlparse(response.request.url).query))

        for job in response.xpath("//div[@id='list']/div/ul[@class='ul-reset']/li"):
            NAME_SELECTOR = 'div.fz-20.block ::text'
            RRP_SELECTOR = 'a ::attr(href)'
            job_title = job.css(NAME_SELECTOR).get()
            yield {
                'name': job_title,
                'job_link': response.urljoin(job.css(RRP_SELECTOR).extract_first()),
                'hosp_region': self.get_hosp_region(job_title),
            }

        next_page = response.xpath("//ul[@class='layout__pagination ul-reset']/li/a/@href").getall()[-1].replace("#list",'')

        if next_page and next_page != "javascript:void(0)":
            next_page_urlparse = urlparse(next_page)
            next_query = dict(parse_qsl(next_page_urlparse.query))
            url_query.update(next_query)
            yield scrapy.Request(
                response.urljoin(next_page_urlparse._replace(query=urlencode(url_query)).geturl()),
                callback=self.parse
            )
    
    def get_hosp_region(self,title):
        '''
        get hospital region for cgumh
        '''
        if '林口' in title:
            return '林口院區'
        elif '台北' in title:
            return '台北院區'
        elif '基隆' in title:
            return '基隆院區'
        elif '嘉義' in title:
            return '嘉義院區'
        elif '雲林' in title:
            return '雲林院區'
        elif '高雄' in title:
            return '高雄院區'
        elif '桃園' in title:
            return '桃園院區'
        elif '台中' in title:
            return '台中院區'
        elif '土城' in title:
            return '土城院區'
        elif '鳳山' in title:
            return '鳳山院區'
        elif '北院區' in title:
            return '北院區'
