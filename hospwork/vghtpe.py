import pandas as pd
from hospwork.hospital_work import Hospital_work
from hospwork.tool.web import get_base_web_data,get_work_page


class Vghtpe(Hospital_work):
    def __init__(self):
        self.name = '台北榮民總醫院'
        self.local_zone = 'Taiwan'
        self.url_base = 'https://www1.vghtpe.gov.tw'
        self.url_work = '/conscribe/indexb.htm?openExternalBrowser=1'
        self.url_full = super().url()
        self.url_admit = '/conscribe/indexa.htm?openExternalBrowser=1'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.78',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Connection': 'keep-alive',
            "Cache-Control": "no-cache",
            "Priority": "u=4",
        }

        self.work_page_base = get_base_web_data(self.url_full, headers=headers)
        self.work_tables = self.work_page_base.find_all('tr')

        self.admit_page_base = get_base_web_data(self.url_base+self.url_admit, headers = User_Agent)
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

