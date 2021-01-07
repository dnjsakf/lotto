from app import create_app
from flask_script import Manager

# Create Flask Application
app = create_app()

# Create Flask Manager
manager = Manager(app)

@manager.command
@manager.option('-n', '--name', help='Your name')
def run(name=None):
  dev_server_config = app.config.get_namespace("DEV_SERVER_")
  app.run(**dev_server_config)

if __name__ == '__main__':
  manager.run()