# -*- coding: utf-8 -*-
# Time       : 2018/12/12 12:06 AM
# Author     : tangdaye
# Description: todo
import socket, time

if __name__ == '__main__':
    host = 'localhost'
    port = 5000

    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.connect((host, port))

    for i in range(10):
        sk.sendall(("你好，我是Client No.%d" % i).encode("utf8"))
        data = sk.recv(1024)
        print(data.decode('UTF-8', 'ignore'))
        time.sleep(2)
        i = i + 1
