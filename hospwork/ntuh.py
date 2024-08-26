import pandas as pd
import re
import requests
import json
import datetime
from hospwork.hospital_work import Hospitalwork
from hospwork.tool.web import get_base_web_data,get_work_page
from hospwork.tool.job import clean_unused_str
from hospwork.tool.time import clean_date

class Ntuh(Hospitalwork):
    def __init__(self):
        self.name = '國立臺灣大學醫學院附設醫院'
        self.url_base='https://www.ntuh.gov.tw/ntuh'
        self.url_work ='/Recruit.action'
        self.url_ajax = '/RecruitAjax.action'
        self.url_admit = '/RecruitAjax!select.action'
        self.url_work_full = super().url()
        self.url_admit_full = super().get_url_full_admit()

        self.admit_table = []
        headers = { 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
        ntuh_req = requests.get(self.url_work_full, headers=headers)
        my_params = {'jobtype': '-1', 'q_seekValue': '','pagenum':'1'}

        ntuh_work_pages=requests.get(self.url_base+self.url_ajax, params=my_params, cookies = ntuh_req.cookies)
        ntuh_admit_pages=requests.get(self.url_admit_full)
        ntu_work_data=json.loads(ntuh_work_pages.content)
        ntu_admit_data=json.loads(ntuh_admit_pages.content)
        totalcount_work = ntu_work_data['totalcount']
        totalPages_work = ntu_work_data['totalPages']
        totalcount_admit = ntu_admit_data['totalcount']
        totalPages_admit = ntu_admit_data['totalPages']
        work_table=[]
        for _page in range(1,totalPages_work):
            my_params = {'jobtype': '-1', 'q_seekValue': '','pagenum':'{}'.format(str(_page))}
            g=requests.get(self.url_base+self.url_ajax, params=my_params, cookies = ntuh_req.cookies, headers = headers)
            ntu_work_data=json.loads(g.content)
            self._get_ntuh_work_table_one_page(self.url_base,ntu_work_data,work_table)
        exam_table = []
        admit_table = []
        for _page in range(1,totalPages_admit):
            g=requests.get(self.url_admit_full+'?page='+str(_page))
            ntu_admit_data=json.loads(g.content)
            self._get_ntuh_admit_table_one_page(self.url_base, ntu_admit_data, exam_table, admit_table)

        self.work_table = pd.DataFrame(work_table, columns=['召聘職稱','召聘單位','期限' ,'詳細連結','報名連結'])
        self.admit_table = pd.DataFrame(admit_table, columns=['召聘職稱','召聘單位','期限' ,'連結','詳細連結']) 


    def _get_ntuh_work_table_one_page(self, url_base, ntu_work_data, work_table):
        for i, item in enumerate(ntu_work_data['queryList']):
            title = clean_unused_str(item['title'],self.name)
            origantion = item['jobDepno']
            begin_date = item['adate_sh']
            if item['edatestr'] != '':
                #dead_line = clean_date(item['edatestr'], self.name)
                dead_line = datetime.datetime.strptime(item["odate"],"%Y-%m-%dT%H:%M:%S").date()
            else:
                dead_line = 'please check page'

            if item['recruitNo'] and "分院" not in origantion:
                #link = 'https://reg.ntuh.gov.tw/WebApplication/Administration/NtuhGeneralSelect/Entry.aspx?selectno='+item['recruitNo']
                detail_link = 'https://reg.ntuh.gov.tw/NtuhGeneralSelect/Openpdf.aspx?SelectNo='+item['recruitNo']+'&FileName='+item['recruitNo']+'.pdf'
                resume_link = 'https://reg.ntuh.gov.tw/NtuhGeneralSelect/Entry.aspx?selectno='+item['recruitNo']
            elif "分院" in origantion:
                break
            else:
                detail_link = url_base+item['ctx'].lstrip('<p><a href="../').split('"><span ')[0]
                resume_link = ''
            #print('#{}召聘職稱: {} 召聘單位: {}\n 期限: {}\n 連結：{}'.format(i+1, title, origantion, dead_line, link))
            work_table.append([title, origantion, dead_line, detail_link, resume_link])
    def _get_ntuh_admit_table_one_page(self, url_base, ntu_admit_data, exam_table, admit_table):
        for i, item in enumerate(ntu_admit_data['queryList']):
            title = clean_unused_str(item['title'],self.name)
            origantion = item['jobDepno']
            begin_date = item['adate_sh']
            if item['edatestr'] != '':
                dead_line = clean_date(item['edatestr'].replace('至',''), self.name)
            else:
                dead_line = 'please check page'

            if item['recruitNo'] and "分院" not in origantion:
                #link = 'https://reg.ntuh.gov.tw/WebApplication/Administration/NtuhGeneralSelect/Entry.aspx?selectno='+item['recruitNo']
                detail_link = 'https://reg.ntuh.gov.tw/NtuhGeneralSelect/Openpdf.aspx?SelectNo='+item['recruitNo']+'&FileName='+item['recruitNo']+'.pdf'
                resume_link = 'https://reg.ntuh.gov.tw/NtuhGeneralSelect/Entry.aspx?selectno='+item['recruitNo']
            elif "分院" in origantion:
                break
            else:
                detail_link = url_base+item['ctx'].lstrip('<p><a href="../').split('"><span ')[0]
                resume_link = ''
            #print('#{}召聘職稱: {} 召聘單位: {}\n 期限: {}\n 連結：{}'.format(i+1, title, origantion, dead_line, link))
            admit_table.append([title, origantion, dead_line, detail_link, resume_link])
