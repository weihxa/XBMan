# XBMan
xbman 是一个linux堡垒机程序，可用于中小型企业运维人员使用。
使用说明：
1、环境准备：
    1、python2.7以上
    2、安装pyDes,paramiko,MySQLdb包
2、部署：
    1、安装linux系统，修改用户启动环境变量.bashrc  清空、添加以下语句：
    /bin/env python demo.py #路径为本系统路径即可，赋予相关权限
    logout
    2、初始化数据库
        创建xbman库
        导入xbman.sql
    3、修改配置文件
        修改conf.py中的数据库链接IP、账户、密码即可
3、使用说明
    本系统在linux系统用户登陆后自动启动，不可退出也不能被kill
    1、管理员账户为admin，默认密码为123456,登陆后可修改密码
    2、服务器ip ,其他操作账户只有管理员可以添加和管理
    3、服务器操作记录，在本软件存放目录下以日期+ip.txt命名
