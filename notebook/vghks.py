# %%
from bs4 import BeautifulSoup
import requests
import pandas as pd
from urllib.parse import urlparse

# %%
url_base='https://www.vghks.gov.tw'
url_work_table='/News.aspx?n=C03011BF96C680C4&sms=5EF61FB0D0F5B657'
url=url_base+url_work_table
g=requests.get(url)
soup=BeautifulSoup(g.content, 'html.parser')

# %%
def get_tables_part(soup):
    tables = soup.find_all('tbody')
    if len(tables) == 1:
        return None,tables
    else:
        return tables[0],tables[1]
pages_table,work_tables = get_tables_part(soup)

# %%
print("page list:",pages_table,"work list:",work_tables)

# %% [markdown]
# # Get page link
# In this website the work table has some page, so the function should find page link for next step.

# %%
if pages_table == None:
    print("only one page")
    pages_link=None
else:
    #print(pages_table.find_all('a'))
    pages_link=[]
    pages_link.append(url)
    for i, item in enumerate(pages_table.find_all('a')):
        s=item.get('href')
        link_s = urlparse(url)._replace(path=s,query=[]).geturl()
        if link_s not in pages_link:
            pages_link.append(link_s)
        print('#{} {}'.format(i , s))

    pages_link

# %% [markdown]
# # Get work table

# %% [markdown]
# The `get_work_page` function is used for getting each work page

# %%
def get_work_page(page_url,page=None):
    global url
    if page != None:
        page_url = page_url+'?page='+str(page)
    if url == None:
        page_url = url
        print(page_url)
    g=requests.get(page_url)
    soup=BeautifulSoup(g.content, 'html.parser')
    return soup

# %% [markdown]
# Using `get_work_page` to read each page and using `get_tables_part` read work table

# %%
def get_work_table(table_,work_table):
    for i, item in enumerate(table_):
        if item.find('a'):
            s=item.find('a')
            if s == -1:
                s = item
                print(i, s)
            else:
                title = s.get('title')
                link = s.get('href')
                link_s = urlparse(url)._replace(path=link,query=[]).geturl()
                all_td = item.find_all('td')
                origination = all_td[1].find('p').text
                dead_line = all_td[-1].find('p').text
                print(i,title,link_s,origination,dead_line)
                work_table.append([i-2, title, dead_line, link_s ])
    return work_table

# %%
work_table=[]
if type(pages_link) != list:
    table_ = work_tables[0]
    work_table = get_work_table(table_,work_table)
else:
    for p_i, p_item in enumerate(pages_link):
        soup_ = get_work_page(p_item)
        table_ = get_tables_part(soup_)[0]
        
        work_table = get_work_table(table_,work_table)


# %%
work_table=pd.DataFrame(work_table, columns=['no','召聘職稱','期限' ,'連結'])

print(work_table)


