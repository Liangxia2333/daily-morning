from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

def getDate():
    """
    Get date: solar + lunar calendar
    :return: String calendar
    """
    ymc = [u"十一", u"十二", u"正", u"二", u"三", u"四",
           u"五", u"六", u"七", u"八", u"九", u"十"]

    rmc = [u"初一", u"初二", u"初三", u"初四", u"初五", u"初六", u"初七", u"初八", u"初九", u"初十",
           u"十一", u"十二", u"十三", u"十四", u"十五", u"十六", u"十七", u"十八", u"十九",
           u"二十", u"廿一", u"廿二", u"廿三", u"廿四", u"廿五", u"廿六", u"廿七", u"廿八", u"廿九", u"三十", u"卅一"]

    numCn = ["天", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]

    # 获取阳历和阴历
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    lunar = sxtwl.Lunar()
    date_lunar = lunar.getDayBySolar(year, month, day)

    print_date = str(date_lunar.y) + "年" + str(date_lunar.m) + \
        "月" + str(date_lunar.d) + "日"

    if date_lunar.Lleap:
        print_lunar = "润" + ymc[date_lunar.Lmc] + \
            "月" + rmc[date_lunar.Ldi] + "日"
    else:
        print_lunar = ymc[date_lunar.Lmc] + "月" + rmc[date_lunar.Ldi] + "日"

    print_week = "星期" + numCn[date_lunar.week]

    calendar = '日期：' + print_date + ', ' + print_week + '\n' + \
        '农历: ' + print_lunar + '\n'

    return calendar


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
