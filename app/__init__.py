from flask import Flask

from .commands import create_tables
from .extensions import db,bcrypt
from flask_login import LoginManager
from flask_bootstrap import Bootstrap


def create_app(config_file='settings.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)

    Bootstrap(app)
    db.init_app(app)

    bcrypt.init_app(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.user.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from app.main.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.taskscheduler.task import task
    app.register_blueprint(task)

    app.cli.add_command(create_tables)

    return app