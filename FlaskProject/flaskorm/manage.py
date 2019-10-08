import sys

from flask_migrate import MigrateCommand
from flask_script import Manager

from views import app
from models import models
manage = Manager(app)

# @manage.command
# def migrate():
#     models.create_all()

manage.add_command("db",MigrateCommand)

if __name__ == '__main__':
    manage.run()




