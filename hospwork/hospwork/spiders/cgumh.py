import scrapy,re
from urllib.parse import urlparse,urlencode,parse_qsl

from hospwork.items import HospworkItem
from hospwork.tool.web import get_base_web_data,get_work_page
from hospwork.tool.job import findjoboriginzation,findjobtype,clean_unused_str
from hospwork.tool.time import clean_date

class CgumhSpider(scrapy.Spider):
    name = "cgumh"
    allowed_domains = ["www.cgmh.org.tw"]

    start_urls = [
        "https://www.cgmh.org.tw/tw/Systems/RecruitInfo/3?bulletinType=A&category=Z"
        ]

    def parse(self, response):
        # Load scarpy item for hospwork
        item = HospworkItem()
        # get url_query for next page
        url_query = dict(parse_qsl(urlparse(response.request.url).query))

        for job in response.xpath("//div[@id='list']/div/ul[@class='ul-reset']/li"):
            JOB_SELECTOR = 'a ::attr(href)'
            job_link = response.urljoin(job.css(JOB_SELECTOR).extract_first())
            item['data_source'] = 'cgmh'
            item['hosp_name'] = '長庚醫院'
            #item['job_name'] = job_title
            #item['job_link'] = job_link
            #item['hosp_region'] = hosp_region

            yield scrapy.Request(
                job_link, self.parse_details, meta={"item": item}
            )

        #next_page = response.xpath("//ul[@class='layout__pagination ul-reset']/li/a/@href").getall()[-1].replace("#list",'')

        if next_page and next_page != "javascript:void(0)":
            next_page_urlparse = urlparse(next_page)
            next_query = dict(parse_qsl(next_page_urlparse.query))
            url_query.update(next_query)
            yield scrapy.Request(
                response.urljoin(next_page_urlparse._replace(query=urlencode(url_query)).geturl()),
                callback=self.parse
            )

    def parse_details(self, response):
        item = response.meta["item"]
        title = clean_unused_str(response.xpath("//head/title/text()").get(),item['hosp_name']).replace('|長庚醫療財團法人全球資訊網','')
        item['hosp_region'] = self.get_hosp_region(title)
        title = title.replace('院','').replace("紀念",'').replace("新北市立","").replace("高雄市立鳳山","").replace("長庚","")
        title = title.replace(item['hosp_region'][:-2],'')
        title_ = title
        title_old = title

        work_detail_web = clean_unused_str(''.join(response.css("article.fz-17::text").getall()), title)

        dead_line = self.get_work_dead_line( work_detail_web ,title)

        if '工作地點' in work_detail_web:
            originzation = findjoboriginzation(work_detail_web.rsplit('工作地點')[1], item['hosp_name'] )
        elif (originzation := findjoboriginzation((title_ if (title_ :=  title_old) else title), item['hosp_name'] )) and originzation != title:
            originzation = originzation
            title = title.replace(originzation,'')
        elif (originzation := findjoboriginzation(work_detail_web, item['hosp_name']) ) and type(originzation) == str:
            originzation = originzation
            title = title.replace(originzation,'')
        else:
            print("Error find originaztion",response.url)
            originzation = ''

        if (new_title :=  findjobtype(title, self.name)) and new_title != title:
            title = new_title.replace('醫院','').replace("紀念",'').replace("新北市立","").replace("高雄市立鳳山","")

        item['job_name'] = title
        item['job_link'] = response.request.url
        item['job_deadline'] = dead_line
        item['job_originzation'] = originzation

        yield item

   
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

    def get_work_dead_line(self, work_detail_web, title):
        work_detail_web = work_detail_web.replace('(日) ','').replace('(日)','').replace('（含）','').replace('即日起，至','即日起至')
        if '報名期限展延至' in work_detail_web:
            return re.findall("\d+年\d+月\d+日",work_detail_web.rsplit('報名期限展延至')[1].split("止")[0].replace(' ',''))[0]
        elif '額滿' in work_detail_web:
            return '額滿為止'
        elif '招募合適人選為止' in work_detail_web or '招募到合適⼈選為' in work_detail_web or '徵到為止' in work_detail_web:
            return '招募合適人選為止'
        elif '隨到隨審' in work_detail_web:
            return '隨到隨審'
        elif '即日起至招聘完成' in work_detail_web:
            return '即日起至招聘完成'
        elif '自即日起' in work_detail_web or '即日起~' in work_detail_web:
            return '自即日起'
        elif '即日起至' in work_detail_web:
            if (new_work_detail_web := work_detail_web.rsplit('即日起至')[1]) and "止" in new_work_detail_web:
                if '截止' in new_work_detail_web:
                    return clean_date(new_work_detail_web.split("截止")[0].replace(' ',''), self.name)
                else:
                    return clean_date(new_work_detail_web.split("止")[0].replace(' ',''), self.name)
            elif (new_work_detail_web := work_detail_web.rsplit('即日起至')[1]) and  "前" in work_detail_web:
                return clean_date(new_work_detail_web.split("前")[0].replace(' ',''), self.name)
            elif "/" in work_detail_web.rsplit('即日起至')[1]:
                return re.findall("\d+/\d+/\d+",work_detail_web.rsplit('即日起至')[1].split("。")[0].replace(' ',''))[0]
        elif '即日起收件至' in work_detail_web:
            return work_detail_web.rsplit("即日起收件至")[1].split("止")[0].replace("：","")
        elif '前報名完成' in work_detail_web:
            return work_detail_web.rsplit("請於")[1].split("前")[0].replace("：","")
        else:
            try:
                if '截止' in work_detail_web.rsplit("報名期限")[1]:
                    return work_detail_web.rsplit("報名期限")[1].split("截止")[0].replace("：","")
                else:
                    return work_detail_web.rsplit("報名期限")[1].split("。")[0].replace("：","")
            except:
                try:
                    return re.findall("\d+年\d+月\d+日",work_detail_web)[0]
                except:
                    print(self.name, title)
                    return 'please check webpage'
