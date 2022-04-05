#!/bin/env python3

from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
url_base='https://www.ntuh.gov.tw/ntuh/'
url_work_table='RecruitAjax!nonDoctor.action'
url=url_base+url_work_table
g=requests.get(url)
#soup=BeautifulSoup(g.content, 'html.parser')
#tables = soup.findAll('table')[0].findAll('tr')
ntu_work_data=json.loads(g)

totalcount = ntu_work_data{'totalcount'}
totalPages = ntu_work_data['totalPages']

work_table=[]
for i, item in enumerate(tables):
    if item.find('a'): #過濾掉被刪除的文章
        s = item.find('a')
        first_td = item.find('td')
        title = first_td.string
        origantion = first_td.find_next_siblings('td')[0].string
        dead_line = first_td.find_next_siblings('td')[2].string
        print('#{}召聘職稱: {} 召聘單位: {}\n 期限: {}\n 連結：{}{}'.format(i+1, title, origantion, dead_line, url_base, s.get('href')))
        work_table.append([i-2, title, origantion, dead_line, url_base+s.get('href')])

work_table=pd.DataFrame(work_table, columns=['no','召聘職稱','召聘單位','期限' ,'連結'])

print(work_table)
