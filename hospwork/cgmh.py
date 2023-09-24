import pandas as pd
import re
from hospwork.hospital_work import Hospital_work
from hospwork.tool.web import get_base_web_data,get_work_page
from hospwork.tool.job import findjoboriginzation,findjobtype,clean_unused_str
from hospwork.tool.time import clean_date
from hospwork.error import errormsg
from urllib.parse import urlparse

class Cgmh(Hospital_work):
    def __init__(self):
        self.name = '長庚醫院'
        self.local_zone = 'Taiwan'
        self.url_base = 'https://www.cgmh.org.tw/tw/Systems/'
        self.url_work = 'RecruitInfo/3?bulletinType=A&category=Z'
        self.url_exam = 'RecruitInfo/3?bulletinType=B&category=Z'
        self.url_admit = 'RecruitInfo/3?bulletinType=C&category=Z'
        self.url_full = super().url()
        self.url_full_exam = super().get_url_full_exam()
        self.url_full_admit = super().get_url_full_exam()
        self.work_page_base_work = get_base_web_data(self.url_full)
        self._pages_work = self.work_page_base_work.find_all('ul' ,class_="layout__pagination ul-reset")[0]
        self.work_page_base_exam = get_base_web_data(self.url_full_exam)
        self._pages_exam = self.work_page_base_work.find_all('ul' ,class_="layout__pagination ul-reset")[0]
        self.work_page_base_admit = get_base_web_data(self.url_full_admit)
        self._pages_admit = self.work_page_base_work.find_all('ul' ,class_="layout__pagination ul-reset")[0]

        work_table = []
        exam_table = []
        admit_table = []
        for _page in range(1,self.get_pages(self._pages_work)+1):
            soup_=get_work_page(self.url_full, page=_page, page_link_part='&page=')
            tables = soup_.find('div',class_="bg-grey pd100").find_all('ul')[-2].find_all('li')
            self.get_work_table(self.url_full, soup_, tables, work_table, exam_table, admit_table)
        for _page in range(1,self.get_pages(self._pages_admit)+1):
            soup_=get_work_page(self.url_full_admit, page=_page, page_link_part='&page=')
            tables = soup_.find('div',class_="bg-grey pd100").find_all('ul')[-2].find_all('li')
            self.get_work_table(self.url_full, soup_, tables, work_table, exam_table, admit_table)
        self.work_table=pd.DataFrame(work_table, columns=['召聘職稱', "召聘單位", '院區', '期限', '詳細連結', '報名方式','報名連結'])
        self.exam_table=pd.DataFrame(exam_table, columns=['召聘職稱', "召聘單位", '院區', '期限', '詳細連結'])
        self.admit_table=pd.DataFrame(admit_table, columns=['召聘職稱', "召聘單位", '院區', '詳細連結'])

    def get_pages(self, pages):
        return int(pages.find_all("li")[-2].text)

    def get_work_dead_line(self, work_detail_web, title):
        work_detail_web = work_detail_web.replace('(日) ','').replace('(日)','').replace('（含）','').replace('即日起，至','即日起至')
        if '報名期限展延至' in work_detail_web:
            return re.findall("\d+年\d+月\d+日",work_detail_web.rsplit('報名期限展延至')[1].split("止")[0].replace(' ',''))[0]
        elif '額滿' in work_detail_web:
            return '額滿為止'
        elif '招募合適人選為止' in work_detail_web or '徵到為止' in work_detail_web:
            return '招募合適人選為止'
        elif '隨到隨審' in work_detail_web:
            return '隨到隨審'
        elif '即日起至招聘完成' in work_detail_web:
            return '即日起至招聘完成'
        elif '自即日起' in work_detail_web or '即日起~' in work_detail_web:
            return '自即日起'
        elif '即日起至' in work_detail_web:
            if (new_work_detail_web := work_detail_web.rsplit('即日起至')[1]) and "止" in new_work_detail_web:
                if '截止' in new_work_detail_web:
                    return clean_date(new_work_detail_web.split("截止")[0].replace(' ',''), self.name)
                else:
                    return clean_date(new_work_detail_web.split("止")[0].replace(' ',''), self.name)
            elif (new_work_detail_web := work_detail_web.rsplit('即日起至')[1]) and  "前" in work_detail_web:
                return clean_date(new_work_detail_web.split("前")[0].replace(' ',''), self.name)
            elif "/" in work_detail_web.rsplit('即日起至')[1]:
                return re.findall("\d+/\d+/\d+",work_detail_web.rsplit('即日起至')[1].split("。")[0].replace(' ',''))[0]
        elif '即日起收件至' in work_detail_web:
            return work_detail_web.rsplit("即日起收件至")[1].split("止")[0].replace("：","")
        elif '前報名完成' in work_detail_web:
            return work_detail_web.rsplit("請於")[1].split("前")[0].replace("：","")
        else:
            try:
                if '截止' in work_detail_web.rsplit("報名期限")[1]:
                    return work_detail_web.rsplit("報名期限")[1].split("截止")[0].replace("：","")
                else:
                    return work_detail_web.rsplit("報名期限")[1].split("。")[0].replace("：","")
            except:
                try:
                    return re.findall("\d+年\d+月\d+日",work_detail_web)[0]
                except:
                    errormsg(self.name, title)
                    return 'please check webpage'

    def get_hosp_region(self,title):
        if '林口' in title:
            return '林口院區'
        elif '台北' in title:
            return '台北院區'
        elif '基隆' in title:
            return '基隆院區'
        elif '嘉義' in title:
            return '嘉義院區'
        elif '雲林' in title:
            return '雲林院區'
        elif '高雄' in title:
            return '高雄院區'
        elif '桃園' in title:
            return '桃園院區'
        elif '台中' in title:
            return '台中院區'
        elif '土城' in title:
            return '土城院區'
        elif '鳳山' in title:
            return '鳳山院區'
        elif '北院區' in title:
            return '北院區'

    def get_work_table(self, url_full, soup, tables, work_table, exam_table, admit_table):
        for i, item in enumerate(tables):
            if item.find('a'):
                s = item.find('a')
                url_base_website = urlparse(url_full)
                work_detail_link = url_base_website._replace(path=urlparse(s.get('href')).path).geturl()
                title = clean_unused_str(item.find_all('div')[1].string,self.name)
                title_old = title
                work_page_soup = get_work_page(work_detail_link)
                try:
                    work_detail_web = clean_unused_str(work_page_soup.find('article').get_text(), self.name)
                except:
                    print(work_page_soup)
                    raise AttributeError
                if '長庚大學' in title or '長庚醫學科技股份有限公司' in title:
                    break
                if (new_title :=  findjobtype(title, self.name)) and new_title != title:

                    title = new_title.replace('醫院','').replace("紀念",'').replace("新北市立","").replace("高雄市立鳳山","")
                if (region := self.get_hosp_region((title_ if (title_ := title_old) else title))) and region is not None:
                    region = region
                    title = title.replace(region,'').replace(region.replace('院區',''),'')
                if '工作地點' in work_detail_web:
                    originzation = findjoboriginzation(work_detail_web.rsplit('工作地點')[1], self.name)
                elif (originzation := findjoboriginzation((title_ if (title_ :=  title_old) else title), self.name)) and originzation != title:
                    originzation = originzation
                    title = title.replace(originzation,'')
                elif (originzation := findjoboriginzation(work_detail_web, self.name) ):
                    originzation = originzation
                    title = title.replace(originzation,'')
                else:
                    originzation = ''
                dead_line = self.get_work_dead_line( work_detail_web ,title)
                if '線上登錄履歷' in work_detail_web or '網路報名' in work_detail_web or '長庚全球資訊網公開招募人才' in work_detail_web:
                    resume_link = 'https://webapp.cgmh.org.tw/resume/adm.ASP'
                    apply_type = 'online'
                elif 'E-mail' in work_detail_web or re.search('\w+@\w+.\w+.\w+',work_detail_web):
                    resume_link = ''
                    apply_type = 'email'
                elif '書面報名' in work_detail_web or '郵戳為憑' in work_detail_web or '通訊報名' in work_detail_web:
                    resume_link = ''
                    apply_type = 'mail'                
                else:
                    resume_link = None
                    apply_type = None

                if '口試' in title_old or '筆試' in title_old or '甄試事宜' in title_old or '甄試日期' in title_old:
                    exam_table.append([title, originzation, region, dead_line, work_detail_link])
                elif '甄試結果' in title_old:
                    admit_table.append([title, originzation, region, work_detail_link])
                else:
                    if apply_type is not None:
                        work_table.append([title, originzation, region, dead_line, work_detail_link, apply_type, resume_link ])

                    else:
                        print(self.name,'Error find resume:',title_old,work_detail_link)
