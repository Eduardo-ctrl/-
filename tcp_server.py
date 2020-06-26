from socket import *
from mysql_python import Mysqlpython
import datetime
import os
import signal

sockfd = socket(AF_INET,SOCK_STREAM)

sockfd.bind(('0.0.0.0',8888))

sockfd.listen(5)

db = Mysqlpython()

#忽略子进程信号
signal.signal(signal.SIGCHLD,signal.SIG_IGN)

def do_child(connfd):
    while True:
        data = connfd.recv(1024)
        L = data.decode().split(' ')
        if L[0] == 'S':
            record = db.chaxun('select * from username where name = %s',L[1:])
            if bool(record):
                s = ' '.join(record[0])
                connfd.send(s.encode())
            else:
                connfd.send(b'False')
        elif L[0] == 'I':
            try:
                db.zengshangai('insert into username values(%s,%s)',[L[1],L[2]])
                sql = ('create table %s(name char(10),word char(20),time datetime)' % L[1])
                db.create(sql)             
                connfd.send(b'OK')
            except Exception as e:
                print('Failed',e)
                connfd.send(b'NO')
        elif L[0] == 'SW':
            explanation = db.chaxun('select explanation from dict where word = %s',L[1:2])
            if bool(explanation):
                s = explanation[0][0]
                connfd.send(s.encode())
                dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                sql = 'insert into {1} values("{1}","{0}","{2}")'.format(L[1],L[2],dt)
                db.zengshangai(sql)
            else:
                connfd.send(b'False')
        elif L[0] == 'SH':
            sql = 'select * from {} order by time DESC'.format(L[1])
            record = db.chaxun(sql)
            if bool(record):
                s = str()
                for x in record:
                    x = list(x)
                    x[2] = str(x[2])
                    s += '/'.join(x) + '/'
                connfd.send(s[0:-1].encode())
            else:
                connfd.send(b'False')

while True:
    try:
        print('waitint for connect...')
        connfd,addr = sockfd.accept()
        print('connect from ',addr)
    except KeyboardInterrupt:
        sockfd.close()
        sys.exit('服务器退出')
    except Exception as e:
        print(e)
        continue


    pid = os.fork()
    if pid == 0:
        sockfd.close()
        do_child(connfd)
    else:
        connfd.close()
        continue


    connfd.close()

db.close()
sockfd.close()



