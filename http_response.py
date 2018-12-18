# -*- coding: utf-8 -*-
# Time       : 2018/12/18 5:49 PM
# Author     : tangdaye
# Description: 返回相应部分


def end_response_header(response):
    """
    结束响应头部
    :param response:    响应
    :return:    响应
    """
    response.append(b'\r\n')
    return response


def add_response_header(header_name, header_value, response):
    """
    为请求增加头部域
    :param response: 响应
    :param header_name: 头部域名称
    :param header_value:  头部域值
    :return: 响应
    """
    response.append("%s: %s\r\n" % (header_name, header_value))
    return response


def generate_response_code(code, message=None, http_version='HTTP/1.1'):
    """
    响应状态码
    :param http_version:    HTTP协议版本，默认1.1
    :param code:    状态码
    :param message: 状态描述
    :return:    状态行信息
    """
    status_line = ["%s %d %s\r\n" % (http_version, code, message)]
    return status_line
