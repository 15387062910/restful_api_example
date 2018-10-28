# encoding: utf-8
# __author__ = "wyb"
# date: 2018/10/28
"""
app/api/v1/gift.py
=============
gift的API:
        /api/v1/gift/<isbn> POST                  搜索图书的接口

"""
from flask import g
from app.utils.error import Success, DuplicateGift
from app.utils.redprint import Redprint
from app.utils.token_auth import auth
from app.models import db
from app.models.book import Book
from app.models.gift import Gift


api = Redprint('gift')


@api.route('/<isbn>', methods=['POST'])
@auth.login_required
def create(isbn):
    """
    创建礼物的接口 -> 礼物必须要在book表中存在 不存在就不能创建礼物! 另外一本书只能加入gift一次!
    :param isbn:
    :return:
    """
    uid = g.user.uid
    with db.auto_commit():
        Book.query.filter_by(isbn=isbn).first_or_404()
        gift = Gift.query.filter_by(isbn=isbn, uid=uid).first()
        if gift:                            # gift已存在不能再添加!
            raise DuplicateGift()
        gift = Gift()
        gift.isbn = isbn
        gift.uid = uid
        db.session.add(gift)
    return Success()




