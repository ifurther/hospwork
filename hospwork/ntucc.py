import pandas as pd
import re
import requests
import json
from hospwork.hospital_work import Hospital_work
from hospwork.tool import get_base_web_data,get_work_page


class Ntucc(Hospital_work):
    def __init__(self):
        self.name = '國立臺灣大學醫學院附設癌醫中心醫院'
        self.url_base='https://www.ntucc.gov.tw/'
        self.url_work ='ntucc/Recruit.action'
        self.url_full = super().url()
        #self.work_page_base = get_base_web_data(self.url_full)
        g=requests.get(self.url_full)
        my_params = {'jobtype': '-1', 'q_seekValue': '','pagenum':'1'}
        ntucc_work_data = json.loads(requests.get(self.url_base+'/ntucc/RecruitAjax.action',params=my_params, cookies = g.cookies).content)
        #soup=BeautifulSoup(g.content, 'html.parser')
        #tables = soup.findAll('table')[0].findAll('tr')
        totalcount = ntucc_work_data['totalPages']
        totalPages = ntucc_work_data['totalPages']
        work_table=[]
        for _page in range(1,totalPages):
            my_params = {'jobtype': '-1', 'q_seekValue': '','pagenum':'{}'.format(str(_page))}
            ntucc_work_data = json.loads(requests.get(self.url_base+'/ntucc/RecruitAjax.action',params=my_params, cookies = g.cookies).content)
            work_table=self._get_ntuh_work_table_one_page(self.url_base, ntucc_work_data, work_table)

        self.work_table=pd.DataFrame(work_table, columns=['召聘職稱','召聘單位','期限' ,'連結'])
        #print('totalcount: {} getdatacount:{}'.format(totalcount,len(work_table)))

    def _get_ntuh_work_table_one_page(self, url_base, ntucc_work_data, work_table):
        for i, item in enumerate(ntucc_work_data['queryList']):
            title = item['title']
            origantion = item['jobDepnm']
            begin_date = item['adate_sh']
            dead_line = item['edate_sh']

            file_list = []
            for _file in item['recruitFile']:
                file_list.append([_file['fileName'],self.url_base+'ntucc/RecruitAjax!download.action?id='+_file['id']])
            #print('#{}召聘職稱: {} 召聘單位: {}\n 期限: {}\n 連結：{}'.format(i+1, title, origantion, dead_line, file_list))
            work_table.append([title, origantion, dead_line, file_list])
        return work_table
