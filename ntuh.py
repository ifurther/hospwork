#!/bin/env python3

from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
url_base='https://www.ntuh.gov.tw/'
url_work_table='ntuh/RecruitAjax!nonDoctor.action'
url=url_base+url_work_table
g=requests.get(url)
#soup=BeautifulSoup(g.content, 'html.parser')
#tables = soup.findAll('table')[0].findAll('tr')
ntu_work_data=json.loads(g.content)

totalcount = ntu_work_data['totalcount']
totalPages = ntu_work_data['totalPages']

work_table=[]
for i, item in enumerate(ntu_work_data['queryList']):
    title = item['title']
    origantion = item['jobDepno']
    dead_line = item['odate']
    
    if item['recruitNo']:
      link = 'https://reg.ntuh.gov.tw/WebApplication/Administration/NtuhGeneralSelect/Entry.aspx?selectno='+item['recruitNo']
    else:
      link = url_base+item['ctx'].lstrip('<p><a href="../').split('"><span ')[0]
    print('#{}召聘職稱: {} 召聘單位: {}\n 期限: {}\n 連結：{}'.format(i+1, title, origantion, dead_line, link))
    work_table.append([i-2, title, origantion, dead_line, link])

work_table=pd.DataFrame(work_table, columns=['no','召聘職稱','召聘單位','期限' ,'連結'])

print(work_table)
