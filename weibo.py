# -*- coding: utf-8 -*-
import setting
import requests
import copy
import re


# 除去字符串中的html标签
def dr_to_dd(dr_str):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', dr_str)
    return str(dd)


# global response
def init():
    # 更改ajax_url
    ajax_url = str(setting.weibo_url())
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}

    # 更改value&pro_id
    form = {
        'containerid': int(setting.weibo_id()),
    }

    response = requests.post(ajax_url, form, headers=header).json()
    return response


def getdata(i):
    response = copy.copy(init())
    datas = response['data']['cards'][i]
    return datas


def checkid(i):
    datas = getdata(i)
    return str(datas['mblog']['id'])


def checkretweet(i):
    datas = getdata(i)
    if datas['mblog'].get('retweeted_status') is None:
        return False
    else:
        return True


def getweibo(i):
    datas = getdata(i)
    r_weibo = str(datas['mblog']['text'])
    # 20170917增加
    # 微博内容去除html标记功能
    r2d_weibo = dr_to_dd(r_weibo)
    return r2d_weibo


def getretweetweibo(i):
    datas = getdata(i)
    r_retweeetweibo = str(datas['mblog']['raw_text'])
    # 20170917增加
    # 微博内容去除html标记功能
    r2d_retweeetweibo = dr_to_dd(r_retweeetweibo)
    return r2d_retweeetweibo


def checkpic(i):
    datas = getdata(i)
    if datas['mblog'].get('pics') is None:
        return False
    else:
        return True


def getpic(i):
    datas = getdata(i)
    picurl = ""
    picnum = 1
    for pic in datas['mblog']['pics']:
        picurl = picurl + "微博配图" + str(picnum) + "：" + str(pic['url']) + '\n'
        picnum += 1
    return picurl


def getscheme(i):
    datas = getdata(i)
    return str(datas['scheme'])


def getidarray():
    weibo_id_array = []
    response = copy.copy(init())
    cards = response['data']['cards']
    for card in cards:
        try:
            weibo_id = card['mblog']['id']
        except Exception as e:
            weibo_id_array.append("0")
        else:
            weibo_id_array.append(weibo_id)
    return weibo_id_array


# 20170926
# 现在查询新微博：返回前5个微博id（如果是微博广告位，id为0）
def get_5_idarray():
    weibo_id_array = []
    response = copy.copy(init())
    cards = response['data']['cards']
    for i in range(0, 5):
        datas = cards[i]
        try:
            weibo_id = datas['mblog']['id']
        except Exception as e:
            weibo_id_array.append("0")
        else:
            weibo_id_array.append(weibo_id)
    return weibo_id_array
