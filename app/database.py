import os
from sqlalchemy import create_engine
from app.config.settings import settings
from app.logger import log

engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)

Base = None
if os.environ.get("FLASK_APP", None):
    log(log.INFO, "Use Flask")
    from admin import db

    Base = db.Model
    db_session = db.session
else:
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import scoped_session, sessionmaker

    log(log.INFO, "Use FastAPI")
    db_session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )
    Base = declarative_base()
    Base.query = db_session.query_property()
