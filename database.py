"""
Contains functions and variables for initializing and connecting to the
database.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:////tmp/test.db", convert_unicode=True)

# Handle threads with scoped_session
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    # Import modules that might define models so that they get registered
    # properly on the metadata. Otherwise you will have to import them first
    # before calling init_db()
    from models import models
    Base.metadata.create_all(bind=engine)
