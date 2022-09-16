import pandas as pd
from hospwork.hospital_work import Hospital_work
from hospwork.tool import get_base_web_data,get_work_page


class Vghtpe(Hospital_work):
    def __init__(self):
        self.name = '台北榮民總醫院'
        self.url_base = 'https://www1.vghtpe.gov.tw/conscribe/'
        self.url_work = 'indexb.htm?openExternalBrowser=1'
        self.url_full = super().url()
        self.work_page_base = get_base_web_data(self.url_full)
        self.work_tables = self.work_page_base.find_all('tr')
        self.url_admit = 'indexa.htm?openExternalBrowser=1'
        self.admit_page_base = get_base_web_data(self.url_base+self.url_admit)
        self.admit_tables = self.admit_page_base.find_all('tr')

        work_table=[]
        for i, item in enumerate(self.work_tables):
            if item.find('a'): #過濾掉被刪除的文章
                s = item.find('a')
                first_td = item.find('td')
                title = first_td.string
                origantion = first_td.find_next_siblings('td')[0].string
                dead_line = first_td.find_next_siblings('td')[2].string
                #print('#{}召聘職稱: {} 召聘單位: {}\n 期限: {}\n 連結：{}{}'.format(i+1, title, origantion, dead_line, self.url_base, s.get('href')))
                work_table.append([title, origantion, dead_line, self.url_base+s.get('href')])
        self.work_table=pd.DataFrame(work_table, columns=['召聘職稱','召聘單位','期限' ,'連結'])

        admit_table=[]
        for i, item in enumerate(self.admit_tables):
            if item.find('a'): #過濾掉被刪除的文章
                s = item.find('a')
                first_td = item.find('td')
                title = first_td.string
                origantion = first_td.find_next_siblings('td')[0].string
                dead_line = first_td.find_next_siblings('td')[2].string
                #print('#{}召聘職稱: {} 召聘單位: {}\n 期限: {}\n 連結：{}{}'.format(i+1, title, origantion, dead_line, self.url_base, s.get('href')))
                admit_table.append([title, origantion, dead_line, self.url_base+s.get('href')])
        self.admit_table=pd.DataFrame(admit_table, columns=['召聘職稱','召聘單位','期限' ,'連結'])

