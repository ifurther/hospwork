import pandas as pd
import re
from hospwork.hospital_work import Hospital_work
from hospwork.tool import get_base_web_data,get_work_page


class Cych(Hospital_work):
    def __init__(self):
        self.name = '嘉義基督教醫院'
        self.url_base = 'https://www.cych.org.tw/cychweb/cych3/'
        self.url_work = 'enlist.aspx?menusub_id=24'
        self.url_full = super().url()
        self.work_page_base = get_base_web_data(self.url_full)
        self.all_table = self.work_page_base.find('table',attrs={'summary':"排版用表格"}).find_all("table")

        work_table=[]
        for no in range(2,13,2):
            work_table = self._get_each_table(no, self.all_table,work_table)

        self.work_table = pd.DataFrame(work_table, columns=['召聘職稱','召聘單位' ,'連結'])

    def _get_each_table(self, no, all_table, work_table):
        for tt in all_table[no].find('table').find_all('tr'):
            all_td = tt.find_all('td')
            if len(all_td)>1:
                no = all_td[0].text.replace('\r','').replace('\n','').replace(' ','')
                title = all_td[2].text.replace('\r','').replace('\n','').replace(' ','')
                originazation = all_td[1].text.replace('\r','').replace('\n','').replace(' ','')
                link = all_td[1].find('a').get('href')
                print('序號:{} 職稱:{} 招募單位:{}'.format(no, title, originazation))
                work_table.append([title, originazation, link])
        return work_table