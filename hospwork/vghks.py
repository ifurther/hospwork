from urllib.parse import urlparse
import pandas as pd
from hospwork.hospital_work import Hospital_work
from hospwork.tool.web import get_base_web_data,get_work_page
from hospwork.tool.job import clean_unused_str

class Vghks(Hospital_work):
    def __init__(self):
        self.name = '高雄榮民總醫院'
        self.url_base = 'https://www.vghks.gov.tw'
        self.url_work = '/News.aspx?n=C03011BF96C680C4&sms=5EF61FB0D0F5B657'
        self.url_admit = '/News.aspx?n=A6CB27885DCE35D9&sms=CB7E1ED53E529904'
        self.url_full = super().url()
        self.work_page_base = get_base_web_data(self.url_full)
        self.pages_table,self.work_tables = self._get_tables_part(self.work_page_base)
        self.pages_link = self._get_pages_link(self.pages_table)
        work_table=[]
        if type(self.pages_link) != list:
            table_ = self.work_tables[0]
            work_table = self._get_work_table(table_,work_table)
        else:
            for p_i, p_item in enumerate(self.pages_link):
                print("page:",p_i+1)
                soup_ = get_work_page(p_item)
                x, table_ = self._get_tables_part(soup_)
                work_table = self._get_work_table(table_,work_table)

        self.work_table=pd.DataFrame(work_table, columns=['召聘職稱','期限' ,"召聘單位" ,'連結'])
        self.admit_table = []
    def _get_pages_link(self,pages_table,page_one=None):
        if page_one is None:
            page_one = self.url_full
        if pages_table is None:
            #print("only one page")
            pages_link=None
        else:
            #print(pages_table.find_all('a'))
            pages_link=[]
            pages_link.append(page_one)
            for i, item in enumerate(pages_table.find_all('a')):
                s=item.get('href')
                link_s = urlparse(page_one)._replace(path=s,query=[]).geturl()
                if link_s not in pages_link:
                    pages_link.append(link_s)
                #print('#{} {}'.format(i , s))
        return pages_link
    def _get_tables_part(self,soup):
        tables = soup.find_all('tbody')
        if len(tables) == 1:
            return None,tables
        else:
            try:
                return tables[1],tables[0]
            except:
                print('Error in get_tables_part')
    def _get_work_table(self,table_,work_table):
        for i, item in enumerate(table_):
            if item.find('a'):
                s=item.find('a')
                if s == -1:
                    s = item
                    #print(i, s)
                else:
                    title = clean_unused_str(s.get('title'),self.name)
                    link = s.get('href')
                    link_s = urlparse(self.url_full)._replace(path=link,query=[]).geturl()
                    all_td = item.find_all('td')
                    origination = all_td[1].find('p').text
                    dead_line = all_td[-1].find('p').text
                    title=title.replace(origination,'')
                    #print(i,title,link_s,origination,dead_line)
                    work_table.append([title, dead_line, origination, link_s ])
        return work_table
