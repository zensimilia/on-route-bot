from .base import Model
from sqlalchemy import Column, Integer, String


class User(Model):
    """User model class."""

    __tablename__ = 'users'
    __mapper_args__ = {'eager_defaults': True}

    user_id = Column(Integer, unique=True, nullable=False, index=True)
    username = Column(String, nullable=False)
    timezone = Column(String, default='Europe/Moscow')
