# encoding: utf-8
# __author__ = "wyb"
# date: 2018/10/20
"""
app/api/v1/user.py
=============
user的CRUD
    API:
        /api/v1/user/ GET                   用户获取自己的信息
        /api/v1/user/<int:uid> GET          管理员获取任意用户的信息
        /api/v1/user/ DELETE                用户删除自己
        /api/v1/user/<int:uid> DELETE       管理员删除任意用户
        /api/v1/user/ PUT                   用户修改自己的信息

    jsonify将字典序列化，与dumps不同之处是设置了返回的content-type为application/json
    用token进行验证 -> 在def上面加装饰器 -> @auth.login_required
    dict()将对象转换成字典(要求对象中有keys方法和__getitem__方法)
"""
from app.utils.redprint import Redprint
from app.models.user import User
from app.utils.error import DeleteSuccess, AuthFailed
from app.utils.token_auth import auth
from flask import jsonify, g
from app.models import db

api = Redprint("user")


@api.route('/<int:uid>', methods=['GET'])
@auth.login_required
def super_get_user(uid):
    """
    根据id号获取用户信息(密码不能获取) -> 管理员才能调用
    :param uid: user id
    :return:
    """
    user = User.query.filter_by(id=uid).first_or_404()
    return jsonify(user)


@api.route('/', methods=['GET'])
@auth.login_required
def get_user():
    """
    根据id号获取当前登陆的用户信息(密码不能获取) -> 当前登陆用户调用自己的
    :return:
    """
    uid = g.user.uid                                        # flask中的g变量是线程隔离的
    user = User.query.filter_by(id=uid).first_or_404()
    return jsonify(user)


@api.route('/<int:uid>', methods=['DELETE'])
@auth.login_required
def super_delete_user(uid):
    """
    删除某个用户 -> 管理员删除权限
    :param uid:
    :return:
    """
    with db.auto_commit():
        user = User.query.filter_by(id=uid).first_or_404()
        user.delete()                                           # 假删除 仅仅是将status设置为0而已
    return DeleteSuccess()


@api.route('', methods=['DELETE'])
@auth.login_required
def delete_user():
    """
    删除用户的接口 -> 根据当前登陆的用户id来删除用户 只有自己才能删除自己
    :return:
    """
    uid = g.user.uid
    with db.auto_commit():
        user = User.query.filter_by(id=uid).first_or_404()
        user.delete()
    return DeleteSuccess()


@api.route('', methods=['PUT'])
@auth.login_required
def update_user():
    """
    更新用户信息 -> 只有用户自己才能修改自己的用户信息
    :return:
    """

    return 'update wyb'


# @api.route('', methods=['POST'])                           # 创建用户 -> client.py中创建
# def create_user():
#     # 用token进行验证
#
#     return 'create user wyb'

