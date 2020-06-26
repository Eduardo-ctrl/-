from pymysql import *

class Mysqlpython:
    def __init__(self,
                 host = 'localhost',
                 user = 'root',
                 password = '123456',
                 database = 'project1',
                 charset = 'utf8'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset

    def open(self):
        self.db = connect(host = self.host,
                          user = self.user,
                          password = self.password,
                          database = self.database,
                          charset = self.charset)
        self.cur = self.db.cursor()

    def close(self):
        self.cur.close()
        self.db.close()

    def zengshangai(self,sql,L=[]):
        try:
            self.open()
            self.cur.execute(sql,L)
            self.db.commit()
            print('OK')
        except Exception as e:
            self.db.rollback()
            print('Failed',e)
        self.close()

    def chaxun(self,sql,L=[]):
        try:
            self.open()
            self.cur.execute(sql,L)
            result = self.cur.fetchall()
            return result
        except Exception as e:
            print('Failed',e)
            self.close()

    def create(self,sql,L=[]):
        try:
            self.open()
            self.cur.execute(sql,L)
            return 'OK'
        except Exception as e:
            print('Failed',e)
            self.close()


