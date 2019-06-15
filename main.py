# -*- coding: utf-8 -*-
from cqhttp import CQHttp
# import _thread
import time
from weibo import Weibo
from koudai48 import Koudai
from setting import groupid, md_interval, kd_interval, wb_interval
from CQLog import INFO, WARN
# 引入时间调度器 apscheduler 的 BlockingScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from lottery import check_new, init_db


# 与group.py设置一样
bot = CQHttp(api_root='http://127.0.0.1:5700/')
# 实例化 BlockingScheduler
sched = BlockingScheduler()

global weibo_id_array
global firstcheck_weibo

weibo_id_array = []
firstcheck_weibo = True

# 查询时间间隔初始化
interval_md = md_interval()
interval_wb = wb_interval()
interval_kd = kd_interval()

# 获取酷q版本
version_dict = bot.get_version_info()
version = version_dict['coolq_edition']

# 初始化数据库
init_db()


def getModian():
    try:
        INFO('check lottery')
        msgs = check_new()
        for msg in msgs:
            for grpid in groupid():
                bot.send_group_msg_async(
                    group_id=grpid, message=msg, auto_escape=False)
                time.sleep(0.5)
    except Exception as e:
        WARN('error when getModian', e, "modian dict:", msgDict_array[-1])
    finally:
        # INFO(printStrTime() + 'modian check completed')
        INFO('modian check completed')


def getWeibo():
    weibo = Weibo()
    try:
        INFO('check weibo')
        global weibo_id_array
        global firstcheck_weibo
        # 初次启动记录前十条微博id
        if firstcheck_weibo is True:
            INFO('first check weibo')
            weibo_id_array = weibo.IdArray
            firstcheck_weibo = False
        if firstcheck_weibo is False:
            # 取最新的前三条微博
            for idcount in range(0, 3):
                # 广告位微博id为0，忽略
                if int(weibo.IdArray[idcount]) == 0:
                    continue
                # 微博id不在记录的id列表里，判断为新微博
                if weibo.IdArray[idcount] not in weibo_id_array:
                    msg = []
                    # 将id计入id列表
                    weibo_id_array.append(weibo.IdArray[idcount])
                    # 检查新微博是否是转发
                    if weibo.checkRetweet(idcount):
                        msg.append(
                            {
                                'type': 'text',
                                'data': {'text': '小偶像刚刚转发了一条微博：\n'}})
                        msg.append(
                            {
                                'type': 'text',
                                'data': {'text': '%s\n' % weibo.getRetweetWeibo(idcount)}})
                    # 原创微博
                    else:
                        msg.append(
                            {
                                'type': 'text',
                                'data': {'text': '小偶像刚刚发了一条新微博：\n'}})
                        msg.append(
                            {
                                'type': 'text',
                                'data': {'text': '%s\n' % weibo.getWeibo(idcount)}})
                        # 检查原创微博是否带图
                        if weibo.checkPic(idcount):
                            # 只取第一张图，pro可以直接发图，air则无
                            msg.append(
                                {
                                    'type': 'image',
                                    'data': {'file': '%s' % weibo.getPic(idcount)[0]}})
                            # 播报图的总数
                            if len(weibo.getPic(idcount)) > 1:
                                msg.append(
                                    {
                                        'type': 'text',
                                        'data': {'text': '\n(一共有%d张图喔)\n' % len(weibo.getPic(idcount))}})
                    msg.append(
                        {
                            'type': 'text',
                            'data': {'text': '传送门：%s' % weibo.getScheme(idcount)}})
                    for grpid in groupid():
                        bot.send_group_msg_async(
                            group_id=grpid, message=msg, auto_escape=False)
                        time.sleep(0.5)
                    # print(msg)
    except Exception as e:
        WARN('error when getWeibo', e)
    finally:
        INFO('weibo check completed')


def getRoomMsg():
    try:
        koudai = Koudai()
        # 检查是否有新消息
        if koudai.checkNew():
            # 判断酷Q版本
            if version == 'air':
                msgArray = koudai.msgAir()
            elif version == 'pro':
                msgArray = koudai.msgPro()
            # 消息序列反向排序
            msgArray.reverse()
            for msg in msgArray:
                for grpid in groupid():
                    bot.send_group_msg_async(
                        group_id=grpid, message=msg, auto_escape=False)
                    time.sleep(0.5)
                # print(msg)
        # 2019 投票播报
        ticket_msg = koudai.getVoteMsg(int(interval_kd))
        if ticket_msg:
            ticket_msg.reverse()
            for msg in ticket_msg:
                for grpid in groupid():
                    bot.send_group_msg_async(
                        group_id=grpid, message=msg, auto_escape=False)
                    time.sleep(0.5)
    except Exception as e:
        # raise e
        WARN('error when getRoomMsg', e)
    else:
        pass
    finally:
        INFO('room-check completed')


# 添加调度任务， 间隔为 0 则不添加
if interval_md != 0:
    # 20180409
    # 增加misfire_grace_time参数：任务错过时间大于一个周期则放弃
    # 增加coalesce参数：多个错过任务合并执行一次
    # 增加max_instances参数：允许5个实例同时运行
    sched.add_job(
        getModian, 'interval', seconds=interval_md,
        misfire_grace_time=interval_md, coalesce=True, max_instances=5)
if interval_wb != 0:
    sched.add_job(
        getWeibo, 'interval', seconds=interval_wb,
        misfire_grace_time=interval_wb, coalesce=True, max_instances=5)
if interval_kd != 0:
    sched.add_job(
        getRoomMsg, 'interval', seconds=interval_kd,
        misfire_grace_time=interval_kd, coalesce=True, max_instances=5)
# 开始调度任务
sched.start()
