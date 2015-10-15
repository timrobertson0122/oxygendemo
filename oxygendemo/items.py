# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class OxygendemoItem(scrapy.Item):
    # define the fields for your item here:
    code = scrapy.Field()
    description = scrapy.Field()
    designer = scrapy.Field()
    gender = scrapy.Field()
    images = scrapy.Field()
    link = scrapy.Field()
    name = scrapy.Field()
    usd_price = scrapy.Field()
    raw_color = scrapy.Field()
    sale_discount = scrapy.Field()
    stock_status = scrapy.Field()
    product_type = scrapy.Field()