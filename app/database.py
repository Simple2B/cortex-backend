from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from app.config.settings import settings


engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, convert_unicode=True)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

Base = declarative_base()

Base.query = db_session.query_property()

# engine.connect()


# Dependency
# def get_db():
#     try:
#         db = SessionLocal()
#         yield db
#     finally:
#         db.close()


def init_db():
    import app.models

    Base.metadata.create_all(bind=engine)


# init_db()
