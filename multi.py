# -*- coding: utf-8 -*-
from cqhttp import CQHttp
import json
import time
from setting import token
import requests
import urllib3
import random
from CQLog import INFO, WARN
from apscheduler.schedulers.blocking import BlockingScheduler
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


groupID = '0'
my_qq = '0'

bot = CQHttp(api_root='http://127.0.0.1:5700/')
sched = BlockingScheduler()


# 5771862陈珂 5780836马玉灵 5770638黄恩如 5771875奶副 5771871liga 5758968刘77 5783223soso 5783256xll 5782038zjy 5776964苏33 5770634llf 5779213wss 5776963zdn
roomIdArray = [5771862, 5780836, 5770638, 5771875, 5771871, 5758968, 5783223, 5783256, 5782038, 5776964, 5770634, 5779213, 5776963]


def proxy():
    proxies = {}
    list_http = ['113.118.98.220:9797', '183.62.196.10:3128', '61.135.217.7:80', '61.155.164.109:3128', '61.155.164.107:3128']
    list_https = ['114.115.140.25:3128', '39.134.169.217:8080', '211.159.177.212:3128']
    proxies['http'] = random.choice(list_http)
    # proxies['http'] = ''
    proxies['https'] = random.choice(list_https)
    # proxies['https'] = ''
    INFO(str(proxies['https']))
    return proxies


def getTime13():
    t = int(time.time()*1000)
    # print(t)
    return t


def getNew(s, roomid_array):
    new = []
    ajax_url = 'https://pjuju.48.cn/imsystem/api/im/v1/room/info/diff'
    header = {
        'Host': 'pjuju.48.cn',
        'version': '5.0.1',
        'os': 'android',
        'Accept-Encoding': 'gzip',
        'IMEI': '866716037825810',
        'token':  token(),
        'User-Agent': 'Mobile_Pocket',
        'Content-Length': '2216',
        'Connection': 'Keep-Alive',
        'Content-Type':  'application/json;charset=utf-8'
    }
    form = {
        "clientTime": getTime13() - int(s*1000),
        "roomIds": roomid_array
    }
    s = requests.session()
    response = s.post(
        ajax_url,
        data=json.dumps(form),
        headers=header,
        verify=False,
        proxies=proxy()
    ).json()
    INFO('multi聚聚房间diff请求一次')
    if response['status'] == 200 and response['content']:
        for content in response['content']:
            # print(content['creatorName'], 'have new msg')
            new.append(content['roomId'])
    INFO(str(new))
    return new


def getRoomMsg(roomid):
    ajax_url = 'https://pjuju.48.cn/imsystem/api/im/v1/member/room/message/mainpage'
    header = {
        'Host': 'pjuju.48.cn',
        'version': '5.0.1',
        'os': 'android',
        'Accept-Encoding': 'gzip',
        'IMEI': '866716037825810',
        'User-Agent': 'Mobile_Pocket',
        'Content-Length': '67',
        'Connection': 'Keep-Alive',
        'Content-Type': 'application/json;charset=utf-8',
        'token': token()
    }
    form = {
        "lastTime": 0,
        "limit": 10,
        "chatType": 0,
        "roomId": roomid
    }
    s = requests.session()
    response = s.post(
        ajax_url,
        data=json.dumps(form),
        headers=header,
        verify=False,
        proxies=proxy()
    ).json()
    INFO('multi聚聚房间mainpage请求一次')
    return response


@sched.scheduled_job('interval', seconds=60)
def get_juju():
    getTime = getTime13()
    # 获取60s内有新消息的房间号
    roomId_newMsg = getNew(60, roomIdArray)
    if roomId_newMsg:
        INFO('有新消息的房间号为')
        INFO(str(roomId_newMsg))
        msgArray = []
        for rmid in roomId_newMsg:
            # 获取对应房间号的response
            response = getRoomMsg(rmid)
            # 初始化消息队列
            msg_array = []
            if response['status'] == 200 and response['message'] == 'success':
                datas = response['content']['data']
                for data in datas:
                    msg = ''
                    # 判断重复
                    if data['msgTime'] < getTime - 60000:
                        continue
                    # 文字消息
                    extInfo = json.loads(data['extInfo'])
                    if data['msgType'] == 0:
                        if extInfo['messageObject'] == 'text':
                            msg = ('%s：%s\n%s' % (extInfo['senderName'], extInfo['text'], data['msgTimeStr']))
                        elif extInfo['messageObject'] == 'faipaiText':
                            msg = ('%s：%s\n翻牌：%s\n%s' % (extInfo['senderName'], extInfo['messageText'], extInfo['faipaiContent'], data['msgTimeStr']))
                        elif extInfo['messageObject'] == 'live':
                            msg = ('%s开视频直播啦 \n 直播标题：%s \n 直播封面：%s \n开始时间：%s \n 直播地址：%s' % (extInfo['senderName'], extInfo['referenceContent'], 'https://source.48.cn' + extInfo['referencecoverImage'], data['msgTimeStr'], 'https://h5.48.cn/2017appshare/memberLiveShare/index.html?id=' + extInfo['referenceObjectId']))
                        elif extInfo['messageObject'] == 'diantai':
                            msg = ('%s开电台啦 \n 电台标题：%s \n 电台封面：%s \n开始时间：%s \n 电台地址：%s' % (extInfo['senderName'], extInfo['referenceContent'], 'https://source.48.cn' + extInfo['referencecoverImage'], data['msgTimeStr'], 'https://h5.48.cn/2017appshare/memberLiveShare/index.html?id=' + extInfo['referenceObjectId']))
                        elif extInfo['messageObject'] == 'idolFlip':
                            # INFO('idol翻牌')
                            msg = ('%s：%s\n问题内容：%s\n%s' % (extInfo['senderName'], extInfo['idolFlipTitle'], extInfo['idolFlipContent'], data['msgTimeStr']))
                        else:
                            msg = '有未知格式的文字消息'
                            WARN('multi有未知格式的文字消息')
                            WARN(data)
                    # image
                    elif data['msgType'] == 1:
                        bodys = json.loads(data['bodys'])
                        msg = ('%s：%s\n%s' % (extInfo['senderName'], bodys['url'], data['msgTimeStr']))
                    # voice
                    elif data['msgType'] == 2:
                        bodys = json.loads(data['bodys'])
                        msg = ('%s：%s\n%s' % (extInfo['senderName'], bodys['url'], data['msgTimeStr']))
                    # video
                    elif data['msgType'] == 3:
                        bodys = json.loads(data['bodys'])
                        msg = ('【口袋48房间视频】\n %s：%s\n%s' % (extInfo['senderName'], bodys['url'], data['msgTimeStr']))
                    else:
                        msg = '有未知类型的消息'
                        WARN('multi有未知类型的消息')
                        WARN(data)
                    msg_array.append(msg)
            else:
                WARN('multi获取口袋房间信息出错')
                WARN(response['message'])
            if msg_array:
                msg_array.reverse()
                for msgdata in msg_array:
                    bot.send_group_msg_async(group_id=groupID, message=msgdata, auto_escape=False)
                    time.sleep(0.5)
            time.sleep(5)


def get_hpyRoom():
    getTime = getTime13()
    response = getRoomMsg(5771863)
    INFO('hpy request one time')
    # 初始化消息队列
    msg_array = []
    if response['status'] == 200 and response['message'] == 'success':
        datas = response['content']['data']
        for data in datas:
            msg = ''
            # 判断重复
            if data['msgTime'] < getTime - 60000:
                continue
            # 文字消息
            extInfo = json.loads(data['extInfo'])
            if data['msgType'] == 0:
                if extInfo['messageObject'] == 'text':
                    msg = ('%s：%s\n%s' % (extInfo['senderName'], extInfo['text'], data['msgTimeStr']))
                elif extInfo['messageObject'] == 'faipaiText':
                    msg = ('%s：%s\n翻牌：%s\n%s' % (extInfo['senderName'], extInfo['messageText'], extInfo['faipaiContent'], data['msgTimeStr']))
                elif extInfo['messageObject'] == 'live':
                    msg = ('%s开视频直播啦 \n 直播标题：%s \n 直播封面：%s \n开始时间：%s \n 直播地址：%s' % (extInfo['senderName'], extInfo['referenceContent'], 'https://source.48.cn' + extInfo['referencecoverImage'], data['msgTimeStr'], 'https://h5.48.cn/2017appshare/memberLiveShare/index.html?id=' + extInfo['referenceObjectId']))
                elif extInfo['messageObject'] == 'diantai':
                    msg = ('%s开电台啦 \n 电台标题：%s \n 电台封面：%s \n开始时间：%s \n 电台地址：%s' % (extInfo['senderName'], extInfo['referenceContent'], 'https://source.48.cn' + extInfo['referencecoverImage'], data['msgTimeStr'], 'https://h5.48.cn/2017appshare/memberLiveShare/index.html?id=' + extInfo['referenceObjectId']))
                elif extInfo['messageObject'] == 'idolFlip':
                    # INFO('idol翻牌')
                    msg = ('%s：%s\n问题内容：%s\n%s' % (extInfo['senderName'], extInfo['idolFlipTitle'], extInfo['idolFlipContent'], data['msgTimeStr']))
                else:
                    msg = '有未知格式的文字消息'
                    WARN('有未知格式的文字消息')
                    WARN(data)
            # image
            elif data['msgType'] == 1:
                bodys = json.loads(data['bodys'])
                msg = ('%s：%s\n%s' % (extInfo['senderName'], bodys['url'], data['msgTimeStr']))
            # voice
            elif data['msgType'] == 2:
                bodys = json.loads(data['bodys'])
                msg = ('%s：%s\n%s' % (extInfo['senderName'], bodys['url'], data['msgTimeStr']))
            # video
            elif data['msgType'] == 3:
                bodys = json.loads(data['bodys'])
                msg = ('【口袋48房间视频】\n %s：%s\n%s' % (extInfo['senderName'], bodys['url'], data['msgTimeStr']))
            else:
                msg = '有未知类型的消息'
                WARN('有未知类型的消息')
                WARN(data)
            msg_array.append(msg)
    else:
        WARN('获取口袋房间信息出错')
        WARN(response['message'])
    if msg_array:
        msg_array.reverse()
        for msgdata in msg_array:
            bot.send_private_msg_async(user_id=my_qq, message=msgdata, auto_escape=False)
            time.sleep(0.1)
