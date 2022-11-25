#!/usr/bin/python
# -*- coding ='utf-8' -*-

import datetime
from getweather import *
import webbrowser
from bottle import template


get_weather()
get_rain()

now_month = datetime.datetime.now().month

with open('./weatherinfo.txt', 'r', encoding='utf-8') as w:
    rain_ = 0
    for time in range(15):
        if time == 0:
            weather = w.readline()
            weather = weather.strip('\n')
        elif time == 1:
            tmr = w.readline()
            tmr = tmr[6:-3]
        elif time == 2:
            wind = w.readline()
            wind = wind[:-4]
        elif time > 2:
            rain = w.readline()
            rain = rain[6:-2]
            if not rain is "" and int(rain) > 0:
                if int(rain) > rain_:
                    rain_ = int(rain)

#weather为天气
#tmr为温度
#wind为风速
#如果rain_返回了未来十小时的下雨百分比，返回了该比例的最大值，大于0则有雨
                    
          
def jijie(now_month):
    if now_month == 3 or now_month == 4:
        return 1
    elif now_month == 5 or now_month == 6 or now_month == 7 or now_month == 8:
        return 2
    elif now_month == 9 or now_month == 10:
        return 3
    elif now_month == 11 or now_month == 12 or now_month == 1 or now_month == 2:
        return 4


jj = jijie(now_month)

num = 0
shang = 0
xia = 0


def chuanyizhishu(jj, wendu):
    global shang
    global xia
    num = (4 + ((30 - float(wendu)) * 2)) / 10
    if jj == 1 or jj == 3:
        shang = num * 4
        xia = num * 2
    elif jj == 2:
        shang = num * 5
        xia = num * 5
    elif jj == 4:
        shang = num * 5
        xia = num * 3


chuanyizhishu(jj, tmr)

neiyi = 0
zhong = 0
waitao = 0
qiuku = 0
waiku = 0


def chuanjiceng(jj, shang, xia):
    global neiyi
    global zhong
    global waitao
    global qiuku
    global waiku
    if jj == 1 or jj == 3:
        neiyi = shang / 2
        waitao = shang / 2
        waiku = xia
    elif jj == 2:
        neiyi = shang
        waiku = xia
    elif jj == 4:
        neiyi = shang / 3
        zhong = shang / 3
        waitao = shang / 3
        qiuku = xia / 2
        waiku = xia / 2


chuanjiceng(jj, shang, xia)
ny = int(neiyi)
zj = int(zhong)
wt = int(waitao)
qk = int(qiuku)
wk = int(waiku)


def get_key(dict, value):
    return [k for k, v in dict.items() if v == value]


waitao = {
    "얇은 코트": 6,
    "두꺼운 코트": 8,
    "오버코트": 10,
    "솜저고리": 12,
    "패딩": 14
}

zhongjiancengyifu = {
    "얇은 스웨터": 6,
    "두꺼운 스웨터": 8,
    "얇은 셔츠": 10,
    "두꺼운 셔츠": 12,
    "보온 셔츠": 14,
}

zuilicengyifu = {
    "반팔 셔츠": 2,
    "얇은 긴팔": 5,
    "두꺼운 긴팔": 8,
    "후드티": 11,
    "보온 내의": 14
}

qiuku = {
    "얇은 내복 바지": 6,
    "두꺼운 내복 바지": 9,
    "따뜻한 바지": 12,
    "솜털 속바지": 15,
}

kuzi = {
    "반바지": 2,
    "얇은 바지": 5,
    "두꺼운 바지": 9,
    "핫바지": 12,
    "패딩 바지": 15
}

# 外衣判断
for i in -1, 0, 1:
    if wt < 6:
        rwaitao = 'not'
        break
    if get_key(waitao, wt + i) == []:
        continue
    else:
        rwaitao = get_key(waitao, wt + i)
        break

# 中间层判断
for i in -1, 0, 1:
    if zj < 6:
        rzhong = 'not'
        break

    if get_key(zhongjiancengyifu, zj + i) == []:
        continue
    else:
        rzhong = get_key(zhongjiancengyifu, zj + i)
        break

# 里层衣判断
for i in -1, 0, 1:
    if get_key(zuilicengyifu, ny + i) == []:
        continue
    else:
        rli = get_key(zuilicengyifu, ny + i)
        break

# 秋裤判断
for i in -1, 0, 1:
    if qk < 6:
        rxiali = "not"
        break
    if get_key(qiuku, qk + i) == []:
        continue
    else:
        rxiali = get_key(qiuku, qk + i)
        break

# 外裤判断
for i in 0, -1, 1, -2, 2:
    if get_key(kuzi, wk + i) == []:
        continue
    else:
        rkuzi = get_key(kuzi, wk + i)
        break
rwaitao = ''.join(rwaitao)
rzhong = ''.join(rzhong)    
rli = ''.join(rli)
rxiali = ''.join(rxiali)
rkuzi = ''.join(rkuzi)

we = "img/weather/"
clo = "img/closthes/"
png = ".png"


# 우산 , 목도리  모자
if weather == "가끔 눈, 한때 눈" or weather == "가끔 비, 한때 비" or weather == "비 또는 눈" or weather == "가끔 비 또는 눈" or weather == "눈 또는 비" or weather == "한때 눈 또는 비" or weather == "눈날림" or weather == "가끔 비 또는 눈,한때 비 또는 눈" or weather =="가끔 눈 또는 비,한때 눈 또는 비" or weather == "비" or weather == "눈" or weather == "빗방울":
    unb = clo+"우산"+png
if rain_ > 0:
    rainmsg = "미래 10시간 강수확률: " + str(rain_) + "% 입니다."
    unb = clo+"우산"+png
else:
    rainmsg="10시간내 비 소식이 없습니다."
    nub = clo+"not"+png
    
if float(tmr) < 0:
    scarf = clo+"목도리"+png
    hat = clo+"모자"+png
else:
    scarf = clo+"not"+png
    hat=clo+"not"+png

weather.replace('\n', '').replace('\r', '')

# 코드 그림 선택
if rwaitao == "얇은 코트" or rwaitao == "두꺼운 코트" or rwaitao=="오버코트":
    closthes1 = clo+"코트"+png
    rwaitao = rwaitao + ","
elif rwaitao == "솜저고리":
    closthes1 = clo+rwaitao+png
    rwaitao = rwaitao + ","
elif rwaitao == "패딩":
    closthes1 =clo+rwaitao+png
    rwaitao = rwaitao + ","
elif rwaitao == 'not':
    closthes1 = clo+rwaitao+png
    rwaitao = ""



# 중간층 그림
if rzhong == "얇은 스웨터" or rzhong == "두꺼운 스웨터" :
    closthes2 = clo+"스웨터"+png
    rzhong = rzhong + ","
elif rzhong == "얇은 셔츠" or rzhong == "두꺼운 셔츠" or rzhong ==  "보온 셔츠":
    closthes2 = clo+"셔츠"+png
    rzhong = rzhong + ","
elif rzhong == "not":
    closthes2 = clo+rzhong+png
    rzhong = ""
    
# 맨 안에 층
if rli =="얇은 긴팔" or rli == "두꺼운 긴팔" or rli == "보온 내의":
    closthes3 = clo+"긴팔 셔츠"+png
elif rli == "반팔 셔츠":
    closthes3 = clo+rli+png
elif rli == "후드티":
    closthes3 = clo+rli+png
elif rli == "not":
    closthes3 = clo+rli+png
    rli = ""

if rkuzi =="패딩 바지" or rkuzi=="핫바지" or rkuzi == "두꺼운 바지" or rkuzi == "얇은 바지":
    pants1=clo+"바지"+png
    rkuzi = rkuzi + ","
elif rkuzi == "반바지":
    pants1 = clo+rkuzi+png
    rkuzi = ""
    


if rxiali != "not":
    pants2 = clo+"내복 바지"+png
else:
    pants2 = clo+rxiali+png
    rxiali = ""






#   html 편집구역



GEN_HTML = "demo_1.html"



tt: str = we+weather+png     # 그림의 이름
tt.replace('\n', '').replace('\r', '')





articles = [(tt ,weather,tmr,rainmsg,closthes1,closthes2,closthes3,pants1,pants2,unb,scarf,hat)]
articles2 = [(rwaitao,rzhong,rli,rkuzi,rxiali)]
template_demo= """
<!DOCTYPE html>
<html>
<head>
    <title>옷차림
    </title>
    <style>
        body{
            background-color: bisque;
        }
        #top{
            height: 130px;;
            width: 630px;
            background-color: rgb(136, 241, 122);
            margin: auto;
            margin-top: 50px;
            border-radius:25px;
            position: relative;
        }
        #weimg{
            height: 130px;;
            width: 200px;
            margin-left: 40px;
            /* background-color: aqua; */
            position: absolute;
            border-radius:25px;
        }
        #wetext{
            height: 130px;;
            width: 200px;
            margin-left: 260px;
            border-radius:25px;
            /* background-color: rgb(235, 212, 162); */
            position:absolute;
        }
        #werain{
            height: 130px;;
            width: 100px;
            margin-left: 480px;
            border-radius:25px;
            /* background-color: rgb(103, 22, 141); */
            position:absolute;
        }
        #main{
            height: 390px;;
            width: 630px;
            background-color: rgb(136, 241, 122);
            margin: auto;
            border-radius:25px;
            position: relative;
            margin-top: 20px;

        }

        #clothes{

            height: 390px;;
            width: 180px;
            margin-left: 25px;
            border-radius:25px;
            background-color:rgb(228, 245, 76);
            border: 1px solid;
            position:absolute;
        }
        #pant{
            height: 390px;;
            width: 180px;
            margin-left: 220px;
            border-radius:25px;
            background-color:rgb(228, 245, 76);
            border: 1px solid;
            position:absolute;
        }

        #tool{
            height: 390px;;
            width: 180px;
            margin-left: 415px;
            border-radius:25px;
            border: 1px solid;
            position:absolute;
            background-color:rgb(228, 245, 76);
        }
        #wepng{
            margin-left: 20%;
        }
        #weather{
            text-align: center;
            font-size: 20px;
        }
        #temperature{
            text-align: center;
            font-size: 20px;

        }
        .upclothes{
            margin-top: 10px;
            height: 110px;
            width: 110px;
            margin-left: 35px;

        }
        .pants{
            height: 110px;
            width: 110px;
            margin-left: 35px;
            margin-top: 10px;
        }
        .tools{

            height: 110px;
            width: 110px;
            margin-left: 35px;
            margin-top: 10px;
        }
        #bottom{
            height: 130px;;
            width: 630px;
            background-color: rgb(136, 241, 122);
            margin: auto;
            margin-top: 20px;
            border-radius:25px;
            position: relative;
        }
        #rain{
            text-align: center;
            font-size: 15px;
        
        }
        #bottomtext{
            height: 110px;;
            width: 600px;
            background-color: rgb(228, 245, 76);
            margin: 0 auto;
            margin-top: 10px;
            margin-left: 15px;
            border-radius:25px; border: 1px solid;
            position:absolute;
        }
        .msg{
            margin-left:15px;
        }

    </style>
</head>
<body>
    % for wear,weather,tmr,rain,closthes1,closthes2,closthes3,pants1,pants2,unb,scarf,hat in items:
    <div id="top">
        <div id="weimg">
            <img src="{{wear}}" alt="" id="wepng">
        </div>

        <div id="wetext">
            <p id="weather">{{weather}}</p>
            <p id = "temperature">현제온도 {{tmr}}°C</p>
        </div>

        <div id="werain"><P id="rain">{{rain}}</p></div>
    </div>
    <div id="main">
        <div id="clothes">

            <img src="{{closthes1}}" alt=""class="upclothes">
            <img src="{{closthes2}}" alt=""class="upclothes">
            <img src="{{closthes3}}" alt="" class="upclothes">


        </div>
        <div id="pant">

            <img src="{{pants1}}" alt=""class="pants">
            <img src="{{pants2}}" alt=""class="pants">

        </div>
        <div id="tool">

            <img src="{{unb}}" alt=""class="tools">
            <img src="{{scarf}}" alt=""class="tools">
            <img src="{{hat}}" alt=""class="tools">
        </div>
    </div>
    %end
    %for rwaitao,rzhong,rli,rkuzi,rxiali in item:
    <div id="bottom">
        <div id="bottomtext">
            <p class = "msg">  오늘 추천 상의 : {{rwaitao}}&nbsp&nbsp{{rzhong}}&nbsp&nbsp{{rli}} </p>
            <p class= "msg">  오늘 추천 바지 : &nbsp&nbsp&nbsp&nbsp{{rkuzi}}&nbsp&nbsp{{rxiali}} </p>
        
            
    
            
        </div>
    </div>
    %end

</body>
</html>"""


html = template(template_demo, items=articles, item=articles2)
with open(GEN_HTML,'w', encoding='utf-8') as f:
    f.write(html)


webbrowser.open(GEN_HTML)
