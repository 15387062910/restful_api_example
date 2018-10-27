# encoding: utf-8
# __author__ = "wyb"
# date: 2018/10/20
from flask import Blueprint
from app.utils.redprint import Redprint
from .user import user
from .item import item
from .client import client
from .token import token


# 将api_v1下的红图注册到bp_v1蓝图上
def create_blueprint_api_v1():
    bp_v1 = Blueprint("api", __name__)
    user.register(bp_v1)
    item.register(bp_v1)
    client.register(bp_v1)
    token.register(bp_v1)

    return bp_v1

