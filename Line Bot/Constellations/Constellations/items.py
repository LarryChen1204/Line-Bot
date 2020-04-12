# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ConstellationsItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    date = scrapy.Field()
    whole_star = scrapy.Field()
    whole_desc = scrapy.Field()
    love_star = scrapy.Field()
    love_desc = scrapy.Field()
    work_star = scrapy.Field()
    work_desc = scrapy.Field()
    money_star = scrapy.Field()
    money_desc = scrapy.Field()
