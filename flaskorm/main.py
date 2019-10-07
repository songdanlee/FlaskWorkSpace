import pymysql
from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_wtf import CSRFProtect # 导入csrf保护
from flask_sqlalchemy import SQLAlchemy
pymysql.install_as_MySQLdb()

app = Flask(__name__)

#配置1 直接配置
# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"+os.path.join(BASE_DIR,"ORM.sqlite")
# # app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:1234@localhost/demo"
# app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
#


# 配置2 ，配置文件
# app.config.from_pyfile("settings.py")


# 配置3 ，配置类
app.config.from_object("settings.Config")

models = SQLAlchemy(app)
#csrf = CSRFProtect(app) #使用csrf保护
api = Api(app)

# 安装数据库管理插件
migrate = Migrate(app,models)