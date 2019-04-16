# -*- coding: utf-8 -*-
import random
import configparser
import os
import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# 小偶像名字
def idol_name():
    BASE_DIR = os.path.dirname(__file__)
    file_path = os.path.join(BASE_DIR, 'setting.conf')
    cf = configparser.ConfigParser()
    # with open(file_path, 'r') as cfgfile:
    with open(file_path, 'r', encoding='utf-8') as cfgfile:
        cf.readfp(cfgfile)
        # idol name
        idol_name = cf.get('idol', 'name')
    return str(idol_name)


# ----------------------摩点微打赏设置----------------------


# # 摩点名称
# def wds_name():
#     BASE_DIR = os.path.dirname(__file__)
#     file_path = os.path.join(BASE_DIR, 'setting.conf')
#     cf = configparser.ConfigParser()
#     # with open(file_path, 'r') as cfgfile:
#     with open(file_path, 'r', encoding='utf-8') as cfgfile:
#         cf.readfp(cfgfile)
#         # modian
#         modian_name = cf.get('modian', 'name')
#         # modian_url = cf.get('modian', 'url')
#         # pro_id = cf.get('modian', 'pro_id')
#     return str(modian_name)
# 
# 
# # 摩点网址 建议使用短网址
# def wds_url():
#     BASE_DIR = os.path.dirname(__file__)
#     file_path = os.path.join(BASE_DIR, 'setting.conf')
#     cf = configparser.ConfigParser()
#     # with open(file_path, 'r') as cfgfile:
#     with open(file_path, 'r', encoding='utf-8') as cfgfile:
#         cf.readfp(cfgfile)
#         # modian
#         # modian_name = cf.get('modian', 'name')
#         modian_url = cf.get('modian', 'url')
#         # pro_id = cf.get('modian', 'pro_id')
#     return str(modian_url)


# 摩点项目对应pro_id
def pro_id():
    BASE_DIR = os.path.dirname(__file__)
    file_path = os.path.join(BASE_DIR, 'setting.conf')
    cf = configparser.ConfigParser()
    # with open(file_path, 'r') as cfgfile:
    with open(file_path, 'r', encoding='utf-8') as cfgfile:
        cf.readfp(cfgfile)
        # modian
        # modian_name = cf.get('modian', 'name')
        # modian_url = cf.get('modian', 'url')
        pro_id = cf.get('modian', 'pro_id')
        array = list(map(int, pro_id.split(',')))
    return (array)


# 摩点查询时间间隔读取
def md_interval():
    BASE_DIR = os.path.dirname(__file__)
    file_path = os.path.join(BASE_DIR, 'setting.conf')
    cf = configparser.ConfigParser()
    with open(file_path, 'r', encoding='utf-8') as cfgfile:
        cf.readfp(cfgfile)
        # modian
        interval = cf.get('modian', 'interval')
    return int(interval)


# # 获取配置中存储的集资消息时间
# def read_md_time10():
#     BASE_DIR = os.path.dirname(__file__)
#     file_path = os.path.join(BASE_DIR, 'setting.conf')
#     cf = configparser.ConfigParser()
#     with open(file_path, 'r', encoding='utf-8') as cfgfile:
#         cf.readfp(cfgfile)
#         msgtime = cf.get('modian', 'time')
#     return int(msgtime)
# 
# 
# # 写入配置中存储的集资消息时间
# def write_md_time10(msgtime10):
#     BASE_DIR = os.path.dirname(__file__)
#     file_path = os.path.join(BASE_DIR, 'setting.conf')
#     cf = configparser.ConfigParser()
#     with open(file_path, 'r', encoding='utf-8') as cfgfile:
#         cf.readfp(cfgfile)
#         with open(file_path, 'w+', encoding='utf-8') as cfgfile2:
#             cf.set('modian', 'time', str(msgtime10))
#             cf.write(cfgfile2)


# --------------------------------------------------------


# ----------------------口袋48设置----------------------


# 口袋48:roomId
def roomId():
    BASE_DIR = os.path.dirname(__file__)
    file_path = os.path.join(BASE_DIR, 'setting.conf')
    cf = configparser.ConfigParser()
    # with open(file_path, 'r') as cfgfile:
    with open(file_path, 'r', encoding='utf-8') as cfgfile:
        cf.readfp(cfgfile)
        roomId = cf.get('koudai48', 'roomId')
        ownerId = cf.get('koudai48', 'ownerId')
    return int(roomId), int(ownerId)


# 获取配置中存储的口袋房间消息时间
def read_kdmsg_time13():
    BASE_DIR = os.path.dirname(__file__)
    file_path = os.path.join(BASE_DIR, 'setting.conf')
    cf = configparser.ConfigParser()
    with open(file_path, 'r', encoding='utf-8') as cfgfile:
        cf.readfp(cfgfile)
        msgtime = cf.get('koudai48', 'msgTime')
    return int(msgtime)


# 写入配置中存储的口袋房间消息时间
def write_kdmsg_time13(msgtime13):
    BASE_DIR = os.path.dirname(__file__)
    file_path = os.path.join(BASE_DIR, 'setting.conf')
    cf = configparser.ConfigParser()
    with open(file_path, 'r', encoding='utf-8') as cfgfile:
        cf.readfp(cfgfile)
        with open(file_path, 'w+', encoding='utf-8') as cfgfile2:
            cf.set('koudai48', 'msgTime', str(msgtime13))
            cf.write(cfgfile2)


# 获取配置中存储的token
def token():
    BASE_DIR = os.path.dirname(__file__)
    file_path = os.path.join(BASE_DIR, 'setting.conf')
    cf = configparser.ConfigParser()
    # with open(file_path, 'r') as cfgfile:
    with open(file_path, 'r', encoding='utf-8') as cfgfile:
        cf.readfp(cfgfile)
        # koudai48
        # user = cf.get('koudai48', 'user')
        # password = cf.get('koudai48', 'password')
        token = cf.get('koudai48', 'token')
    return str(token)


# 验证token
def token_verify():
    BASE_DIR = os.path.dirname(__file__)
    file_path = os.path.join(BASE_DIR, 'setting.conf')
    cf = configparser.ConfigParser()
    # with open(file_path, 'r') as cfgfile:
    with open(file_path, 'r', encoding='utf-8') as cfgfile:
        cf.readfp(cfgfile)
        # koudai48
        # user = cf.get('koudai48', 'user')
        # password = cf.get('koudai48', 'password')
        token = cf.get('koudai48', 'token')

    url = 'https://pocketapi.48.cn/im/api/v1/chatroom/msg/list/homeowner'
    form = {
        'ownerId': 63558,
        'roomId': 67313743
    }
    header = {
        'Host': 'pocketapi.48.cn',
        'accept': '*/*',
        'Accept-Language': 'zh-Hans-CN;q=1',
        'User-Agent': 'PocketFans201807/6.0.0 (iPhone; iOS 12.2; Scale/2.00)',
        'Accept-Encoding': 'gzip, deflate',
        'appInfo': '{"vendor":"apple","deviceId":"0","appVersion":"6.0.0","appBuild":"190409","osVersion":"12.2.0","osType":"ios","deviceName":"iphone","os":"ios"}',
        'Content-Type': 'application/json;charset=utf-8',
        'Connection': 'keep-alive',
        'token': token
    }
    response = requests.post(
            url,
            data=json.dumps(form),
            headers=header,
            verify=False,
            timeout=15).json()
    if response['status'] == 200:
        return True
    else:
        return False


# 获取新token
def getNewToken():
    BASE_DIR = os.path.dirname(__file__)
    file_path = os.path.join(BASE_DIR, 'setting.conf')
    cf = configparser.ConfigParser()
    # with open(file_path, 'r') as cfgfile:
    with open(file_path, 'r', encoding='utf-8') as cfgfile:
        cf.readfp(cfgfile)
        # koudai48
        user = cf.get('koudai48', 'user')
        password = cf.get('koudai48', 'password')
        # token = cf.get('koudai48', 'token')
        # request
        ajax_url = "https://pocketapi.48.cn/user/api/v1/login/app/mobile"
        header = {
            'Host': 'pocketapi.48.cn',
            'accept': '*/*',
            'Accept-Language': 'zh-Hans-CN;q=1',
            'User-Agent': 'PocketFans201807/6.0.0 (iPhone; iOS 12.2; Scale/2.00)',
            'Accept-Encoding': 'gzip, deflate',
            'appInfo': '{"vendor":"apple","deviceId":"0","appVersion":"6.0.0","appBuild":"190409","osVersion":"12.2.0","osType":"ios","deviceName":"iphone","os":"ios"}',
            'Content-Type': 'application/json;charset=utf-8',
            'Connection': 'keep-alive'
        }
        form = {
            "mobile": user,
            "pwd": password
        }
        response = requests.post(
            ajax_url,
            data=json.dumps(form),
            headers=header,
            verify=False
        ).json()
        if response['status'] == 200:
            newToken = response['content']['token']
            cf.set('koudai48', 'token', newToken)
            with open(file_path, 'w+', encoding='utf-8') as cfgfile2:
                cf.write(cfgfile2)
            return 'success'
        else:
            return response['message']


# 口袋48房间查询时间间隔读取
def kd_interval():
    BASE_DIR = os.path.dirname(__file__)
    file_path = os.path.join(BASE_DIR, 'setting.conf')
    cf = configparser.ConfigParser()
    with open(file_path, 'r', encoding='utf-8') as cfgfile:
        cf.readfp(cfgfile)
        interval = cf.get('koudai48', 'interval')
    return int(interval)


# --------------------------------------------------------


# ----------------------qq群设置----------------------


# qq群id
def groupid():
    BASE_DIR = os.path.dirname(__file__)
    file_path = os.path.join(BASE_DIR, 'setting.conf')
    cf = configparser.ConfigParser()
    # with open(file_path, 'r') as cfgfile:
    with open(file_path, 'r', encoding='utf-8') as cfgfile:
        cf.readfp(cfgfile)
        group_id = cf.get('QQqun', 'id')
        array = list(map(int, group_id.split(',')))
    return array


# 欢迎信息
def welcome():
    BASE_DIR = os.path.dirname(__file__)
    file_path = os.path.join(BASE_DIR, 'setting.conf')
    cf = configparser.ConfigParser()
    # with open(file_path, 'r') as cfgfile:
    with open(file_path, 'r', encoding='utf-8') as cfgfile:
        cf.readfp(cfgfile)
        # group_welcome
        words = cf.get('QQqun', 'welcome')
        msg = words.replace('\\n', '\n')
    return msg


# 关键词触发
# 禁言关键词,留空则无禁言
def shutup():
    BASE_DIR = os.path.dirname(__file__)
    file_path = os.path.join(BASE_DIR, 'setting.conf')
    cf = configparser.ConfigParser()
    # with open(file_path, 'r') as cfgfile:
    with open(file_path, 'r', encoding='utf-8') as cfgfile:
        cf.readfp(cfgfile)
        shutword = cf.get('QQqun', 'shutword')
        if shutword:
            wordlist = shutword.split(',')
        else:
            wordlist = []
    return wordlist


# --------------------------------------------------------


# ----------------------微博设置----------------------


# 手机网页版微博地址
def weibo_url():
    BASE_DIR = os.path.dirname(__file__)
    file_path = os.path.join(BASE_DIR, 'setting.conf')
    cf = configparser.ConfigParser()
    # with open(file_path, 'r') as cfgfile:
    with open(file_path, 'r', encoding='utf-8') as cfgfile:
        cf.readfp(cfgfile)
        weibo_url = cf.get('weibo', 'weiboURL')
    return str(weibo_url)


# weibo container id
def weibo_id():
    BASE_DIR = os.path.dirname(__file__)
    file_path = os.path.join(BASE_DIR, 'setting.conf')
    cf = configparser.ConfigParser()
    # with open(file_path, 'r') as cfgfile:
    with open(file_path, 'r', encoding='utf-8') as cfgfile:
        cf.readfp(cfgfile)
        weibo_id = cf.get('weibo', 'weiboID')
    return int(weibo_id)


# weibo房间查询时间间隔读取
def wb_interval():
    BASE_DIR = os.path.dirname(__file__)
    file_path = os.path.join(BASE_DIR, 'setting.conf')
    cf = configparser.ConfigParser()
    with open(file_path, 'r', encoding='utf-8') as cfgfile:
        cf.readfp(cfgfile)
        interval = cf.get('weibo', 'interval')
    return int(interval)


# --------------------------------------------------------


# ----------------------代理设置----------------------


def proxy():
    BASE_DIR = os.path.dirname(__file__)
    file_path = os.path.join(BASE_DIR, 'setting.conf')
    cf = configparser.ConfigParser()
    # with open(file_path, 'r') as cfgfile:
    with open(file_path, 'r', encoding='utf-8') as cfgfile:
        cf.readfp(cfgfile)
        https = cf.get('proxy', 'https')
        if https:
            list_https = https.split(',')
            proxies = {}
            proxies['https'] = random.choice(list_https)
        else:
            list_https = []
            proxies = {}
    # list_http = ['113.118.98.220:9797', '183.62.196.10:3128', '61.135.217.7:80', '61.155.164.109:3128', '61.155.164.107:3128']
    # list_https = ['114.115.140.25:3128', '59.56.74.205:3128', '116.31.75.97:3128', '121.43.178.58:3128', '113.79.75.82:9797']
    # proxies['http'] = random.choice(list_http)
    # proxies['https'] = random.choice(list_https)
    return proxies


# ---------------------长网址转短网址----------------------------


def get_short_url(long_url_str):
    url = 'http://api.t.sina.com.cn/short_url/shorten.json?source=3271760578&url_long=' + str(long_url_str)
    response = requests.get(
        url,
        verify=False
        ).json()
    # print(response)
    return response[0]['url_short']


# -------------------------------------------------------

# ---------------------长网址转短网址----------------------------


def bang_api_token(type, token_value):
    url = 'http://api.t.sina.com.cn/short_url/shorten.json?source=3271760578&url_long=' + str(long_url_str)
    response = requests.get(
        url,
        verify=False
        ).json()
    # print(response)
    return response[0]['url_short']


# -------------------------------------------------------
