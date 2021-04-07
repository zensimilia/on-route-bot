from datetime import datetime

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.orm import registry
from sqlalchemy.orm.decl_api import DeclarativeMeta

mapper_registry = registry()


class Model(metaclass=DeclarativeMeta):
    """Abstract Model class."""

    __abstract__ = True
    __mapper_args__ = {'eager_defaults': True}

    registry = mapper_registry
    metadata = mapper_registry.metadata

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(
        DateTime(timezone=True),
        default=datetime.now(),
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.now(),
        onupdate=datetime.now(),
    )

    def __repr__(self):
        return '<%s #%s>' % (self.__class__.__name__, self.id)
