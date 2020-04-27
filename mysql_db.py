import pymysql
import hashlib

#定义盐
SALT = '_#AID'


class Database:
    def __init__(self,host='localhost',
                 port=3306,
                 user='root',
                 password='123456',
                 database=None,
                 charset='utf8'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        self.connect_database() #连接数据库

    #连接数据库
    def connect_database(self):
        self.db = pymysql.connect(host = self.host,
                        port = self.port,
                        user = self.user,
                        password = self.password,
                        database = self.database,
                        charset = self.charset)
    #断开连接
    def my_close(self):
        self.db.close()

    #创建游标
    def create_cursor(self):
        self.cur = self.db.cursor()

    def register(self,name,password):
        #在数据库中查询有没有此用户
        sql = "select * from user where name = '%s'" %name
        self.cur.execute(sql)
        res = self.cur.fetchone()
        if res:
            return False

        #生成哈希对象
        hash = hashlib.md5((name+SALT).encode())
        hash.update(password.encode()) #加密
        password = hash.hexdigest() #获取加密字串

        #讲用户信息插入到user表中
        sql = "insert into user (name,password) values (%s,%s)"
        try:
            self.cur.execute(sql,[name,password])
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False

    def login(self,name,password):

        hash = hashlib.md5((name + SALT).encode())
        hash.update(password.encode())  # 加密
        password = hash.hexdigest()  # 获取加密字串

        #数据库中查找
        sql = "select * from user where name = '%s' and password= '%s'" %(name,password)
        self.cur.execute(sql)
        res = self.cur.fetchone()
        if res:
            return True
        else:
            return False

    def query(self,word):
        sql = "select mean from words where word='%s'" % word
        self.cur.execute(sql)
        res = self.cur.fetchone() #单词解释，元祖类型
        if res: #如果查到了
            return res[0]

    def insert_history(self,name,word):
        sql = "insert into history (name,word) values (%s,%s)"
        try:
            self.cur.execute(sql,[name,word])
            self.db.commit()
        except Exception:
            self.db.rollback()


    def history(self,name):
        pass