import pyautogui
import time
import requests
import pyperclip
import hashlib
import datetime
import random


# send_message
def send_message(name, message):
    def openWechat(str1, str2, str3):
        pyautogui.keyDown(str1)
        pyautogui.keyDown(str2)
        pyautogui.keyDown(str3)
        pyautogui.keyUp(str1)
        pyautogui.keyUp(str2)
        pyautogui.keyUp(str3)

    def searchWechat():
        pyautogui.keyDown('ctrl')
        pyautogui.keyDown('f')
        pyautogui.keyUp('ctrl')
        pyautogui.keyUp('f')

    def paste():
        pyautogui.keyDown('ctrl')
        pyautogui.keyDown('v')
        pyautogui.keyUp('ctrl')
        pyautogui.keyUp('v')

    time.sleep(1)
    openWechat('ctrl', 'alt', 'w')
    searchWechat()
    pyperclip.copy(name)
    paste()
    time.sleep(1)
    pyautogui.press('\n')
    time.sleep(1)
    pyperclip.copy(message)
    paste()
    pyautogui.press('\n')
    openWechat('ctrl', 'alt', 'w')

# weather api


def find_message_weather():
    key = '6c1b4dd0cdb5803a54689c22f5433e9c'
    city = '310000'
    url_weather = f'https://restapi.amap.com/v3/weather/weatherInfo?city={city}&key={key}'
    response_weather = requests.get(url=url_weather)
    json_response = response_weather.json()
    city = json_response['lives'][0]['city']
    weather = json_response['lives'][0]['weather']
    temperature = json_response['lives'][0]['temperature']
    windpower = json_response['lives'][0]['windpower']
    data = {}
    appid = "20220603001237604"
    salt = "1"
    key = "UUdT2hvJIClmrtTGdoHw"
    name = f'今天{city}天气为{weather}，当前温度为{temperature}，当前风力为{windpower}。'
    data['q'] = name
    data['from'] = 'zh'
    data['to'] = 'en'
    data['appid'] = appid
    data['salt'] = salt
    sign = appid + name + salt + key
    sign = bytes(sign, encoding="utf8")
    data['sign'] = hashlib.md5(sign).hexdigest()
    url_translate = f"http://api.fanyi.baidu.com/api/trans/vip/translate"
    response_translate = requests.post(url=url_translate, data=data)
    translate_word_weather = response_translate.json()[
        'trans_result'][0]['dst']
    return translate_word_weather

# translate api


def translate(name):
    data = {}
    appid = "20220603001237604"
    salt = "1"
    key = "UUdT2hvJIClmrtTGdoHw"
    data['q'] = name
    data['from'] = 'zh'
    data['to'] = 'en'
    data['appid'] = appid
    data['salt'] = salt
    sign = appid + name + salt + key
    sign = bytes(sign, encoding="utf8")
    data['sign'] = hashlib.md5(sign).hexdigest()
    url_translate = f"http://api.fanyi.baidu.com/api/trans/vip/translate"
    response_translate = requests.post(url=url_translate, data=data)
    translate_word = response_translate.json()['trans_result'][0]['dst']
    return translate_word


def birthday_wishes():
    with open(r'D:\bigdata\final\wishes.txt', 'r', encoding='utf-8') as f:
        datas = f.readlines()
        data = datas.pop(-1)
    with open(r'D:\bigdata\final\wishes.txt', 'w', encoding='utf-8') as f:
        for i in datas:
            f.write(i)
    return data


def choose(s):
    if (u'\u0041' <= s <= u'\u005a') or (u'\u0061' <= s <= u'\u007a'):
        return 1
    return 0

# everyday learn english


def everyday():
    data = {}
    data['count'] = '10'
    data['app_id'] = 'ptulcuqtlflgu9rn'
    data['app_secret'] = 'OTExajJNNnQ5S2VKUUZWK2wxdGlHdz09'
    url = 'https://www.mxnzp.com/api/daily_word/recommend'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.30"
    }
    response = requests.get(url=url, headers=headers,
                            params=data)  # ,params=data)
    sentences = response.json()['data']
    for sentence in sentences:
        count = 0
        for s in sentence['content']:
            count += choose(s)
        if count >= 10:
            continue
        else:
            return sentence['content']


if __name__ == '__main__':

    # =====================================================================
    # Birthday, corresponding to month, day, hour
    birthday = ['06', '08', '00']
    # Username
    user = 'Girl'
    # interval between each judgment
    sleep = 1
    # Time to send good morning and weather(00-24)

    time_weather = '7'
    # Time to send a daily sentence of English(00-24)
    time_every = '13'
    # =====================================================================

    choose_birthday = True
    choose_weather = True
    choose_day = True
    while 1:
        time_day = datetime.datetime.now().strftime("%m-%d-%H").split('-')
        if time_day[-1] == time_weather:
            if choose_weather:
                message_weather = find_message_weather()
                with open(r'D:\bigdata\final\morning.txt', 'r', encoding='utf-8') as f:
                    datas = f.readlines()
                    data = random.choice(datas)
                message = f"{data}\n" \
                          f"weather:{message_weather}\n"
                send_message(user, message)
                choose_weather = False
        else:
            choose_weather = True

        if time_day[-1] == time_every:
            if choose_day:
                sentence = everyday()
                time.sleep(1)
                sentence_translate = translate(sentence)
                message = f"sentence:{sentence}\n" \
                          f"sentence_translate:{sentence_translate}"
                send_message(user, message)
                choose_day = False
        else:
            choose_day = True

        if time_day == birthday:
            if choose_birthday:
                message = birthday_wishes()
                send_message(user, message)
                choose_birthday = False
        else:
            choose_1 = True
        time.sleep(sleep)
