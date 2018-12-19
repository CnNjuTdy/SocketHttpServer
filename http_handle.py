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
    # todo 如果以/结尾，重定向到没有/的请求 301
    if url[:-1] == '/':
        pass
    func = route(url, method)
    func(headers, body, connection, address)


# 路由选择
def route(url, method):
    if method == 'POST':
        if url == '/login':
            return login
        else:
            # todo 其余的请求只能被get 405
            pass
    else:
        if url == '/login' or url == '/upload':
            # todo 这两个请求只能被post 405
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
        # todo 未找到错误 404
        pass
    elif os.path.isdir(abs_path):
        # todo 目录攻击，禁止访问 403
        pass
    elif abs_root_path not in abs_path:
        # todo 不在规定的目录下，禁止访问 403
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
        # todo 缺少参数 400
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
        # todo 缺少参数 400
        pass
    try:
        num1, num2 = int(paras['num1']), int(paras['num2'])
        if num2 == 0:
            # todo 服务器内部错误，除零错误 500
            pass
        else:
            print(num1)
            print(num2)
            result = {'result': '结果是' + str(round(num1 / num2, 2))}
            http_response.send_response_full(connection=connection,
                                             body=json.dumps(result, ensure_ascii=False).encode('utf8'),
                                             content_type='application/json', code=200)
    except ValueError:
        # todo 参数有问题 400
        pass
