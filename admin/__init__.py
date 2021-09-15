import os

from werkzeug.exceptions import HTTPException

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from app.models import Doctor

from app.logger import log

# instantiate extensions
login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()


def create_app(environment="development"):

    from admin.config import config

    # from app.views import ()
    # from app.models import ()

    # Instantiate app.
    app = Flask(__name__)

    # Set app config.
    env = os.environ.get("FLASK_ENV", environment)
    log(log.INFO, "configuration: [%s]", env)
    app.config.from_object(config[env])
    config[env].configure(app)

    # Set up extensions.
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Register blueprints.
    # app.register_blueprint()

    # Set up flask login.
    @login_manager.user_loader
    def get_user(id):
        return Doctor.query.get(int(id))

    # login_manager.login_view = "main.index"
    login_manager.login_message_category = "info"
    # login_manager.anonymous_user = AnonymousUser

    # Error handlers.
    # @app.errorhandler(HTTPException)
    # def handle_http_error(exc):
    #     if exc.code == 404:
    #         return render_template("page-404.html")
    #     if exc.code == 500:
    #         return render_template("page-500.html")

    #     return render_template("error.html", error=exc), exc.code

    return app
