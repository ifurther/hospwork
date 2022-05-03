import requests
from bs4 import BeautifulSoup

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