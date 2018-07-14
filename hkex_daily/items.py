# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class Daily(Item):
    area= Field()
    date = Field()
    rank = Field()
    buy_in = Field()
    buy_out = Field()

class DailyTop10(Item):
    area = Field()
    date = Field()
    rank = Field()
    name = Field()
    stock_code = Field()
    buy_in = Field()
    buy_out = Field()
    turnover = Field()

