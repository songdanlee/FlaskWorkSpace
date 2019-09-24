import sys
from flaskorm.models import models
from flaskorm.views import app


if __name__ == '__main__':
    if sys.argv[1] == "migrate":
        models.create_all()
    elif sys.argv[1] == "runserver":
        app.run("127.0.0.1",port=8000,debug=True)




