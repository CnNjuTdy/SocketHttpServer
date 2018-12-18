# -*- coding: utf-8 -*-
# Time       : 2018/12/18 5:49 PM
# Author     : tangdaye
# Description: 请求分析部分

from http_error import ParseRequestError
import urllib.parse


def pass_request(connection, addr):
    headers_buff, body_buff = bytes(), bytes()
    # 头部信息是字符串
    headers = ''
    # body是字符流，因为没法判断是不是字符串
    body = bytes()
    # 获取headers部分
    while True:
        buf = connection.recv(1024)
        if '\r\n\r\n'.encode('utf8') not in buf:
            # headers部分还没有结束
            headers_buff += buf
        else:
            headers_index = buf.find('\r\n\r\n'.encode('utf8'))
            headers_buff += buf[:headers_index]
            headers = parse_headers(headers_buff)
            body_buff += buf[headers_index + 4:]
            break
    print(headers)
    # 如果请求方法是post，会有body部分
    if headers['method'] == 'POST':
        content_length = int(headers['headers']['Content-Length'])
        while len(body_buff) < content_length:
            body_buff += connection.recv(1024)
    body = body_buff
    return headers, body


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
                raise ParseRequestError(msg='Parse url error. Get parameters has no key!  %s' % para)
            elif equal_index < 0:
                raise ParseRequestError(msg='Parse url error. Get parameters parses wrongly. %s' % para)
            else:
                para_key, para_value = para[:equal_index], para[equal_index + 1:]
                paras[para_key] = para_value
    else:
        true_url = url
        paras = []
    return true_url, paras


# Description: 解析请求数据头部，期待异常parse_request_error
# Input:       请求数据
# Output:      请求方法，请求url，请求http版本，请求头（key-value)
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
'''


def parse_headers(buf):
    data = buf.decode('utf8')
    parse_result = {'method': '', 'url': '', 'http_version': '', 'headers': {}, 'paras': []}
    lines = [line.strip() for line in data.strip().split('\r\n')]
    try:
        parse_result['method'], parse_result['url'], parse_result['http_version'] = lines[0].split(' ')
    except ValueError:
        raise ParseRequestError(
            msg='Parse request line error. First line of request data have to be '
                'Request-Line containing method, url and http version')
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
            raise ParseRequestError(msg='Parse request headers error. Too much keys in request data: %s' % line)
        else:
            raise ParseRequestError(msg='Parse request headers error. No key in line: %s' % line)
    return parse_result
