# encoding: utf-8
# __author__ = "wyb"
# date: 2018/10/24
from wtforms import Form
from app.utils.error import ParameterException
from flask import request


class BaseForm(Form):
    def __init__(self):
        data = request.json
        super(BaseForm, self).__init__(data=data)

    def validate_for_api(self):
        validate = super(BaseForm, self).validate()
        if not validate:
            raise ParameterException(msg=self.errors)
        return self     # 返回Form

