import logging
import time
from typing import Optional

from aiogram.utils.markdown import hide_link
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.providers import yandex

from .base import Model

log = logging.getLogger(__name__)


class Route(Model):
    """Route model class."""

    __tablename__ = 'routes'

    user_id = Column(
        Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False
    )
    name = Column(String(64), nullable=False)
    url = Column(String(), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    schedules = relationship(
        'Schedule',
        back_populates='route',
        cascade='all, delete',
        passive_deletes=True,
    )

    def __int__(self):
        return self.id

    def message(self) -> Optional[str]:
        """Returns message about route for sending to user.

        Raises:
            KeyError: if no route selected.

        Returns:
            String message in HTML format or None if have a problem with
            request or parsing.
        """
        if not self.url:
            raise KeyError  # todo: add message

        try:
            yamp = yandex.YAMParser(self.url)  # map parser instance

            # weather parser instance
            yawp = yandex.YAWParser(yamp.coords)

            temp = yawp.temp
            fact = yawp.fact
            time_left = yamp.time

            timestamp = time.time()
            # add timestamp to avoid image caching
            map_url = hide_link(f'{yamp.map}&{timestamp}')

            return (
                f'{map_url}'
                f'Маршрут <b>{self.name}</b> займет <b>{time_left}</b> '
                f'<a href="{yamp.url}">(открыть)</a>. '
                f'За окном <b>{temp}</b> {fact} '
                f'<a href="{yawp.url}">(подробнее)</a>.'
            )
        except (yandex.YAParseError, yandex.YARequestError) as e:
            log.warning('Can\'t get map or weather: %s', e)

        return None
