# CQBot_hzx

[TOC]

## 简介

基于酷Q Air的 [richardchien / CoolQ HTTP API](https://github.com/richardchien/coolq-http-api)  & [richardchien / CQHttp Python SDK](https://github.com/richardchien/cqhttp-python-sdk) 的QQ机器人，主要包括摩点（微打赏）播报、新微博播报、口袋房间／直播播报。

特别感谢 http API 和 python SDK 的作者 [richardchien](https://github.com/richardchien)，同时请注意[开源许可证、重新分发](https://github.com/richardchien/coolq-http-api#开源许可证重新分发)。

本项目代码逻辑由基于qqbot（webqq）的 [chinshin/qqbot_hzx](https://github.com/chinshin/qqbot_hzx) 移植而来，并作少许修改。

------

环境：`Windows Server` + `Python3`


## 更新记录



## 使用方法

1. win server: 安装酷Q Air／Pro，进入开发者模式；
2. 把 `io.github.richardchien.coolqhttpapi.cpk`([release地址](https://github.com/richardchien/coolq-http-api/releases)) 加入酷Q文件夹下app文件夹，重启酷Q并在应用管理中打开该http-api；
3. 安装`cqhttp`，终端输入：`pip install cqhttp`，环境为py2的使用pip3安装；
4. （可选）修改 `group.py` - Line 7 和 `main.py` - Line 14 ：

	```
bot = CQHttp(api_root='http://127.0.0.1:5700/',
                 access_token='your-token',
                 secret='your-secret')
```
	其中`access_token`和`secret`可以不设置；

5. 修改酷Q文件夹下`app\io.github.richardchien.coolqhttpapi\`下配置文件，将`post_url`的值修改为`http://127.0.0.1:8080/`，具体端口与`group.py`中最后一行设置的`bot.run`端口相同；如果在第4步中设置了`access_token`和`secret`，则也要在配置文件中设置对应项；
6. 修改`setting.conf`，填入相关信息；
7. （可选）修改`main.py`中 Line 120 - 126 ，最后的int即为查询的时间间隔；如果有不需要的功能请注释；
8. 在分别终端中运行`group.py`和`main.py`。
9. 如果有其他需求或疑问，可以先查阅 [richardchien / CoolQ HTTP API](https://github.com/richardchien/coolq-http-api) 和 [richardchien / CQHttp Python SDK](https://github.com/richardchien/cqhttp-python-sdk) 的相关文档，或者提交[Issues](https://github.com/chinshin/CQBot_hzx/issues)给我；