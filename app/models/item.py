# encoding: utf-8
# __author__ = "wyb"
# date: 2018/11/1
from sqlalchemy import Column, String, Integer, orm, SmallInteger, DateTime, ForeignKey
from app.models import Base


class Item(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    itemName = Column(String(50))
    type = Column(SmallInteger)
    time = Column(DateTime)
    srcs = Column(String(300))
    des = Column(String(200))
    price = Column(String(20))
    user_id = Column(Integer, ForeignKey('user.id'))

    image = Column(String(50))

    @orm.reconstructor              # ORM通过元类来创建模型对象 所以要在构造函数前添加这个装饰器
    def __init__(self):
        super(Item, self).__init__()
        # self.fields定义默认输出字段
        self.fields = ['id', 'itemName', 'type', 'des', 'price']