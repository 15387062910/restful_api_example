# encoding: utf-8
# __author__ = "wyb"
# date: 2018/10/20
from app.utils.redprint import Redprint
"""
app/api/v1/item.py
=============
item的API:

"""
api = Redprint("item")


@api.route('')
def get_item():
    return 'item'






