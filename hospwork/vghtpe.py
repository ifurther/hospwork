import pandas as pd
from hospwork.hospital_work import Hospital_work
from hospwork.tool import get_base_web_data,get_work_page


class Vghtpe(Hospital_work):
    def __init__(self):
        self.name = '台北榮民總醫院'
        self.url_base = 'https://www1.vghtpe.gov.tw/conscribe/'
        self.url_work = 'indexb.htm?openExternalBrowser=1'
        self.url_full = super().url()
        self.work_page_base = get_base_web_data(self.url_full)
        self.work_tables = soup.find_all('tr')

work_table=[]
for i, item in enumerate(tables):
    if item.find('a'): #過濾掉被刪除的文章
        s = item.find('a')
        first_td = item.find('td')
        title = first_td.string
        origantion = first_td.find_next_siblings('td')[0].string
        dead_line = first_td.find_next_siblings('td')[2].string
        print('#{}召聘職稱: {} 召聘單位: {}\n 期限: {}\n 連結：{}{}'.format(i+1, title, origantion, dead_line, url_base, s.get('href')))
        work_table.append([i-2, title, origantion, dead_line, url_base+s.get('href')])

work_table=pd.DataFrame(work_table, columns=['no','召聘職稱','召聘單位','期限' ,'連結'])
