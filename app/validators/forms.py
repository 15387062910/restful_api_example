# encoding: utf-8
# __author__ = "wyb"
# date: 2018/10/22
# 验证表单
from wtforms import StringField, IntegerField, ValidationError
from wtforms.validators import DataRequired, length, Email, Regexp
from app.utils.enums import ClientTypeEnum
from app.models.user import User
from app.validators.base import BaseForm as Form


class ClientForm(Form):
    account = StringField(validators=[DataRequired(message="不允许为空"), length(min=5, max=32)])        # email
    secret = StringField(validators=[DataRequired(message="不允许为空")])                                # 密码
    type = IntegerField(validators=[DataRequired()])                                                    # 注册登陆类型

    def validate_type(self, value):
        try:
            client = ClientTypeEnum(value.data)          # 检测注册登陆类型是否符合枚举中的类型
        except ValueError as e:
            raise e
        self.type.data = client


class UserEmailForm(ClientForm):
    account = StringField(validators=[Email(message='invalidate email')])
    secret = StringField(
        validators=[
            DataRequired(message="不允许为空"),
            # 能匹配的组合为：数字+字母，数字+特殊字符，字母+特殊字符，数字+字母+特殊字符组合，而且不能是纯数字，纯字母，纯特殊字符
            Regexp(r'^(?![\d]+$)(?![a-zA-Z]+$)(?![^\da-zA-Z]+$).{6,20}$')
        ]
    )
    nickname = StringField(validators=[DataRequired(), length(min=2, max=22)])

    def validate_account(self, value):
        if User.query.filter_by(email=value.data).first():
            raise ValidationError(message="账号已存在")
