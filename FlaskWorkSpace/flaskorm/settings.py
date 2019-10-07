import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# 第二种配置
# SQLALCHEMY_DATABASE_URI = "sqlite:///"+os.path.join(BASE_DIR,"ORM.sqlite")
# # SQLALCHEMY_DATABASE_URI = "mysql://root:1234@localhost/demo"
# SQLALCHEMY_COMMIT_ON_TEARDOWN = True
# SQLALCHEMY_TRACK_MODIFICATIONS = True
# DEBUG = True

STATIC_FILES_DIR = os.path.join(BASE_DIR,"static")
# 第三种配置
class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "ORM.sqlite")
    # SQLALCHEMY_DATABASE_URI = "mysql://root:1234@localhost/demo"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True
    SECRET_KEY = '123456'

class RunConfig(Config):
    DEBUG = False
