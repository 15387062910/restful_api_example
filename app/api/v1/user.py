# encoding: utf-8
# __author__ = "wyb"
# date: 2018/10/20
from . import Redprint
from app.models.user import User
from app.utils.error import NotFound
from app.utils.token_auth import auth
from flask import jsonify
from app.models import db

user = Redprint("user")


@user.route('/<int:uid>', methods=['GET'])                  # 根据id号获取用户信息
@auth.login_required
def get_user(uid):
    # 用token进行验证 -> 在def上面加装饰器 -> @auth.login_required
    now_user = User.query.get_or_404(uid)
    # dict()将对象转换成字典(要求对象中有keys方法和__getitem__方法) jsonify再将字典序列化
    return jsonify(dict(now_user))


@user.route('/<int:uid>', methods=['DELETE'])                         # 删除用户
def delete_user(uid):
    # 用token进行验证

    return 'delete wyb'


@user.route('', methods=['PUT'])                            # 更新用户信息
def update_user():
    # 用token进行验证

    return 'update wyb'


@user.route('', methods=['POST'])                           # 创建用户
def create_user():
    # 用token进行验证

    return 'create user wyb'

