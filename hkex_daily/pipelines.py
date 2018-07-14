# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
from hkex_daily import items

class HkexDailyPipeline(object):

    def __init__(self):
        self.brandCategoryCsv = csv.writer(open('Daily.csv', 'w'))
        self.brandCategoryCsv.writerow(["地區", "日期", "買入成交額 (RMB mil)", "賣出成交額 (RMB mil)"])

        self.brandsCsv = csv.writer(open('Top10Daily.csv', 'w'))
        self.brandsCsv.writerow(
            ['地區', '日期', '排名', '股票代碼', '股票名稱', '買入金額(RMB)', '賣出金額(RMB)', '買入及賣出金額(RMB)'])

    def process_item(self, item, spider):
        if isinstance(item, items.Daily):
            self.brandCategoryCsv.writerow([item['area'], item['date'], item['buy_in'], item['buy_out']])
            return item
        if isinstance(item, items.DailyTop10):
            self.brandsCsv.writerow([item['area'], item['date'], item['rank'], item['stock_code'], item['name'], item['buy_in'], item['buy_out'], item['turnover']])
            return item
