import requests
from bs4 import BeautifulSoup

def get_work_page(url,page=None):
    if page != None:
        url = url+'?page='+str(page)
        
    g=requests.get(url)
    soup=BeautifulSoup(g.content, 'html.parser')
    return soup