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


# 微打赏名称
def wds_name():
    BASE_DIR = os.path.dirname(__file__)
    file_path = os.path.join(BASE_DIR, 'setting.conf')
    cf = configparser.ConfigParser()
    # with open(file_path, 'r') as cfgfile:
    with open(file_path, 'r', encoding='utf-8') as cfgfile:
        cf.readfp(cfgfile)
        # modian
        modian_name = cf.get('modian', 'name')
        # modian_url = cf.get('modian', 'url')
        # pro_id = cf.get('modian', 'pro_id')
    return str(modian_name)


# 微打赏网址 建议使用短地址t.cn
def wds_url():
    BASE_DIR = os.path.dirname(__file__)
    file_path = os.path.join(BASE_DIR, 'setting.conf')
    cf = configparser.ConfigParser()
    # with open(file_path, 'r') as cfgfile:
    with open(file_path, 'r', encoding='utf-8') as cfgfile:
        cf.readfp(cfgfile)
        # modian
        # modian_name = cf.get('modian', 'name')
        modian_url = cf.get('modian', 'url')
        # pro_id = cf.get('modian', 'pro_id')
    return str(modian_url)


# 微打赏项目对应pro_id
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
    return int(pro_id)


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
# 黄子璇roomId：9108720
def roomId():
    BASE_DIR = os.path.dirname(__file__)
    file_path = os.path.join(BASE_DIR, 'setting.conf')
    cf = configparser.ConfigParser()
    # with open(file_path, 'r') as cfgfile:
    with open(file_path, 'r', encoding='utf-8') as cfgfile:
        cf.readfp(cfgfile)
        group = cf.get('idol', 'group')
        name = cf.get('idol', 'name')
        file_path = os.path.join(BASE_DIR, 'roomID.conf')
        # with open(file_path, 'r') as cfgfile2:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as cfgfile2:
            cf.readfp(cfgfile2)
            roomid = cf.get(group, name)
    return int(roomid)


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
# token 存活时间为 30 天
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

    ajax_url = 'https://puser.48.cn/usersystem/api/user/v1/show/cardInfo'
    header = {
        'Host': 'puser.48.cn',
        'version': '5.0.1',
        'os': 'android',
        'Accept-Encoding': 'gzip',
        'IMEI': '866716037125810',
        'User-Agent': 'Mobile_Pocket',
        'Content-Length': '0',
        'Connection': 'Keep-Alive',
        'Content-Type': 'application/json;charset=utf-8',
        'token': token
    }
    response = requests.post(
        ajax_url,
        headers=header,
        verify=False
    ).json()
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
        token = cf.get('koudai48', 'token')
        # request
        ajax_url = 'https://puser.48.cn/usersystem/api/user/v1/login/phone'
        header = {
            'Host': 'puser.48.cn',
            'version': '5.0.1',
            'os': 'android',
            'Accept-Encoding': 'gzip',
            'IMEI': '866716037125810',
            'User-Agent': 'Mobile_Pocket',
            'Content-Length': '75',
            'Connection': 'Keep-Alive',
            'Content-Type': 'application/json;charset=utf-8',
            'token': '0'
        }
        form = {
            "latitude": 0,
            "longitude": 0,
            "password": password,
            "account": user
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
    return int(group_id)


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


# --------------------------------------------------------
