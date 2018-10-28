# encoding: utf-8
# __author__ = "wyb"
# date: 2018/10/25
"""
app/api/v1/token.py
=============
token的API:
        /api/v1/token POST               生成token
        /api/v1/token/secret POST        获取token信息
"""
from app.utils.redprint import Redprint
from app.utils.error import AuthFailed
from app.utils.enums import ClientTypeEnum
from app.validators.forms import ClientForm, TokenForm
from app.models.user import User
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from flask import current_app, jsonify

api = Redprint("token")


def generate_auth_token(uid, ac_type, scope=None, expiration=7200):
    """
    generate a token
    :param uid: user id
    :param ac_type: type of login equipment
    :param scope: a power or a right
    :param expiration: expiry time
    :return:
    """
    s = Serializer(current_app.config["SECRET_KEY"], expires_in=expiration)
    res = s.dumps({
        'uid': uid,
        'type': ac_type.value,
        'scope': scope
    })
    return res


@api.route('', methods=["POST"])
def get_token():
    """
    验证ClientForm来生成token
    :return:
    """
    form = ClientForm().validate_for_api()
    promise = {
        ClientTypeEnum.USER_EMAIL: User.verify,
    }
    identity = promise[ClientTypeEnum(form.type.data)](
        form.account.data,
        form.secret.data
    )

    # generate a token
    expiration = current_app.config["TOKEN_EXPIRATION"]
    user_token = generate_auth_token(identity["uid"], form.type.data, identity['scope'], expiration)
    t = {
        'token': user_token.decode('ascii')
    }

    return jsonify(t), 201


@api.route('/secret', methods=['POST'])
def get_token_info():
    """
    获取token信息的接口
    :return:
    """
    form = TokenForm().validate_for_api()
    s = Serializer(current_app.config['SECRET_KEY'])
    # 尝试解析token 出错说明token过期 or 不是真正的token
    try:
        data = s.loads(form.token.data, return_header=True)
    except SignatureExpired:
        raise AuthFailed(msg='token is expired', error_code=1003)
    except BadSignature:
        raise AuthFailed(msg='token is invalid', error_code=1002)

    r = {
        'scope': data[0]['scope'],
        'uid': data[0]['uid'],
        'create_at': data[1]['iat'],
        'expire_in': data[1]['exp'],
    }
    return jsonify(r)
