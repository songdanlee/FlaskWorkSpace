from main import models


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


class User(BaseModel):

    __tablename__ = "user"
    user_name = models.Column(models.String(64))
    password = models.Column(models.String(32))
    email = models.Column(models.String(32))


class Leave(BaseModel):
    __tablename__ = "leave"
    request_id = models.Column(models.Integer)# 请假人id
    request_name = models.Column(models.String(32))# 请假人姓名
    request_type = models.Column(models.String(32))# 假期类型
    start_time = models.Column(models.String(32))# 起始时间
    end_time = models.Column(models.String(32))# 结束时间
    description = models.Column(models.Text)# 请假事由
    phone = models.Column(models.String(32))# 联系方式
    status = models.Column(models.Integer)# 假条状态 0 申请  1批准  2驳回 3销假

