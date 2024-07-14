#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import re
from datetime import time
from pathlib import Path
import random
from hospwork.hospital_work import Hospital_work
from hospwork.tool.web import get_base_web_data,get_work_page
from hospwork.tool.job import findjobtype,findjoboriginzation,clean_unused_str


class Vhcy(Hospital_work):
    def __init__(self):
        self.name = '臺中榮民總醫院嘉義分院'
        self.local_zone = 'Taiwan'
        self.url_base = 'https://www.vhcy.gov.tw'
        self.url_work = '/UnitPage/RowView?WebMenuID=fb60be6b-ced8-485b-95dc-b470a3c4264f&UnitID=1f7b14c3-842f-4091-b3ca-4972e4c53524%20&UnitDefaultTemplate=1'
        self.url_full = super().url()
        if (cafile := Path().cwd().joinpath('cacert.pem')) and cafile.exists():
            self.work_page_base = get_base_web_data(self.url_full, verify=cafile )
        else:
            self.work_page_base = get_base_web_data(self.url_full)
        self.work_page_work_table = self.work_page_base.find("tbody")
        self.pages_link = self._get_pages_link(self.work_page_base,self.url_base,self.url_full)

        work_table = []
        exam_table = []
        admit_table = []
        for p_item in self.pages_link:
            table_ = get_work_page(p_item)
            work_table = self._get_work_table(self.url_base,table_,work_table,exam_table,admit_table)

        self.work_table=pd.DataFrame(work_table, columns=['召聘職稱','期限' ,"召聘單位" ,'報名簡章'])
        self.exam_table=pd.DataFrame(exam_table, columns=['召聘職稱','連結'])
        self.admit_table=pd.DataFrame(admit_table, columns=['召聘職稱','連結'])

    def _get_pages_link(self,soup,url_base,url_full):
        pages_link=[]
        pages_link.append(url_full)
        for o in soup.find("div",class_="pager").find_all("a"):
            if o.text == "下一頁" or o.text == "»":
                pass
            else:
                link = url_base+o.get('href')
                pages_link.append(link)
                #print(o.text,link)
        return pages_link

    def get_work_detail(self,link):
        try:
            time.sleep(random.uniform(1, 5))
            work_detail = get_work_page(link).find("div",class_="newContent").text
        except:
            return None
        if work_detail is None and work_detail.replace("\n","") == "":
            return None
        else:
            return get_work_page(link).find("div",class_="newContent").text.replace("\r","").replace("\t","").split("\n")



    def get_work_originazation(self,title,link):
        try:
            origination = re.search("((.*)[組,部,科,室,心])",title).group(1)
        except AttributeError:
            g = self.get_work_detail(link)
            if g == None:
                return "check page"
            try:
                origination = findjoboriginzation(g, self.name)
            except:
                origination = "check page"
        return origination.replace(self.name,"").replace("醫院","")



    def get_work_deadtime(self,link):
        g = self.get_work_detail(link)
        if g == None:
            return "check page"
        try:
            ggg = [gg for gg in g if gg != '']
            try:
                dead = re.findall("\d+年\d+月\d+日|\d+.\d+.\d+",ggg[ggg.index("上網期間")+1])[-1]
            except:
                for gggg in ggg:

                    if "上網期間" in gggg or "報名方式" in gggg or "報名人員請於" in gggg or "日前" in gggg or "報名日期" in gggg or "（含）前" in gggg:
                        try:
                            dead = re.findall("\d+年\d+月\d+日|\d+.\d+.\d+",[gg for gg in g if "上網期間" in gg or "報名方式" in gg or "報名日期" in gg or "（含）前" in gg][0].split("：")[-1])[-1]
                        except:
                            dead = "check page"
        except:
            dead = "check page"

        finally:
            if 'dead' not in locals():
                dead = "check page"
            return dead

    def _get_work_table(self,url_base,table_,work_table,exam_table,admit_table):
        for p_i, p_item in enumerate(table_.find_all("tr")):
            if p_item.find('a'):
                p_item_a = p_item.find('a')
                title = p_item_a.text
                link_s = url_base+p_item_a.get('href')
                if "錄取公告" in title or "甄試結果公告" in title or "核定" in title:
                    admit_table.append([title.replace("錄取公告：",""), link_s])
                elif '考試公告' in title:
                    exam_table.append([title.replace("考試公告：",""), link_s])
                else:
                    pass
                new_title = findjobtype(title, self.name).replace("部契約","契約")

                if self.get_work_detail(link_s) == None:
                    break
                origination = self.get_work_originazation(title,link_s)
                dead_line = self.get_work_deadtime(link_s)
                #print(p_i-1,new_title,link_s,dead_line, origination)
                work_table.append([new_title, dead_line, origination, link_s ])
        return work_table




