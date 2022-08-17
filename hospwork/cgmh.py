import pandas as pd
import re
from hospwork.hospital_work import Hospital_work
from hospwork.tool import get_base_web_data,get_work_page
from hospwork.error import errormsg
from urllib.parse import urlparse

class Cgmh(Hospital_work):
    def __init__(self):
        self.name = '長庚醫院'
        self.url_base = 'https://www.cgmh.org.tw/tw/Systems/'
        self.url_work = 'RecruitInfo/3?bulletinType=A&category=Z'
        self.url_full = super().url()
        self.work_page_base = get_base_web_data(self.url_full)
        self.pages = self.work_page_base.find_all('ul' ,class_="layout__pagination ul-reset")[0]

        work_table=[]
        for _page in range(1,self.get_pages(self.pages)+1):
            soup_=get_work_page(self.url_full, page=_page, page_link_part='&page=')
            tables = soup_.find('div',class_="bg-grey pd100").find_all('ul')[-2].find_all('li')
            self.get_work_table(self.url_full, soup_, tables, work_table)
        self.work_table=pd.DataFrame(work_table, columns=['no','召聘職稱','期限' , '詳細連結', '報名連結'])

    
    def get_pages(self, pages):
        return int(pages.find_all("li")[-2].text)

    def get_work_dead_line(self, soup):  
        work_detail_web = soup.find('article').get_text().replace("\xa0","").replace('\n',"").replace("\u3000","")
        if '報名期限展延至' in work_detail_web:
            return re.findall("\d+年\d+月\d+日",work_detail_web.rsplit('報名期限展延至')[1].split("止")[0].replace(' ',''))[0]
        elif '額滿' in work_detail_web:
            return '額滿為止'
        elif '招募合適人選為止' in work_detail_web:
            return '招募合適人選為止'
        elif '自即日起' in work_detail_web:
            return '自即日起'
        elif '即日起至' in work_detail_web:
            if "止" in work_detail_web.rsplit('即日起至')[1]:
                return re.findall("\d+年\d+月\d+日",work_detail_web.rsplit('即日起至')[1].split("止")[0].replace(' ',''))[0]
            elif "前" in work_detail_web:
                return re.findall("\d+年\d+月\d+日",work_detail_web.rsplit('即日起至')[1].split("前")[0].replace(' ',''))[0]
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
                    errormsg(self.name, title)
                    return 'please check webpage'

    def get_work_table(self, url_full, soup, tables, work_table):
        for i, item in enumerate(tables):
            if item.find('a'): #過濾掉被刪除的文章
                s = item.find('a')
                url_base_website = urlparse(url_full)
                work_detail_link = url_base_website._replace(path=urlparse(s.get('href')).path).geturl()
                title = item.find_all('div')[1].string
                work_page_soup = get_work_page(work_detail_link)
                dead_line = self.get_work_dead_line( work_page_soup )
                resume_link = 'https://webapp.cgmh.org.tw/resume/adm.ASP'
                #print('#{}召聘職稱: {} 期限: {}\n 連結：{}'.format(i+1, title, dead_line, work_detail_link ))
                work_table.append([i-2, title, dead_line, work_detail_link, resume_link ])
