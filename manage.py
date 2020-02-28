from exts import db
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from models import User, Post
from app import app

manager = Manager(app)

migrate = Migrate(app,db)

manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    manager.run()

