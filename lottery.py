# -*- coding: utf-8 -*-
from modian import sorted_orders, md_init, getDetail
import sqlite3
import os
from setting import pro_id, idol_name
import random
import time
from CQLog import INFO, WARN


def strtime2stamptime10(strtime):
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
            WARN("db init pro_id table failed", e)
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
        WARN("db init lottery-records table failed", e)
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
        WARN("db init qq&user_id table failed", e)
        print(e)
    else:
        conn.commit()
    # create table for r/sr/ssr
    try:
        for cardNo in range(1, 4):
            cardList = init_card(cardNo)
            cardType = cardList[0].split(" ")[0]
            cardArray = sorted(list(map(lambda e: e.split(" ")[1], cardList)))
            sql = """CREATE TABLE card_%s(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                modian_id INT NOT NULL UNIQUE""" % cardType
            for cardEle in cardArray:
                sql += """,%s INT NOT NULL DEFAULT 0""" % (cardType + cardEle)
            sql += """);"""
            c.execute(sql)
    except Exception as e:
        conn.rollback()
        WARN("db init create table for r/sr/ssr failed", e)
        print(e)
    else:
        conn.commit()
    # create table for point
    try:
        c.execute("""CREATE TABLE points(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            modian_id INT NOT NULL UNIQUE,
            point INT NOT NULL DEFAULT 0
        );""")
    except Exception as e:
        conn.rollback()
        WARN("db init create table for point failed", e)
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
            WARN("[1] api req failed", res['message'])
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
                WARN("[2] api req failed", res['message'])
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
                WARN("db init write order failed", e)
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
# 1:r 2:sr 3:ssr
def init_card(level):
    BASE_DIR = os.path.dirname(__file__)
    if level == 1:
        cardpool_r = os.path.join(BASE_DIR, 'cardpool/R/')
        list_r = read_dir_card(cardpool_r)
        return list_r
    elif level == 2:
        cardpool_sr = os.path.join(BASE_DIR, 'cardpool/SR/')
        list_sr = read_dir_card(cardpool_sr)
        return list_sr
    elif level == 3:
        cardpool_ur = os.path.join(BASE_DIR, 'cardpool/SSR/')
        list_ur = read_dir_card(cardpool_ur)
        return list_ur


# 抽对应卡
# 1:r 2:sr 3:ssr
def choose_card(level):
    cardpool = init_card(level)
    random.shuffle(cardpool)
    return random.choice(cardpool)


# 对传入的金额进行分类抽卡
def pick(float_money):
    float_money = float(float_money)
    # 初始化抽卡结果
    result = []
    # 现在有r，sr，ssr三种卡。
    # 10.7～106.99是抽一次，抽r概率95%，抽sr概率5%。
    # 107～519.99抽3次，70%出r，27%出sr，2.6出ssr。
    # 520级以上抽11次，保底一个sr，剩下的10张，70%出r，27%出sr，2.6出ssr。
    # #
    # >520
    if float_money >= 520.0:
        for i3 in range(int(float_money/520.0)):
            # 先抽保底sr 1 张
            result.append(choose_card(2))
            # 再抽10张
            for i in range(10):
                seed10 = random.normalvariate(50, 16)
                # 71%概率
                if 34 < seed10 < 66:
                    # 抽r
                    result.append(choose_card(1))
                elif 15 < seed10 < 85:
                    # 抽1张sr
                    result.append(choose_card(2))
                # 2.85%
                else:
                    # 抽1张ssr
                    result.append(choose_card(3))
    # 107~520
    elif float_money >= 107.0:
        for i2 in range(int(float_money/107.0)):
            for i in range(3):
                seed3 = random.normalvariate(50, 16)
                # 71%概率
                if 34 < seed3 < 66:
                    # 抽r
                    result.append(choose_card(1))
                elif 15 < seed3 < 85:
                    # 抽1张sr
                    result.append(choose_card(2))
                # 2.85%
                else:
                    # 抽1张ssr
                    result.append(choose_card(3))
    elif float_money >= 10.7:
        for i1 in range(int(float_money/10.7)):
            seed1 = random.normalvariate(50, 16)
            # 95.5%概率
            if 28 < seed1 < 82:
                # 抽r
                result.append(choose_card(1))
            # 2.85%
            else:
                # 抽1张sr
                result.append(choose_card(2))
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
            WARN("[3] api req failed", res['message'])
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
                WARN("[4] api req failed", res['message'])
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
                WARN("checknew insert order failed", e)
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
            init_table_by_mdid(data['user_id'])
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
                    WARN("checknew insert records failed", e)
                    print(e)
                else:
                    conn.commit()
            points_total, pointValue = cardresult2db(card_results, data['user_id'])
            if card_results:
                # 排列ur-sr-r-n
                card_results.sort(reverse=True)
                msg_lot = [{'type': 'text', 'data': {
                    'text': '\n本次抽卡结果:\n%s' % '\n'.join(card_results)}}
                ]
                msg_lot += [{'type': 'text', 'data': {
                    'text': '\n新增积分:%d, 当前积分共:%d' % (points_total, pointValue + points_total)}}
                ]
                for itr_card in card_results:
                    msg_lot += [{'type': 'image', 'data': {
                        'file': 'file://' + os.path.dirname(__file__)+'\\cardpool\\%s\\%s.png' % (itr_card.split()[0], itr_card)}}]
            else:
                msg_lot = [{'type': 'text', 'data': {
                    'text': "\n满额有抽卡喔，聚聚不来试一下？\n回复“抽卡”了解详情"}}]
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
        WARN("inquire card failed", e)
        print(e)
    else:
        msg = "您拥有的卡片如下："
        result_sql = list(map(lambda e: e[5], c.fetchall()))
        if not result_sql:
            return "暂无记录"
        try:
            c.execute("""SELECT point FROM points
                        WHERE modian_id = ?;""", (int(uid),))
            pointsValue = int(c.fetchall()[0][0])
        except Exception as e:
            WARN("inquire_card: SELECT point FROM points failed", e)
        else:
            msg += "积分：%d" % pointsValue
        result_set = list(set(result_sql))
        # result_set.sort(reverse=True)
        result_set.sort(reverse=False)
        num_r, num_sr, num_ssr = 0, 0, 0
        msg_r, msg_sr, msg_ssr = "", "", ""
        for item in result_set:
            # msg += "\n%sx%d  " % (item, result_sql.count(item))
            if item.split()[0] == "R":
                num_r += 1
                # msg_r += "\n%sx%d  " % (item, result_sql.count(item))
                msg_r += "\n%s" % item
            elif item.split()[0] == "SR":
                num_sr += 1
                # msg_sr += "\n%sx%d  " % (item, result_sql.count(item))
                msg_sr += "\n%s" % item
            elif item.split()[0] == "SSR":
                num_ssr += 1
                # msg_ssr += "\n%sx%d  " % (item, result_sql.count(item))
                msg_ssr += "\n%s" % item
        # progress
        sum_r = len(init_card(1))
        sum_sr = len(init_card(2))
        sum_ssr = len(init_card(3))
        if sum_r == num_r and sum_sr == num_sr and sum_ssr == num_ssr:
            msg += "\n恭喜您集齐了所有的卡！"
        msg += "\n目前完成进度：\n===SSR %d/%d ===" % (num_ssr, sum_ssr)
        msg += msg_ssr
        msg += "\n===SR %d/%d ===" % (num_sr, sum_sr)
        msg += msg_sr
        msg += "\n===R %d/%d ===" % (num_r, sum_r)
        msg += msg_r
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
            WARN("inquire qqid failed", e)
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
            WARN("bind qq failed", e)
            print(e)
            return False
        else:
            conn.commit()
            return True
        finally:
            conn.close()
    else:
        return False


# 补抽卡
def patch(pro_id, uid, money, card_num):
    BASE_DIR = os.path.dirname(__file__)
    sql_FILE = os.path.join(BASE_DIR, 'modian.db')
    conn = sqlite3.connect(sql_FILE)
    c = conn.cursor()
    if card_num == "1":
        card_results = pick(11)
    elif card_num == "3":
        card_results = pick(108)
    elif card_num == "11":
        card_results = pick(521)
    else:
        return False, "补卡次数指定失败"
    # 用摩点id初始化表
    init_table_by_mdid(uid)
    for card_result in card_results:
        try:
            c.execute("""INSERT INTO records VALUES(
                        NULL,?,?,?,?,?);""", (
                            int(uid),
                            int(pro_id),
                            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                            float(money),
                            card_result
                            ))
        except Exception as e:
            conn.rollback()
            WARN("patch insert records failed", e)
            print(e)
            return False, "写入数据库失败"
        else:
            conn.commit()
    points_total, pointValue = cardresult2db(card_results, uid)
    # 排列ur-sr-r-n
    card_results.sort(reverse=True)
    msg_lot = [{'type': 'text', 'data': {
        'text': '\n#%s补卡成功，本次补卡结果:\n%s' % (str(uid), '\n'.join(card_results))}}]
    msg_lot += [{'type': 'text', 'data': {
                    'text': '\n新增积分:%d, 当前积分共:%d' % (points_total, pointValue + points_total)}}]
    for itr_card in card_results:
        msg_lot += [{'type': 'image', 'data': {
            'file': 'file://' + os.path.dirname(__file__)+'\\cardpool\\%s\\%s.png' % (itr_card.split()[0], itr_card)}}]
    return True, msg_lot


def patch_msg(msg_input):
    msg_input = str(msg_input)
    msg_split = msg_input.split()
    if len(msg_split) == 5:
        try:
            status, msg_output = patch(msg_split[1], msg_split[2], msg_split[3], msg_split[4])
        except Exception as identifier:
            print(identifier)
            WARN("patch_msg failed", e)
            return "补卡失败"
        else:
            if status:
                return msg_output
            else:
                print(msg_output)
                return "补卡失败"
    else:
        return "补卡指令：\n补卡 项目ID 补卡用户摩点数字ID 金额 补卡次数"


def init_table_by_mdid(md_id):
    BASE_DIR = os.path.dirname(__file__)
    sql_FILE = os.path.join(BASE_DIR, 'modian.db')
    conn1 = sqlite3.connect(sql_FILE)
    c1 = conn1.cursor()
    # 查card_R/SR/SSR和points表中是否有 modian_id
    try:
        md_id = int(md_id)
        c1.execute("SELECT * FROM card_R WHERE modian_id=?;", (md_id,))
        inquire_result = c1.fetchall()
        # card_R中未绑定modian_id
        if not inquire_result:
            for exec_card_r in ["R", "SR", "SSR"]:
                c1.execute("""INSERT INTO card_%s (modian_id)VALUES(
                    ?);""" % exec_card_r, (
                        md_id,
                        ))
        c1.execute("SELECT * FROM points WHERE modian_id=?;", (md_id,))
        inquire_result = c1.fetchall()
        # points中未绑定modian_id
        if not inquire_result:
            c1.execute("""INSERT INTO points (modian_id)VALUES(
                ?);""", (
                    md_id,
                    ))
    except Exception as e:
        WARN("inquire SELECT * FROM card_R WHERE modian_id failed", e)
    else:
        conn1.commit()
    finally:
        conn1.close()


def cardresult2db(card_results, md_id):
    BASE_DIR = os.path.dirname(__file__)
    sql_FILE = os.path.join(BASE_DIR, 'modian.db')
    conn2 = sqlite3.connect(sql_FILE)
    c2 = conn2.cursor()
    points_total = 0
    md_id = int(md_id)
    for card_result in card_results:
        # 写入card_R/SR/SSR table
        if card_result.startswith("R"):
            try:
                cardColumn = "".join(card_result.split(" "))
                c2.execute("""SELECT %s from card_R
                    where modian_id = ?;""" % cardColumn, (md_id,))
                cardValue = c2.fetchall()[0][0]
                if not cardValue:
                    c2.execute("""UPDATE card_R SET %s = 1
                        where modian_id = ?;""" % cardColumn, (md_id,))
                else:
                    points_total += 5
            except Exception as e:
                conn2.rollback()
                WARN("SELECT %s from card_R failed", e)
                print(e)
            else:
                conn2.commit()
        elif card_result.startswith("SR"):
            try:
                cardColumn = "".join(card_result.split(" "))
                c2.execute("""SELECT %s from card_SR
                    where modian_id = ?;""" % cardColumn, (md_id,))
                cardValue = c2.fetchall()[0][0]
                if not cardValue:
                    c2.execute("""UPDATE card_SR SET %s = 1
                        where modian_id = ?;""" % cardColumn, (md_id,))
                else:
                    points_total += 20
            except Exception as e:
                conn2.rollback()
                WARN("SELECT %s from card_SR failed", e)
                print(e)
            else:
                conn2.commit()
        elif card_result.startswith("SSR"):
            try:
                cardColumn = "".join(card_result.split(" "))
                c2.execute("""SELECT %s from card_SSR
                    where modian_id = ?;""" % cardColumn, (md_id,))
                cardValue = c2.fetchall()[0][0]
                if not cardValue:
                    c2.execute("""UPDATE card_SSR SET %s = 1
                        where modian_id = ?;""" % cardColumn, (md_id,))
                else:
                    points_total += 100
            except Exception as e:
                conn2.rollback()
                WARN("SELECT %s from card_SSR failed", e)
                print(e)
            else:
                conn2.commit()
    pointValue = 0
    if points_total:
        try:
            c2.execute("""SELECT point FROM points
                WHERE modian_id = ?;""", (md_id,))
            pointValue = int(c2.fetchall()[0][0])
            c2.execute("""UPDATE points SET point = ?
                WHERE modian_id = ?;""", (int(pointValue + points_total), md_id))
        except Exception as e:
            conn2.rollback()
            WARN("UPDATE points SET point failed", e)
            print(e)
        else:
            conn2.commit()
    conn2.close()
    return points_total, pointValue


def points2card(cardtype, mdid):
    BASE_DIR = os.path.dirname(__file__)
    sql_FILE = os.path.join(BASE_DIR, 'modian.db')
    conn = sqlite3.connect(sql_FILE)
    c = conn.cursor()
    init_table_by_mdid(mdid)
    if cardtype == 1:
        charge = 40
    elif cardtype == 2:
        charge = 100
    elif cardtype == 3:
        charge = 400
    else:
        return False, "cardtype Error"
    try:
        mdid = int(mdid)
        c.execute("""SELECT point FROM points
            WHERE modian_id = ?;""", (mdid,))
        pointValue = int(c.fetchall()[0][0])
        if charge > pointValue:
            return False, "积分不足"
        else:
            # 积分抽卡 - 扣分
            c.execute("""UPDATE points SET point = ?
                WHERE modian_id = ?;""", (pointValue - charge, mdid))
            conn.commit()
            # 积分抽卡 - 抽卡
            result = choose_card(cardtype)
            points_total, pointValue = cardresult2db([result], mdid)
            # 写records库
            c.execute("""INSERT INTO records VALUES(
                NULL,?,?,?,?,?);""", (
                    mdid,
                    0,
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    0,
                    result
                    ))
            conn.commit()
    except Exception as e:
        conn.rollback()
        WARN("points2card failed", e)
        return False, "failed to update db"
    else:
        conn.commit()
    finally:
        conn.close()
    return result, (points_total, pointValue)


def handlePointPickMsg(msg, qqid):
    """积分抽R"""
    BASE_DIR = os.path.dirname(__file__)
    sql_FILE = os.path.join(BASE_DIR, 'modian.db')
    conn = sqlite3.connect(sql_FILE)
    c = conn.cursor()
    # 无user_id，查询qq是否在ids表中
    try:
        c.execute("SELECT user_id FROM ids WHERE qq=?;", (int(qqid),))
    except Exception as e:
        WARN("handlePointPickMsg inquire qqid failed", e)
        return "积分抽卡失败，database err"
    else:
        result = c.fetchall()
    # ids中绑定过了qq
    if not result:
        return "积分抽卡失败，请先绑定摩点数字ID"
    mdid = result[0][0]
    cardtype = len(msg[3:])
    pickResult, pointList = points2card(cardtype, mdid)
    if not pickResult:
        return pointList
    msg = [{'type': 'text', 'data': {
        'text': '#%d积分抽卡成功，本次抽卡结果:\n%s' % (mdid, pickResult)}}]
    pointSum = pointList[0] + pointList[1]
    if not pointSum:
        msg += [{'type': 'text', 'data': {
            'text': '\n恭喜抽到新卡'}}]
    else:
        msg += [{'type': 'text', 'data': {
            'text': '\n当前积分共:%d' % (pointList[0] + pointList[1])}}]
    return msg


def migrateRecord2Point():
    BASE_DIR = os.path.dirname(__file__)
    sql_FILE = os.path.join(BASE_DIR, 'modian.db')
    conn = sqlite3.connect(sql_FILE)
    c = conn.cursor()
    try:
        c.execute("SELECT user_id,card FROM records;")
    except Exception as e:
        WARN("migrateRecord2Point inquire failed", e)
        results = []
    else:
        results = c.fetchall()
    for result in results:
        mdid = int(result[0])
        cardName = result[1]
        init_table_by_mdid(mdid)
        cardresult2db([cardName], mdid)


#

# #
