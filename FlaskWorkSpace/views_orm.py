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

class Curriculum(models.Model):
    __tablename__ = "curriculum"
    id = models.Column(models.Integer,primary_key=True)
    c_id = models.Column(models.String(32))
    c_name = models.Column(models.String(32))
    c_time = models.Column(models.Date)

# models.create_all()
import datetime
# 增
# c = Curriculum(c_id="1001",c_name="python",c_time=datetime.datetime.now())
# c1 = Curriculum(c_id="1002",c_name="html",c_time=datetime.datetime.now())
# c2 = Curriculum(c_id="1003",c_name="mysql",c_time=datetime.datetime.now())
# c3 = Curriculum(c_id="1004",c_name="linux",c_time=datetime.datetime.now())
# session = models.session()
# session.add(c) 单条数据
# 多条数据
# session.add_all([c,c1,c2,c3,])
#
# session.commit()


# 查询所有
# all_c = Curriculum.query.all()
# for i in all_c:
#     print(i.c_name)

# 条件查询
# all_c = Curriculum.query.filter_by(id=2)
# all_c = Curriculum.query.filter_by(id=2)
# 复杂条件查询
# all_c = Curriculum.query.filter(Curriculum.id>2,Curriculum.c_id=="1003")
#
# for i in all_c:
#     print(i.c_name)

# 查询1条，id查询
# c = Curriculum.query.get(1)
# print(c.id,c.c_name)

# 获取第一条数据
# c = Curriculum.query.filter_by().first()
# print(c.id,c.c_name)

# 倒序
# all_c = Curriculum.query.filter().order_by(models.desc("id"))
# for i in all_c:
#     print(i.c_name)

# 分页
# all_c = Curriculum.query.offset(0).limit(2)
# for i in all_c:
#     print(i.c_name)

# filter,filter_by,limit 返回  <class 'flask_sqlalchemy.BaseQuery'>
# all 返回列表

# 删除
# c = Curriculum.query.get(1)
# session = models.session()
# session.delete(c)
# session.commit()

# 修改
c = Curriculum.query.get(2)
c.c_name = "PYTHON"
session = models.session()
session.add(c)
session.commit()