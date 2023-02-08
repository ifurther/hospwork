import pandas as pd
import re
from hospwork.hospital_work import Hospital_work
from hospwork.tool.web import get_base_web_data,get_work_page
from hospwork.tool.job import findjoboriginzation,findjobtype,clean_unused_str

class Vghtc(Hospital_work):
    def __init__(self):
        self.name = '臺中榮民總醫院'
        self.local_zone = 'Taiwan'
        self.url_base = 'https://www.vghtc.gov.tw'
        self.url_work = '/Module/RecruitMent?WebMenuID=9d005e46-411b-46fc-b438-e0bd561eba78'
        self.url_admit = '/Module/Admission?WebMenuID=9d005e46-411b-46fc-b438-e0bd561eba78'
        self.url_full = super().url()
        self.url_full_admit = super().get_url_full_admit()
        self.work_page_base = get_base_web_data(self.url_full)
        self.page_links = self.get_page_links(self.url_base, self.url_full, self.work_page_base)
        self.admit_page_base = get_base_web_data(self.url_full_admit)
        self.admit_tables = self.admit_page_base.find_all('tr')

        work_table=[]
        for _page_link in self.page_links:
            _soup = get_work_page(_page_link)
            _table = _soup.find('table').find_all('tr')
            #print('#{}召聘職稱: {} 召聘單位: {}\n 期限: {}\n 連結：{}{}'.format(i+1, title, origantion, dead_line, self.url_base, s.get('href')))
            self.get_work_table(self.url_base,_table,work_table)

        work_table=pd.DataFrame(work_table)
        if work_table.empty:
            #assert(work_table.empty,'Error',self.name,'get work table')
            self.work_table = pd.DataFrame([],columns=['召聘職稱','召聘單位','詳細連結','期限'])
        else:
            self.work_table=work_table

        admit_table=[]
        self.get_admit_table(self.admit_tables, admit_table)
        if bool(admit_table):
            self.admit_table=pd.DataFrame(admit_table, columns=['召聘職稱','期限' ,'連結'])

    def get_page_links(self, url_base, url_full, work_page_base):
        pages_link = []

        pages_link.append(url_full)

        for pp in work_page_base.find('div', class_="pager").find_all('a'):
            if pp.get('title') == 'Next page':
                pass
            else:
                pages_link.append(url_base+pp.get('href'))

        return pages_link

    def get_work_table(self, url_base, tables, work_table):
        for tt in tables:
            _one_job_data ={}
            for ttt in tt.findAll('td'):
                if ttt.get('data-th') == '報名截止日':
                    #print('期限' , ttt.text)
                    _one_job_data['期限'] = ttt.text
                elif ttt.get('data-th') == '徵才項目':
                    job_type_clean = clean_unused_str(ttt.text, self.name)
                    _one_job_data['召聘職稱'] = job_type_clean
                    try:
                        try:
                            _one_job_data['召聘單位'] = findjoboriginzation(job_type_clean, self.name)
                            _one_job_data['召聘職稱'] = job_type_clean.replace( _one_job_data['召聘單位'],'')
                        except:
                            _one_job_data['召聘職稱'] = findjobtype(job_type_clean, self.name)
                            _one_job_data['召聘單位'] = None
                    except:
                        print(self.name,ttt.text,'get job origization error')
                        _one_job_data['召聘職稱'] = None
                    job_detail_link = url_base+ttt.find('a').get('href')
                    #print('詳細連結', job_detail_link)
                    _one_job_data['連結'] = job_detail_link

            if _one_job_data:
                work_table.append(_one_job_data)

    def get_admit_table(self, admit_tables, admit_table):
        for tt in admit_tables:
            _admit_data = {}
            for ttt in tt.findAll('td'):
                if ttt.get('data-th') == "徵才項目":
                    _admit_data['召聘職稱'] = ttt.text.replace("【錄取公告】","").replace("	","")
                elif ttt.get('data-th') == '公告迄日':
                    _admit_data['期限'] = ttt.text
                elif ttt.get('data-th') == '錄取名單':
                    job_detail_link = ttt.find('a')
                    _admit_data['連結'] = self.url_base+job_detail_link.get('href')
                else:
                    print("Error",self.name, ttt , "other message")
            if not bool(_admit_data):
                admit_table.append(_admit_data)
