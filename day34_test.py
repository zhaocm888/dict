电子词典



技术点的确定
    套接字:tcp
    并发：多进程  fork  Process
    历史记录:10条
    注册成功：直接登录

数据表的建立
    dict    words       id  word    mean
            user        id  name    password(128)
            history     id  name    word        time

    user:
        create table user (id int primary key auto_increment,
                            name varchar(32) not null,
                            password varchar(128) not null);

    history:
        create table history (id int primary key auto_increment,
                                name varchar(32) not null,
                                word varchar(28) not null,
                                time datetime default now());



结构设计: 模块  封装    功能

    服务端：
        模块设计：
            逻辑处理模块  dict_server.py
            数据库操作处理 mysql_db.py

        封装：函数封装
                直接写一个功能提供给使用者

        功能：
            搭建网络,并发
            登录
            注册
            查单词
            查历史记录（10条）





    客户端:
        搭建网络
        根据用户的输入，发送不同的请求，得到服务端的反馈
        一级界面
        二级界面
        登录
        注册
        查单词
        查历史记录



拓展：
    隐藏输入:
        import getpass
        getpass.getpass()


    加密处理：
        import hashlib
        hash = hashlib.md5((name+'*#qwe').encode())#生成哈希对象
        hash.update(pwd.encode()) #算法加密
        pwd = hash.hexdigest() #提取加密后密码
        print(pwd)



制定协议：
    注册： R
    登录： L
    查单词：Q
    历史记录:H
    退出:E


具体功能分析：shoudao
    1.注册：
        客户端：
            输入注册信息
            发送请求 R + name + password
            得到反馈

        服务端：
            接收请求
            判断是否能注册 （数据库里面去查一查，有没有这个人）
            允许注册，将用户信息存入数据库
            给客户端发送反馈


    2.登录
        客户端
            输入登录信息
            发送请求
            得到反馈

        服务端
            接收请求
            判断是否允许登录（在数据库中查找输入的信息和数据库中的是否一致）
            发送结果


    3.退出


二级界面：
    查单词
        客户端：
            输入单词
            发送请求 Q name word
            等待接收结果

        服务端：
            接收请求
            查找单词    (数据库中)
            发送结果
            插入历史记录: name,word

    历史记录:
         客户端：
            发送请求

         服务端：
            接收请求
            查询历史记录(10跳)
            发送结果


    注销
