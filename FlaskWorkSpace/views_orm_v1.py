import os
from flask import  Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)

#配置参数
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"+os.path.join(BASE_DIR,"ORM.sqlite")
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:1234@localhost/demo"
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

models = SQLAlchemy(app)

class BaseModel(models.Model):
    def __init__(self):
        id = models.Column(models.Integer, primary_key=True,autoincrement=True)

    def save(self):
        db = models.session()
        db.add(self)
        db.commit()

    def delete(self):
        db = models.session()
        db.delete(self)
        db.commit()



class Curriculum(models.Model):
    __tablename__ = "curriculum"

    c_id = models.Column(models.String(32))
    c_name = models.Column(models.String(32))
    c_time = models.Column(models.Date)


# 删除
# c = Curriculum.query.get(1)
# session = models.session()
# session.delete(c)
# session.commit()

# 修改
# c = Curriculum.query.get(2)
# c.c_name = "PYTHON"
# session = models.session()
# session.add(c)
# session.commit()