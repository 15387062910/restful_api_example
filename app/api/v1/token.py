# encoding: utf-8
# __author__ = "wyb"
# date: 2018/10/25
# token相关接口
from app.utils.redprint import Redprint
from app.validators.forms import ClientForm, UserEmailForm
from app.models.user import User
from app.utils.enums import ClientTypeEnum
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, jsonify

token = Redprint("token")


def generate_auth_token(uid, ac_type, scope=None, expiration=7200):
    """
    生成token
    :param uid: 用户id
    :param ac_type: 登陆设备
    :param scope:
    :param expiration: 过期时间
    :return:
    """
    s = Serializer(current_app.config["SECRET_KEY"], expires_in=expiration)
    res = s.dumps({
        'uid': uid,
        'type': ac_type.value,
        'scope': scope
    })
    return res


@token.route('', methods=["POST"])
def get_token():
    form = ClientForm().validate_for_api()
    promise = {
        ClientTypeEnum.USER_EMAIL: User.verify,
    }
    identity = promise[ClientTypeEnum(form.type.data)](
        form.account.data,
        form.secret.data
    )

    # 生成token
    expiration = current_app.config["TOKEN_EXPIRATION"]
    user_token = generate_auth_token(identity["uid"], form.type.data, None, expiration)
    t = {
        'token': user_token.decode('ascii')
    }
    # 返回token
    return jsonify(t), 201


