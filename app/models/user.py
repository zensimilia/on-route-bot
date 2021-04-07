from typing import Any

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Model


class User(Model):
    """User model class."""

    __tablename__ = 'users'

    uid: int = Column(Integer, unique=True, nullable=False, index=True)
    username: str = Column(String, nullable=False)
    timezone: str = Column(String, default='Europe/Moscow')
    routes: Any = relationship(
        'Route',
        backref='user',
        cascade='all, delete',
        passive_deletes=True,
        lazy='dynamic',
    )

    def __repr__(self):
        return '<%s #%s (user_id=%s, username="%s")>' % (
            self.__class__.__name__,
            self.id,
            self.user_id,
            self.username,
        )
