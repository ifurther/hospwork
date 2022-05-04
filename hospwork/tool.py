from bs4 import BeautifulSoup
import requests

def get_base_web_data(url_base,url_work_table=None):
    url_base='https://www.cgmh.org.tw/tw/Systems/'
    url_work_table='RecruitInfo/3'
    url=url_base+url_work_table
    g=requests.get(url)
    soup=BeautifulSoup(g.content, 'html.parser')
    return soup


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
