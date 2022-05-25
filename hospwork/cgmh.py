import pandas as pd
import re
from hospwork.hospital_work import Hospital_work
from hospwork.tool import get_base_web_data,get_work_page
from urllib.parse import urlparse

class Cgmh(Hospital_work):
    def __init__(self):
        self.name = '長庚醫院'
        self.url_base = 'https://www.cgmh.org.tw/tw/Systems/'
        self.url_work = 'RecruitInfo/3'
        self.url_full = super().url()
        self.work_page_base = get_base_web_data(self.url_full)
        self.pages = self.work_page_base.find_all('ul' ,class_="layout__pagination ul-reset")[0]

        work_table=[]
        for _page in range(1,self.get_pages(self.pages)+1):
            soup_=get_work_page(self.url_full,page=_page)
            tables = soup_.find('div',class_="bg-grey pd100").find_all('ul')[-2].find_all('li')
            self.get_work_table(self.url_full, soup_, tables, work_table)
        self.work_table=pd.DataFrame(work_table, columns=['no','召聘職稱','期限' ,'連結'])

    
    def get_pages(self, pages):
        counter=0
        for i, item in enumerate(pages):
            if item.find('a') :
                s = item.find('a')
                counter += 1
                try:
                    #print(s.get("href") ,s.string)
                    if s.get("href") == "javascript:void(0)":
                        counter -= 1
                except:
                    counter -= 1
                    #print(item,'error')
        return counter

    def get_work_dead_line(self, soup):  
        work_detail_web = soup.find('article').get_text().replace("\xa0","").replace('\n',"").replace("\u3000","")
        if '額滿為止' in work_detail_web:
            return '額滿為止'
        elif '自即日起' in work_detail_web:
            return '自即日起'
        elif '即日起至' in work_detail_web:
            dead_line = re.findall("\d+年\d+月\d+日",work_detail_web.rsplit('即日起至')[1].split("止")[0].replace(' ',''))[0]
            return dead_line
        elif '即日起收件至' in work_detail_web:
            dead_line = work_detail_web.rsplit("即日起收件至")[1].split("止")[0].replace("：","")
            return dead_line      
        else:
            try:
                dead_line = work_detail_web.rsplit("報名期限")[1].split("截止")[0].replace("：","")
            except:
                return re.findall("\d+年\d+月\d+日",work_detail_web)[0]
    
    def get_work_table(self, url_full, soup, tables, work_table):
        for i, item in enumerate(tables):
            if item.find('a'): #過濾掉被刪除的文章
                s = item.find('a')
                url_base_website = urlparse(url_full)
                work_detail_link = url_base_website._replace(path=urlparse(s.get('href')).path).geturl()
                title = item.find_all('div')[1].string
                work_page_soup = get_work_page(work_detail_link)
                dead_line = self.get_work_dead_line( work_page_soup )
                print('#{}召聘職稱: {} 期限: {}\n 連結：{}'.format(i+1, title, dead_line, work_detail_link ))
                work_table.append([i-2, title, dead_line, work_detail_link ])
