import json
import scrapy
import datetime as datetime

class DailySpider(scrapy.Spider):
    name = "daily"
    url = "https://www.hkex.com.hk/chi/csm/DailyStat/data_tab_daily_{}c.js"

    def generate_url(self, stock_num, month, day):
        if month < 10:
            month = "0"+ str(month)
        if day < 10:
            day = "0" + str(day)
        date ="2018" + str(month) + str(day)
        return self.url.format(date)

    def start_requests(self):
        for i in range (0, 3):
            for j in range (0, datetime.datetime.today().month + 1):
                for k in range (0, 32):
                    yield scrapy.Request(url=self.generate_url(i, j, k), callback=self.parse)

    def parse(self, response):
        print(response.url)
        r_body = response.body.decode("utf-8").split("=")[-1]
        jsonresponse = json.loads(r_body)
        print("Date: " + str(jsonresponse[0]['date']))
        for i in range (0, 4):
            if i == 0:
                print("滬股通")
            elif i == 1:
                print("港股通（滬)")
            elif i == 2:
                print("深股通")
            else:
                print("港股通（深)")
            print("買入成交額 (RMB mil): " + str(jsonresponse[i]['content'][0]['table']['tr'][1]['td'][0][0]))
            print("賣出成交額 (RMB mil): " + str(jsonresponse[i]['content'][0]['table']['tr'][2]['td'][0][0]))
            print("top 10")
            for rank in range(0, 10):
                print("Rank: " + str(rank + 1) + " Stock Name: " + str(jsonresponse[i]['content'][1]['table']['tr'][rank]['td'][0][2]) +
                      " 買入: " + str(jsonresponse[i]['content'][1]['table']['tr'][rank]['td'][0][3]) +
                      " 賣出:" + str(jsonresponse[i]['content'][1]['table']['tr'][rank]['td'][0][4]))
