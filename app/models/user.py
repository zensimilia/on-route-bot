from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Model


class User(Model):
    """User model class."""

    __tablename__ = 'users'

    uid = Column(Integer, unique=True, nullable=False, index=True)
    username = Column(String, nullable=False)
    timezone = Column(String, default='Europe/Moscow')
    routes = relationship(
        'Route',
        backref='user',
        cascade='all, delete',
        passive_deletes=True,
    )

    def __repr__(self):
        return '<%s #%s (user_id=%s, username="%s")>' % (
            self.__class__.__name__,
            self.id,
            self.uid,
            self.username,
        )
