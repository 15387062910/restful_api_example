# encoding: utf-8
# __author__ = "wyb"
# date: 2018/10/20
from app.utils.error import NotFound
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import inspect, Column, Integer, SmallInteger, orm
from contextlib import contextmanager


class SQLAlchemy(_SQLAlchemy):
    """
        重写SQLAlchemy
        主要新增:
            auto_commit: 增加自动commit和出错自动回滚机制
    """
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


class Query(BaseQuery):
    """
        重写flask_sqlalchemy封装的查询
        主要新增:
            filter_by方法:
                实现在未删除的元素中查找元素(在查找的参数中增加一个status)
                使用方法: xxx.query.filter_by(xxx=xxx).first_or_404()       # status为1且xxx=xxx的元素才能被找到
            get_or_404方法:
                实现根据id返回元素 存在就返回该元素 不存在就返回NotFound对象
            first_or_404方法:
                实现返回Query元素的第一个值，为None就返回NotFound对象
    """
    def filter_by(self, **kwargs):                          # 在未删除的元素中寻找
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1                            # 确保status为0的不被找出来
        return super(Query, self).filter_by(**kwargs)

    # 有就返回 没有就返回error中的NotFound
    def get_or_404(self, ident):
        rv = self.get(ident)
        if not rv:
            raise NotFound()
        return rv

    # 有就返回 没有就返回error中的NotFound
    def first_or_404(self):
        rv = self.first()
        if not rv:
            raise NotFound()
        return rv


# 实例化db
db = SQLAlchemy(query_class=Query)


# 数据模型基类
class Base(db.Model):
    """
        重写db.Model
        新增:
            create_time属性: 创建时间()
            status属性: 实现假删除(默认为1, 1表示可用，0表示删除)
            __init__方法: 初始化create_time，格式为时间戳(integer)
            __getitem__方法: 获取指定键对应的值
            create_datetime方法:
            set_attrs方法:
            delete方法:
            keys方法:
            hide方法:
            append方法:
    """
    __abstract__ = True
    create_time = Column(Integer)
    status = Column(SmallInteger, default=1)

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())

    def __getitem__(self, item):
        return getattr(self, item)

    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None

    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    def delete(self):
        self.status = 0

    def keys(self):
        return self.fields

    def hide(self, *keys):
        for key in keys:
            self.fields.remove(key)
        return self

    def append(self, *keys):
        for key in keys:
            self.fields.append(key)
        return self


class MixinJSONSerializer:
    """
        更好用的一个将对象转换成字典的方法
        也就是一个更方便的序列化器
    """
    @orm.reconstructor
    def init_on_load(self):
        self._fields = []
        # self._include = []
        self._exclude = []

        self._set_fields()
        self.__prune_fields()

    def _set_fields(self):
        pass

    def __prune_fields(self):
        columns = inspect(self.__class__).columns
        if not self._fields:
            all_columns = set(columns.keys())
            self._fields = list(all_columns - set(self._exclude))

    def hide(self, *args):
        for key in args:
            self._fields.remove(key)
        return self

    def keys(self):
        return self._fields

    def __getitem__(self, key):
        return getattr(self, key)
