'''dict服务端
功能：业务逻辑处理
模型：tcp,多进程并发：Process
'''

from socket import *
from multiprocessing import Process
import signal,sys  #处理僵尸进程
from mysql_db import Database
from time import sleep

#全局变量
ADDR = ('0.0.0.0',8000)

db = Database(database='dict')

def do_register(c,data):
    res = data.split(' ')
    name = res[1]
    password = res[2]
    if db.register(name,password):
        c.send(b'OK')
    else:
        c.send(b'Fail')

def do_login(c,data):
    res = data.split(' ')
    name = res[1]
    password = res[2]
    if db.login(name,password):
        c.send(b'OK')
    else:
        c.send(b'Fail')

def do_query(c,data):
    res = data.split(' ')
    name = res[1]
    word = res[2]

    #插入历史记录
    db.insert_history(name,word)

    mean = db.query(word)
    if not mean:
        c.send('没有该单词'.encode())
    else:
        msg = "%s : %s" % (word,mean)
        c.send(msg.encode())


def do_history(c,data):
    pass






def request(c):
    #循环接收客户端发送来的请求
    while True:
        db.create_cursor() #每个子进程生成自己的游标
        data = c.recv(1024).decode()
        print(c.getpeername(),':',data)
        #R name password

        if not data or data[0] == 'E':
            sys.exit() #对应的子进程关闭
        elif data[0] == 'R':  #注册
            do_register(c,data) #参数：

        elif data[0] == 'L':#登录
            do_login(c,data)

        elif data[0] == 'Q':#查单词
            do_query(c,data)

        elif data[0] == 'H': #历史记录
            do_history(c,data)




#搭建网络
def main():
    s = socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(5)
    #处理僵尸进程
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)

    print('Listen The Port 8000.....')
    #循环等待客户端连接
    while True:
        try:
            c,addr = s.accept() #等待客户端连接
            print('Connect from',addr)
        except KeyboardInterrupt:  #ctrl+c 服务端退出
            s.close()
            db.my_close()
            sys.exit('服务端退出')
        except Exception as e:
            print(e)
            continue

        #有客户端连接进来了
        p = Process(target=request,args=(c,))
        p.daemon = True  #父进程退出，子进程随之退出
        p.start()


if __name__ == '__main__':
    main()




