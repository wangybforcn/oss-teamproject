import datetime
from getweather import *
import webbrowser
from bottle import template

now_month = datetime.datetime.now().month

get_weather()
get_rain()

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
                    rain_ = rain

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
print(ny, zj, wt, qk, wk)


def get_key(dict, value):
    return [k for k, v in dict.items() if v == value]


waitao = {
    "얇은 코트": 6,
    "두꺼운 코트": 8,
    "오버코트": 10,
    "솜저고리": 12,
    "패딩": 14
}

zuilicengyifu = {
    "반팔 셔츠": 2,
    "얇은 긴팔": 5,
    "두꺼운 긴팔": 8,
    "후드티": 11,
    "보온 내의": 14
}

zhongjiancengyifu = {
    "얇은 스웨터": 6,
    "두꺼운 스웨터": 8,
    "얇은 셔츠": 10,
    "두꺼운 셔츠": 12,
    "보온 셔츠": 14,
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
        rwaitao = 'buchuanwaitao'
        break
    if get_key(waitao, wt + i) == []:
        continue
    else:
        rwaitao = get_key(waitao, wt + i)
        break

# 中间层判断
for i in -1, 0, 1:
    if zj < 6:
        rzhong = 'buchuanzhongjian'
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
        rxiali = "buchuanqiuku"
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

print(rwaitao)
print(rzhong)
print(rli)
print(rxiali)
print(rkuzi)

if weather == "가끔 눈, 한때 눈" or weather == "가끔 비, 한때 비" or weather == "비 또는 눈" or weather == "가끔 비 또는 눈" or weather == "눈 또는 비" or weather == "한때 눈 또는 비" or weather == "눈날림":
    print("우산를 챙겨가세요")

if float(tmr) < 0:
    print("목도리 챙겨가세요")
    print("보온 모자 챙겨가세요")

weather.replace('\n', '').replace('\r', '')


#
#
#
#
#   html 편집구역
#
#
print(tmr)

GEN_HTML = "demo_1.html"
ss = "img/weather/"
ll = ".png"
tt: str = ss+weather+ll     # 그림의 이름
tt.replace('\n', '').replace('\r', '')

rain="10시간내 비 소식이 없습니다."

articles = [(tt ,weather, tmr,rain)]
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
            width: 160px;
            margin-left: 10px;

        }
        .pants{
            height: 110px;
            width: 160px;
            margin-left: 10px;
            margin-top: 10px;
        }
        .tools{

            height: 110px;
            width: 160px;
            margin-left: 10px;
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
            font-size: 20px;
        
        }

    </style>
</head>
<body>
    % for wear,weather,tmr,rain in items:
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

            <img src="" alt=""class="upclothes">
            <img src="" alt=""class="upclothes">
            <img src="" alt="" class="upclothes">


        </div>
        <div id="pant">

            <img src="" alt=""class="pants">
            <img src="" alt=""class="pants">

        </div>
        <div id="tool">

            <img src="" alt=""class="tools">
            <img src="" alt=""class="tools">
            <img src="" alt=""class="tools">
        </div>
    </div>
    <div id="bottom">
    </div>
    %end

</body>
</html>"""

print("html ")
html = template(template_demo, items=articles)
with open(GEN_HTML,'w') as f:
    f.write(html)


webbrowser.open(GEN_HTML)
