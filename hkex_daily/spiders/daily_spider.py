import json
import scrapy
import datetime as datetime
from hkex_daily.items import Daily, DailyTop10

class DailySpider(scrapy.Spider):
    name = "daily"
    url = "https://www.hkex.com.hk/chi/csm/DailyStat/data_tab_daily_{}c.js"
    url_rb= "http://www.hkex.com.hk/chi/csm/DailyStat/data_tab_daily_{}c.js?_=1531573908835"

    def generate_url(self, stock_num, month, day):
        if month < 10:
            month = "0"+ str(month)
        if day < 10:
            day = "0" + str(day)
        date ="2018" + str(month) + str(day)
        return self.url_rb.format(date)

    def start_requests(self):
        for i in range (0, 3):
            for j in range (0, datetime.datetime.today().month + 1):
                for k in range (0, 32):
                    yield scrapy.Request(url=self.generate_url(i, j, k), callback=self.parse)

    def parse(self, response):
        print(response.url)
        r_body = response.body.decode("utf-8").split("=")[-1]
        jsonresponse = json.loads(r_body)
        if str(jsonresponse[0]['content'][0]['table']['tr'][1]['td'][0][0]) == "-":
            return

        itemTop = DailyTop10()
        daily = Daily()

        print("Date: " + str(jsonresponse[0]['date']))
        itemTop['date'] = str(jsonresponse[0]['date'])
        daily['date'] = str(jsonresponse[0]['date'])

        for i in range (0, 4):
            if i == 0:
                print("滬股通")
                daily["area"] = "滬股通"
                itemTop["area"] = "滬股通"
            elif i == 1:
                print("港股通（滬)")
                daily["area"] = "港股通（滬)"
                itemTop["area"] = "港股通（滬)"
            elif i == 2:
                print("深股通")
                daily["area"] = "深股通"
                itemTop["area"] = "深股通"
            else:
                print("港股通（深)")
                daily["area"] = "港股通（深)"
                itemTop["area"] = "港股通（深)"

            print("買入成交額 (RMB mil): " + str(jsonresponse[i]['content'][0]['table']['tr'][1]['td'][0][0]))
            daily["buy_in"] = str(jsonresponse[i]['content'][0]['table']['tr'][1]['td'][0][0])
            print("賣出成交額 (RMB mil): " + str(jsonresponse[i]['content'][0]['table']['tr'][2]['td'][0][0]))
            daily["buy_out"] = str(jsonresponse[i]['content'][0]['table']['tr'][2]['td'][0][0])
            print("top 10")
            for rank in range(0, 10):
                itemTop["rank"] = str(jsonresponse[i]['content'][1]['table']['tr'][rank]['td'][0][0])
                itemTop["stock_code"] = str(jsonresponse[i]['content'][1]['table']['tr'][rank]['td'][0][1])
                itemTop["name"] = str(jsonresponse[i]['content'][1]['table']['tr'][rank]['td'][0][2])
                itemTop["buy_in"] = str(jsonresponse[i]['content'][1]['table']['tr'][rank]['td'][0][3])
                itemTop["buy_out"] = str(jsonresponse[i]['content'][1]['table']['tr'][rank]['td'][0][4])
                itemTop["turnover"] = str(jsonresponse[i]['content'][1]['table']['tr'][rank]['td'][0][5])

                print("Rank: " + str(jsonresponse[i]['content'][1]['table']['tr'][rank]['td'][0][0]) + " Stock Name: " + str(jsonresponse[i]['content'][1]['table']['tr'][rank]['td'][0][2]) +
                      " 買入: " + str(jsonresponse[i]['content'][1]['table']['tr'][rank]['td'][0][3]) +
                      " 賣出:" + str(jsonresponse[i]['content'][1]['table']['tr'][rank]['td'][0][4]))
                yield itemTop
            yield daily
