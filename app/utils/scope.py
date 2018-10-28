# scope -> 作用域
# 用来控制用户权限
"""
app/utils/scope.py
=====================================
自定义权限类及判断权限函数
    UserScope类 -> 普通用户
    AdminScope类 -> 管理员用户
    is_in_scope函数 -> 判断当前用户是否有权限访问当前接口
"""


class Scope:
    """
        allow_api属性: 记录能访问哪些视图函数API
        allow_module属性: 记录能访问哪些模块
        forbidden属性: 记录禁止访问的相关内容
        __add__方法: 实现向一个权限类型中添加另一个权限类型中的相关属性的魔法方法(运算符重载)
    """
    allow_api = []
    allow_module = []
    forbidden = []

    def __add__(self, other):
        """
        向一种权限类型中添加另一种权限类型的相关属性 eg: 向AdminScope中添加UserScope
        :param other: 添加的权限类型对象
        :return:
        """
        self.allow_api = self.allow_api + other.allow_api
        self.allow_api = list(set(self.allow_api))              # 去重

        self.allow_module = self.allow_module + other.allow_module
        self.allow_module = list(set(self.allow_module))

        self.forbidden = self.forbidden + other.forbidden
        self.forbidden = list(set(self.forbidden))

        return self         # 返回self才能实现链式操作


class AdminScope(Scope):
    """
        管理员可以访问user下所有的视图函数
    """
    # allow_api = ['api_v1.user+super_get_user']
    allow_module = ['api_v1.user']

    def __init__(self):
        pass


class UserScope(Scope):
    # allow_module = ['api_v1.xxx']
    forbidden = ['api_v1.user+super_get_user',
                 'api_v1.user+super_delete_user']

    def __init__(self):
        self + AdminScope()


def is_in_scope(scope, endpoint):
    """
    判断当前用户是否有权限访问当前接口 -> 用globals实现反射(根据类名的字符串实例化对象)
    :param scope: 当前用户权限(str), eg: AdminScope、UserScope
    :param endpoint: 当前想访问的视图函数(str), eg: api_v1.user+super_get_user
    :return:
    """
    # endpoint: api_v1.view_func -> api_v1.module_name+view_func -> api_v1.red_name+view_func
    # 下面的scope是权限对象  red_name是蓝图名.模块名
    scope = globals()[scope]()
    splits = endpoint.split('+')
    red_name = splits[0]
    if endpoint in scope.forbidden:
        return False
    if endpoint in scope.allow_api:
        return True
    if red_name in scope.allow_module:
        return True
    else:
        return False
