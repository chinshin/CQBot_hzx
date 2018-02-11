# -*- coding: utf-8 -*-
from cqhttp import CQHttp
import json
import time
from setting import token
import requests
import urllib3
import random
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


groupID = 0


def printStrTime():
    t = int(time.time()*1000)
    x = time.localtime(t / 1000)
    time_str = time.strftime('%Y-%m-%d %H:%M:%S', x)
    return time_str


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
    print(printStrTime() + str(proxies['https']))
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
        # "roomIds": [5771876, 18863833, 18869478, 5771873, 5771874, 5783217, 5771882, 5778537, 5758972, 5778533, 18874571, 18872373, 18865486, 8951607, 5777253, 5776968, 5779222, 5758968, 5777252, 18863978, 5777242, 18868708, 5779220, 18874574, 5779217, 5779213, 5776896, 9338140, 9021937, 5777255, 18925326, 5780843, 9046692, 5771862, 5776971, 20899904, 5773823, 5779226, 9339220, 5779211, 9342380, 18716506, 5778527, 5780839, 5782038, 5774523, 5782035, 18709707, 8961080, 18876868, 18931483, 18876438, 19412890, 5776974, 18712468, 5783238, 5776913, 18717305, 5779224, 5771870, 18721105, 9255077, 5776938, 9341101, 5770642, 5782033, 5758970, 5776891, 5776962, 18709668, 5782041, 5770641, 5776969, 5773822, 9339537, 5777250, 5758973, 5776904, 5774514, 5771868, 9106599, 5770621, 17870659, 5783237, 5771871, 5780789, 5758969, 5758967, 5758963, 5770640, 5783223, 9340808, 5780791, 9125456, 5777251, 5777241, 9342446, 5782031, 18054323, 5777232, 5758974, 5770633, 5774530, 5773805, 9333412, 5780790, 5771883, 5776933, 5776963, 5779214, 5783236, 5783244, 5777243, 5783166, 8960034, 18931469, 18702980, 5783215, 5777257, 5771865, 5773743, 5771872, 5783234, 18706972, 8967027, 5773813, 5783222, 20939691, 5773746, 18933202, 5780841, 5776961, 18931527, 5783159, 9046720, 9011537, 5776960, 9108720, 5778530, 5782039, 5773753, 5771880, 5776916, 5770622, 5777256, 17877365, 5777228, 5771855, 11190812, 5778528, 5780792, 5770634, 18710871, 5783160, 5783164, 5779209, 5776899, 5776915, 5773766, 5779212, 5773747, 20899897, 18713709, 5779210, 5776958, 5771885, 5776909, 5777254, 5783256, 5770618, 5771879, 5776932, 5773799, 5771863, 5777235, 5773750, 5780837, 5780835, 5777248, 5776973, 9337363, 5774521, 5774519, 5770638, 9066006, 5771875, 9332797, 9335784, 5780793, 18912170, 5758971, 5771856, 5778538, 5778526, 9335706, 18696906, 5776897, 5770619, 5758962, 9225254, 5771867, 5777238, 8078734, 5773820, 18724509, 5782036, 5776912, 5782030, 5774517, 5770616, 5777239, 5783221, 5783240, 5776964, 5758965, 5780836, 5776914, 5777229, 9343067, 5777227, 5774518, 5774511, 5777247, 5782029, 5771886, 5771857, 5776965, 5777230, 5770636, 5778534, 5770620, 5770628, 5770630, 5770635, 5770639, 5771860, 5774515, 5774516, 5774524, 5776901, 5776908, 5776953, 5776975, 5777244, 5777246, 5778524, 5778536, 5778539, 5779207, 5779225, 5779228, 5783153, 5783226, 5783243, 9032606, 9073567, 9139038, 9153877, 9297138, 9335787, 9350286, 9401875, 9835470, 17928298, 18304811, 18716764, 18866539]
    }
    s = requests.session()
    response = s.post(
        ajax_url,
        data=json.dumps(form),
        headers=header,
        verify=False,
        proxies=proxy()
    ).json()
    print(printStrTime()+'聚聚房间diff请求一次')
    if response['status'] == 200 and response['content']:
        for content in response['content']:
            # print(content['creatorName'], 'have new msg')
            new.append(content['roomId'])
    print(printStrTime()+str(new))
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
    print(printStrTime()+'聚聚房间mainpage请求一次')
    return response


def get_juju():
    # global firstcheck_juju
    # 仅需修改播报的qq群昵称
    getTime = getTime13()
    # 获取60s内有新消息的房间号
    roomId_newMsg = getNew(60, roomIdArray)
    if roomId_newMsg:
        print(printStrTime()+'有新消息的房间号为')
        print(printStrTime()+str(roomId_newMsg))
        msgArray = []
        for rmid in roomId_newMsg:
            # # 首次检查
            # if firstcheck_juju is True:
            #     firstcheck_juju = False
            #     INFO('first check juju')
            #     break
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
                            pass
                        else:
                            msg = '有未知格式的文字消息'
                            print(printStrTime()+'有未知格式的文字消息')
                            print(printStrTime()+data)
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
                        print(printStrTime()+'有未知类型的消息')
                        print(printStrTime()+data)
                    msg_array.append(msg)
            else:
                print(printStrTime()+'获取口袋房间信息出错')
                print(printStrTime()+response['message'])
            if msg_array:
                msgArray.append(msg_array)
            time.sleep(5)
        return msgArray


bot = CQHttp(api_root='http://127.0.0.1:5700/')
msgArray = get_juju()
if msgArray:
    for msg_array in msgArray:
        if msg_array:
            msg_array.reverse()
            for msgdata in msg_array:
                bot.send_group_msg_async(group_id=groupID, message=msgdata, auto_escape=False)
                time.sleep(0.5)
