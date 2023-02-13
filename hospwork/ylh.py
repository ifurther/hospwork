import pandas as pd
import re
from hospwork.hospital_work import Hospital_work
from hospwork.tool.web import get_base_web_data,get_work_page
from hospwork.tool.job import findjobtype,findjoboriginzation,clean_unused_str
from hospwork.tool.time import clean_date


class Ylh(Hospital_work):
    def __init__(self):
        self.name = '國立臺灣大學醫學院附設醫院雲林分院'
        self.local_zone = 'Taiwan'
        self.url_base = 'https://www.ylh.gov.tw'
        self.url_work = '/?aid=104'
        self.url_full = super().url()
        self.work_page_base = get_base_web_data(self.url_full)
        self.pages_link = self._get_pages_link(self.url_full,self.url_base,self.work_page_base)

        work_table = []
        exam_table = []
        admit_table = []

        for page in self.pages_link:
            soup = get_base_web_data(page)
            self._get_each_page_wrok_table(soup, work_table, exam_table, admit_table)

        self.work_table = pd.DataFrame(work_table, columns=['召聘職稱','期限' ,"召聘單位" , '院區','詳細連結'])
        self.exam_table = pd.DataFrame(exam_table, columns=['召聘職稱','期限' ,"召聘單位" , '院區','詳細連結'])
        self.admit_table = pd.DataFrame(admit_table, columns=['召聘職稱','期限' ,"召聘單位" , '院區','詳細連結'])

    def _get_pages_link(self,url_full,url_base,soup):
        pages_link=[]
        pages_link.append(url_full)
        for link in soup.find_all('li',class_="page-item"):
            if link.find("a"):
                if link.find("a") == -1 or link.text == "第一頁" or link.text == "«" or link.text == "»":
                    pass
                elif link.text == "最末頁":
                    pages_link.append(url_base+link.find('a').get('href'))
                elif link.find('a').has_attr("disabled"):
                    #print('skip:',link.text)
                    pass
                else:
                    pages_link.append(url_base+link.find('a').get('href'))
        return pages_link

    def _get_detail_data(self,title, all_td, table):
        place = '察看連結的簡章'
        deadline = clean_date(all_td[2].text, self.name)
        link=self.url_base+all_td[3].find('a').get('href')
        jobtype = findjobtype(title, self.name).replace("部","").replace("科","")
        try:
            if (originzation := findjoboriginzation(title, self.name)) and originzation == title:
                originzation = re.search(r"\B院((.*)[室,部,中心])", title).group(1)
            else:
                originzation = originzation
        except:
            originzation = "error"
            print(self.name,'error: find originzation',title)
        try:
            if jobtype == title:
                new_title = re.search("\B[聘,選]((.*)[員,師,廚,長])",title).group(1).replace("部","")
        except:
            jobtype="error"
            print(self.name,'error find jobtype',title,link)
        #print("召聘職稱",new_title,'院區',place,"截止日期",deadline,"職缺單位",originization,"links",link)
        table.append([jobtype, deadline, originzation, place, link])

    def _get_each_page_wrok_table(self, soup, work_table, exam_table, admit_table):
        for work in soup.find_all('table',class_="table table-striped table-hover news_table")[0].find("tbody").find_all("tr"):
            all_td = work.find_all("td")
            title = all_td[0].text

            if "承辦人分機更新" in title:
                pass
            elif "志願服務工作" in title:
                #print('skip: ',title)
                pass
            elif "公共服務" in title:
                pass
            elif "甄審會" in title:
                #print('skip: ',title)
                pass
            elif "時薪人員" in title:
                #print('skip: ',title)
                pass
            elif "錄取名單" in title:
                self._get_detail_data(title, all_td, admit_table)
            elif "甄試名單" in title:
                self._get_detail_data(title, all_td, exam_table)
            elif "複試名單" in title:
                self._get_detail_data(title, all_td, exam_table)
            elif "初試名單" in title:
                self._get_detail_data(title, all_td, exam_table)
            elif "初試結果" in title:
                self._get_detail_data(title, all_td, exam_table)
            else:
                self._get_detail_data(title, all_td, work_table)
