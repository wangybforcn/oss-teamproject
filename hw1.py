import datetime
from getweather import *
import webbrowser

now_month = datetime.datetime.now().month

get_weather()

with open('./weatherinfo.txt', 'r', encoding='utf-8') as w:
    for time in range(3):
        if time == 0:
            weather = w.readline()
            weather = weather.strip('\n')
        elif time == 1:
            tmr = w.readline()
            tmr = tmr[6:-3]
        elif time == 2:
            wind = w.readline()
            wind = wind[:-4]

float(tmr)
print(weather,end="")
print("온도:" + tmr)
print("풍력:" + wind)


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
    "얇은 속바지": 6,
    "두꺼운 속바지": 9,
    "따뜻한 속바지": 12,
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
GEN_HTML = "demo_1.html"
ll = ".png"
tt = weather+ll
tt.replace('\n', '').replace('\r', '')

print(tt)

f = open(GEN_HTML, 'w+')
message = """
<html>
<head>
    <title>옷차림</title>
</head>

<body>

    <img src="%s" alt="">
</body>
</html>
""" % (tt)

f.write(message)
f.close()

webbrowser.open(GEN_HTML, new=1)
