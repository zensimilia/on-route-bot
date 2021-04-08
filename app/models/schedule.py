from typing import List, Optional, Type, TypeVar, Union

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
    def get_active(
        cls: Type[T], route: Optional[Union['Route', int]] = None
    ) -> List[T]:
        """Get list of active schedules. Parent route needs to be active too.

        Args:
            route (Route, int): A Route instance or route id. Defaults to None.

        Returns:
            List of Schedule instances or empty list
            if no active schedules found.
        """
        active_routes = select(Route).where(Route.is_active.__eq__(True))
        if route is not None:
            route_id = int(route)
            active_routes = active_routes.where(Route.id.__eq__(route_id))
        stmt = (
            select(cls)
            .where(cls.is_active.__eq__(True))
            .join(active_routes.cte())
        )
        with db_session() as db:
            return db.execute(stmt).scalars().all()
