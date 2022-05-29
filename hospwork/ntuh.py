import pandas as pd
import re
import requests
import json
from hospwork.hospital_work import Hospital_work
from hospwork.tool import get_base_web_data,get_work_page


class Ntuh(Hospital_work):
    def __init__(self):
        self.name = '國立臺灣大學醫學院附設醫院'
        self.url_base='https://www.ntuh.gov.tw/'
        self.url_work ='ntuh/RecruitAjax!nonDoctor.action'
        self.url_full = super().url()
        #self.work_page_base = get_base_web_data(self.url_full)
        g=requests.get(self.url_full)
        #soup=BeautifulSoup(g.content, 'html.parser')
        #tables = soup.findAll('table')[0].findAll('tr')
        ntu_work_data=json.loads(g.content)

        totalcount = ntu_work_data['totalcount']
        totalPages = ntu_work_data['totalPages']
        work_table=[]
        for _page in range(1,totalPages):
            g=requests.get(self.url_full+'?page='+str(_page))
            ntu_work_data=json.loads(g.content)
            work_table=self._get_ntuh_work_table_one_page(self.url_base,ntu_work_data,work_table)

        self.work_table=pd.DataFrame(work_table, columns=['召聘職稱','召聘單位','期限' ,'連結'])
        #print('totalcount: {} getdatacount:{}'.format(totalcount,len(work_table)))

    def _get_ntuh_work_table_one_page(self, url_base, ntu_work_data, work_table):
        for i, item in enumerate(ntu_work_data['queryList']):
            title = item['title']
            origantion = item['jobDepno']
            begin_date = item['adate_sh']
            dead_line = item['edatestr']

            if item['recruitNo']:
                link = 'https://reg.ntuh.gov.tw/WebApplication/Administration/NtuhGeneralSelect/Entry.aspx?selectno='+item['recruitNo']
            else:
                link = url_base+item['ctx'].lstrip('<p><a href="../').split('"><span ')[0]
            #print('#{}召聘職稱: {} 召聘單位: {}\n 期限: {}\n 連結：{}'.format(i+1, title, origantion, dead_line, link))
            work_table.append([title, origantion, dead_line, link])
        return work_table
