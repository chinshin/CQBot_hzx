# CQBot_hzx

[TOC]

## 简介

基于酷Q Air的 [richardchien / CoolQ HTTP API](https://github.com/richardchien/coolq-http-api)  & [richardchien / CQHttp Python SDK](https://github.com/richardchien/cqhttp-python-sdk) 的QQ机器人，主要包括摩点（微打赏）播报、新微博播报、口袋房间／直播播报。

特别感谢 http API 和 python SDK 的作者 [richardchien](https://github.com/richardchien)，同时请注意[开源许可证、重新分发](https://github.com/richardchien/coolq-http-api#开源许可证重新分发)。

本项目代码逻辑由基于qqbot（webqq）的 [chinshin/qqbot_hzx](https://github.com/chinshin/qqbot_hzx) 移植而来，并作少许修改。

抽卡版本demo请访问[抽卡分枝](https://github.com/chinshin/CQBot_hzx/tree/branch-lottery)


------

环境：`Windows Server` + `Python3`

CoolQ HTTP API请更新至 [最新版本4.10](https://github.com/richardchien/coolq-http-api/releases/download/v4.10.0/io.github.richardchien.coolqhttpapi.cpk)


## 更新记录

**2019.06.09更新：** `main.py`、`koudai48.py` 增加2019总选投票播报

**2019.04.22更新：** `main.py`、`group.py` fix

1. 修改了`main.py` line143，修改错误；

2. 修改了`group.py`的新加群事件，更新至CQHttp Python SDK对应的最新写法。

3. CoolQ HTTP API请更新至[最新版本4.10](https://github.com/richardchien/coolq-http-api/releases/download/v4.10.0/io.github.richardchien.coolqhttpapi.cpk)。

**2019.04.22更新：** `koudai48.py` 改进

1.修改了`koudai48.py`： 改进log部分，酷Qpro部分。

2.更新了`io.github.richardchien.coolqhttpapi.cpk`，该4.x版本需要 [Visual C++ Redistributable for Visual Studio 2015](https://www.microsoft.com/zh-cn/download/confirmation.aspx?id=48145)的x86环境，如果报msvp140.dll缺失请安装该依赖。现在可以正常发送语音和图片了。

***2019.04.16更新：*** **口袋48改版**。

修改了`koudai48.py`、`main.py`、`setting.py`、`setting.conf`，使用了新接口，感谢t\*\*z、b\*\*、z\*、y\*\*等等的share。

本版本仅经过简单测试，后果自负。

现在需要在`setting.conf`中加入roomId和ownerId。

可以使用`searchMember.py`查询，用法见该文件头部说明。

**2019.03.21更新：** 感谢Shichao, ckg48整体下线, 接口更新.

**2018.11.11更新：** 祝大家节日快乐。给所有的request请求增加了timeout=5，防止请求pending导致的apscheduler instances limit堵塞任务。

**2018.07.12更新：** 增加了对翻牌消息中聚聚id的识别

现在查询不到翻牌name后，会通过新接口查询口袋id对应的nickName显示到翻牌消息中。在此 **特别感谢[flydsc](https://github.com/flydsc)** 的接口分享。

**2018.06.15更新：抽卡分枝上线** 增加了branch-lottery

具体访问[抽卡分枝](https://github.com/chinshin/CQBot_hzx/tree/branch-lottery)

**2018.06.14更新：** 摩点API增加 + 口袋房间投票消息播报（暂时性增加，总选后移除）

1.更新了`modian.py`，增加了增加自定义订单排序（sorted_orders，感谢htt家）；

2.更新了`koudai48.py`，增加两个def，用于查询留言板boardpage上投票的信息；

3.更新了`main.py`，在口袋消息def下增加了对投票信息的播报。

**2018.06.09更新：** 更新口袋房间id+优化口袋自己消息识别

1.更新了`roomid.conf`，成员口袋房间id更至20180609最新（主要ft+bej5期）；

2.更新了`koudai48.py`，增加对帐号自己发送的消息的识别。

**2018.04.27更新：** 增加多群支持、优化日志模块

1. 修改了`setting.py`、`group.py`和`main.py` ，将group_id修改为列表，支持多群发送；注意，只有第一个群支持入群机器人自动欢迎功能。
2. 修改了`CQLog.py` ，将日志自动分割的RotatingFileHandler暂时改为FileHandler，消除报错。


**2018.04.11 重大更新：** **支持酷Q版本识别，Pro现在可以发图片和语音了！**

1. 修改了`weibo.py`：现在微博设计成一个Weibo类，减少了重复请求；现在只有查询到新原创微博才会提取第一章图片，并播报图片总数，转发型微博不在播报图片；注意，因为旧微博（前十条以外）被买热门导致当成新微博播报的情况仍然存在。

2. 修改了`koudai.py`：现在口袋也被设计成一个Koudai类，将请求功能分开实现，现在支持返回酷Q air类型消息（纯str）和返回酷Q pro类型消息（拼接消息）。

3. 修改了`main.py`：现在对微博和口袋的请求均基于Weibo和Koudai类的实例。

4. 特别注意，由于传递给酷Q pro的图片/语音消息均是文件网址的形式，存在一定的请求时间；此外本项目酷Q除`group.py`之外，其他所有的消息发送方式均为异步发送（不会阻塞主线程），因此可能导致先发送的图片/语音消息晚于后发送的文字消息出现在qq中。



**2018.04.09更新：** 改进定时任务设置

1.修改了`main.py`，针对任务阻塞问题，增加了三个参数

| 参数名 | 描述 |
| :-: | :-: |
| misfire\_grace\_time | 任务错过时间大于一个周期则放弃，初步设置为一个查询周期 |
| coalesce | 多任务阻塞则合并，只执行一次 |
| max_instances | 同时运行的实例数，初步设置为5个 |

2.增加了一个现役全成员资料表`member.csv`，不定期维护。



**2018.03.25更新：** 回滚了微博修改 + 改进Log

1. 上一次更新造成了查询新微博的list超出，现在已经回滚；
2. 修改了`CQLog.py`，现在各功能（如INFO、WARN等）支持多参数（示例`WARN("phrase 1", parameter 1, parameter 2)`）；同时在微博、摩点、口袋、主文件中增加了log，便于日志查看。


**2018.03.20更新：** 摩点改进（空订单的应对）

1.修改了 `modian.py` ：增加了空订单判断，现在遇到空订单会最多重复查询5次，如果重试五次后依然返回空订单，则判断无人集资；

~~ 2.修改了 `weibo.py`：将缓存的微博数目增加到10个。 ~~


**2018.02.22更新：** 针对摩点查询做出改进（多项目查询）

1.修改了`setting.conf`、`setting.py`、`modian.py`、`group.py`和`main.py`5个文件

2.现在只需设置摩点pro_id，可以同时设置多个，用英文逗号隔开


**2018.02.19更新：** 

1.引入定时任务框架`apscheduler`，删除了死循环的辣鸡写法，极大降低CPU占用；

2.将摩点、口袋、微博查询间隔设置移入`setting.conf`，任意一项设置为0则不启用该项功能；

3.改进了`group.py`中群成员增加方法，现在只对设置文件中的指定群有效，并且at有效；

4.改动的文件有`setting.conf`、`setting.py`、`group.py`和`main.py`四个

## 使用方法

1. win server: 安装酷Q Air／Pro，进入开发者模式；
2. 把 `io.github.richardchien.coolqhttpapi.cpk`([release地址](https://github.com/richardchien/coolq-http-api/releases)) 加入酷Q文件夹下app文件夹，重启酷Q并在应用管理中打开该http-api；
3. 安装`cqhttp` 和 `apscheduler`，终端输入：`pip install cqhttp` 和 `pip install apscheduler `，环境为py2的使用pip3安装；
4. （可选）修改 `group.py` - Line 7 和 `main.py` - Line 14 ：


	```
		bot = CQHttp(api_root='http://127.0.0.1:5700/',
		             access_token='your-token',
		             secret='your-secret')
	```
	
	其中`access_token`和`secret`可以不设置；

5. 修改酷Q文件夹下`data\app\io.github.richardchien.coolqhttpapi\config\<QQ id>.json`下配置文件，将`post_url`的值修改为`http://127.0.0.1:8080/`，具体端口与`group.py`中最后一行设置的`bot.run`端口相同；如果在第4步中设置了`access_token`和`secret`，则也要在配置文件中设置对应项；
6. 修改`setting.conf`，填入相关信息；
7. 在分别终端中运行`group.py`和`main.py`。
8. 如果有其他需求或疑问，可以先查阅 [richardchien / CoolQ HTTP API](https://github.com/richardchien/coolq-http-api) 和 [richardchien / CQHttp Python SDK](https://github.com/richardchien/cqhttp-python-sdk) 的相关文档，或者提交[Issues](https://github.com/chinshin/CQBot_hzx/issues)给我；