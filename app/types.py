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
    """Data type for day of week cron field."""

    SUN = DayField('0', 'Воскресенье', 'Вс')
    MON = DayField('1', 'Понедельник', 'Пн')
    TUE = DayField('2', 'Вторник', 'Вт')
    WED = DayField('3', 'Среда', 'Ср')
    THU = DayField('4', 'Четверг', 'Чт')
    FRI = DayField('5', 'Пятница', 'Пт')
    SAT = DayField('6', 'Суббота', 'Сб')
    WORK = DayField('1-5', 'Рабочие дни', 'Раб')
    END = DayField('6,0', 'Выходные дни', 'Вых')
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

            day = DayOfWeek.by_string('1-2')
            print(day.cron, day.`title) # 1-2 Понедельник-Вторник

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
