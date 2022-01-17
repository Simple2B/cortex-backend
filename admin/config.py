import os
from dotenv import load_dotenv

from app.logger import log

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(os.path.dirname(BASE_DIR), ".env"))


class BaseConfig(object):
    """Base configuration."""

    APP_NAME = "CORTEX"
    DEBUG_TB_ENABLED = False
    SECRET_KEY = os.environ.get(
        "SECRET_KEY", "Ensure you set a secret key, this is important!"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False

    ADMIN_FIRST_NAME = os.environ.get("ADMIN_FIRST_NAME", "Admin")
    ADMIN_LAST_NAME = os.environ.get("ADMIN_LAST_NAME", "Cortex")
    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@gmail.com")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")

    FLASK_ADMIN_SWATCH = "cerulean"

    MAIL_SERVER = os.environ.get("MAIL_SERVER", "google.com")
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_PORT = os.environ.get("MAIL_PORT", 587)
    MAIL_DEBUG = False
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "unknown_user")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "set_passwd")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", "sender@email.com")
    MAIL_MAX_EMAILS = 15
    MAIL_SUPPRESS_SEND = False
    MAIL_ASCII_ATTACHMENTS = False

    URL_REG_DOCTOR = "password-choose/{api_key}"

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
        "sqlite:///"
        + os.path.join(os.path.dirname(BASE_DIR), "database-devel.sqlite3"),
    )


class TestingConfig(BaseConfig):
    """Testing configuration."""

    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    MAIL_DEBUG = True
    MAIL_SUPPRESS_SEND = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "TEST_DATABASE_URL",
        "sqlite:///" + os.path.join(os.path.dirname(BASE_DIR), "database-test.sqlite3"),
    )


class ProductionConfig(BaseConfig):
    """Production configuration."""

    WTF_CSRF_ENABLED = False

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(os.path.dirname(BASE_DIR), "database.sqlite3"),
    )


config = dict(
    development=DevelopmentConfig, testing=TestingConfig, production=ProductionConfig
)
