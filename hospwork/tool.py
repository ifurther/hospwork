from bs4 import BeautifulSoup
import requests

def get_base_web_data(url_base,url_work_table=None):
    if url_work_table != None:
        url = url_base + url_work_table
    else:
        url = url_base
    g=requests.get(url)
    soup=BeautifulSoup(g.content, 'html.parser')
    return soup


def get_work_page(page_url,page=None,page_link_part='?page='):
    global url
    if page != None:
        page_url = page_url+page_link_part+str(page)
    if 'url' in globals():
        page_url = url
    g=requests.get(page_url)
    soup=BeautifulSoup(g.content, 'html.parser')
    return soup
