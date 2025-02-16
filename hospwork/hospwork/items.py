# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from dataclasses import dataclass

class HospworkItem(scrapy.Item):
    # define the fields for your item here like:
    data_source = scrapy.Field()
    hosp_name = scrapy.Field()
    job_name = scrapy.Field()
    job_link = scrapy.Field()
    job_deadline = scrapy.Field()
    hosp_region = scrapy.Field()
    job_originzation = scrapy.Field()