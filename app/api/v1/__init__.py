# encoding: utf-8
# __author__ = "wyb"
# date: 2018/10/20
from flask import Blueprint
from .user import api as user
from .item import api as item
from .client import api as client
from .token import api as token
from .book import api as book
from .gift import api as gift


# 将api_v1下的红图注册到bp_v1蓝图上
def create_blueprint_api_v1():
    bp_v1 = Blueprint("api_v1", __name__)
    user.register(bp_v1)
    item.register(bp_v1)
    client.register(bp_v1)
    token.register(bp_v1)
    book.register(bp_v1)
    gift.register(bp_v1)

    return bp_v1

