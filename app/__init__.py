# encoding: utf-8
# __author__ = "wyb"
# date: 2018/10/20
from .app import Flask
from app.api.v1 import create_blueprint_api_v1
from app.admin import admin as admin_blueprint
from app.models import db


# 注册app下的蓝图
def register_blueprint(app):
    app.register_blueprint(create_blueprint_api_v1(), url_prefix="/api/v1")
    app.register_blueprint(admin_blueprint, url_prefix="/admin")


# 注册db
def register_plugin(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()


# 创建app对象
def create_app():
    app = Flask(__name__)
    app.config.from_object('app.settings')
    register_blueprint(app)
    register_plugin(app)
    return app

