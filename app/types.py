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


class DayOfWeek(Enum):
    """Data type for day of week cron field."""

    SUN = DayField('0', 'Воскресенье')
    MON = DayField('1', 'Понедельник')
    TUE = DayField('2', 'Вторник')
    WED = DayField('3', 'Среда')
    THU = DayField('4', 'Четверг')
    FRI = DayField('5', 'Пятница')
    SAT = DayField('6', 'Суббота')
    WORK = DayField('1-5', 'Рабочие дни')
    END = DayField('6,0', 'Выходные дни')
    EVERY = DayField('*', 'Ежедневно')

    @property
    def cron(self) -> str:
        return self.value.cron

    @property
    def title(self) -> str:
        return self.value.title

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
            DayField: object with attributes: cron, title.
        """
        pattern = re.compile(r'^(\*|[0-6](-[0-6])?)(,(\*|[0-6](-[0-6])?))*$')
        if not pattern.match(field):
            log.error(f'Can\'t parse cron field: {field}.')
            raise ValueError('arg not in valid format')
        try:
            return next(t.value for t in cls if t.value.cron == field)
        except StopIteration:
            log.warning(f'Can\'t find constant for cron field: {field}.')
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
        separator = re.findall(r'[^\d\s]', field)[0]
        for num in field.split(separator):
            titles.append(cls.by_string(num).title)
        return DayField(field, separator.join(titles))
