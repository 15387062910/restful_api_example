# encoding: utf-8
# __author__ = "wyb"
# date: 2018/10/20
from . import admin


@admin.route('/login')
def login():
    return 'admin login'

