# -*- coding: utf-8 -*-
# Time       : 2018/12/16 2:15 PM
# Author     : tangdaye
# Description: todo

# __author__ = "wyb"
# date: 2018/6/5
# 代码: 高内聚低耦合 -> 使用函数封装一些逻辑代码 -> 功能函数

import socket
import ssl
"""
在 Python3 中，bytes 和 str 的互相转换方式是
str.encode('utf-8')
bytes.decode('utf-8')

send 函数的参数和 recv 函数的返回值都是 bytes 类型

一、使用 https
    1, https 请求的默认端口是 443
    2, https 的 socket 连接需要 import ssl
        并且使用 s = ssl.wrap_socket(socket.socket()) 来初始化

二、HTTP 协议的 301 状态
    请求豆瓣电影 top250 (注意协议)
    http://movie.douban.com/top250
    返回结果是一个 301
    301 状态会在 HTTP 头的 Location 部分告诉你应该转向的 URL
    所以, 如果遇到 301, 就请求新地址并且返回
        HTTP/1.1 301 Moved Permanently
        Date: Sun, 05 Jun 2016 12:37:55 GMT
        Content-Type: text/html
        Content-Length: 178
        Connection: keep-alive
        Keep-Alive: timeout=30
        Location: https://movie.douban.com/top250
        Server: dae
        X-Content-Type-Options: nosniff

        <html>
        <head><title>301 Moved Permanently</title></head>
        <body bgcolor="white">
        <center><h1>301 Moved Permanently</h1></center>
        <hr><center>nginx</center>
        </body>
        </html>

https 的默认端口是 443, 所以你需要在 get 函数中根据协议设置不同的默认端口
"""


# 功能函数:
# 解析url产生protocol、host、port、path
def parsed_url(url):
    """
    :param url: 字符串, 可能的值如下
    'g.cn'
    'g.cn/'
    'g.cn:3000'
    'g.cn:3000/search'
    'http://g.cn'
    'https://g.cn'
    'http://g.cn/'
    :return: 返回一个 tuple, 内容: (protocol, host, port, path)
    """
    protocol = "http"
    if url[:7] == "http://":
        u = url.split("://")[1]
    elif url[:8] == "https://":
        protocol = "https"
        u = url.split("://")[1]
    else:
        u = url

    # 检查默认path
    i = u.find("/")
    if i == -1:
        host = u
        path = "/"
    else:
        host = u[:i]
        path = u[i:]

    # 检查端口
    port_dict = {
        "http": 80,
        "https": 443,
    }
    # 默认端口
    port = port_dict[protocol]
    if ":" in host:
        h = host.split(":")
        host = h[0]
        port = int(h[1])

    return protocol, host, port, path


# 根据协议返回socket实例
def socket_by_protocol(protocol):
    """
    根据协议返回socket实例
    :param protocol: 协议
    :return: socket实例
    """
    if protocol == "http":
        s = socket.socket()             # 生成一个socket对象

    else:
        # HTTPS 协议需要使用 ssl.wrap_socket 包装一下原始的 socket
        # 除此之外无其他差别
        s = ssl.wrap_socket(socket.socket())
    return s


# 根据socket对象接受数据
def response_by_socket(s):
    """
    接受数据
    :param s: socket实例
    :return: response
    """
    response = b""
    buffer_size = 1024
    while True:
        r = s.recv(buffer_size)
        if len(r) == 0:
            break
        response += r
    return response


# 把 response 解析出 状态码 headers body 返回
def parsed_response(r):
    """
    解析response对象获取状态码、headers、body
    :param r: response
    :return: tuple(status_code, headers, body)
    """
    header, body = r.split('\r\n\r\n', 1)
    h = header.split('\r\n')
    # headers的头部: HTTP/1.1 200 OK
    status_code = h[0].split()[1]
    status_code = int(status_code)

    headers = {}
    for line in h[1:]:
        k, v = line.split(': ')
        headers[k] = v
    return status_code, headers, body


# 主逻辑函数:
# 把向服务器发送 HTTP 请求并且获得数据这个过程封装成函数 -> 复杂的逻辑(具有重用性)封装成函数
def get(url):
    """
    使用 socket 连接服务器，获取服务器返回的数据并返回
    :param url: 链接地址，url的值如下:
    'g.cn'
    'g.cn/'
    'g.cn:3000'
    'g.cn:3000/search'
    'http://g.cn'
    'https://g.cn'
    'http://g.cn/'
    :return: 返回tuple(status_code, headers, body)
    """
    protocol, host, port, path = parsed_url(url)

    # 得到socket对象并连接服务器
    s = socket_by_protocol(protocol)
    s.connect((host, port))

    # 发送请求
    request = 'GET {} HTTP/1.1\r\nhost: {}\r\nConnection: close\r\n\r\n'.format(path, host)
    encoding = 'utf-8'
    s.send(request.encode(encoding))

    # 获得响应
    response = response_by_socket(s)
    r = response.decode(encoding)

    # 解析响应
    status_code, headers, body = parsed_response(r)
    # 当状态码为301或302时表示为重定向
    if status_code in [301, 302]:
        url = headers['Location']
        return get(url)

    return status_code, headers, body


# 单元测试:
def test_parsed_url():
    """
    parsed_url函数很容易出错，我们写测试函数来运行检测是否正确运行
    """
    http = "http"
    https = "https"
    host = "g.cn"
    path = "/"
    test_items = [
        ('http://g.cn', (http, host, 80, path)),
        ('http://g.cn/', (http, host, 80, path)),
        ('http://g.cn:90', (http, host, 90, path)),
        ('http://g.cn:90/', (http, host, 90, path)),
        ('https://g.cn', (https, host, 443, path)),
        ('https://g.cn:233', (https, host, 233, path)),
    ]
    for t in test_items:
        url, expected = t
        u = parsed_url(url)
        # assert 是一个语句, 名字叫 断言
        # 如果断言成功, 条件成立, 则通过测试, 否则为测试失败, 中断程序报错
        e = "parsed_url ERROR, ({}) ({}) ({})".format(url, u, expected)
        assert u == expected, e


def test_get():
    """
        测试是否能正确处理 HTTP 和 HTTPS
    """
    urls = [
        'http://movie.douban.com/top250',
        'https://movie.douban.com/top250',
    ]
    for u in urls:
        res = get(u)
        print(res)


# 使用:
def main():
    url = 'http://movie.douban.com/top250'
    # r = get(url)
    # print(r)
    status_code, headers, body = get(url)
    print("status_code: ", status_code)
    print("headers: ", headers)
    print("body: ", body)


if __name__ == '__main__':
    # test_parsed_url()
    # test_get()
    main()