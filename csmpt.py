#!/usr/bin/env python
# coding: utf-8



from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
from urllib.parse import urlparse




url_base='http://www.csmpt.org.tw/news'
url_work_table='/index.php?type=4'
url=url_base+url_work_table
g=requests.get(url)
soup=BeautifulSoup(g.content, 'html.parser')


# # Get page link
# In this website the work table has some page, so the function should find page link for next step.



pages_link=[]
for o in soup.find(class_="page").find_all('span'):
    if o.find('a'):
        O=o.find("a")
        if O.text == "到最後>|" or O.text == ">":
            pass
        else:
            link = url.replace("?type=4","")+O.get('href')
            pages_link.append(link)
            print(O.text,link)



http://www.csmpt.org.tw/news/index.php?sub=3&continue=Y&type=4


# # Get work table

# The `get_work_page` function is used for getting each work page


work_page = soup.find_all('article')[0]



def get_work_page(page_url,page=None,page_link_part='?page='):
    global url
    if page != None:
        page_url = page_url+page_link_part+str(page)
    if url == None:
        page_url = url
        print(page_url)
    g=requests.get(page_url)
    soup=BeautifulSoup(g.content, 'html.parser')
    return soup


# Using `get_work_page` to read each page and using `get_tables_part` read work table



def get_work_detail(link):
    g=requests.get(link)
    soup=BeautifulSoup(g.content, 'html.parser')
    return soup


# In[249]:


def get_work_deadtime(link):
    y=get_work_detail(link).find('div', class_="content").text.replace('\xa0','').replace("\n","").replace(" 年","年").replace(" 月","月").replace(" 日","日")
    date_pattern="(\d{1,4}年)((([0?][1-9])月)|(([1?][0-2])月)|([1-9]月)?)(([0?][1-9]日)|([1?][0-9]日)|([2?][1-9]日)|([3][0-1]日)?)"
    return re.search(date_pattern,re.search("(?<=期限)(.*)年(.*)月(.*)日",y)[0]).group(0)




def get_work_table(table_,work_table):
    for p_i, p_item in enumerate(table_.find_all('li')):
        if p_item.find('a'):
            p_item_a = p_item.find('a')
            title = p_item_a.text
            link_s = url_base+'/'+p_item_a.get('href')
            try:
                dead_line = get_work_deadtime(link_s)
            except:
                dead_line = "null(check webpage)"
            print(p_i-1,title,link_s,dead_line)
            work_table.append([p_i-1, title, dead_line, link_s ])
    return work_table



work_table=[]
work_table = get_work_table(work_page,work_table)
for p_i, p_item in enumerate(pages_link):
    table_ = get_work_page(p_item)

    work_table = get_work_table(table_,work_table)



work_table=pd.DataFrame(work_table, columns=['no','召聘職稱','期限' ,'連結'])

print(work_table)



