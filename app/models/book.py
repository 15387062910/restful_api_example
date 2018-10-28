from sqlalchemy import Column, String, Integer, orm
from app.models import Base


class Book(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    author = Column(String(30), default='未名')
    binding = Column(String(20))
    publisher = Column(String(50))
    price = Column(String(20))
    pages = Column(Integer)
    pubdate = Column(String(20))
    isbn = Column(String(15), nullable=False, unique=True)
    summary = Column(String(1000))
    image = Column(String(50))

    @orm.reconstructor              # ORM通过元类来创建模型对象 所以要在构造函数前添加这个装饰器
    def __init__(self):
        super(Book, self).__init__()
        # self.fields定义默认输出字段
        self.fields = ['id', 'title', 'author', 'binding',  'publisher',
                       'price', 'pages', 'pubdate', 'isbn', 'summary', 'image']

