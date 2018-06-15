# -*- coding: utf-8 -*-
from modian import sorted_orders, md_init, getDetail
import sqlite3
import os
from setting import pro_id, idol_name
import random


def strtime2stamptime10(strtime):
    import time
    return int(time.mktime(time.strptime(strtime, '%Y-%m-%d %H:%M:%S')))


# 初始化数据库、表、将order表更新至最新
def init_db():
    # create db
    BASE_DIR = os.path.dirname(__file__)
    sql_FILE = os.path.join(BASE_DIR, 'modian.db')
    conn = sqlite3.connect(sql_FILE)
    c = conn.cursor()
    # create table by pro_id
    for pid in pro_id():
        try:
            c.execute("""CREATE TABLE order_%s(
                oid INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INT NOT NULL,
                nickname    TEXT    NOT NULL,
                order_time  CHAR(19)    NOT NULL,
                pay_success_time    CHAR(19)    NOT NULL,
                backer_money    FLOAT NOT NULL
            );""" % str(pid))
        except Exception as e:
            conn.rollback()
            print(e)
        else:
            conn.commit()
    # create table for lottery-records
    try:
        c.execute("""CREATE TABLE records(
            rid INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INT NOT NULL,
            pro_id  INT,
            pay_success_time    CHAR(19),
            backer_money    FLOAT,
            card   CHAR(13)    NOT NULL
        );""")
    except Exception as e:
        conn.rollback()
        print(e)
    else:
        conn.commit()
    # create table for qq&user_id
    try:
        c.execute("""CREATE TABLE ids(
            iid INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INT NOT NULL UNIQUE,
            qq INT UNIQUE,
            nickname_modian TEXT
        );""")
    except Exception as e:
        conn.rollback()
        print(e)
    else:
        conn.commit()
    # sync by sorted_orders API
    for pid in pro_id():
        # 查询order_proid表中最新的时间
        for row in c.execute("SELECT max(rowid), pay_success_time FROM order_%d" % pid):
            # 空表则置0
            if not row[1]:
                dborder_latest_time = "0"
            else:
                dborder_latest_time = row[1]
        list_data = []
        page = 1
        res = sorted_orders(pid, page)
        # API请求错误则break
        if res['status'] == 2:
            print(res['message'])
            break
        # 空单则break
        if not res['data']:
            break
        # 遍历订单第1页data
        for data in res['data']:
            if data['pay_success_time'] > dborder_latest_time:
                list_data.append(data)
        # 当前页最后一条订单仍新于表，则请求前一页
        while res['data'][-1]['pay_success_time'] > dborder_latest_time:
            page += 1
            res = sorted_orders(pid, page)
            if res['status'] == 2:
                print(res['message'])
                break
            if not res['data']:
                break
            for data in res['data']:
                if data['pay_success_time'] > dborder_latest_time:
                    list_data.append(data)
        # 按原顺序去重，倒序（按paytime从旧到新排列）
        # dict不可hash，无法去重
        # list_data_all = sorted(set(list_data), key=list_data.index, reverse=True)
        list_data.reverse()
        # 写入order表
        for data in list_data:
            try:
                c.execute("""INSERT INTO order_%s VALUES(
                    NULL,?,?,?,?,?);""" % pid, (
                        data['user_id'],
                        data['nickname'],
                        data['order_time'],
                        data['pay_success_time'],
                        data['backer_money']
                        ))
            except Exception as e:
                conn.rollback()
                print(e)
            else:
                conn.commit()
    conn.close()


# 读目录中以.jpg结尾的文件，返回一个list
def read_dir_card(dir):
    list_card = []
    for filename in os.listdir(dir):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            list_card.append(filename[0:-4])
    return list_card


# 初始化card
# 0:n 1:r 2:sr 3:ur
def init_card(level):
    BASE_DIR = os.path.dirname(__file__)
    if level == 0:
        cardpool_n = os.path.join(BASE_DIR, 'cardpool/N/')
        list_n = read_dir_card(cardpool_n)
        return list_n
    elif level == 1:
        cardpool_r = os.path.join(BASE_DIR, 'cardpool/R/')
        list_r = read_dir_card(cardpool_r)
        return list_r
    elif level == 2:
        cardpool_sr = os.path.join(BASE_DIR, 'cardpool/SR/')
        list_sr = read_dir_card(cardpool_sr)
        return list_sr
    elif level == 3:
        cardpool_ur = os.path.join(BASE_DIR, 'cardpool/UR/')
        list_ur = read_dir_card(cardpool_ur)
        return list_ur


# 抽对应卡
# 0:n 1:r 2:sr 3:ur
def choose_card(level):
    cardpool = init_card(level)
    random.shuffle(cardpool)
    return random.choice(cardpool)


# 对传入的金额进行分类抽卡
def pick(float_money):
    float_money = float(float_money)
    # 初始化抽卡结果
    result = []
    # 设置区间
    # #
    # 借鉴lovelive
    # n为普通卡，概率95%
    # r为稀有卡，概率5%
    # ur 5%
    # sr 15%
    # r 80%
    # #
    # 考虑正态分布，具有分布意义
    # 正态分布 半边 1σ:34.1%; 2σ:13.6%; 3σ:2.1%; 0.1%;
    # normalvariate(µ, σ)中，µ是位置参数，σ是尺度参数
    # #
    # 最终设置如下
    # 单抽:
    # 10.7～106.99抽一次，金额越高越容易出稀有卡（不含ur）
    # 稀有率为5.5% ~ 17%
    # 稀有中 r为95.4%， sr为4.4%
    # 连抽
    # 107及以上11连抽，保底1张sr，只有11连才可能出ur
    # 稀有率为32%
    # 稀有中 68.2%r, 27.2%sr, 4.4%ur
    if float_money >= 107.0:
        # 先抽保底sr 1 张
        result.append(choose_card(2))
        # 再抽10张
        for i in range(10):
            # 68%概率
            if 34 < int(random.normalvariate(50, 16)) < 66:
                # 抽普通n
                result.append(choose_card(0))
            # 32%
            else:
                seed10 = int(random.normalvariate(50, 16))
                # 抽稀有（有ur）, 68.2%r, 27.2%sr, 4.4%ur
                if 34 < seed10 < 66:
                    # 抽1张r
                    result.append(choose_card(1))
                elif 18 < seed10 < 82:
                    # 抽1张sr
                    result.append(choose_card(2))
                else:
                    # 抽1张ur
                    result.append(choose_card(3))
    # elif float_money >= 10.7:
    elif float_money >= 10:
        # 稀有概率为5.5% ~ 17%，以10.6的整数倍为阶梯增加
        seed1 = int(random.normalvariate(50, 16))
        if (seed1 >= 82-float_money/10.6) or (seed1 <= 18+float_money/10.6):
            # 抽稀有（无ur）,95.4%r, 4.4%sr
            if 18 < int(random.normalvariate(50, 16)) < 82:
                # 抽1张r
                result.append(choose_card(1))
            else:
                # 抽1张sr
                result.append(choose_card(2))
        else:
            # 抽1张n
            result.append(choose_card(0))
    return result


def check_new():
    msg_list = []
    pro_id_array = md_init(pro_id())
    # 查询订单，逻辑于init_db相同
    BASE_DIR = os.path.dirname(__file__)
    sql_FILE = os.path.join(BASE_DIR, 'modian.db')
    conn = sqlite3.connect(sql_FILE)
    c = conn.cursor()
    for pro_id_dict in pro_id_array:
        detail = getDetail(pro_id_dict['pro_id'])
        list_data = []
        # 查询order_proid表中最新的时间
        for row in c.execute("SELECT max(rowid), pay_success_time FROM order_%d" % pro_id_dict['pro_id']):
            # 空表则置0
            if not row[1]:
                dborder_latest_time = "0"
            else:
                dborder_latest_time = row[1]
        page = 1
        res = sorted_orders(pro_id_dict['pro_id'], page)
        # API请求错误则break
        if res['status'] == 2:
            print(res['message'])
            break
        # 空单则break
        if not res['data']:
            break
        # 遍历订单第1页data
        for data in res['data']:
            if data['pay_success_time'] > dborder_latest_time:
                list_data.append(data)
        # 当前页最后一条订单仍新于表，则请求前一页
        while res['data'][-1]['pay_success_time'] > dborder_latest_time:
            page += 1
            res = sorted_orders(pro_id_dict['pro_id'], page)
            if res['status'] == 2:
                print(res['message'])
                break
            if not res['data']:
                break
            for data in res['data']:
                if data['pay_success_time'] > dborder_latest_time:
                    list_data.append(data)
        list_data.reverse()
        for data in list_data:
            try:
                c.execute("""INSERT INTO order_%s VALUES(
                    NULL,?,?,?,?,?);""" % pro_id_dict['pro_id'], (
                        data['user_id'],
                        data['nickname'],
                        data['order_time'],
                        data['pay_success_time'],
                        data['backer_money']
                        ))
                '''c.execute("""INSERT INTO records VALUES(
                    NULL,?,?,?,?,?,?);""", (
                        data['user_id'],
                        pro_id_dict['pro_id'],
                        data['pay_success_time'],
                        data['backer_money'],
                        card
                        ))'''
            except Exception as e:
                conn.rollback()
                print(e)
            else:
                conn.commit()
            msg_md_top = "ID: " + data['nickname'] + " #" + str(data['user_id']) +\
                " 的聚聚刚刚在【" + pro_id_dict['name'] + "】中支持了 ¥" +\
                str(data['backer_money']) + '\n' + "感谢这位聚聚对" +\
                idol_name() + "的支持" + '\n'
            msg_md_end = '【摩点】：' + pro_id_dict['url_short'] + '\n目前集资进度：¥' +\
                str(detail['data'][0]['already_raised']) + '\n目标：¥' +\
                str(detail['data'][0]['goal'])
            msg_md = [{'type': 'text', 'data': {
                    'text': msg_md_top + msg_md_end}}]
            # 写入抽卡结果
            card_results = pick(data['backer_money'])
            for card_result in card_results:
                try:
                    c.execute("""INSERT INTO records VALUES(
                        NULL,?,?,?,?,?);""", (
                            data['user_id'],
                            pro_id_dict['pro_id'],
                            data['pay_success_time'],
                            data['backer_money'],
                            card_result
                            ))
                except Exception as e:
                    conn.rollback()
                    print(e)
                else:
                    conn.commit()
            if card_results:
                # 排列ur-sr-r-n
                card_results.sort(reverse=True)
                msg_lot = [{'type': 'text', 'data': {
                    'text': '\n本次抽卡结果:%s' % ','.join(card_results)}},
                    {'type': 'image', 'data': {
                        'file': 'file://' + os.path.dirname(__file__)+'\\cardpool\\%s\\%s.jpg' % (card_results[0].split()[0], card_results[0])}}
                ]
            else:
                msg_lot = [{'type': 'text', 'data': {
                    'text': "满额有抽卡喔，聚聚不来试一下？回复“抽卡”了解详情"}}]
            # 播报至酷q
            msg = msg_md + msg_lot
            msg_list.append(msg)
    conn.close()
    return msg_list


# 查records
def inquire_card(uid):
    BASE_DIR = os.path.dirname(__file__)
    sql_FILE = os.path.join(BASE_DIR, 'modian.db')
    conn = sqlite3.connect(sql_FILE)
    c = conn.cursor()
    try:
        c.execute("SELECT * FROM records WHERE user_id=?;", (int(uid),))
    except Exception as e:
        print(e)
    else:
        msg = "您拥有的卡片如下：\n"
        result_sql = list(map(lambda e: e[5], c.fetchall()))
        result_set = list(set(result_sql))
        for item in result_set:
            msg += "%sx%d  " % (item, result_sql.count(item))
        return msg
    finally:
        conn.close()


# 查询功能
def inquire(qqid, uid=None):
    BASE_DIR = os.path.dirname(__file__)
    sql_FILE = os.path.join(BASE_DIR, 'modian.db')
    conn = sqlite3.connect(sql_FILE)
    c = conn.cursor()
    # 无user_id，查询qq是否在ids表中
    if not uid:
        try:
            c.execute("SELECT * FROM ids WHERE qq=?;", (int(qqid),))
        except Exception as e:
            print(e)
        else:
            result = c.fetchall()
        # ids中绑定过了qq
        if result:
            return inquire_card(result[0][1])
        else:
            return False
    # 有user_id，查询卡片
    else:
        return inquire_card(uid)


# qq绑定user_id
def bind_qq(qq, uid):
    if qq and uid:
        BASE_DIR = os.path.dirname(__file__)
        sql_FILE = os.path.join(BASE_DIR, 'modian.db')
        conn = sqlite3.connect(sql_FILE)
        c = conn.cursor()
        try:
            if inquire(qq):
                c.execute("UPDATE ids set user_id=? where qq=?", (int(uid), int(qq)))
            else:
                c.execute("INSERT INTO ids VALUES(NULL,?,?,NULL);", (int(uid), int(qq)))
        except Exception as e:
            conn.rollback()
            print(e)
            return False
        else:
            conn.commit()
            return True
        finally:
            conn.close()
    else:
        return False


#
#
