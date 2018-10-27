# encoding: utf-8
# __author__ = "wyb"
# date: 2018/10/20
# user CRUD
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
    用token进行验证 -> 在def上面加装饰器 -> @auth.login_required
    dict()将对象转换成字典(要求对象中有keys方法和__getitem__方法)
    :param uid: user id
    :return: 返回一个jsonify对象 jsonify将字典序列化，与dumps不同之处是设置了返回的content-type为application/json
    """
    is_admin = g.user.is_admin
    if not is_admin:
        raise AuthFailed
    user = User.query.filter_by(id=uid).first_or_404()
    return jsonify(user)


@api.route('/<int:uid>', methods=['DELETE'])
def super_delete_user(uid):
    """
    管理员删除权限
    :param uid:
    :return:
    """
    pass


@api.route('', methods=['DELETE'])
@auth.login_required
def delete_user():
    """
    删除用户的接口
    根据当前登陆的用户id来删除用户 只有自己才能删除自己
    flask中的g变量是线程隔离的
    :return:
    """
    uid = g.user.uid
    with db.auto_commit():
        user = User.query.filter_by(id=uid).first_or_404()
        user.delete()
    return DeleteSuccess()


@api.route('', methods=['PUT'])                            # 更新用户信息
def update_user():
    # 用token进行验证

    return 'update wyb'


@api.route('', methods=['POST'])                           # 创建用户
def create_user():
    # 用token进行验证

    return 'create user wyb'

