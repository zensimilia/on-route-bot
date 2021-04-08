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
        active_route_query = select(Route).where(Route.is_active.__eq__(True))
        if route is None:  # get all active schedules in active routes
            stmt = select(cls).where(cls.is_active.__eq__(True))
        else:  # get specific route active schedules
            route_id = route if isinstance(route, int) else route.id
            stmt = (
                select(cls)
                .where(cls.is_active.__eq__(True))
                .where(cls.route_id.__eq__(route_id))
            )
        with db_session() as db:
            return db.query(stmt.subquery()).join(active_route_query).all()
