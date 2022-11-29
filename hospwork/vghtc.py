import pandas as pd
import re
from hospwork.hospital_work import Hospital_work
from hospwork.tool.web import get_base_web_data,get_work_page
from hospwork.tool.job import findjobtype

class Vghtc(Hospital_work):
    def __init__(self):
        self.name = '臺中榮民總醫院'
        self.local_zone = 'Taiwan'
        self.url_base = 'https://www.vghtc.gov.tw'
        self.url_work = '/Module/RecruitMent?WebMenuID=9d005e46-411b-46fc-b438-e0bd561eba78'
        self.url_full = super().url()
        self.work_page_base = get_base_web_data(self.url_full)
        self.page_links = self.get_page_links(self.url_base, self.url_full, self.work_page_base)
        self.url_admit = '/Module/Admission?WebMenuID=9d005e46-411b-46fc-b438-e0bd561eba78'
        self.admit_page_base = get_base_web_data(self.url_base+self.url_admit)
        self.admit_tables = self.admit_page_base.find_all('tr')

        work_table=[]
        for _page_link in self.page_links:
            _soup = get_work_page(_page_link)
            _table = _soup.find('table').find_all('tr')
            #print('#{}召聘職稱: {} 召聘單位: {}\n 期限: {}\n 連結：{}{}'.format(i+1, title, origantion, dead_line, self.url_base, s.get('href')))
            work_table = self.get_work_table(self.url_base,_table,work_table)

        work_table=pd.DataFrame(work_table)
        work_table.columns=['召聘職稱','召聘單位','詳細連結','期限' ]
        self.work_table=work_table

        # admit_table=[]
        # for i, item in enumerate(self.admit_tables):
        #     if item.find('a'): #過濾掉被刪除的文章
        #         s = item.find('a')
        #         first_td = item.find('td')
        #         title = first_td.string
        #         origantion = first_td.find_next_siblings('td')[0].string
        #         dead_line = first_td.find_next_siblings('td')[2].string
        #         #print('#{}召聘職稱: {} 召聘單位: {}\n 期限: {}\n 連結：{}{}'.format(i+1, title, origantion, dead_line, self.url_base, s.get('href')))
        #         admit_table.append([title, origantion, dead_line, self.url_base+s.get('href')])
        # self.admit_table=pd.DataFrame(admit_table, columns=['召聘職稱','召聘單位','期限' ,'連結'])

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
                    _one_job_data['deadline'] = ttt.text
                elif ttt.get('data-th') == '徵才項目':
                    job_type_clean = ttt.text.replace('【徵才公告】','').replace(self.name,'').replace('【徵才】','')
                    _one_job_data['jobtype'] = job_type_clean
                    try:
                        _one_job_data['job_type'] = findjobtype(job_type_clean)
                        _one_job_data['jobtype'] = job_type_clean.replace( _one_job_data['job_type'],'').replace('：','')
                    except:
                        print(self.name,ttt.text,'get job_type error')
                        _one_job_data['job_type'] = None
                    job_detail_link = url_base+ttt.find('a').get('href')
                    #print('詳細連結', job_detail_link)
                    _one_job_data['job_detail_link'] = job_detail_link

            if _one_job_data != {}:
                work_table.append(_one_job_data)
        return work_table
