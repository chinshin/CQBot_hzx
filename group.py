# -*- coding: utf-8 -*-
from cqhttp import CQHttp
import setting
import modian


bot = CQHttp(api_root='http://127.0.0.1:5700/')


@bot.on_message('group')
def handle_msg(context):
    if context['group_id'] == setting.groupid() and context['user_id'] != context['self_id']:
        if setting.shutup():
            for word in setting.shutup():
                if word in context['message']:
                    bot.set_group_ban(group_id=setting.groupid(), user_id=context['user_id'], duration=30*60)
        if context['message'] == '集资' or context['message'] == 'jz' or context['message'] == '打卡' or context['message'] == 'dk':
            jz = ''
            jz += setting.wds_name() + '\n' + setting.wds_url()
            bot.send(context, jz)
        elif context['message'] == 'wds20' or context['message'] == 'jz20' or context['message'] == 'rank' or context['message'] == '聚聚榜' or context['message'] == 'jzb' or context['message'] == '集资榜':
            bot.send(context, modian.rank(1))
        elif context['message'] == 'dkb' or context['message'] == '打卡榜' or context['message'] == 'dk20' or context['message'] == 'dakabang':
            bot.send(context, modian.rank(2))
        elif "独占" in context['message']:
            duzhan = "独占请集资" + '\n' + setting.wds_name() + '\n' + setting.wds_url()
            bot.send(context, duzhan)
        elif context['message'] == '欢迎新人':
            bot.send(context, setting.welcome())
        elif context['message'] == '项目进度' or context['message'] == '进度':
            jd = modian.result(setting.pro_id()) + '\n' + setting.wds_url()
            bot.send(context, jd)


@bot.on_event('group_increase')
def handle_group_increase(context):
    ret = bot.get_stranger_info(user_id=context['user_id'], no_cache=False)
    welcome = '欢迎新聚聚：@' + ret['nickname'] + ' 加入本群\n\n' + setting.welcome()
    bot.send(context, message=welcome, is_raw=True)  # 发送欢迎新人


bot.run(host='127.0.0.1', port=8080)
