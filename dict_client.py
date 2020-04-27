'''
dict客户端
根据客户端不用的输入，发送不同的请求
一级界面：注册，登录，退出
二级界面：查单词，历史记录，注销
'''

from socket import *
import getpass,sys

#全局变量
ADDR = ('127.0.0.1',8000)
#tcp套接字
s = socket()
s.connect(ADDR)

#注册
def do_register():
    while True:
        name = input('User:')
        password = getpass.getpass() #默认提示语是password
        password1 = getpass.getpass() #确认注册的密码

        if password != password1:
            print('两次密码不一致!!!')
            continue

        #账号和密码里不能有空格
        if ' ' in name or ' ' in password:
            print('用户名和密码不允许用空格')
            continue

        msg = 'R %s %s' % (name,password) #请求
        s.send(msg.encode()) #讲请求发送给服务器
        data = s.recv(128).decode() #接收服务端反馈
        if data == 'OK':
            print('注册成功')
        else:
            print('注册失败')
        return

#登录
def do_login():
    name = input('User:')
    password = getpass.getpass()
    msg = "L %s %s" %(name,password)
    s.send(msg.encode())
    data = s.recv(128).decode()
    if data == 'OK':
        print('登录成功')
        sec_interfce(name)
    else:
        print('登录失败')

def do_query(name):
    while True:
        word = input('Word:')
        if word == '##': #结束查询
            break
        msg = "Q %s %s" % (name,word)
        s.send(msg.encode())
        #接收查询结果
        data = s.recv(2048).decode()
        print(data)

def do_history(name):
    pass

#二级界面
def sec_interfce(name): #name为登录成的name
    while True:
        print('''
            二级界面
            ==============================
            1.查单词    2.历史记录    3.注销
            ==============================
            ''')
        cmd = input('请选择操作序号:')
        if cmd == '1':
            do_query(name)
        elif cmd == '2':
            do_history(name)
        elif cmd == '3':
            return
        else:
            print('请输入正确的选项')


def main():
    while True:
        print('''
            一级界面
            =========================
            1.注册    2.登录    3.退出
            =========================
            ''')
        cmd = input('请选择操作序号:')
        if cmd == '1':
            do_register()  #套接字s
        elif cmd == '2':
            do_login()
        elif cmd == '3':
            s.send(b'E')
            sys.exit()
        else:
            print('请输入正确的选项')


if __name__ == '__main__':
    main()