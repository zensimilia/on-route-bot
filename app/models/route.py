import logging
import time
from typing import Optional

from aiogram.utils.markdown import hide_link
from peewee import BooleanField, CharField, ForeignKeyField

from app.providers import yandex
from app.utils import uchar

from .base import BaseModel
from .user import User

log = logging.getLogger(__name__)


class Route(BaseModel):
    """Route model class."""

    name = CharField(null=False)
    url = CharField(null=False)
    user = ForeignKeyField(User, backref='routes')
    is_active = BooleanField(null=False, default=True)

    class Meta:
        table_name = 'routes'

    def message(self) -> Optional[str]:
        """Returns message about route for sending to user.

        Raises:
            KeyError: if no route selected.

        Returns:
            str|None: message in HTML format or None if have a problem with
            request or parsing.
        """
        if not self.url:
            raise KeyError  # todo: add message

        try:
            yamp = yandex.YAMParser(self.url)  # map parser instance
            map_center = yamp.coords

            # weather parser instance
            yawp = yandex.YAWParser(map_center['lat'], map_center['lon'])

            temp = yawp.temp + f'{uchar.DEGREE}C'
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
