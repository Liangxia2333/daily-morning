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
 response = requests.get(html)
    content = response.content.decode("utf-8")
    aim = re.findall(
        r'<input type="hidden" id="hidden_title" value="(.*?)月(.*?)日(.*?)时(.*?) (.*?)  (.*?)  (.*?)"', content)
    airdata = re.findall(
        r'<li class="li6">\n<i></i>\n<span>(.*?)</span>\n<em>(.*?)</em>\n<p>(.*?)</p>', content)
    ult_index = re.findall(
        r'<li class="li1">\n<i></i>\n<span>(.*?)</span>\n<em>(.*?)</em>\n<p>(.*?)</p>\n</li>', content)
    cloth_index = re.findall(
        r'<i></i>\n<span>(.*?)</span>\n<em>(.*?)</em>\n<p>(.*?)</p>\n</a>\n</li>\n<li class="li4">', content)
    # wash_index = re.findall(r'<li class="li4">\n<i></i>\n<span>(.*?)</span>\n<em>(.*?)</em>\n<p>(.*?)</p>', content)
    lose_index = re.findall(
        r'</span>\n<em>(.*?)</em>\n<p>(.*?)</p>\n</a>\n</li>\n<li class="li5">', content)
    # print(lose_index)
    txt1 = '@天气预报:'+'\n'
    txt2 = '天气情况: '+aim[0][5]+'\n'+'温度情况: '+aim[0][6]+'\n'
    txt3 = '穿衣指数: '+cloth_index[0][0]+', '+cloth_index[0][2]+'\n'
    txt4 = '减肥指数：' + lose_index[0][1]+'\n'
    txt5 = '空气指数: '+airdata[0][0]+', '+airdata[0][2]+'\n'
    txt6 = '紫外线指数: '+ult_index[0][0]+', '+ult_index[0][2]+'\n'

    # txt7 = '洗车指数: '+wash_index[0][0]+', '+wash_index[0][2]+'\n'

    more_information = '\n'+txt1+txt2+txt3+txt4+txt5+txt6
    return more_information(weather['temp'])

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


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
