from sqlalchemy import Boolean, Column, ForeignKey, Integer, LargeBinary
from .base import Model


class Schedule(Model):
    """Schedule model class."""

    __tablename__ = 'schedules'

    route_id = Column(
        Integer, ForeignKey('routes.id', ondelete='CASCADE'), nullable=False
    )
    cron = Column(LargeBinary, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
