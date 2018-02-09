# -*- coding: utf-8 -*-
import setting
import requests
import json
# 消去https请求的不安全warning
# import urllib3
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import urllib
import hashlib
import time


# -------------------------------
# init
header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) Appl\
eWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}


# 计算签名
def getSign(ret):
    # 将字典按键升序排列，返回一个元组tuple
    tuple = sorted(ret.items(), key=lambda e: e[0], reverse=False)
    md5_string = urllib.parse.urlencode(tuple).encode(encoding='utf_8', errors='strict')
    md5_string += b'&p=das41aq6'
    # md5计算 & 十六进制转化 & 根据规则从第6位开始取16位
    sign = hashlib.md5(md5_string).hexdigest()[5: 21]
    return sign


# page从1开始，每页最多20条数据


# 项目订单查询 10285
def getOrders(pro_id, page):
    url = 'https://wds.modian.com/api/project/orders'
    form = {
        'page': page,
        'pro_id': pro_id
    }
    sign = getSign(form)
    form['sign'] = sign
    response = requests.post(url, form, headers=header).json()
    return response


# 项目聚聚榜查询
# type = 1 聚聚榜
# type = 2 打卡榜
def getRankings(pro_id, type, page):
    url = 'https://wds.modian.com/api/project/rankings'
    form = {
        'page': page,
        'pro_id': pro_id,
        'type': type
    }
    sign = getSign(form)
    form['sign'] = sign
    response = requests.post(url, form, headers=header).json()
    return response


# 项目筹款结果查询
# 查询多个项目用逗号分隔，如getDetail(10250,10280)
def getDetail(*pro_id):
    # 将形参（一个元组）中int元素转为str元素，用逗号拼接成字符串
    pro_id_str = ','.join(map(str, pro_id))
    url = 'https://wds.modian.com/api/project/detail'
    form = {
        'pro_id': pro_id_str
    }
    sign = getSign(form)
    form['sign'] = sign
    response = requests.post(url, form, headers=header).json()
    return response


# init end
# ---------------------------------
# func


# rank
def rank(type):
    msg = ''
    err = False
    err_msg = '返回rank错误\n'
    detail = getDetail(str(setting.pro_id()))
    # type=1:总额榜
    if type == 1:
        msg = msg + setting.wds_name() + '·聚聚榜TOP20\n' + '------------\n'
        dic = getRankings(setting.pro_id(), 1, 1)
        if int(dic['status']) == 0:
            for data in dic['data']:
                msg = msg + '【第' + str(data['rank']) + '名】: ' +data['nickname'] + '支持了' + str(data['backer_money']) + '元\n'
        elif int(dic['status']) == 2:
            err = True
            err_msg += dic['message']
    elif type == 2:
        msg = msg + setting.wds_name() + '·打卡榜TOP20\n' + '------------\n'
        dic = getRankings(setting.pro_id(), 2, 1)
        if int(dic['status']) == 0:
            for data in dic['data']:
                msg = msg + '【第' + str(data['rank']) + '名】: ' +data['nickname'] + '已打卡' + str(data['support_days']) + '天\n'
        elif int(dic['status']) == 2:
            err = True
            err_msg += dic['message']
    msg = msg + '【摩点】：' + setting.wds_url() + '\n目前集资进度：¥' +\
        str(detail['data'][0]['already_raised']) + '\n目标：¥' +\
        detail['data'][0]['goal']
    if err is True:
        return err_msg
    elif err is False:
        return msg


def result(pro_id):
    response = getDetail(pro_id)
    msg = '当前项目信息：\n'
    msg += response['data'][0]['pro_name'] + '\n' + '项目进度：' + response['data'][0]['already_raised'] + '/' + response['data'][0]['goal'] + '\n结束时间：' + response['data'][0]['end_time']
    return msg


# 旧逻辑代码，已不再使用
# # 支持的次数&人数
# def num():
#     datas = {'status': 0}
#     page = 1
#     sum = 0
#     sum_person = 0
#     person = []
#     # 总次数
#     while True:
#         orders = getOrders(setting.pro_id(), page)
#         page += 1
#         if int(orders['status']) == 2:
#             datas['status'] = 2
#             datas['err_msg'] = orders['message']
#             break
#         if len(orders['data']) == 0:
#             break
#         sum += len(orders['data'])
#         for data in orders['data']:
#             if data['nickname'] not in person:
#                 person.append(data['nickname'])
#     datas['sum'] = sum
#     sum_person = len(person)
#     datas['sum_person'] = sum_person
#     return datas
# 
# 
# # 返回集资信息
# def diff(num):
#     detail = getDetail(str(setting.pro_id()))
#     msg = ''
#     if num > 20:
#         num = 20
#     order = getOrders(setting.pro_id(), 1)
#     if int(order['status']) == 2:
#         return order['message']
#     for i in range(0, num):
#         msg += "ID: " + order['data'][i]['nickname'] +\
#             " 的聚聚刚刚在【" + setting.wds_name() + "】中支持了 ¥" +\
#             str(order['data'][i]['backer_money']) + '\n' + "感谢这位聚聚对" +\
#             setting.idol_name() + "的支持" + '\n'
#     msg += '【摩点】：' + setting.wds_url() + '\n目前集资进度：¥' +\
#         str(detail['data'][0]['already_raised']) + '\n目标：¥' +\
#         str(detail['data'][0]['goal'])
#     return msg


def newOrder(stamp10, secondsDelay):
    newOrders = []
    # 获取一次订单信息，返回一个dictionary
    orderDict = getOrders(setting.pro_id(), 1)
    # 查询失败则返回错误信息
    if int(orderDict['status']) == 2:
        return orderDict['message']
    # 查询成功，遍历data
    for data in orderDict['data']:
        pay_time = data['pay_time']
        # 将字符串时间转换为unix时间戳
        data['pay_time'] = int(time.mktime(time.strptime(pay_time, '%Y-%m-%d %H:%M:%S')))
        # 筛选订单时间在查询时间前的设定时间段之间的订单
        if data['pay_time'] >= stamp10 - secondsDelay and data['pay_time'] < stamp10:
            newOrders.append(data)
    msgDict = {}
    # 有新订单
    if newOrders:
        # 获取项目信息
        detail = getDetail(setting.pro_id())
        # 查询失败则返回错误信息
        if int(detail['status']) == 2:
            return detail['message']
        # 查询成功，初始化消息
        msgDict['msg'] = []
        msg = ''
        for newOrder in newOrders:
            msg = "ID: " + newOrder['nickname'] +\
                " 的聚聚刚刚在【" + setting.wds_name() + "】中支持了 ¥" +\
                str(newOrder['backer_money']) + '\n' + "感谢这位聚聚对" +\
                setting.idol_name() + "的支持" + '\n'
            msgDict['msg'].append(msg)
        msgDict['end'] = '【摩点】：' + setting.wds_url() + '\n目前集资进度：¥' +\
            str(detail['data'][0]['already_raised']) + '\n目标：¥' +\
            str(detail['data'][0]['goal'])
    return msgDict
