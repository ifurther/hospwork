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
    
    def _get_pages_link(self,soup,url_base):
        pages_link=[]
        for link in soup.find_all('li',class_="page-item"):
            if link.find("a"):
                if link.find("a") == -1 or link.text == "第一頁" or link.text == "«" or link.text == "»" or link.text == "最末頁" or link.text == "...":
                    pass
                elif link.find('a').has_attr("disabled"):
                    #print('skip:',link.text)
                    pages_link.append(url_full)
                else:
                    pages_link.append(url_base+link.find('a').get('href'))
        return pages_link