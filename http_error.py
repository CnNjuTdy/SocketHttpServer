# -*- coding: utf-8 -*-
# Time       : 2018/12/18 5:52 PM
# Author     : tangdaye
# Description: 错误部分


class HttpError(Exception):
    def __init__(self, code='500', msg=None):
        Exception.__init__(self, msg)
        self.code = code
        self.msg = msg


class ParseRequestError(HttpError):
    def __init__(self, msg=None):
        HttpError.__init__(self, msg=msg, code='500')
