#!/bin/env python3

from bs4 import BeautifulSoup
import requests
import pandas as pd
from urllib.parse import urlparse

url_base='https://www.cgmh.org.tw/tw/Systems/'
url_work_table='RecruitInfo/3'
url=url_base+url_work_table
g=requests.get(url)
soup=BeautifulSoup(g.content, 'html.parser')

pages=soup.find_all('ul' ,class_="layout__pagination ul-reset")[0]
def get_pages(pages):
  counter=0
  for i, item in enumerate(pages):
      if item.find('a') :
        s = item.find('a')
        counter += 1
        try:
          #print(s.get("href") ,s.string)
          if s.get("href") == "javascript:void(0)":
            counter -= 1
        except:
          counter -= 1
          #print(item,'error')
  return counter
get_pages(pages)

tables = soup.find('div',class_="bg-grey pd100").find_all('ul')[-2].find_all('li')

def get_work_dead_line( soup):
  work_detail_web = soup.find('article').get_text().replace("\xa0","").replace('\n',"").replace("\u3000","")
  if '額滿為止' in work_detail_web:
    return '額滿為止'
  elif '即日起收件至' in work_detail_web:
    dead_line = work_detail_web.rsplit("即日起收件至")[1].split("止")[0].replace("：","")
    return dead_line      
  else:
    dead_line = work_detail_web.rsplit("報名期限")[1].split("截止")[0].replace("：","")
    return dead_line
      

def get_work_page(page):
    g=requests.get(url+'?page='+str(page))
    soup=BeautifulSoup(g.content, 'html.parser')
    return soup

def get_work_detail(link):
    g=requests.get(link)
    soup=BeautifulSoup(g.content, 'html.parser')
    return soup

def get_work_table(soup,tables,work_table):
    for i, item in enumerate(tables):
        if item.find('a'): #過濾掉被刪除的文章
            s = item.find('a')
            url_base_website = urlparse(url)
            work_detail_link = url_base_website._replace(path=urlparse(s.get('href')).path).geturl()
            title = item.find_all('div')[1].string
            work_page_soup = get_work_detail(work_detail_link)
            dead_line = get_work_dead_line( work_page_soup )
            print('#{}召聘職稱: {} 期限: {}\n 連結：{}'.format(i+1, title, dead_line, work_detail_link ))
            work_table.append([i-2, title, dead_line, work_detail_link ])

work_table=[]
for _page in range(1,get_pages(pages)+1):
    soup_= get_work_page(_page)
    tables = soup_.find('div',class_="bg-grey pd100").find_all('ul')[-2].find_all('li')
    get_work_table(soup_,tables,work_table)

work_table=pd.DataFrame(work_table, columns=['no','召聘職稱','期限' ,'連結'])

print(work_table)
