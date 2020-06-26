from socket import *

def First_interface():
    while True:
        print('1-->登录\n2-->注册\n3-->退出')
        numb = input("请输入:")
        if numb == '1':
            if denglu():
                break
        elif numb == '2':
            if zhuce():
                break
        elif numb == '3':
            return
        else:
            print("输入错误，请重新输入")

def Secondary_interface(username):
    while True:
        print('4-->查单词\n5-->历史记录\n6-->退出')
        numb = input("请输入:")
        if numb == '4':
            find_words(username)

        elif numb =='5':
            history(username)

        elif numb == '6':
            First_interface()
            return

        else:
            print("输入错误，请重新输入") 

def denglu():
    username = input("请输入用户名:")
    sockfd.send(('S '+username).encode())
    data = sockfd.recv(1024).decode()
    if data == 'False':
        print('Please register your account first')
    else:
        password = input("请输入密码:")
        if data.split(' ')[1] == password:
            print('Login successful')
            Secondary_interface(username)
            return True
        else:
            print('Incorrect password in put')

def zhuce():
    username = input("请输入用户名:")
    sockfd.send(('S '+username).encode())
    data = sockfd.recv(1024).decode()
    if data == 'False':
        while True:
            password = input("请输入密码:")
            if len(password) > 0 and len(password) <= 8:
                break
            else:
                print('Password only allow one to eight characters') 
        s = username + ' ' + password
        sockfd.send(('I '+s).encode())
        data = sockfd.recv(1024).decode()
        if data == 'OK':
            print('You have reqistered successfully')
            Secondary_interface(username)
            return True
        else:
            print('Please reqister agagin')
    else:
        print('This username aleady exists')

def find_words(username):
    while True:
        word = input('请输入你要查找的单词(##退出):')
        if word == '##':
            break
        sockfd.send(('SW ' + word + ' ' + username).encode())
        data = sockfd.recv(1024).decode()
        if data == 'False':
            print('There is no such word')
        else:
            print(data)

def history(username):
    while True:
        print('1-->View the last ten records\n2-->View all records\n3-->return')
        numb = input('Please enter:')
        sockfd.send(('SH ' + username).encode())
        data = sockfd.recv(1024).decode()
        if data == 'False':
            print('Record is zero')
        else:
            L = data.split('/') 
            if numb == '1':
                for x in range(min(10,len(L)//3)):
                    print(L[3*x:3*x+3])
            elif numb == '2':
                for x in range(len(L)//3):
                    print(L[3*x:3*x+3])
            elif numb == '3':
                break
            else:
                print('Input error,please re-enter')

def main():
    global sockfd
    sockfd = socket(AF_INET,SOCK_STREAM)
    sockfd.connect(('127.0.0.1',8888))
    First_interface()
    # Secondary_interface()
    sockfd.close()

if __name__ == '__main__':
    main()