import logging
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from app.config import Config

log = logging.getLogger(__name__)

db_engine = create_engine('sqlite:///%s' % Config.DB_FILE, echo=Config.DEBUG)


@contextmanager
def db_session():
    session = scoped_session(sessionmaker(bind=db_engine))
    try:
        session.execute('PRAGMA foreign_keys=ON')
        yield session
        session.commit()
        session.flush()
    except:
        log.error('An error has occured in runtime SQL query.')
        session.rollback()
        raise
    finally:
        session.close()
