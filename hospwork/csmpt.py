import pandas as pd
import re
from hospwork.hospital_work import Hospital_work
from hospwork.tool import get_base_web_data,get_work_page


class Csmpt(Hospital_work):
    def __init__(self):
        self.name = '中華民國醫學物理學會'
        self.url_base = 'http://www.csmpt.org.tw/news'
        self.url_work = '/index.php?type=4'
        self.url_full = super().url()
        self.work_page_base = get_base_web_data(self.url_full)
        self.pages_link = self._get_pages_link(self.work_page_base, self.url_full)

        work_table=[]
        work_table = self._get_work_table(self.work_page_base.find_all('article')[0],self.url_base,work_table)
        for p_i, p_item in enumerate(self.pages_link):
            table_ = get_work_page(p_item).find_all('article')[0]

            work_table = self._get_work_table(table_,self.url_base,work_table)

        self.work_table=pd.DataFrame(work_table, columns=['召聘職稱','期限' ,'連結'])

    def _get_pages_link(self,soup,url):
        pages_link=[]
        for o in soup.find(class_="page").find_all('span'):
            if o.find('a'):
                O=o.find("a")
                if O.text == "到最後>|" or O.text == ">":
                    pass
                else:
                    link = url.replace("?type=4","")+O.get('href')
                    pages_link.append(link)
                    #print(O.text,link)
        return pages_link

    def _get_work_deadtime(link):
        y=get_work_detail(link).find('div', class_="content").text.replace('\xa0','').replace("\n","").replace(" 年","年").replace(" 月","月").replace(" 日","日")
        date_pattern="(\d{1,4}年)((([0?][1-9])月)|(([1?][0-2])月)|([1-9]月)?)(([0?][1-9]日)|([1?][0-9]日)|([2?][1-9]日)|([3][0-1]日)?)"
        return re.search(date_pattern,re.search("(?<=期限)(.*)年(.*)月(.*)日",y)[0]).group(0)

    def _get_work_table(self,table_,url_base,work_table):
        for p_i, p_item in enumerate(table_.find_all('li')):
            if p_item.find('a'):
                p_item_a = p_item.find('a')
                title = p_item_a.text
                link_s = url_base+'/'+p_item_a.get('href')
                try:
                    dead_line = _get_work_deadtime(link_s)
                except:
                    dead_line = "null(check webpage)"
                #print(p_i-1,title,link_s,dead_line)
                work_table.append([title, dead_line, link_s ])
        return work_table
