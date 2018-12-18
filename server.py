# -*- coding: utf-8 -*-
# Time       : 2018/12/11 11:46 PM
# Author     : tangdaye
# Description: todo

import socket
import queue
import threading
import http_request, http_response

general_header_field = [
    'Cache-Control', 'Connection', 'Date', 'Pragma', 'Trailer', 'Transfer-Encoding', 'Upgrade', 'Via', 'Warning'
]
request_header_field = [
    'Accept', 'Accept-Charset', 'Accept-Encoding', 'Accept-Language', 'Authorization', 'Expect', 'From', 'Host',
    'If-Match', 'If-Modified-Since', 'If-None-Match', 'If-Range', 'If-Unmodified-Since', 'Max-Forwards',
    'Proxy-Authorization', 'Range', 'Referer', 'TE', 'User-Agent'
]
response_header_field = [
    'Accept-Ranges', 'Age', 'ETag', 'Location', 'Proxy-Authenticate', 'Retry-After', 'Server', 'Vary',
    'WWW-Authenticate'
]
entity_header_field = [
    'Allow', 'Content-Encoding', 'Content-Language', 'Content-Length', 'Content-Location', 'Content-MD5',
    'Content-Range', 'Content-Type', 'Expires', 'Last-Modified', 'extension-header'
]


# 线程类
class WorkThread(threading.Thread):
    def __init__(self, work_queue):
        super().__init__()
        self.work_queue = work_queue
        self.daemon = True

    def run(self):
        while True:
            func, args = self.work_queue.get()
            func(*args)
            self.work_queue.task_done()


# 连接池管理
class ThreadPoolManger:
    def __init__(self, thread_number):
        self.thread_number = thread_number
        self.work_queue = queue.Queue()
        for i in range(self.thread_number):  # 生成一些线程来执行任务
            thread = WorkThread(self.work_queue)
            thread.start()

    def add_work(self, func, *args):
        self.work_queue.put((func, args))


# Description: 请求主函数，将会交给线程池中的一个线程来执行
# Input:       连接，地址
# Output:      None
def tcp_link(connection, address):
    # 获得请求头和body
    headers, body = http_request.pass_request(connection, address)
    # todo 业务处理
    print(headers)
    print(body)
    # todo 组装并返回response
    connection.send('Hello world!'.encode('utf8'))


class Server:
    def __init__(self, host='localhost', port=5000):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.socket.listen(1)
        self.thread_pool = ThreadPoolManger(5)
        print('Serving HTTP on port %d' % port)

    def start(self):
        while True:
            connection, address = self.socket.accept()
            self.thread_pool.add_work(tcp_link, *(connection, address))


if __name__ == '__main__':
    server = Server()
    server.start()
