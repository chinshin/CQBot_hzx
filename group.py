# -*- coding: utf-8 -*-
from cqhttp import CQHttp
import setting
import modian


bot = CQHttp(api_root='http://127.0.0.1:5700/')
# 也可以添加access_token和secret，更加安全
# bot = CQHttp(api_root='http://127.0.0.1:5700/',
#              access_token='your-token',
#              secret='your-secret')
# 如果设置了access_token和secret，请修改http-API插件的配置文件中对应的部分


# 群消息操作
@bot.on_message('group')
def handle_msg(context):
    if context['group_id'] == setting.groupid() and context['user_id'] != context['self_id']:
        # 关键词禁言
        if setting.shutup():
            for word in setting.shutup():
                if word in context['message']:
                    bot.set_group_ban(group_id=setting.groupid(), user_id=context['user_id'], duration=30*60)
        # 关键词回复
        if context['message'] == '集资' or context['message'] == 'jz' or context['message'] == '打卡' or context['message'] == 'dk':
            jz = ''
            jz_array = modian.md_init(setting.pro_id())
            for jz_dict in jz_array:
                jz += jz_dict['name'] + '\n' + jz_dict['url_short'] + '\n'
            bot.send(context, jz)
        elif context['message'] == 'wds20' or context['message'] == 'jz20' or context['message'] == 'rank' or context['message'] == '聚聚榜' or context['message'] == 'jzb' or context['message'] == '集资榜':
            rank1_array = modian.rank(1)
            for rank1_msg in rank1_array:
                bot.send(context, rank1_msg)
        elif context['message'] == 'dkb' or context['message'] == '打卡榜' or context['message'] == 'dk20' or context['message'] == 'dakabang':
            rank2_array = modian.rank(2)
            for rank2_msg in rank2_array:
                bot.send(context, rank2_msg)
        elif "独占" in context['message']:
            dz = ''
            dz_array = modian.md_init(setting.pro_id())
            for dz_dict in dz_array:
                dz += dz_dict['name'] + '\n' + dz_dict['url_short'] + '\n'
            duzhan = "独占请集资" + '\n' + dz
            bot.send(context, duzhan)
        elif context['message'] == '欢迎新人':
            bot.send(context, setting.welcome())
        elif context['message'] == '项目进度' or context['message'] == '进度':
            jd_array = modian.result(setting.pro_id())
            jd = ''
            for jd_msg in jd_array:
                jd += jd_msg + '\n'
            bot.send(context, jd)


# 新人加群提醒
@bot.on_event('group_increase')
def handle_group_increase(context):
    if context['group_id'] == setting.groupid():
        # ret = bot.get_stranger_info(user_id=context['user_id'], no_cache=False)
        # welcome = '欢迎新聚聚：@' + ret['nickname'] + ' 加入本群\n\n' + setting.welcome()
        welcome = [{'type': 'text', 'data': {'text': '欢迎新聚聚：'}},
        {'type': 'at', 'data': {'qq': context['user_id']}},
        {'type': 'text', 'data': {'text': '加入本群\n\n%s' % setting.welcome()}}
        ]
        bot.send(context, message=welcome, is_raw=True)  # 发送欢迎新人


# 如果修改了端口，请修改http-API插件的配置文件中对应的post_url
bot.run(host='127.0.0.1', port=8080)
