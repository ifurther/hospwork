import pandas as pd
import re
from hospwork.hospital_work import Hospital_work
from hospwork.tool import get_base_web_data,get_work_page
from hospwork.error import errormsg

class Hch(Hospital_work):
    def __init__(self):
        self.name = '國立臺灣大學醫學院附設醫院新竹臺大分院'
        self.local_zone = 'Taiwan'
        self.url_base = 'https://www.hch.gov.tw'
        self.url_work = '/?aid=506&pid=0&page_name=list&pageNo=1'
        self.url_full = super().url()
        self.work_page_base = get_base_web_data(self.url_full)
        self.pages_link = self._get_pages_link(self.work_page_base, self.url_full)

        work_table = []
        for page in self.pages_link:
            soup = get_base_web_data(page)
            work_table = self._get_each_page_wrok_table(self.url_base,soup,work_table)
        self.work_table = pd.DataFrame(work_table, columns=['召聘職稱','期限' ,"職缺單位" , '院區', '報名方式', '報名簡章', '報名表', '作業基金現職人員申請院內外補同意書', '信封封面'])

    def _get_pages_link(self,soup,url_full):
        pages_link=[]
        for link in soup.find('ul',class_="pagination pagination-sm justify-content-center"):
            if link.find("a"):
                if link.find("a") == -1 or link.text == "第一頁" or link.text == "«" or link.text == "»" or link.text == "最末頁" or link.text == " ":
                    pass
                elif link.find('a').has_attr("disabled"):
                    #print('skip:',link.text)
                    pages_link.append(url_full)
                else:
                    no_page_link=url_full.replace("pageNo=1","pageNo=")
                    pages_link.append(no_page_link+link.find('a').text)
        return pages_link
    def _get_each_page_wrok_table(self,url_base,soup,work_table):
        for work in soup.find_all('table',class_="table table-striped table-hover news_table")[0].find("tbody").find_all("tr"):
            all_td = work.find_all("td")
            title = all_td[3].text
            place = all_td[0].text
            deadline = all_td[4].text
            originization = all_td[2].text
            link={}
            for i in all_td[5].find_all("a"):
                link[i.text]=url_base+i.get('href')
                if '簡則' in i.text :
                    link['detail_file_link'] = url_base+i.get('href')
                if '台大醫院新竹臺大分院各類人員甄選登記表及查核授權書' in i.text :
                    link['application_file_link'] = url_base+i.get('href')
                if '作業基金現職人員申請院內外補同意書' in i.text :
                    link['other_file_link'] = url_base+i.get('href')
                if '信封封面' in i.text :
                    link['letter_file_link'] = url_base+i.get('href')
            #print("召聘職稱",title,'院區',place,"截止日期",deadline,"職缺單位",originization,"links",link)
            try:
                work_table.append([title, deadline, originization, place, 'mail',link['detail_file_link'], link['application_file_link'], link['other_file_link'], link['letter_file_link'] ])
            except:
                errormsg(self.name, title)
        return work_table
