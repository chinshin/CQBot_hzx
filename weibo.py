# -*- coding: utf-8 -*-
import setting
import requests
import re
from CQLog import INFO


class Weibo:
    """docstring for Weibo"""
    response = {}
    IdArray = []

    def __init__(self):
        super(Weibo, self).__init__()
        url = str(setting.weibo_url())
        header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 \
            Safari/537.36'}
        form = {
            'containerid': int(setting.weibo_id()),
        }
        # 设置response
        self.response = requests.post(url, form, headers=header, timeout=5).json()
        # 设置id序列
        self.IdArray = self.getIdArray()

    # 去除html标签
    def dr_to_dd(self, dr_str):
        dr = re.compile(r'<[^>]+>', re.S)
        dd = dr.sub('', dr_str)
        return str(dd)

    # 获取id序列
    def getIdArray(self):
        weibo_id_array = []
        cards = self.response['data']['cards']
        for card in cards:
            try:
                weibo_id = card['mblog']['id']
            except Exception as e:
                # 广告位无id，将其置0
                weibo_id_array.append("0")
            else:
                weibo_id_array.append(weibo_id)
        INFO("weibo_id_array", weibo_id_array)
        return weibo_id_array

    # def getData(self, i):
    #     datas = self.response['data']['cards'][i]
    #     return datas

    # 检查id
    def checkId(self, i):
        datas = self.response['data']['cards'][i]
        return str(datas['mblog']['id'])

    # 检查是否为转发微博
    def checkRetweet(self, i):
        datas = self.response['data']['cards'][i]
        if datas['mblog'].get('retweeted_status') is None:
            return False
        else:
            return True

    # 获取微博正文
    def getWeibo(self, i):
        datas = self.response['data']['cards'][i]
        r_weibo = str(datas['mblog']['text'])
        r2d_weibo = self.dr_to_dd(r_weibo)
        return r2d_weibo

    # 获取转发微博
    def getRetweetWeibo(self, i):
        datas = self.response['data']['cards'][i]
        r_retweeetweibo = str(datas['mblog']['raw_text'])
        r2d_retweeetweibo = self.dr_to_dd(r_retweeetweibo)
        return r2d_retweeetweibo

    # 检查是否有图片
    def checkPic(self, i):
        datas = self.response['data']['cards'][i]
        if datas['mblog'].get('pics') is None:
            return False
        else:
            return True

    # 获取图片
    def getPic(self, i):
        datas = self.response['data']['cards'][i]
        picUrlArray = []
        for pic in datas['mblog']['pics']:
            picUrlArray.append(str(pic['url']))
        return picUrlArray

    # 获取微博链接
    def getScheme(self, i):
        datas = self.response['data']['cards'][i]
        # 转换为短网址
        url = setting.get_short_url(str(datas['scheme']))
        return str(url)

    # def getNewIdArray(self, num):
    #     weibo_id_array = []
    #     cards = self.response['data']['cards']
    #     for i in range(0, num):
    #         datas = cards[i]
    #         try:
    #             weibo_id = datas['mblog']['id']
    #         except Exception as e:
    #             weibo_id_array.append("0")
    #         else:
    #             weibo_id_array.append(weibo_id)
    #     INFO("weibo_new_id_array", weibo_id_array)
    #     return weibo_id_array

#
