from typing import List, TypeVar, Type, Optional
from sqlalchemy import Boolean, Column, ForeignKey, Integer, LargeBinary, select
from sqlalchemy.orm import relationship


from app.db import db_session

from .base import Model
from .route import Route

T = TypeVar('T', bound='Schedule')


class Schedule(Model):
    """Schedule model class."""

    __tablename__ = 'schedules'

    route_id = Column(
        Integer, ForeignKey('routes.id', ondelete='CASCADE'), nullable=False
    )
    cron = Column(LargeBinary, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    route = relationship(
        'Route',
        back_populates='schedules',
        cascade='all, delete',
        passive_deletes=True,
        single_parent=True,
    )

    @classmethod
    def get_active(cls: Type[T], route: Optional[Route] = None) -> List[T]:
        active_route_query = select(Route).where(Route.is_active.__eq__(True))
        if not route is None:
            query = (
                select(cls)
                .where(
                    (cls.is_active.__eq__(True))
                    & (cls.route_id.__eq__(route.id))
                )
                .subquery()
            )
        else:
            query = select(cls).where(cls.is_active.__eq__(True)).subquery()
        with db_session() as db:
            return db.query(query).join(active_route_query).all()
