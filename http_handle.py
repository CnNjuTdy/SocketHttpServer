# -*- coding: utf-8 -*-
# Time       : 2018/12/18 7:18 PM
# Author     : tangdaye
# Description: 业务处理部分
import http_response
import os


def handle(headers, body, connection, address):
    print(headers)
    print(body)
    url = headers['url']
    method = headers['method']
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
        if url == '/upload':
            return upload
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
    url = headers['url']
    path = os.path.join(root_path, url)
    # 绝对地址
    abs_root_path = os.path.abspath(root_path)
    abs_path = os.path.abspath(path)

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
        # todo 正常返回静态文件 200
        pass


# post请求处理登录请求
def login(headers, body, connection, address):
    json_str = body.encode()
    pass


# post请求处理文件上传请求
def upload(headers, body, connection, address):
    pass


# get请求除以一个数字（可能导致除零出错）
def divide(headers, body, connection, address):
    paras = headers['paras']
    if not paras['num1'] or not paras['num2']:
        # todo 正常返回，缺少参数 200
        pass
    try:
        num1, num2 = int(paras['num1']), int(paras['num1'])
        if num2 == 0:
            # todo 服务器内部错误，除零错误
            pass
        else:
            result = num1 / num2
            # todo 正常返回结果 200
    except ValueError:
        # todo 正常返回，参数有问题 200
        pass
