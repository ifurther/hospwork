import pandas as pd
import re
import requests
import json
from hospwork.hospital_work import Hospital_work
from hospwork.tool import get_base_web_data,get_work_page


class Ntucc(Hospital_work):
    def __init__(self):
        self.name = '國立臺灣大學醫學院附設癌醫中心醫院'
        self.url_base='https://www.ntucc.gov.tw/ntucc/'
        self.url_work ='Recruit.action'
        self.url_ajax = 'RecruitAjax.action'
        self.url_full = super().url()
        self.admit_table = []
        #self.work_page_base = get_base_web_data(self.url_full)
        g=requests.get(self.url_full)
        my_params = {'jobtype': '-1', 'q_seekValue': '','pagenum':'1'}
        ntucc_work_data = json.loads(requests.get(self.url_base+self.url_ajax,params=my_params, cookies = g.cookies).content)
        #soup=BeautifulSoup(g.content, 'html.parser')
        #tables = soup.findAll('table')[0].findAll('tr')
        totalcount = ntucc_work_data['totalPages']
        totalPages = ntucc_work_data['totalPages']
        work_table=[]
        for _page in range(1,totalPages):
            my_params = {'jobtype': '-1', 'q_seekValue': '','pagenum':'{}'.format(str(_page))}
            ntucc_work_data = json.loads(requests.get(self.url_base+self.url_ajax,params=my_params, cookies = g.cookies).content)
            work_table=self._get_ntuh_work_table_one_page(ntucc_work_data, work_table)

        self.work_table=pd.DataFrame(work_table, columns=['召聘職稱','召聘單位','期限' ,'報名方式', '報名簡章', '報名表(doc)', '報名表(odt)', '報名表(pdf)', '信封封面'])
        #print('totalcount: {} getdatacount:{}'.format(totalcount,len(work_table)))
    def _get_file_link(self,id):
        return self.url_base+self.url_ajax+'!download.action?id='+id
    def _get_ntuh_work_table_one_page(self, ntucc_work_data, work_table):
        for i, item in enumerate(ntucc_work_data['queryList']):
            title = item['title']
            origantion = item['jobDepnm']
            begin_date = item['adate_sh']
            dead_line = item['edate_sh']
            file_list = {}
            for _file in item['recruitFile']:
                if _file['title'] == "甄選簡則(PDF檔)":
                    file_list['detail_file_link'] = self._get_file_link(_file['id'])
                else:
                    file_list['detail_file_link'] = 'end'
                if "信封封面" in _file['title']:
                    file_list['letter_file_link'] = self._get_file_link(_file['id'])
                else:
                    file_list['letter_file_link'] = ''

                if _file['typeNo'] == "2":
                    if _file['fileExt'] == '.pdf':
                        file_list['application_file_pdf_link'] = self._get_file_link(_file['id'])
                    elif _file['fileExt'] == '.odt':
                        file_list['application_file_odt_link'] = self._get_file_link(_file['id'])
                    elif "doc" in _file['fileExt']:
                        file_list['application_file_doc_link'] = self._get_file_link(_file['id'])
                if _file['typeNo'] == "4":
                    file_list['first_admit_file_link'] = self._get_file_link(_file['id'])
                if _file['typeNo'] == "5":
                    file_list['second_admit_file_link'] = self._get_file_link(_file['id'])
            #print('#{}召聘職稱: {} 召聘單位: {}\n 期限: {}\n 連結：{}'.format(i+1, title, origantion, dead_line, file_list))
            
            if 'first_admit_file_link' in file_list:
                self.admit_table.append([title, origantion, file_list['first_admit_file_link']])
            if 'second_admit_file_link' in file_list:
                self.admit_table.append([title, origantion, file_list['second_admit_file_link']])

            if file_list['detail_file_link'] == 'end':
                break
            if 'application_file_doc_link' not in file_list and 'application_file_odt_link' not in file_list:
                work_table.append([title, origantion, dead_line, 'online', file_list['detail_file_link'], '', '', '',''])
            else:    
                work_table.append([title, origantion, dead_line, 'mail', file_list['detail_file_link'], file_list['application_file_doc_link'], file_list['application_file_odt_link'], file_list['application_file_pdf_link'], file_list['letter_file_link']])



        return work_table
