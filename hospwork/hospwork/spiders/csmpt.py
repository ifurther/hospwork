import scrapy
import re

from hospwork.tool.job import findjoboriginzation,findjobtype,clean_unused_str

from hospwork.items import HospworkItem


class CsmptSpider(scrapy.Spider):
    name = "csmpt"
    allowed_domains = ["www.csmpt.org.tw"]
    start_urls = ["http://www.csmpt.org.tw/news/index.php?type=4"]

    def parse(self, response):
        item = HospworkItem()
        for job in response.xpath("//article[@id='mainContent']/ul/li"):
            NAME_SELECTOR = 'a ::text'
            RRP_SELECTOR = 'a ::attr(href)'
            job_title = job.css(NAME_SELECTOR).get()
            title_pattern = r"(.*院)"
            title_match = re.search(title_pattern, job_title)
            if title_match:
                job_title_new = title_match.group(1)
                item['hosp_name'] = job_title_new
                job_name = clean_unused_str(job_title.replace(job_title_new,''),job_title_new)
                job_originazition = findjoboriginzation(job_name,job_title_new)
                if job_originazition:
                    job_name_new = job_name.replace(job_originazition,'')
                    if job_name_new:
                        item['job_name'] = job_name_new
                        item['job_originzation'] = job_originazition
                    else:
                        item['job_name'] = job_name
                else:
                    item['job_name'] = job_name
            else:
                item['hosp_name'] = '醫學物理學會'
                item['job_name'] = job_title

            job_link = response.urljoin(job.css(RRP_SELECTOR).extract_first())
            #hosp_region = self.get_hosp_region(job_title)
            item['data_source'] = 'csmpt'
            item['job_link'] = job_link
            #item['hosp_region'] = hosp_region

            yield item


