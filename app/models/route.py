import logging
import time
from typing import Optional

from aiogram.utils.markdown import hide_link
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.providers import yandex
from app.providers.weather import NoWeatherContent
from app.providers.maps import NoMapContent

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
            raise KeyError  # TODO: add message

        timestamp = time.time()
        maps = yandex.YandexMaps(self.url)

        try:
            weather = yandex.YandexWeather(maps.coords)

            # add timestamp to avoid image caching
            map_url = hide_link(f'{maps.map}&{timestamp}')

            return (
                f'{map_url}'
                f'Маршрут <b>{self.name}</b> займет <b>{maps.time}</b> '
                f'<a href="{maps.url}">(открыть)</a>. '
                f'За окном <b>{weather.temp}</b> {weather.fact} '
                f'<a href="{maps.url}">(подробнее)</a>.'
            )
        except (NoMapContent, NoWeatherContent):
            return None
