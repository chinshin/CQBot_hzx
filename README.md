# CQBot_hzx:Branch_lottery 抽卡版本分枝

[TOC]

## 简介

基于20180614版本的[branch-master](https://github.com/chinshin/CQBot_hzx/tree/c201fa0fe06c74aecdf125ea349557af3e32e577)修改，引入了SQLite3数据库。

------

环境：`Windows Server` + `Python3` + `SQLite3`


## 更新记录

**2018.06.15更新：** init

## 使用方法

1. 按照[branch-master](https://github.com/chinshin/CQBot_hzx#使用方法)的说明文件进行配置。

2. 安装`SQLite3`，[下载地址](https://www.sqlite.org/2018/sqlite-tools-win32-x86-3240000.zip)。
将解压的三个exe文件放在C盘下的`sqlite`文件夹下，然后配置环境变量，右键计算机-属性-高级系统设置-高级-环境变量，编辑用户变量PATH，在变量值的最后增加`;C:\sqlite`。在cmd或power shell中输入`sqlite3`回车，能进入则配置成功，否则去百度！

3. 配置卡片，在本项目插件目录下有`cardpool`卡池文件夹，内含四个对应卡等级的文件夹n、r、sr、ur，将对应等级的卡放入对应文件夹即可。注意！！！**卡的文件名一定要以卡等级+空格+说明文字为命名方式，而且只支持jpg格式，如“N 01测试卡牌.jpg”，反正里面放了四个demo了，照着改然后把demo删掉就行；卡牌文件也不要过大，控制在单张500k以内吧，太大对酷q稳定性有严重影响**。

4. 抽卡默认是单抽和连抽。
单抽：10.7～106.99抽一次，金额越高越容易出稀有卡（不含ur），稀有率为5.5% ~ 17%，稀有中 r为95.4%， sr为4.4%； 
连抽：107及以上11连抽，保底1张sr，只有11连才可能出ur；稀有率为32%；稀有中 68.2%r, 27.2%sr, 4.4%ur。

5. 本抽卡概率基于高斯分布（正态分布）设置，有利于分布随机和结果随机，具有分布意义和统计意义。如果要改概率，在`lottery.py`的pick函数中修改尺度区间即可。

6. 在`group.py`中修改抽卡的说明（主要是[line60](https://github.com/chinshin/CQBot_hzx/blob/branch-lottery/group.py#L60)）。
qq群操作主要有绑卡和插卡两个命令。
```
查卡：如果已经绑定则直接返回结果，否则返回提示；
查卡#123456：会查询摩点数字id（可通过集资播报或者摩点app查询）为123456的卡片信息；
绑定#123456: 会将消息发送者的qq号与摩点数字id123456绑定，以后直接输入查卡即可查询，可无限次换绑。
```

7. 每次运行`mian.py`后，会自动进行初始化操作，将摩点订单写入本地数据库，有的摩点项目订单巨大，可能会有一定的延迟，工作后会将数据库与查询的摩点订单比对，杜绝了漏订单情况。

8. 本抽卡版本仅经过了一天的测试，有问题[issue](https://github.com/chinshin/CQBot_hzx/issues)。
