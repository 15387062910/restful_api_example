# encoding: utf-8
# __author__ = "wyb"
# date: 2018/10/25
"""
app/utils/token_auth.py
============================
验证token
    verify_password函数: 实现@auth.login_required对应的token验证
    verify_auth_token函数: 验证token的合法性以及判断用户是否能访问该接口

"""
from collections import namedtuple
from flask import current_app, g, request
from flask_httpauth import HTTPBasicAuth      # 把账号和密码放到HTTP头里发送
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from app.utils.error import AuthFailed, Forbidden
from app.utils.scope import is_in_scope


auth = HTTPBasicAuth()
user_tuple = namedtuple('user_tuple', ['uid', 'ac_type', 'scope'])


@auth.verify_password
def verify_password(token, password):
    """
    @auth.login_required对应的token验证
    :param token:
    :param password:
    :return:
    """
    user_info = verify_auth_token(token)
    if not user_info:
        return False
    else:
        # request
        g.user = user_info          # save user
        return True


def verify_auth_token(token):
    """
    验证token的合法性以及判断用户是否能访问该接口
    :param token:
    :return: 返回一个namedtuple(名为user_tuple，包含三项: 'uid', 'ac_type', 'is_admin')
    """
    s = Serializer(current_app.config['SECRET_KEY'])
    # 尝试解析token 出错说明token过期 or 不是真正的token
    try:
        data = s.loads(token)
    except BadSignature:                                # 非法token
        raise AuthFailed(msg='token is invalid',
                         error_code=1002)
    except SignatureExpired:                            # 过期token
        raise AuthFailed(msg='token is expired',
                         error_code=1003)
    uid = data['uid']
    ac_type = data['type']
    scope = data['scope']
    # request 视图函数
    allow = is_in_scope(scope, request.endpoint)
    if not allow:
        raise Forbidden()
    return user_tuple(uid, ac_type, scope)
