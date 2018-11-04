# encoding: utf-8
# __author__ = "wyb"
# date: 2018/10/22
from sqlalchemy import Column, Integer, String, SmallInteger, orm
from werkzeug.security import generate_password_hash, check_password_hash                # 加密密码以及检测hash过的密码
from . import Base, db
from app.utils.error import AuthFailed


class User(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(33), unique=True, nullable=False)
    nickname = Column(String(33), unique=True)
    auth = Column(SmallInteger, default=1)
    _password = Column('password', String(100))

    @orm.reconstructor                              # ORM通过元类来创建模型对象 所以要在构造函数前添加这个装饰器
    def __init__(self):
        super(User, self).__init__()
        # self.fields定义默认输出字段
        self.fields = ["id", "email", "nickname", "auth"]

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    @staticmethod
    def register_by_email(name, account, secret):
        with db.auto_commit():
            user = User()
            user.email = account
            user.nickname = name
            user.password = secret
            db.session.add(user)

    @staticmethod
    def verify(email, password):
        user = User.query.filter_by(email=email).first_or_404()
        if not user.check_password(password):
            raise AuthFailed()
        scope = 'AdminScope' if user.auth == 666 else 'UserScope'
        return {'uid': user.id, 'scope': scope}

    def check_password(self, raw):
        if not self._password:
            return False
        return check_password_hash(self._password, raw)