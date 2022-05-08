import pandas as pd
import re
from hospwork.hospital_work import Hospital_work
from hospwork.tool import get_base_web_data,get_work_page


class Ylh(Hospital_work):
    def __init__(self):
        self.name = '國立臺灣大學醫學院附設醫院雲林分院'
        self.url_base = 'https://www.ylh.gov.tw'
        self.url_work = '/?aid=104'
        self.url_full = super().url()
        self.work_page_base = get_base_web_data(self.url_full)
        self.pages_link = self._get_pages_link(self.work_page_base, self.url_base)
    
        work_table = []
        for page in self.pages_link:
            soup = get_base_web_data(page)
            work_table = self._get_each_page_wrok_table(self.url_base,soup,work_table)
        self.work_table = pd.DataFrame(work_table, columns=['召聘職稱','期限' ,"職缺單位" , '院區','連結'])

    def _get_pages_link(self,soup,url_base):
        pages_link=[]
        for link in soup.find_all('li',class_="page-item"):
            if link.find("a"):
                if link.find("a") == -1 or link.text == "第一頁" or link.text == "«" or link.text == "»":
                    pass
                elif link.find('a').has_attr("disabled"):
                    #print('skip:',link.text)
                    pages_link.append(url_full)
                else:
                    pages_link.append(url_base+link.find('a').get('href'))
        return pages_link
    
    def _get_each_page_wrok_table(self,url_base,soup,work_table):
        for work in soup.find_all('table',class_="table table-striped table-hover news_table")[0].find("tbody").find_all("tr"):
            all_td = work.find_all("td")
            title = all_td[0].text
            place = '察看連結的簡章'
            deadline = all_td[2].text
            
            link=url_base+all_td[3].find('a').get('href')
            if "錄取名單" in title:
                #print('skip: ',title)
                pass
            elif "甄試名單" in title:
                #print('skip: ',title)
                pass
            elif "複試名單" in title:
                #print('skip: ',title)
                pass
            elif "志願服務工作" in title:
                #print('skip: ',title)
                pass
            elif "甄審會" in title:
                #print('skip: ',title)
                pass
            elif "時薪人員" in title:
                #print('skip: ',title)
                pass
            else:
                originization = re.search("\B院((.*)[室,部,中心])",title).group(1)
                new_title = re.search("\B聘((.*)[員,師,廚])",title).group(1)
                #print("召聘職稱",new_title,'院區',place,"截止日期",deadline,"職缺單位",originization,"links",link)
                work_table.append([new_title, deadline, originization, place, link ])
        return work_table