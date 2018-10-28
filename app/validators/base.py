# encoding: utf-8
# __author__ = "wyb"
# date: 2018/10/24
from wtforms import Form
from app.utils.error import ParameterException
from flask import request


class BaseForm(Form):
    def __init__(self):
        """
        获取body数据和查询参数并保存
        """
        data = request.get_json(silent=True)
        args = request.args.to_dict()
        super(BaseForm, self).__init__(data=data, **args)

    def validate_for_api(self):
        validate = super(BaseForm, self).validate()
        if not validate:
            raise ParameterException(msg=self.errors)
        return self     # 返回Form

