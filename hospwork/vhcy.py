#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import re
from hospwork.hospital_work import Hospital_work
from hospwork.tool.web import get_base_web_data,get_work_page

class Vhcy(Hospital_work):
    def __init__(self):
        self.name = '台北榮民總醫院'
        self.url_base='https://www.vhcy.gov.tw'
        self.url_work = '/PageView/RowView?WebMenuID=1c791b28-2968-49c9-8d5a-32dceca8ad1b'
        self.url_full = super().url()
        self.work_page_base = get_base_web_data(self.url_full)
        self.work_page_work_table = self.work_page_base.find("tbody")
        self.pages_link = self._get_pages_link(self.work_page_base,self.url_base,self.url_full)
        
        work_table=[]
        for p_i, p_item in enumerate(self.pages_link):
            table_ = get_work_page(p_item)

            work_table = self._get_work_table(self.url_base,table_,work_table)

        self.work_table=pd.DataFrame(work_table, columns=['召聘職稱','期限' ,"職缺單位" ,'報名簡章'])


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
        work_detail = get_work_page(link).find("div",class_="newContent").text
        if work_detail.replace("\n","") == "":
            return None
        else:
            return get_work_page(link).find("div",class_="newContent").text.replace("\r","").replace("\t","").split("\n")



    def get_work_title(self,title):
        try:
            new_title = re.search("\B[科,短,社,契,牙,秘,醫,部,室](.*)[員,理,工,師,生]",title).group(0)
        except AttributeError:
            print("ERROR:",title)
        return new_title



    def get_work_originazation(self,title,link):
        try:
            origination = re.search("((.*)[組,部,科,室,心])",title).group(1)
        except AttributeError:
            g = self.get_work_detail(link)
            if g == None:
                return "check page"
            try:
                origination = [gg for gg in g if "職稱" in gg][0].split("：")[-1]
            except AttributeError:
                ggg = [gg for gg in g if gg != '']
                origination = ggg[ggg.index("職稱")+1]
            except:
                origination = "check page"
        return origination



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

    def _get_work_table(self,url_base,table_,work_table):
        for p_i, p_item in enumerate(table_.find_all("tr")):
            if p_item.find('a'):
                p_item_a = p_item.find('a')
                title = p_item_a.text
                if "錄取公告" in title or '考試公告' in title or "甄試結果公告" in title or "核定" in title:
                    break
                new_title = self.get_work_title(title)
                link_s = url_base+p_item_a.get('href')
                if self.get_work_detail(link_s) == None:
                    break
                origination = self.get_work_originazation(title,link_s)
                dead_line = self.get_work_deadtime(link_s)
                #print(p_i-1,new_title,link_s,dead_line, origination)
                work_table.append([new_title, dead_line, origination, link_s ])
        return work_table




