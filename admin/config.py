import os
from dotenv import load_dotenv
from app.logger import log

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, "../.env"))


class BaseConfig(object):
    """Base configuration."""

    APP_NAME = "Cortex_Admin"
    DEBUG_TB_ENABLED = False
    SECRET_KEY = os.environ.get(
        "SECRET_KEY", "Ensure you set a secret key, this is important!"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False

    ADMIN_FIRST_NAME = os.environ.get("ADMIN_FIRST_NAME", "Admin")
    ADMIN_LAST_NAME = os.environ.get("ADMIN_LAST_NAME", "Cortex")
    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@gmail.com")

    FLASK_ADMIN_SWATCH = "cerulean"

    LOG_LEVEL = int(os.environ.get("LOG_LEVEL", log.INFO))

    @staticmethod
    def configure(app):
        # Implement this method to do further configuration on your app.
        log.set_level(app.config["LOG_LEVEL"])


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DEVEL_DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "database-devel.sqlite3"),
    )


class TestingConfig(BaseConfig):
    """Testing configuration."""

    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "TEST_DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "database-test.sqlite3"),
    )


class ProductionConfig(BaseConfig):
    """Production configuration."""

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///" + os.path.join(BASE_DIR, "database.sqlite3")
    )
    WTF_CSRF_ENABLED = True


config = dict(
    development=DevelopmentConfig, testing=TestingConfig, production=ProductionConfig
)
