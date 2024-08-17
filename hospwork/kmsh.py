import pandas as pd
import re
from hospwork.hospital_work import Hospitalwork
from hospwork.tool.web import get_base_web_data,get_work_page
from hospwork.error import errormsg
from urllib.parse import urlparse


class Kmsh(Hospitalwork):
    def __init__(self):
        self.name = '高雄市立小港醫院'
        self.url_base = 'https://www.kmsh.org.tw/affairs/6300_file/HRDataBase/'
        self.url_work = 'index.asp'
        self.url_full = super().url()
        self.work_page_base = get_base_web_data(self.url_full)
        self.pages = self.work_page_base.find_all('ul' ,class_="layout__pagination ul-reset")[0]

        work_table=[]
        for _page in range(1,self.get_pages(self.pages)+1):
            soup_=get_work_page(self.url_full, page=_page, page_link_part='&page=')
            tables = soup_.find('div',class_="bg-grey pd100").find_all('ul')[-2].find_all('li')
            self.get_work_table(self.url_full, soup_, tables, work_table)
        self.work_table=pd.DataFrame(work_table, columns=['no','召聘職稱','期限' , '詳細連結', '報名連結'])
