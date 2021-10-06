#!/user/bin/env python
import click

# from flask_mail import Mail
from admin import create_app
from admin import db
from app import models

from app.logger import log
from admin.config import BaseConfig as conf

from admin.database import generate_test_data

# from test import generate_test_data

log.set_level(conf.LOG_LEVEL)

app = create_app()


# flask cli context setup
@app.shell_context_processor
def get_context():
    """Objects exposed here will be automatically available from the shell."""
    return dict(app=app, db=db, m=models)


@app.cli.command()
def create_db():
    """Create the configured database."""
    db.create_all()
    generate_test_data()


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
