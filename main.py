# -*- coding: utf-8 -*-
from cqhttp import CQHttp
import _thread
import time
from modian import newOrder
import copy
from weibo import getidarray, get_5_idarray, checkretweet, checkpic, getscheme, getretweetweibo, getweibo, getpic
from setting import groupid
from koudai48 import roomMsg
from CQLog import INFO, WARN


# 与group.py设置一样
bot = CQHttp(api_root='http://127.0.0.1:5700/')

global weibo_id_array
global firstcheck_weibo

weibo_id_array = []
firstcheck_weibo = True


def printStrTime():
    t = int(time.time()*1000)
    x = time.localtime(t / 1000)
    time_str = time.strftime('%Y-%m-%d %H:%M:%S', x)
    return time_str


def getModian(delay):
    # bot = CQHttp(api_root='http://127.0.0.1:5700/')
    while True:
        try:
            # INFO(printStrTime() + 'check modian')
            INFO('check modian')
            stampTime = int(time.time())
            msgDict = newOrder(stampTime, int(delay))
            if msgDict:
                for msg in msgDict['msg']:
                    msg += msgDict['end']
                    # print(printStrTime() + msg)
                    bot.send_group_msg_async(group_id=groupid(), message=msg, auto_escape=False)
                    time.sleep(0.1)
        except Exception as e:
            WARN('error when getModian')
        finally:
            # INFO(printStrTime() + 'modian check completed')
            INFO('modian check completed')
            time.sleep(int(delay))


def getWeibo(delay):
    # bot = CQHttp(api_root='http://127.0.0.1:5700/')
    while True:
        try:
            # INFO(printStrTime() + 'check weibo')
            INFO('check weibo')
            global weibo_id_array
            global firstcheck_weibo
            wbcontent = ''
            idcount = -1
            if (firstcheck_weibo == 1):
                # INFO(printStrTime() + 'first check weibo')
                INFO('first check weibo')
                weibo_id_array = copy.copy(getidarray())
                firstcheck_weibo = False
            checkwbid = copy.copy(get_5_idarray())
            if (firstcheck_weibo == 0):
                for cardid in checkwbid:
                    idcount += 1
                    if int(cardid) == 0:
                        continue
                    if cardid not in weibo_id_array:
                        weibo_id_array.append(cardid)
                        retweet = checkretweet(idcount)
                        wbpic = checkpic(idcount)
                        wbscheme = getscheme(idcount)
                        if (retweet):
                            wbcontent = "小偶像刚刚[转发]了一条微博：" + '\n' + '\n' + getretweetweibo(idcount) + '\n'
                            wbcontent = wbcontent + '\n' + "传送门：" + wbscheme
                        else:
                            wbcontent = "小偶像刚刚发了一条新微博：" + '\n' + '\n' + getweibo(idcount) + '\n'
                            if (wbpic):
                                wbcontent = wbcontent + getpic(idcount)
                            wbcontent = wbcontent + '\n' + "传送门：" + wbscheme
                        # print(printStrTime() + wbcontent)
                        bot.send_group_msg_async(group_id=groupid(), message=wbcontent, auto_escape=False)
        except Exception as e:
            WARN('error when getWeibo')
        finally:
            # INFO(printStrTime() + 'weibo check completed')
            INFO('weibo check completed')
            time.sleep(int(delay))


def getRoomMsg(delay):
    # bot = CQHttp(api_root='http://127.0.0.1:5700/')
    while True:
        try:
            INFO('check room')
            msg_array = roomMsg()
            if msg_array:
                INFO('new room msg')
                msg_array.reverse()
                for msgdata in msg_array:
                    bot.send_group_msg_async(group_id=groupid(), message=msgdata, auto_escape=False)
        except Exception as e:
            # raise e
            WARN('error when getRoomMsg')
        else:
            pass
        finally:
            INFO('room-check completed')
            time.sleep(int(delay))


try:
    # 摩点查询线程，时间间隔30s
    # 可修改查询时间间隔。由于摩点API缓存时间为5s，因此时间间隔不建议小于5s
    _thread.start_new_thread(getModian, (30,))
    # 微博查询线程，时间间隔60s
    # 可修改查询时间间隔。不建议小于一分钟
    _thread.start_new_thread(getWeibo, (60,))
    # 口袋房间查询线程，时间间隔30s
    # 可修改查询时间间隔。不建议小于5s（会被口袋banIP）；如果小于5s，请一定要在setting.conf中设置代理
    _thread.start_new_thread(getRoomMsg, (30,))
except Exception as e:
    WARN('error when start thread')
    # print(printStrTime() + 'Error:  unable to start thread')

while True:
    pass
