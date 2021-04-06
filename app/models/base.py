from app.config import Config
from sqlalchemy.orm import registry, sessionmaker
from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy import create_engine, Column, DateTime, func, Integer

mapper_registry = registry()
engine = create_engine('sqlite:///%s' % Config.DB_FILE, echo=Config.DEBUG)
Session_maker = sessionmaker(bind=engine)
session = Session_maker()


class Model(metaclass=DeclarativeMeta):
    """Abstract Model class."""

    __abstract__ = True

    registry = mapper_registry
    metadata = mapper_registry.metadata

    id = Column(
        Integer,
        primary_key=True,
        unique=True,
        autoincrement=True,
        nullable=False,
    )
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(
        DateTime, server_default=func.now(), server_onupdate=func.now()
    )

    def __repr__(self):
        return '<%s (id=%s)>' % (self.__class__.__name__, self.id)
