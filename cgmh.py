#!/bin/env python3

from bs4 import BeautifulSoup
import requests
import pandas as pd
url_base='https://www.cgmh.org.tw/tw/Systems/RecruitInfo/'
url_work_table='3'
url=url_base+url_work_table
g=requests.get(url)
soup=BeautifulSoup(g.content, 'html.parser')

pages=soup.find_all('ul' ,class_="layout__pagination ul-reset")
for i, item in enumerate(pages[0]):
    if item.find('a'):
      print(item.string)

tables = soup.find('div',class_="bg-grey pd100").find_all('ul')[-2].find_all('li')

def get_work_detail():
    work_detail_web = soup.find('article').get_text().replace("\xa0","").replace('\n',"").replace("\u3000","")
    dead_line = work_detail_web.rsplit("報名期限")[1].split("截止")[0].replace("：","")
work_table=[]
for i, item in enumerate(tables):
    if item.find('a'): #過濾掉被刪除的文章
        s = item.find('a')
        work_detail_link = url_base+'/'+s.get('href').split('/')[-1]
        title = item.find_all('div')[1].string
        origantion = first_td.find_next_siblings('td')[0].string
        dead_line = first_td.find_next_siblings('td')[2].string
        print('#{}召聘職稱: {} 召聘單位: {}\n 期限: {}\n 連結：{}'.format(i+1, title, origantion, dead_line, work_detail_link ))
        work_table.append([i-2, title, origantion, dead_line, work_detail_link ])

work_table=pd.DataFrame(work_table, columns=['no','召聘職稱','召聘單位','期限' ,'連結'])

print(work_table)
