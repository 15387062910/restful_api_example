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

api = Redprint("token")


def generate_auth_token(uid, ac_type, is_admin=None, expiration=7200):
    """
    生成token
    :param uid: user id
    :param ac_type: type of login equipment
    :param is_admin: scope
    :param expiration: expiry time
    :return:
    """
    s = Serializer(current_app.config["SECRET_KEY"], expires_in=expiration)
    res = s.dumps({
        'uid': uid,
        'type': ac_type.value,
        'is_admin': is_admin
    })
    return res


@api.route('', methods=["POST"])
def get_token():
    """
    a interface to get a token
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
    user_token = generate_auth_token(identity["uid"], form.type.data, identity['is_admin'], expiration)
    t = {
        'token': user_token.decode('ascii')
    }

    return jsonify(t), 201


