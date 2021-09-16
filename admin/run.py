#!/user/bin/env python
import click

from flask_admin import Admin
from admin import create_app, db
from app import models


# from app.models import User, PhotoContest
# from admin.views import (
#     UserAdminModelView,
#     CortexAdminIndexView,
# )
from app.logger import log
from admin.config import BaseConfig as conf

from admin.database import add_admin_to_db

log.set_level(conf.LOG_LEVEL)

app = create_app()
admin = Admin(app)

# admin.add_view(UserAdminModelView(User, db.session))


# flask cli context setup
@app.shell_context_processor
def get_context():
    """Objects exposed here will be automatically available from the shell."""
    return dict(app=app, db=db, m=models)


@app.cli.command()
def create_db():
    """Create the configured database."""
    db.create_all()
    add_admin_to_db()


@app.cli.command()
@click.confirmation_option(prompt="Drop all database tables?")
def drop_db():
    """Drop the current database."""
    db.drop_all()


@app.cli.command()
@click.confirmation_option(prompt="Drop all database tables?")
def reset_db():
    """Reset the current database."""
    db.drop_all()
    db.create_all()


if __name__ == "__main__":
    app.run()
