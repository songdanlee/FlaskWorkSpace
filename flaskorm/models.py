from flaskorm import models


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
