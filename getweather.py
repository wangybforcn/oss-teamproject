#!usr/bin/python
# -*- coding = utf-8 -*-

#首先，我不想写注释！！！！！！！

import requests
from bs4 import BeautifulSoup


def get_weather():
    url = 'https://search.naver.com/search.naver?'

    kw = {
        'query': '날씨'
    }

    headers1 = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    }

    response = requests.get(url, headers=headers1,params=kw)

    
    #上面为爬虫部分
    #下面为关键字检索部分
    
    soup = BeautifulSoup(response.content.decode(), 'lxml')
        
    with open('weatherinfo.txt','w+',encoding='utf-8') as info:
        info.truncate(0)
            
        weather_name = soup.body.find_all(class_= 'weather before_slash')
        for i in weather_name:
            ii = i.string
            info.write(ii)
        info.write('\n')

        weather_tmr = soup.body.find(class_ = 'temperature_text')        
        soup2 = BeautifulSoup(str(weather_tmr), "lxml")
        txttmr = soup2.get_text()
        info.write(txttmr)
        info.write('\n')

        weather_w = soup.body.find(class_ = 'temperature_info').select('dl')
        soup3 = BeautifulSoup(str(weather_w), "lxml")
        wind = soup3.dd.find_next(class_ = 'desc')
        wind = wind.find_next('dd')
        info.write(wind.get_text())
        info.write('\n')


def get_rain():
    rain = 'https://www.weather.go.kr/w/wnuri-fct2021/main/digital-forecast.do?'

    headers = {
    'Accept': 'text/html, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-TW,zh-CN;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6',
    'Connection': 'keep-alive',
    'Cookie': 'JSESSIONID=3GHyi2nFv9LIkLXQOmQL4QEqlS4NSToPrM00aoPt.standalone; XTVID=A221008140211914803; xloc=1920X1080; _harry_lang=zh-TW; _harry_fid=hh-1118589055; _TRK_UID=93c1ddfca21712e65be484450bf18be7:7; _TRK_SID=5a7d0e60fd0818baa85557362d629bd7; _TRK_CR=https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EA%B0%95%EC%88%98%EB%9F%89; _harry_ref=https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EA%B0%95%EC%88%98%EB%9F%89; _harry_url=https://www.weather.go.kr/w/weather/forecast/short-term.do; _harry_hsid=A221120104739993915; _harry_dsid=A221120104739993831; _TRK_EX=8',
    'Host': 'www.weather.go.kr',
    'Referer': 'https://www.weather.go.kr/w/index.do',
    'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
    }

    kw = {
        'code': '1159068000',
        'unit': 'm/s',
        'hr1': 'Y'
    }
    
    response = requests.get(rain, headers=headers, params=kw)
    
    #以上为爬取动态网页部分，kw参数code很重要！！

    soup = BeautifulSoup(response.content.decode(), 'lxml')
    rainlink = soup.body.find_all(class_ = 'item-wrap')
    souprainlink = BeautifulSoup(str(rainlink), 'lxml')

    with open('./weatherinfo.txt', 'a', encoding='utf-8') as f:
        f.write('\n')

        tagul = souprainlink.ul
        tagli = tagul.li
        for i in range(5):
            tagli = tagli.find_next('li')
        f.write(tagli.get_text())
        f.write('\n')
        i = 0

        
        #大循环数字决定爬取几个小时的数据
        for i in range(10):
            tagul = tagul.find_next('ul')
            tagli = tagul.li
            for i in range(5):
                tagli = tagli.find_next('li')
            f.write(tagli.get_text())
            f.write('\n')
            
