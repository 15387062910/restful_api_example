# encoding: utf-8
# __author__ = "wyb"
# date: 2018/10/20
from app.utils.redprint import Redprint
from app.utils.enums import ClientTypeEnum
from app.validators.forms import ClientForm, UserEmailForm
from app.utils.error import Success
from app.models.user import User

client = Redprint("client")


@client.route('/register', methods=["POST"])
def create_client():
    # 表单 json 提交数据:  表单 -> 网页  json -> 小程序 移动端
    form = ClientForm().validate_for_api()
    promise = {
        ClientTypeEnum.USER_EMAIL: _register_user_by_email,
    }
    promise[form.type.data]()
    # 异常:
    # 我们可以预知的异常 已知异常 -> APIException
    # 我们完全没有意识到的异常 未知异常 -> AOP 在出口抓住异常
    return Success()


def _register_user_by_email():
    form = UserEmailForm().validate_for_api()
    User.register_by_email(form.nickname.data, form.account.data, form.secret.data)
