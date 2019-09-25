from views import app
from flask_script import Manager
from models import models
import sys
manage = Manager(app)

@manage.command
def migrate():
    models.create_all()

if __name__ == '__main__':
    manage.run()




