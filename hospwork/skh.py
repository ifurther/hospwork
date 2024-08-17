import pandas as pd
import re
import requests
import json
from hospwork.hospital_work import Hospitalwork
from hospwork.tool.web import get_base_web_data,get_work_page
from hospwork.tool.job import clean_unused_str
from hospwork.tool.time import clean_date

class Skh(Hospitalwork):
    def __init__(self):
        self.name = '新光醫院'
        self.url_base='https://recruitweb.skh.org.tw'
        self.url_work ='/JobVacancyResume/findJobVacancyResume'
        self.url_full = super().url()

        skh_work_pages=requests.get(self.url_full)
        ntu_work_data=json.loads(skh_work_pages.content)
        work_table=[]
        for _page in range(1,totalPages_work):
            g=requests.get(self.url_full+'?page='+str(_page))
            ntu_work_data=json.loads(g.content)
            self._get_skh_work_table_one_page(self.url_base,ntu_work_data,work_table)

        self.work_table = pd.DataFrame(work_table, columns=['召聘職稱','召聘單位','期限' ,'詳細連結','報名連結'])


    def _get_skh_work_table_one_page(self, url_base, ntu_work_data, work_table):
        for i, item in enumerate(ntu_work_data['queryList']):
            title = clean_unused_str(item['title'],self.name)
            origantion = item['workAddress']
            begin_date = item['adate_sh']
            if item['edatestr'] is not '':
                dead_line = clean_date(item['edatestr'].replace('至',''), self.name)
            else:
                dead_line = 'please check page'

            if item['recruitNo'] and "分院" not in origantion:
                #link = 'https://reg.skh.gov.tw/WebApplication/Administration/skhGeneralSelect/Entry.aspx?selectno='+item['recruitNo']
                detail_link = 'https://reg.skh.gov.tw/skhGeneralSelect/Openpdf.aspx?SelectNo='+item['recruitNo']+'&FileName='+item['recruitNo']+'.pdf'
                resume_link = 'https://reg.skh.gov.tw/skhGeneralSelect/Entry.aspx?selectno='+item['recruitNo']
            elif "分院" in origantion:
                break
            else:
                detail_link = url_base+item['ctx'].lstrip('<p><a href="../').split('"><span ')[0]
                resume_link = ''
            #print('#{}召聘職稱: {} 召聘單位: {}\n 期限: {}\n 連結：{}'.format(i+1, title, origantion, dead_line, link))
            work_table.append([title, origantion, dead_line, detail_link, resume_link])
