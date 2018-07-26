# -*- coding: utf-8 -*-
# from cqhttp import CQHttp
import json
import time
import setting
import requests
import urllib3
from CQLog import WARN, INFO
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Koudai:
    """docstring for Koudai"""
    response = {}
    # 系统时间
    sysTime13 = 0
    # 配置文件记录时间
    cfgTime13 = 0
    # 口袋房间消息时间
    kdmsgTime13 = 0

    # 初始化
    def __init__(self):
        super(Koudai, self).__init__()
        # 获取系统时间和配置文件时间
        self.sysTime13 = self.getSysTime13()
        self.cfgTime13 = self.getCfgTime13()
        # 请求一次口袋房间
        res = self.getMainpage()
        # 请求成功
        if res['status'] == 200:
            # 获取response
            self.response = res
            # 获取最新口袋消息时间
            self.kdmsgTime13 = self.getKdmsgTime13()
        elif res['status'] == 401:
            WARN('koudai48.py授权验证失败')
            if not setting.token_verify():
                WARN('token失效，尝试获取新token')
                setting.getNewToken()
        else:
            WARN('获取口袋房间信息出错', res['message'])

    # 请求口袋房间
    def getMainpage(self):
        url = 'https://pjuju.48.cn/imsystem/api/im/v1/member/room/message/mainpage'
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
        res = requests.post(
            url,
            data=json.dumps(form),
            headers=header,
            verify=False
        ).json()
        return res

    def getSysTime13(self):
        t = int(time.time() * 1000)
        return t

    def getCfgTime13(self):
        t = setting.read_kdmsg_time13()
        return t

    # 写配置文件时间
    def writeCfgTime13(self, t):
        setting.write_kdmsg_time13(t)

    def getKdmsgTime13(self):
        t = self.response['content']['data'][0]['msgTime']
        return t

    # 检查新消息
    def checkNew(self):
        # 判断response非空
        if self.response:
            # 忽略超过60秒的消息
            if self.sysTime13 > self.cfgTime13 + 60000:
                # 将配置文件时间设置为 系统时间 - 60s
                self.writeCfgTime13(self.sysTime13 - 60000)
                # 更新cfgTime13
                self.cfgTime13 = self.sysTime13 - 60000
            elif self.cfgTime13 == self.kdmsgTime13:
                pass
            elif self.cfgTime13 > self.kdmsgTime13:
                # 说明有撤回消息
                pass
            if self.cfgTime13 < self.kdmsgTime13:
                # 有新消息
                # 将配置文件时间设置为 最新一条消息的时间
                self.writeCfgTime13(self.kdmsgTime13)
                return True

    # 酷Qair消息
    def msgAir(self):
        msg_array = []
        datas = self.response['content']['data']
        for data in datas:
            # 判断重复
            if data['msgTime'] <= self.cfgTime13:
                continue
            #
            # 文字消息
            extInfo = json.loads(data['extInfo'])
            if data['msgType'] == 0:
                if extInfo['messageObject'] == 'text':
                    msg = ('%s：%s\n%s' % (
                        extInfo['senderName'],
                        extInfo['text'],
                        data['msgTimeStr']))
                elif extInfo['messageObject'] == 'faipaiText':
                    # 20171221 16:38 黄子璇(roomid=9108720)发生err：翻牌信息未返回faipaiName
                    try:
                        msg = ('%s：%s\n%s：%s\n%s' % (
                            extInfo['senderName'], extInfo['messageText'],
                            extInfo['faipaiName'], extInfo['faipaiContent'],
                            data['msgTimeStr']))
                    except Exception as e:
                        msg = ('%s：%s\n翻牌：%s\n%s' % (
                            extInfo['senderName'], extInfo['messageText'],
                            extInfo['faipaiContent'], data['msgTimeStr']))
                    #
                elif extInfo['messageObject'] == 'live':
                    msg = ('小偶像开视频直播啦 \n直播标题：%s \n直播封面：https://source.48.\
                        cn%s \n开始时间：%s \n直播地址：https://h5.48.cn/2017appshare/memberLiveShare/index.html?id=%s' % (
                        extInfo['referenceContent'],
                        extInfo['referencecoverImage'], data['msgTimeStr'],
                        extInfo['referenceObjectId']))
                elif extInfo['messageObject'] == 'diantai':
                    msg = ('小偶像开电台啦 \n电台标题：%s \n电台封面：https://source.48.cn%s \n开始时间：%s \n电台地址：https://h5.48.cn/2017appshare/\
                        memberLiveShare/index.html?id=%s' % (
                        extInfo['referenceContent'],
                        extInfo['referencecoverImage'], data['msgTimeStr'],
                        extInfo['referenceObjectId']))
                elif extInfo['messageObject'] == 'idolFlip':
                    # INFO('idol翻牌')
                    msg = ('%s：%s\n问题内容：%s\n%s' % (
                        extInfo['senderName'], extInfo['idolFlipTitle'],
                        extInfo['idolFlipContent'], data['msgTimeStr']))
                # 自己发的消息
                elif extInfo['messageObject'] == 'messageBoard':
                    pass
                else:
                    msg = '有未知格式的文字消息'
                    INFO('有未知格式的文字消息')
                    INFO(extInfo)
            # image
            elif data['msgType'] == 1:
                bodys = json.loads(data['bodys'])
                msg = ('%s：图片消息：%s\n%s' % (
                    extInfo['senderName'], bodys['url'], data['msgTimeStr']))
            # voice
            elif data['msgType'] == 2:
                bodys = json.loads(data['bodys'])
                msg = ('%s：语音消息：%s\n%s' % (
                    extInfo['senderName'], bodys['url'], data['msgTimeStr']))
            # video
            elif data['msgType'] == 3:
                bodys = json.loads(data['bodys'])
                msg = ('%s：视频消息：%s\n%s' % (
                    extInfo['senderName'], bodys['url'], data['msgTimeStr']))
            else:
                msg = '有未知类型的消息'
                INFO('有未知类型的消息')
                INFO(data)
            msg_array.append(msg)
        return msg_array

    # 酷QPro消息
    def msgPro(self):
        msg_array = []
        datas = self.response['content']['data']
        for data in datas:
            # 判断重复
            if data['msgTime'] <= self.cfgTime13:
                continue
            #
            # 文字消息
            extInfo = json.loads(data['extInfo'])
            if data['msgType'] == 0:
                if extInfo['messageObject'] == 'text':
                    msg = ('%s：%s\n%s' % (
                        extInfo['senderName'],
                        extInfo['text'],
                        data['msgTimeStr']))
                elif extInfo['messageObject'] == 'faipaiText':
                    # 20171221 16:38 黄子璇(roomid=9108720)发生err：翻牌信息未返回faipaiName
                    try:
                        msg = ('%s：%s\n%s：%s\n%s' % (
                            extInfo['senderName'], extInfo['messageText'],
                            extInfo['faipaiName'], extInfo['faipaiContent'],
                            data['msgTimeStr']))
                    except Exception as e:
                        msg = ('%s：%s\n翻牌：%s\n%s' % (
                            extInfo['senderName'], extInfo['messageText'],
                            extInfo['faipaiContent'], data['msgTimeStr']))
                    #
                elif extInfo['messageObject'] == 'live':
                    msg = [{'type': 'text', 'data': {
                        'text': '小偶像开视频直播啦 \n 直播标题：%s \n \
                        直播封面：' % extInfo['referenceContent']}},
                        {'type': 'image', 'data': {
                            'file': 'https://source.48.cn%s' % extInfo['referencecoverImage']}},
                        {'type': 'text', 'data': {
                            'text': '\n开始时间：%s \n 直播地址：https://h5.48.cn/2017appshare/memberLiveShare/index.html?id=%s' % (
                                data['msgTimeStr'],
                                extInfo['referenceObjectId'])}}
                    ]
                elif extInfo['messageObject'] == 'diantai':
                    msg = [{'type': 'text', 'data': {
                        'text': '小偶像开电台啦 \n 电台标题：%s \n \
                        电台封面：' % extInfo['referenceContent']}},
                        {'type': 'image', 'data': {
                            'file': 'https://source.48.cn%s' % extInfo['referencecoverImage']}},
                        {'type': 'text', 'data': {
                            'text': '\n开始时间：%s \n 电台地址：https://h5.48.cn/2017appshare/memberLiveShare/index.html?id=%s' % (
                                data['msgTimeStr'],
                                extInfo['referenceObjectId'])}}
                    ]
                elif extInfo['messageObject'] == 'idolFlip':
                    # INFO('idol翻牌')
                    msg = ('%s：%s\n问题内容：%s\n%s' % (
                        extInfo['senderName'], extInfo['idolFlipTitle'],
                        extInfo['idolFlipContent'], data['msgTimeStr']))
                # 自己发的消息
                elif extInfo['messageObject'] == 'messageBoard':
                    pass
                else:
                    msg = '有未知格式的文字消息'
                    INFO('有未知格式的文字消息')
                    INFO(extInfo)
            # image
            elif data['msgType'] == 1:
                bodys = json.loads(data['bodys'])
                msg = [{'type': 'text', 'data': {
                    'text': '%s：图片消息' % extInfo['senderName']}},
                    {'type': 'image', 'data': {
                        'file': '%s' % bodys['url']}},
                    {'type': 'text', 'data': {
                        'text': '\n%s' % data['msgTimeStr']}}
                ]
            # voice
            elif data['msgType'] == 2:
                bodys = json.loads(data['bodys'])
                msg = [{'type': 'text', 'data': {
                    'text': '%s：语音消息' % extInfo['senderName']}},
                    {'type': 'record', 'data': {
                        'file': '%s' % bodys['url']}},
                    {'type': 'text', 'data': {
                        'text': '\n%s' % data['msgTimeStr']}}
                ]
            # video
            elif data['msgType'] == 3:
                bodys = json.loads(data['bodys'])
                msg = ('%s：视频消息：%s\n%s' % (
                    extInfo['senderName'], bodys['url'], data['msgTimeStr']))
            else:
                msg = '有未知类型的消息'
                INFO('有未知类型的消息')
                INFO(data)
            msg_array.append(msg)
        return msg_array

    # 2018总选额外功能，检查留言板投票
    # 取前30条留言板消息，筛选出有投票的消息
    def getboardpage(self):
        cmts = []
        url = 'https://pjuju.48.cn/imsystem/api/im/v1/member/room/message/boardpage'
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
            "limit": 30,
            "isFirst": True,
            "roomId": setting.roomId()
        }
        res = requests.post(
            url,
            data=json.dumps(form),
            headers=header,
            verify=False
        ).json()
        for data in res['content']['data']:
            extInfo = json.loads(data['extInfo'])
            if "giftId" in extInfo and "voteticket" in extInfo['giftId']:
                cmts.append((extInfo['senderName'], extInfo['giftName'], data['msgTimeStr'], data['msgTime']))
        return cmts

    # 根据传入的时间间隔筛选投票消息，并包装str消息返回
    def msg_ticket(self, interval_sec):
        msgs = []
        cmts = self.getboardpage()
        if not cmts:
            return False
        for cmt in cmts:
            if cmt[3] > self.sysTime13 - 1000.0*interval_sec:
                msg = '%s：投了%s\n%s' % (cmt[0], cmt[1], cmt[2])
            msgs.append(msg)
        return msgs

#
