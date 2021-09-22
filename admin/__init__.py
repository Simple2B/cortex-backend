import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_mail import Mail


from app.logger import log

# instantiate extensions
login_manager = LoginManager()
db = SQLAlchemy()
mail = Mail()
migrate = Migrate()
admin = None


def create_app(environment="development"):
    global admin
    from admin.config import config

    from admin.views import (
        auth_blueprint,
        message_blueprint,
    )

    # from app.views import ()
    from app.models import Doctor, AnonymousUser, Client
    from admin.views import CortexAdminIndexView, DoctorAdminModelView

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
    mail.init_app(app)

    # Register blueprints.
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(message_blueprint)

    # Set up flask login.
    @login_manager.user_loader
    def get_user(id):
        return Doctor.query.get(int(id))

    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"
    login_manager.anonymous_user = AnonymousUser

    admin = Admin(
        app,
        index_view=CortexAdminIndexView(),
        name="Cortex",
        template_mode="bootstrap3",
    )

    admin.add_view(DoctorAdminModelView(Doctor, db.session))
    admin.add_view(ModelView(Client, db.session))

    return app
