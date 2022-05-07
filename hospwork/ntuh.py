import pandas as pd
import re
from hospwork.hospital_work import Hospital_work
from hospwork.tool import get_base_web_data,get_work_page


class Ntuh(Hospital_work):
    def __init__(self):
        self.name = '國立臺灣大學醫學院附設醫院'
        self.url_base='https://www.ntuh.gov.tw/'
        self.url_work ='ntuh/RecruitAjax!nonDoctor.action'
        self.url_full = super().url()
        self.work_page_base = get_base_web_data(self.url_full)
        self.pages_link = self._get_pages_link(self.work_page_base, self.url_full)

        work_table=[]
for _page in range(1,totalPages):
    g=requests.get(url+'?page='+str(_page))
    ntu_work_data=json.loads(g.content)
    work_table=get_ntuh_work_table_one_page(ntu_work_data,work_table)

        self.work_table=pd.DataFrame(work_table, columns=['召聘職稱','期限' ,'連結'])
    def get_ntuh_work_table_one_page(ntu_work_data,work_table):
    for i, item in enumerate(ntu_work_data['queryList']):
        title = item['title']
        origantion = item['jobDepno']
        begin_date = item['adate_sh']
        dead_line = item['edatestr']
        
        if item['recruitNo']:
            link = 'https://reg.ntuh.gov.tw/WebApplication/Administration/NtuhGeneralSelect/Entry.aspx?selectno='+item['recruitNo']
        else:
            link = url_base+item['ctx'].lstrip('<p><a href="../').split('"><span ')[0]
        print('#{}召聘職稱: {} 召聘單位: {}\n 期限: {}\n 連結：{}'.format(i+1, title, origantion, dead_line, link))
        work_table.append([i, title, origantion, dead_line, link])
    return work_table
