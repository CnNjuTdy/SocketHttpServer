# -*- coding: utf-8 -*-
# Time       : 2018/12/11 11:46 PM
# Author     : tangdaye
# Description: todo

import socket
import queue
import threading
import urllib.parse
import socketserver

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


class Server:
    def __init__(self, host='localhost', port=5000):
        print('Serving HTTP on port %d' % port)
        self.server = socketserver.ThreadingTCPServer((host, port), MyTCPHandler)

    def start(self):
        self.server.serve_forever()


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            data = self.request.recv(1024)
            if not data: break
            print(data)
            print(len(data))
        print('xxx')


class HttpError(Exception):
    def __init__(self, code='500', msg=None):
        Exception.__init__(self, msg)
        self.code = code
        self.msg = msg


class ParseRequestError(HttpError):
    def __init__(self, msg=None, parameter=None, para_value=None):
        err = msg if msg else 'The parameter "{0}" is not legal:{1}'.format(parameter, para_value)
        self.parameter = parameter
        self.para_value = para_value
        HttpError.__init__(self, msg=err)


# Description: 解析请求数据，期待异常parse_request_error
# Input:       请求数据
# Output:      请求方法，请求url，请求http版本，请求头（key-value），请求实体
'''
POST / HTTP/1.1
Host: localhost:5000
Connection: keep-alive
Content-Length: 20
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36
Cache-Control: no-cache
Origin: chrome-extension://fhbjgbiflinjbdggehcddcbncdddomop
Postman-Token: eef90e56-d8cb-076f-70ed-22d0aa37241b
Content-Type: application/json
Accept: */*
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8

{
        "name":"你好"
}
'''


def parse_request(data):
    parse_result = {'method': '', 'url': '', 'http_version': '', 'headers': {}, 'parameters': [], 'body': []}
    lines = [line.strip() for line in data.strip().split('\r\n')]
    try:
        parse_result['method'], parse_result['url'], parse_result['http_version'] = lines[0].split(' ')
    except ValueError:
        raise ParseRequestError(
            msg='First line of request data have to be Request-Line containing method, url and http version')
    if parse_result['method'] == 'GET':
        url = parse_result['url']
        try:
            parse_result['url'], parse_result['paras'] = parse_url(url)
        except ParseRequestError as e:
            raise e
        for line in lines[1:]:
            if len(line) == 0:
                continue
            if len(line.split(': ')) == 2:
                key, value = line.split(': ')
                parse_result['headers'][key] = value
            elif len(line.split(': ')) > 2:
                raise ParseRequestError(msg='Too much keys in request data: %s' % line)
            else:
                raise ParseRequestError(msg='Get request has no body like %s' % line)
    elif parse_result['method'] == 'POST':
        url = parse_result['url']
        try:
            parse_result['url'], parse_result['paras'] = parse_url(url)
        except ParseRequestError as e:
            raise e
        for line in lines[1:]:
            if len(line) == 0:
                continue
            if len(line.split(': ')) == 2:
                key, value = line.split(': ')
                parse_result['headers'][key] = value
            elif len(line.split(': ')) > 2:
                raise ParseRequestError(msg='Too much keys in request data: %s' % line)

    else:
        pass

    return parse_result


# Description: 解析出url中的参数
# Input:       url
# Output:      true_url,{para_key:para_value}
def parse_url(url):
    # 找到第一个?，并按照第一个?分割为url和paras(用index的话如果没有?会报错)
    question_mark_index = url.find('?')
    if question_mark_index >= 0:
        true_url = url[:question_mark_index]
        temp_paras = url[question_mark_index + 1:].split('&')
        paras = {}
        for para in temp_paras:
            # 一些自动转义的还原出来(%20表示空格，中文的变成中文）
            para = urllib.parse.unquote(para)
            # 按照第一个=分割
            equal_index = para.find('=')
            if equal_index == 0:
                raise ParseRequestError(msg='Get parameters has no key!  %s' % para)
            elif equal_index < 0:
                raise ParseRequestError(msg='Get parameters parses wrongly. %s' % para)
            else:
                para_key, para_value = para[:equal_index], para[equal_index + 1:]
                paras[para_key] = para_value
    else:
        true_url = url
        paras = []
    return true_url, paras


if __name__ == '__main__':
    server = Server()
    server.start()