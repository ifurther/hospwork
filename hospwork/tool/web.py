from bs4 import BeautifulSoup
import requests

def get_base_web_data(url_base,headers=None,verify=None,url_work_table_link=None) -> BeautifulSoup:
    if url_work_table_link != None:
        url = url_base + url_work_table_link
    else:
        url = url_base

    if headers != None and verify != None:
        g=requests.get(url, headers = headers, verify=verify)
    elif headers != None:
        g=requests.get(url,headers = headers)
    elif verify != None:
        g=requests.get(url, verify=verify)
    else:
        g=requests.get(url)
    soup=BeautifulSoup(g.content, 'html.parser')
    return soup


def get_work_page(page_url,page=None,page_link_part='?page=',**resp_data) -> BeautifulSoup:
    global url
    if page != None:
        page_url = page_url+page_link_part+str(page)
    if 'url' in globals():
        page_url = url
    #g=requests.get(page_url)
    #soup=BeautifulSoup(g.content, 'html.parser')
    soup = get_base_web_data(page_url, **resp_data)
    return soup
