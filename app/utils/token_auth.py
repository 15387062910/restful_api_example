from collections import namedtuple
from flask import current_app, g, request
from flask_httpauth import HTTPBasicAuth      # 把账号和密码放到HTTP头里发送
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from app.utils.error import AuthFailed, Forbidden
from app.utils.scope import is_in_scope
# 验证token


auth = HTTPBasicAuth()
user_tuple = namedtuple('user_tuple', ['uid', 'ac_type', 'is_admin'])


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
    验证token的合法性
    :param token:
    :return: 返回一个namedtuple(名为user_tuple，包含三项: 'uid', 'ac_type', 'is_admin')
    """
    s = Serializer(current_app.config['SECRET_KEY'])
    # 尝试解析token 出错说明不是真正的token
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
    is_admin = data['is_admin']
    # request 视图函数
    # allow = is_in_scope(scope, request.endpoint)
    # if not allow:
    #     raise Forbidden()
    return user_tuple(uid, ac_type, is_admin)
