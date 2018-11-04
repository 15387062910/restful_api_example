# encoding: utf-8
# __author__ = "wyb"
# date: 2018/11/3


class Base(object):
    def __init__(self):
        self.fields = []

    def __getitem__(self, item):
        return getattr(self, item)

    def keys(self):
        return self.fields

    def hide(self, *keys):                  # 隐藏域
        for key in keys:
            self.fields.remove(key)
        return self

    def append(self, *keys):                # 添加域
        for key in keys:
            self.fields.append(key)
        return self


class Sx(Base):
    name = "wyb"
    age = 21

    def __init__(self):
        super(Base, self).__init__()
        self.gender = 'male'
        # self.fields定义默认输出字段
        self.fields = ["name", "age"]


o1 = Sx()
print(dict(o1))
o2 = Sx()
print(dict(o2.hide("age")))
o3 = Sx()
print(dict(o3.append("gender")))

# 输出结果:
# {'name': 'wyb', 'age': 21}
# {'name': 'wyb'}
# {'name': 'wyb', 'age': 21, 'gender': 'male'}


