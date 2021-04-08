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
        if not route is None:
            parent_cls = route.__class__
            with db_session() as db:
                return (
                    db.query(cls)
                    .where(
                        (cls.is_active.__eq__(True))
                        & (cls.route_id.__eq__(route.id))
                    )
                    .join(parent_cls)
                    .where(parent_cls.is_active.is_(True))
                    .all()
                )
        else:
            with db_session() as db:
                return (
                    db.query(cls)
                    .where(cls.is_active.__eq__(True))
                    .join(Route)
                    .where(Route.is_active.__eq__(True))
                    .all()
                )
