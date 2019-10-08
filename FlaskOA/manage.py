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
