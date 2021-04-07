from sqlalchemy import Boolean, Column, ForeignKey, Integer, LargeBinary
from .base import Model


class Schedule(Model):
    """Schedule model class."""

    __tablename__ = 'schedules'

    route_id: int = Column(
        Integer, ForeignKey('routes.id', ondelete='CASCADE'), nullable=False
    )
    cron: str = Column(LargeBinary, nullable=False)
    is_active: bool = Column(Boolean, nullable=False, default=True)
