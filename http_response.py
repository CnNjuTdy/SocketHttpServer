# -*- coding: utf-8 -*-
# Time       : 2018/12/18 5:49 PM
# Author     : tangdaye
# Description: 返回响应部分

# 本server处理的状态码
from http_status import HTTPStatus
import html

status_code = [200, 301, 400, 403, 404, 405, 500]
status = {
	v: (v.phrase, v.description)
	for v in HTTPStatus.__members__.values() if v in status_code
}

# 默认错误信息页模板
DEFAULT_ERROR_MESSAGE = """\
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
        "http://www.w3.org/TR/html4/strict.dtd">
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
        <title>Error response</title>
    </head>
    <body>
        <h1>Error response</h1>
        <p>Error code: %(code)d</p>
        <p>Message: %(message)s.</p>
        <p>Error code explanation: %(code)s - %(explain)s.</p>
    </body>
</html>
"""

DEFAULT_ERROR_CONTENT_TYPE = 'text/html;charset=utf-8'


def end_response_header(response):
	"""
	结束响应头部
	:param response: 响应
	:return: 响应
	"""
	return response + '\r\n'


def add_response_header(header_name, header_value, response):
	"""
	为请求增加头部域
	:param response: 响应
	:param header_name: 头部域名称
	:param header_value:  头部域值
	:return: 响应
	"""
	response += '%s: %s\r\n' % (header_name, header_value)
	return response


def generate_response_code(code, msg=None, http_version='HTTP/1.1'):
	"""
	响应状态码
	:param http_version: HTTP协议版本，默认1.1
	:param code:    状态码
	:param msg: 状态描述
	:return:    状态行信息
	"""
	if msg is None:
		msg, descr = status[code]
	status_line = '%s %d %s\r\n' % (http_version, code, msg)
	return status_line


def respond_not_found(connection, headers=None, http_version='HTTP/1.1'):
	'''
	404 响应
	:param connection:连接
	:param headers:已有头部
	:param http_version:http协议版本
	:return:
	'''
	response = generate_response_code(404, http_version=http_version)
	send_error(connection, response, 404, http_version=http_version)
	return


def respond_redirect():
	# todo 重定向301
	pass


def respond_server_error():
	# todo 服务器内部错误500
	pass


def send_response_full(connection, body, content_type='text/plain; charset=UTF-8', code=200, http_version='HTTP/1.1',
                       headers=None):
	'''

	:param connection:
	:param http_version:
	:param body:
	:param content_type:
	:param code:
	:param headers:
	:return:
	'''
	response = generate_response_code(code, http_version=http_version)
	response = add_response_header('Content-Type', content_type, response)
	response = add_response_header('Content-Length', len(body), response)

	if headers is not None:
		for header, value in headers.items():
			response = add_response_header(header, value, response)
	response = end_response_header(response)

	response = bytes(response, encoding='UTF-8') + body

	connection.sendall(response)
	return


def send_error(connection, response, code, msg=None, description=None, http_version='HTTP/1.1'):
	"""
	返回错误页
	:param connection:连接
	:param response:已有响应部分
	:param http_version: http协议版本
	:param code: 状态码
	:param msg: 状态信息
	:param description: 状态描述
	:return:
	"""
	# 获取与状态码相关的信息
	try:
		shortmsg, longmsg = status[code]
	except KeyError:
		shortmsg, longmsg = '???', '???'
	if msg is None:
		msg = shortmsg
	if description is None:
		description = longmsg

	# 增加头部'Connection'为'close'
	response = add_response_header('Connection', 'close', response)

	# 处理body，返回相应的错误页信息
	body = None
	if (code >= 200 and code not in
			(HTTPStatus.NO_CONTENT, HTTPStatus.RESET_CONTENT, HTTPStatus.NOT_MODIFIED)):
		content = (DEFAULT_ERROR_MESSAGE % {
			'code': code,
			'message': html.escape(msg, quote=False),
			'explain': html.escape(description, quote=False)
		})
		body = content.encode('UTF-8', 'replace')
		response = add_response_header('Content-Type', DEFAULT_ERROR_CONTENT_TYPE, response)
		response = add_response_header('Content-Length', int(len(body)), response)
	response = end_response_header(response)

	response = bytes(response, encoding='UTF-8')
	if body:
		response += body

	# print(response)
	connection.sendall(response)
	return


'''
响应报文:
    响应行：
    HTTP/1.1 200 OK
        格式：HTTP版本 状态码 说明
            2xx:代表成功
            3xx：代表重定向(某个服务器有问题会重定向到另外一台服务器上)
            4xx:代表浏览器故障
            5xx：代表服务器故障
    响应头：     
    Connection: Keep-Alive
        代表连接方式，keep-Alive:长连接
    Content-Encoding: gzip
        代表支持的压缩算法
    Content-Type: text/html; charset=utf-8
        代表返回浏览器请求的数据
    Date: Fri, 06 Apr 2018 11:42:46 GMT
        代表时间


    响应报文组成：
        响应行\r\n+响应头\r\n+空行(\r\n)+响应体(服务器发送给浏览器的数据)
'''


def send_response(headers=None, body=None, http_version='HTTP/1.1'):
	status_msg = status[200]
	response = generate_response_code(200, 'OK', http_version)

	# Todo
	if headers is not None:
		if 'Content-Type' not in headers:
			print('Content-Type')
			pass
		if 'Content-Length' not in headers:
			print('Content-Length')
			pass


if __name__ == '__main__':
	response = generate_response_code(200, 'OK')
	response = add_response_header('Content-Length', '438', response)
	response = end_response_header(response)
	respond_not_found('')
