import pandas as pd
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from hospwork.hospital_work import Hospital_work
from hospwork.tool.web import get_base_web_data,get_work_page
from hospwork.tool.httpadapter import TLSAdapter
from hospwork.tool.time import clean_date

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

        session = requests.Session()
        adapter = TLSAdapter()
        session.mount('https://',adapter)
        if (cafile := Path().cwd().joinpath('cacert.pem')) and cafile.exists():
            print(self.name, 'using the modify ca file {}'.format(cafile))
            self.work_page_base_raw = session.get(self.url_full, headers=headers, verify=cafile)
        else:
            self.work_page_base_raw = session.get(self.url_full, headers=headers)
        self.work_page_base = BeautifulSoup(self.work_page_base_raw.content, 'html.parser')
        self.work_tables = self.work_page_base.find_all('tr')

        if (cafile := Path().cwd().joinpath('cacert.pem')) and cafile.exists():
            self.admit_page_base_raw = session.get(self.url_base+self.url_admit, headers = headers, verify=cafile)
        else:
            self.admit_page_base_raw = session.get(self.url_base+self.url_admit, headers = headers)
        self.admit_page_base = BeautifulSoup(self.admit_page_base_raw.content, 'html.parser')
        self.admit_tables = self.admit_page_base.find_all('tr')

        work_table=[]
        for i, item in enumerate(self.work_tables):
            if item.find('a'): #過濾掉被刪除的文章
                s = item.find('a')
                first_td = item.find('td')
                title = first_td.string
                origantion = first_td.find_next_siblings('td')[0].string
                dead_line = clean_date(first_td.find_next_siblings('td')[2].string.replace('即日起至',''),self.name)
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
                if (dead_line_raw:=first_td.find_next_siblings('td')[2].string) and dead_line_raw is not None:
                    dead_line = clean_date(dead_line_raw.replace('即日起至',''),self.name)
                #print('#{}召聘職稱: {} 召聘單位: {}\n 期限: {}\n 連結：{}{}'.format(i+1, title, origantion, dead_line, self.url_base, s.get('href')))
                admit_table.append([title, origantion, dead_line, self.url_base+s.get('href')])
        self.admit_table=pd.DataFrame(admit_table, columns=['召聘職稱','召聘單位','期限' ,'連結'])


