# -*- coding: utf-8 -*-
# Time       : 2018/12/18 7:18 PM
# Author     : tangdaye
# Description: 业务处理部分
import http_response
import json
import os


def handle(headers, body, connection, address):
    url = headers['url']
    method = headers['method']
    print(url)
    print(method)
    if url[-1] == '/':
        http_response.send_error(connection, code=301, location=url[:-1])
    func = route(url, method, connection)
    func(headers, body, connection, address)


# 路由选择
def route(url, method, connection):
    if method == 'POST':
        if url == '/login':
            return login
        else:
            http_response.send_error(connection, code=405, msg='Method Forbidden',
                                     description='Path: %s should use method GET' % url)
            pass
    else:
        if url == '/login' or url == '/upload':
            http_response.send_error(connection, code=405, msg='Method Forbidden',
                                     description='Path: %s should use method POST' % url)
            pass
        if url == '/divide':
            return divide
        return static_resource


# get请求，请求静态资源，支持：html，js，css，png，jpg
def static_resource(headers, body, connection, address):
    root_path = './static'
    url = headers['url'][1:]
    # 绝对地址
    abs_root_path = os.path.abspath(root_path)
    abs_path = os.path.join(abs_root_path, url)
    if not os.path.exists(abs_path):
        http_response.send_error(connection, code=404, msg='File not found',
                                 description='Path: %s not found' % abs_path)
    elif os.path.isdir(abs_path):
        http_response.send_error(connection, code=403, msg='Directory Attack!',
                                 description='Target resource is a directory!')
        pass
    elif 'private' in abs_path:
        http_response.send_error(connection, code=403, msg='403 Forbidden',
                                 description='No authority')
        pass
    else:
        if abs_path[-4:] == 'html':
            content_type = 'text/html;charset=utf-8'
        elif abs_path[-2:] == 'js':
            content_type = 'application/x-javascript'
        elif abs_path[-3:] == 'css':
            content_type = 'text/css'
        elif abs_path[-3:] == 'jpg':
            content_type = 'image/jpeg'
        else:
            content_type = 'text/plain;charset=utf-8'
        with open(abs_path, 'rb') as f:
            http_response.send_response_full(connection=connection, body=f.read(), content_type=content_type, code=200)


# post请求处理登录请求
def login(headers, body, connection, address):
    json_str = body.decode('utf8')
    req = json.loads(json_str)
    if not req['name'] or not req['password']:
        http_response.send_error(connection, code=400, msg='Need at least two paras')
        pass
    if req['name'] == 'admin' and req['password'] == '123456':
        result = {'result': '登录成功'}
    else:
        result = {'result': '登录失败'}
    http_response.send_response_full(connection=connection,
                                     body=json.dumps(result, ensure_ascii=False).encode('utf8'),
                                     content_type='application/json', code=200)


# get请求除以一个数字（可能导致除零出错）
def divide(headers, body, connection, address):
    paras = headers['paras']
    if not paras['num1'] or not paras['num2']:
        http_response.send_error(connection, code=400, msg='Need at least two paras')
        pass
    try:
        num1, num2 = int(paras['num1']), int(paras['num2'])
        if num2 == 0:
            http_response.send_error(connection, code=500, msg='Sever error')
        else:
            print(num1)
            print(num2)
            result = {'result': '结果是' + str(round(num1 / num2, 2))}
            http_response.send_response_full(connection=connection,
                                             body=json.dumps(result, ensure_ascii=False).encode('utf8'),
                                             content_type='application/json', code=200)
    except ValueError:
        http_response.send_error(connection, code=400, msg='Paras have problems')
        pass
