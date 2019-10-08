### Flask 蓝图项目结构

![1570536060525](flask_assert/1570536060525.png)

```shell
FlaskOA # 项目根目录
|----app # 所有 app目录
|    |--------main  # 第一个蓝图应用
|    |        ├── forms.py # 表单校验类
|    |        ├── __init__.py # 创建蓝图，导入views
|    |        └── views.py # 视图处理文件
|    |--------static  #静态目录
|    |--------templates #模板目录
|    |--------__init__.py  # 初始化文件 ，定义创建app的类，app加载插件，注册蓝图
|    |--------models.py  # 数据库模型文件
|    |--------myutils.py #工具类
|----manage.py # 项目启动控制文件
|----settings.py # 项目配置文件
|----package.txt # 项目依赖包列表
|----uwsgi.ini # uwsgi的配置文件
|----nginx.conf # nginx的配置文件
```

settings.py

```python

import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


STATIC_FILES_DIR = os.path.join(BASE_DIR,"static")

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "ORM.sqlite")
    # SQLALCHEMY_DATABASE_URI = "mysql://root:1234@localhost/demo"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True
    SECRET_KEY = '123456'

class RunConfig(Config):
    DEBUG = False
```

manage.py

```
from app import create_app,models
from flask_script import Manager
from flask_migrate import MigrateCommand,Migrate

app = create_app()
manage = Manager(app)
migrate = Migrate(app,models)


manage.add_command("db",MigrateCommand)

@manage.command
def runserver_gevent():
    """
    当前代码用于io频繁的flask项目，可以提高flask项目的效率
    """
    from gevent import pywsgi
    server = pywsgi.WSGIServer(("127.0.0.1",5000),app)
    server.serve_forever() # 启动服务

if __name__ == '__main__':
    manage.run()
```

app/__init__.py

```python
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

```

app/models.py

```python
from app import models


class BaseModel(models.Model):

    __abstract__ = True
    id = models.Column(models.Integer, primary_key=True,autoincrement=True)

    def save(self):
        db = models.session()
        db.add(self)
        db.commit()

    def delete(self):
        db = models.session()
        db.delete(self)
        db.commit()

    def update(self):
        db = models.session()
        db.add(self)
        db.commit()


class Curriculum(BaseModel):
    __tablename__ = "curriculum"

    c_id = models.Column(models.String(32))
    c_name = models.Column(models.String(32))
    c_time = models.Column(models.Date)
```

app/main/__init__.py

```
from flask import Blueprint
main = Blueprint("main",__name__)
from . import views
```

app/main/forms.py

```python
import wtforms
from wtforms.validators import ValidationError
from flask_wtf import FlaskForm
from wtforms import validators
from app.models import User


# 自定义检验函数
def keywords_valid(form, field):
    """

    :param form:  表单
    :param field:  字段
    这两个不用主动传参
    """
    data = field.data  # 获取input内容，value
    keywords = ["admin", "root", "管理员", "版主"]
    if data in keywords:
        raise ValidationError("不可以使用敏感词命名")


class TaskForm(FlaskForm):
    name = wtforms.StringField(

        render_kw={
            "class": "form-control",
            "placeholder": "任务名称"
        },
        validators=[
            validators.DataRequired("姓名不可以为空"),

            keywords_valid
        ]
    )

    description = wtforms.TextField(
        render_kw={
            "class": "form-control",
            "placeholder": "任务描述"
        },
        validators=[
            validators.DataRequired("描述不可以为空"),
            validators.Length(min=5,message='长度必须大于5')]
    )
    time = wtforms.DateField(
        render_kw={
            "class": "form-control",
            "placeholder": "任务时间"
        }
    )
    public = wtforms.StringField(
        render_kw={
            "class": "form-control",
            "placeholder": "公布任务人"
        }, validators=[
            validators.DataRequired("不可以为空"),
        ]
    )

```

app/main/views.py

```python
import os
import functools

from flask import render_template
from flask_restful import Resource
from flask import jsonify, session
from app.models import Curriculum, User, Leave, models

from . import main
from app import api
from .forms import TaskForm
from .forms import LoginForm
from app.myutils import Calender, get_password, Pagintor


def loginCheck(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        username = request.cookies.get("username")
        id = request.cookies.get("id", 0)
        session_name = session.get("username")
        if id:
            user = User.query.get(int(id))
            if user:
                if user.user_name == username and session_name == username:
                    return func(*args, **kwargs)
        return redirect("/login/")

    return inner


@main.route("/index/")
@loginCheck
def index():
    # c = Curriculum.query.get(1)
    # c.c_name = "flask"
    # c.update()
    curriculum_list = Curriculum.query.all()

    return render_template("index.html", curriculum_list=curriculum_list)
```

