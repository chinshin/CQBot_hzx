# -*- coding: utf-8 -*-
from cqhttp import CQHttp
import json
import time
import setting
import requests
import urllib3
from CQLog import DEBUG, WARN, INFO
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# 13位unix时间戳（ms）转为字符串时间
def stamp_to_str(timestamp):
    x = time.localtime(timestamp / 1000)
    time_str = time.strftime('%Y-%m-%d %H:%M:%S', x)
    return time_str


def getTime13():
    t = int(time.time()*1000)
    # print(t)
    return t


def roomMsg():
    # bot = CQHttp(api_root='http://127.0.0.1:5700/')
    # request
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
        'token': setting.token()
    }
    form = {
        "lastTime": 0,
        "limit": 10,
        "chatType": 0,
        "roomId": setting.roomId()
    }
    response = requests.post(
        ajax_url,
        data=json.dumps(form),
        headers=header,
        verify=False,
        proxies=setting.proxy()
    ).json()
    # 初始化消息队列
    msg_array = []
    #
    if response['status'] == 200:
        # 系统时间
        sysTime13 = getTime13()
        # 配置文件存储的最后一条消息时间
        cfgTime13 = setting.read_kdmsg_time13()
        # 获取的房间的最新消息时间
        kdmsgTime13 = response['content']['data'][0]['msgTime']
        # 超过60s的消息会被丢弃
        if sysTime13 > cfgTime13 + 60000:
            setting.write_kdmsg_time13(sysTime13-60000)
        elif cfgTime13 == kdmsgTime13:
            pass
        elif cfgTime13 > kdmsgTime13:
            # 说明有撤回消息
            pass
        if setting.read_kdmsg_time13() < kdmsgTime13:
            # 有新消息
            datas = response['content']['data']
            for data in datas:
                msg = ''
                # 判断重复
                if data['msgTime'] <= cfgTime13:
                    continue
                #
                # 文字消息
                extInfo = json.loads(data['extInfo'])
                if data['msgType'] == 0:
                    if extInfo['messageObject'] == 'text':
                        msg = ('%s：%s\n%s' % (extInfo['senderName'], extInfo['text'], data['msgTimeStr']))
                    elif extInfo['messageObject'] == 'faipaiText':
                        # 20171221 16:38 黄子璇(roomid=9108720)发生err：翻牌信息未返回faipaiName
                        try:
                            msg = ('%s：%s\n%s：%s\n%s' % (extInfo['senderName'], extInfo['messageText'], extInfo['faipaiName'], extInfo['faipaiContent'], data['msgTimeStr']))
                        except:
                            msg = ('%s：%s\n翻牌：%s\n%s' % (extInfo['senderName'], extInfo['messageText'], extInfo['faipaiContent'], data['msgTimeStr']))
                        #
                    elif extInfo['messageObject'] == 'live':
                        msg = ('小偶像开视频直播啦 \n 直播标题：%s \n 直播封面：%s \n开始时间：%s \n 直播地址：%s' % (extInfo['referenceContent'], 'https://source.48.cn' + extInfo['referencecoverImage'], data['msgTimeStr'], 'https://h5.48.cn/2017appshare/memberLiveShare/index.html?id=' + extInfo['referenceObjectId']))
                    elif extInfo['messageObject'] == 'diantai':
                        msg = ('小偶像开电台啦 \n 电台标题：%s \n 电台封面：%s \n开始时间：%s \n 电台地址：%s' % (extInfo['referenceContent'], 'https://source.48.cn' + extInfo['referencecoverImage'], data['msgTimeStr'], 'https://h5.48.cn/2017appshare/memberLiveShare/index.html?id=' + extInfo['referenceObjectId']))
                    elif extInfo['messageObject'] == 'idolFlip':
                        # INFO('idol翻牌')
                        msg = ('%s：%s\n问题内容：%s\n%s' % (extInfo['senderName'], extInfo['idolFlipTitle'], extInfo['idolFlipContent'], data['msgTimeStr']))
                    else:
                        msg = '有未知格式的文字消息'
                        INFO(str(extInfo))
                # image
                elif data['msgType'] == 1:
                    bodys = json.loads(data['bodys'])
                    msg = ('【口袋48房间图片】\n %s：%s\n%s' % (extInfo['senderName'], bodys['url'], data['msgTimeStr']))
                # voice
                elif data['msgType'] == 2:
                    bodys = json.loads(data['bodys'])
                    msg = ('【口袋48房间语音】\n %s：%s\n%s' % (extInfo['senderName'], bodys['url'], data['msgTimeStr']))
                # video
                elif data['msgType'] == 3:
                    bodys = json.loads(data['bodys'])
                    msg = ('【口袋48房间视频】\n %s：%s\n%s' % (extInfo['senderName'], bodys['url'], data['msgTimeStr']))
                else:
                    msg = '有未知类型的消息'
                    INFO(str(data))
                msg_array.append(msg)
            setting.write_kdmsg_time13(kdmsgTime13)
    # 获取失败，检查token
    # elif response['status'] == 401 and response['message'] == '授权验证失败':
    elif response['status'] == 401:
        WARN('koudai48.py授权验证失败')
        if not setting.token_verify():
            WARN('token失效，尝试获取新token')
            setting.getNewToken()
    else:
        WARN('获取口袋房间信息出错')
        WARN(response['message'])
    return msg_array
    # if msg_array:
    #     msg_array.reverse()
    #     for msgdata in msg_array:
    #         bot.send_group_msg_async(group_id=setting.groupid(), message=msgdata, auto_escape=False)
    #         time.sleep(0.5)
