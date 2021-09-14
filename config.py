import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))


class BaseConfig(object):
    """Base configuration."""

    APP_NAME = "Cortex_Admin"
    DEBUG_TB_ENABLED = False
    SECRET_KEY = os.environ.get(
        "SECRET_KEY", "Ensure you set a secret key, this is important!"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False

    TEST_API_KEY = os.environ.get("TELEGRAM_TEST_API_KEY", "1234567890:UNKNOWN-VALUE")
    API_KEY = os.environ.get("TELEGRAM_API_KEY")

    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "unknown_user")
    ADMIN_FIRST_NAME = os.environ.get("ADMIN_FIRST_NAME", "Paul Jackson")
    ADMIN_LAST_NAME = os.environ.get("ADMIN_LAST_NAME", "Pollock")
    ADMIN_TELEGRAM_ID = os.environ.get("ADMIN_TELEGRAM_ID", "88888888")
    TELEGRAM_REDIRECT_URL = os.environ.get("TELEGRAM_REDIRECT_URL")
    TELEGRAM_BOT_USERNAME = os.environ.get("TELEGRAM_BOT_USERNAME")

    TELEGRAM_DEFAULT_GROUP_NAME = os.environ.get(
        "TELEGRAM_DEFAULT_GROUP_NAME", "Group_Pollock"
    )
    TELEGRAM_DEFAULT_GROUP_ID = int(
        os.environ.get("TELEGRAM_DEFAULT_GROUP_ID", -592013051)
    )

    PHOTO_PATH = os.path.join(BASE_DIR, "data/photo")

    FLASK_ADMIN_SWATCH = "cerulean"

    GALLERY_PHOTO_PER_PAGE = int(os.environ.get("GALLERY_PHOTO_PER_PAGE", 15))

    LOG_LEVEL = int(os.environ.get("LOG_LEVEL", 20))

    @staticmethod
    def configure(app):
        # Implement this method to do further configuration on your app.
        pass


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
    NUMBER_TEST_PHOTOS = int(os.environ.get("NUMBER_TEST_PHOTOS", 5))


class ProductionConfig(BaseConfig):
    """Production configuration."""

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///" + os.path.join(BASE_DIR, "database.sqlite3")
    )
    WTF_CSRF_ENABLED = True


config = dict(
    development=DevelopmentConfig, testing=TestingConfig, production=ProductionConfig
)
