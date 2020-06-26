import re
from mysql_python import Mysqlpython
  
db = Mysqlpython()


L = []
pattern1 = r'\A\w+'
pattern2 = r'\s+.+$'

f = open('dict.txt','r',encoding='gbk')

for line in f:
    word = re.findall(pattern1,line)
    print(word)
    regex = re.findall(pattern2,line)
    if bool(regex):
        explanation = regex[0].lstrip()
    else:
        explanation = ' '
    L.append((word[0],explanation))

f.close()

sql = 'insert into dict values'
for x in L:
    sql += str(x)
    sql += ','
sql = sql[0:-1] + ';' 
db.zengshangai(sql)


