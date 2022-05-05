from urllib.parse import urlparse
import pandas as pd
from hospwork.hospital_work import Hospital_work
from hospwork.tool import get_base_web_data,get_work_page

class vghks(Hospital_work):
    def __init__(self):
        super().__init__(url_full)
        self.name = '高雄榮民總醫院'
        self.url_base = 'https://www.vghks.gov.tw'
        self.url_work = '/News.aspx?n=C03011BF96C680C4&sms=5EF61FB0D0F5B657'
        self.work_page_base = get_base_web_data(self.url_full)
        self.pages_table,self.work_tables = self.get_tables_part(soup)
        self.pages_link = self.get_pages_link(self.pages_table)
        work_table=[]
        if type(self.pages_link) != list:
            table_ = self.work_tables[0]
            work_table = self.get_work_table(table_,work_table)
        else:
            for p_i, p_item in enumerate(self.pages_link):
                soup_ = get_work_page(p_item)
                table_ = self.get_tables_part(soup_)[0]
                
                work_table = self.get_work_table(table_,work_table)

        self.work_table=pd.DataFrame(work_table, columns=['no','召聘職稱','期限' ,'連結'])

    def get_pages_link(self,pages_table):
        if pages_table == None:
            print("only one page")
            pages_link=None
        else:
            #print(pages_table.find_all('a'))
            pages_link=[]
            pages_link.append(self.url_full)
            for i, item in enumerate(pages_table.find_all('a')):
                s=item.get('href')
                link_s = urlparse(self.url_full)._replace(path=s,query=[]).geturl()
                if link_s not in pages_link:
                    pages_link.append(link_s)
                print('#{} {}'.format(i , s))
        return pages_link
    def get_tables_part(self,soup):
        tables = soup.find_all('tbody')
        if len(tables) == 1:
            return None,tables
        else:
            return tables[0],tables[1]
    def get_work_table(self,table_,work_table):
        for i, item in enumerate(table_):
            if item.find('a'):
                s=item.find('a')
                if s == -1:
                    s = item
                    print(i, s)
                else:
                    title = s.get('title')
                    link = s.get('href')
                    link_s = urlparse(self.url_full)._replace(path=link,query=[]).geturl()
                    all_td = item.find_all('td')
                    origination = all_td[1].find('p').text
                    dead_line = all_td[-1].find('p').text
                    print(i,title,link_s,origination,dead_line)
                    work_table.append([i-2, title, dead_line, link_s ])
        return work_table