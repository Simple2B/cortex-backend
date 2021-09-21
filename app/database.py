import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from app.config.settings import settings
from app.logger import log


engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, convert_unicode=True)


Base = None
if os.environ.get("FLASK_APP", None):
    log(log.INFO, "Use Flask")
    from admin import db

    Base = db.Model
    db_session = db.session
else:
    log(log.INFO, "Use FastAPI")
    db_session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )
    Base = declarative_base()
    Base.query = db_session.query_property()


def init_db():

    Base.metadata.create_all(bind=engine)
