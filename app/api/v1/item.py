# encoding: utf-8
# __author__ = "wyb"
# date: 2018/10/20
from app.utils.redprint import Redprint
"""
app/api/v1/item.py
=============
item的API:
        /api/v1/item/ GET                       获取所有物品信息
        /api/v1/item/<int:item_id> GET          获取某件物品信息
        /api/v1/item/<int:item_id> DELETE       删除某件物品信息
        /api/v1/item/<int:item_id> PUT          修改物品信息
        /api/v1/item/<int:user_id> POST         添加物品信息
"""
api = Redprint("item")


@api.route('/', methods=['GET'])
def get_items():
    return 'item'


@api.route('/<int:item_id>', methods=['GET'])
def get_item(item_id):

    return 'item'


@api.route('/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):

    return 'item'


@api.route('/<int:item_id>', methods=['PUT'])
def edit_item(item_id):

    return 'item'


@api.route('/<int:user_id>', methods=['POST'])
def delete_item(user_id):

    return 'item'

