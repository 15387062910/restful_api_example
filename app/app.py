# encoding: utf-8
# __author__ = "wyb"
# date: 2018/10/26
from flask import Flask as _Flask
from flask.json import JSONEncoder as _JSONEncoder
from app.utils.error import ServerError
from datetime import date


class JSONEncoder(_JSONEncoder):                # 重写jsonify
    def default(self, o):
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        if isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        raise ServerError()


class Flask(_Flask):
    json_encoder = JSONEncoder


