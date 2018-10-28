# encoding: utf-8
# __author__ = "wyb"
# date: 2018/10/20
"""
app/utils/enums.py
======================
枚举

"""
from enum import Enum


class ClientTypeEnum(Enum):
    USER_EMAIL = 100
    USER_MOBILE = 101

    # 微信小程序
    USER_MINA = 200
    # 微信公众号
    USER_WX = 201

