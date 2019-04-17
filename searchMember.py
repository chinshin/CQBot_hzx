# -*- coding: utf-8 -*-
"""
使用方法：命令行中输入：文件名 -n <小偶像名字全部或部分>
或者直接使用下方def searchmember
print(searchmember("小偶像名字全部或部分"))

命令行示例:
root# python3 CQBot_hzx/searchMember.py -n 洪珮雲
result are as follows:

room name: 聊天室A
room id: 67313743
ownerId:63558
ownerName:洪珮雲

root# python3 CQBot_hzx/searchMember.py  -n 洪
result are as follows:

room name: 大型相亲交流群
room id: 67303319
ownerId: 679462
ownerName: SHY48-李苏洪

room name: A
room id: 67199579
ownerId: 327566
ownerName: GNZ48-洪静雯

room name: 聊天室A
room id: 67313743
ownerId: 63558
ownerName: 洪珮雲
"""
import requests
import json
import getopt
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def searchmember(membername):
    url = "https://pocketapi.48.cn/im/api/v1/im/search"
    form = {
        'name': membername
    }
    header = {
        'Host': 'pocketapi.48.cn',
        'accept': '*/*',
        'Accept-Language': 'zh-Hans-CN;q=1',
        'User-Agent': 'PocketFans201807/6.0.0 (iPhone; iOS 12.2; Scale/2.00)',
        'Accept-Encoding': 'gzip, deflate',
        'appInfo': '{"vendor":"apple","deviceId":"0","appVersion":"6.0.0","appBuild":"190409","osVersion":"12.2.0","osType":"ios","deviceName":"iphone","os":"ios"}',
        'Content-Type': 'application/json;charset=utf-8',
        'Connection': 'keep-alive'
    }
    try:
        response = requests.post(
            url,
            data=json.dumps(form),
            headers=header,
            verify=False,
            timeout=15).json()
        return response
    except Exception as e:
        raise e


def get_option_mem(argv):
    try:
        opts, args = getopt.getopt(argv, "n:", ["name="])
    except Exception as identifier:
        print(identifier)
        sys.exit(1)
    for opt, arg in opts:
        if opt in ("-n", "--name"):
            name = arg
            res = searchmember(name)
            if res['status'] == 200 and res['content']['data']:
                print("result are as follows:\n")
                for data in res['content']['data']:
                    msg = "room name: %s\nroom id: %s\nownerId: %s\nownerName: %s\n" % (data['targetName'], data['targetId'], data['ownerId'], data['ownerName'])
                    print(msg)
        else:
            print("""please use "searchMember.py -n <Member Name>" """)


get_option_mem(sys.argv[1:])
