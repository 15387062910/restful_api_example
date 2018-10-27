# encoding: utf-8
# __author__ = "wyb"
# date: 2018/10/20
from . import Redprint

item = Redprint("item")


@item.route('')
def get_item():
    return 'item'






