from app.utils import uchar
import logging
import re
from enum import Enum
from typing import NamedTuple

log = logging.getLogger(__name__)


class GeoPoint(NamedTuple):
    lat: float
    lon: float


class DayField(NamedTuple):
    cron: str
    title: str
    short: str


class DayOfWeek(Enum):
    """Data type for day of week cron field.

    NOTICE: The first weekday is always monday.
    Will be fixed in 4.0 release of APScheduler.
    https://github.com/agronholm/apscheduler/issues/465
    """

    MON = DayField('0', 'Понедельник', 'Пн')
    TUE = DayField('1', 'Вторник', 'Вт')
    WED = DayField('2', 'Среда', 'Ср')
    THU = DayField('3', 'Четверг', 'Чт')
    FRI = DayField('4', 'Пятница', 'Пт')
    SAT = DayField('5', 'Суббота', 'Сб')
    SUN = DayField('6', 'Воскресенье', 'Вс')
    WORK = DayField('0-4', 'Рабочие дни', 'Раб')
    END = DayField('5-6', 'Выходные дни', 'Вых')
    EVERY = DayField('*', 'Ежедневно', 'Ежд')

    @property
    def cron(self) -> str:
        return self.value.cron

    @property
    def title(self) -> str:
        return self.value.title

    @property
    def short(self) -> str:
        return self.value.short

    @classmethod
    def by_string(cls, field: str) -> DayField:
        """Get matching object by cron field string.

        Example::

            day = DayOfWeek.by_string('0-1')
            print(day.cron, day.`title) # 0-1 Понедельник-Вторник

        Args:
            field (str): cron field string.

        Raises:
            ValueError: if arg not in valid format.

        Returns:
            DayField: object with attributes: cron, title, short.
        """
        pattern = re.compile(r'^(\*|[0-6](-[0-6])?)(,(\*|[0-6](-[0-6])?))*$')
        if not pattern.match(field):
            log.error('Can\'t parse cron field: %s.', field)
            raise ValueError('arg not in valid format')
        try:
            return next(t.value for t in cls if t.value.cron == field)
        except StopIteration:
            log.warning('Can\'t find constant for cron field: %s.', field)
            return cls.__parse_cron(field)

    @classmethod
    def __parse_cron(cls, field: str) -> DayField:
        """Parse cron field and return day object.

        Args:
            field (str): cron field string.

        Returns:
            DayField: object with attributes: cron, title.
        """
        titles = list()
        shorts = list()
        separator = re.findall(r'[^\d\s]', field)[0]
        for num in field.split(separator):
            item = cls.by_string(num)
            titles.append(item.title)
            shorts.append(item.short)
        return DayField(field, separator.join(titles), separator.join(shorts))


class Bell(str, Enum):
    ON = f'{uchar.BELL}'
    OFF = f'{uchar.BELL_STROKE}'

    @classmethod
    def by_state(cls, state: bool) -> str:
        """Returns bell string by state."""
        return cls.ON.value if state else cls.OFF.value
