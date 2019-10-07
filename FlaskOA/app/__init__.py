import pymysql
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect  # 导入csrf保护

pymysql.install_as_MySQLdb()

csrf = CSRFProtect()
api = Api()
models = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object("settings.Config")

    models.init_app(app)  # ==> models = SQLAlchemy(app) #加载数据库
    # 加载csrf插件
    # csrf.init_app(app)
    # 加载restful插件
    api.init_app(app)

    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    return app



