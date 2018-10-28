# encoding: utf-8
# __author__ = "wyb"
# date: 2018/10/28
"""
app/api/v1/book.py
=============
book的API:
        /api/v1/book/search GET                  搜索图书的接口
        /api/v1/book/<isbn>/details GET          查看某个isbn号对应的图书的详情的接口

"""
from sqlalchemy import or_
from app.utils.redprint import Redprint
from app.models.book import Book
from app.validators.forms import BookSearchForm
from flask import jsonify


api = Redprint('book')


@api.route('/search', methods=['GET'])
def search():
    """
    根据传入的查询参数搜索图书信息 -> 用like实现模糊查询, or_在filter中表示或关系
    :return:
    """
    form = BookSearchForm().validate_for_api()
    q = '%' + form.q.data + '%'
    # # book = Book()
    # # 元类 ORM
    books = Book.query.filter(or_(Book.title.like(q), Book.publisher.like(q))).all()
    books = [book.hide('summary', 'id') for book in books]            # 隐藏summary字段
    return jsonify(books)


@api.route('/<isbn>/details', methods=['GET'])
def detail(isbn):
    """
    根据传入的isbn号查询对应图书的详情
    :param isbn:
    :return:
    """
    book = Book.query.filter_by(isbn=isbn).first_or_404()
    return jsonify(book)
