import logging
import re
from enum import Enum
from typing import NamedTuple

log = logging.getLogger(__name__)


class GeoPoint(NamedTuple):
    """ Data type for geo coordinates. """
    lat: float
    lon: float


class CronDay(NamedTuple):
    """ Data type for cron `day of week` field. """
    cron: str
    title: str


class DayOfWeek(Enum):
    """ Day of week data type.

    Attributes:
        cron  (str) : Day in cron string format.
        title (str) : Title of week day or week period.
    """
    SUN = CronDay('0', 'Воскресенье')
    MON = CronDay('1', 'Понедельник')
    TUE = CronDay('2', 'Вторник')
    WED = CronDay('3', 'Среда')
    THU = CronDay('4', 'Четверг')
    FRI = CronDay('5', 'Пятница')
    SAT = CronDay('6', 'Суббота')
    WRK = CronDay('1-5', 'Рабочие дни')
    WND = CronDay('6,0', 'Выходные дни')
    ALL = CronDay('*', 'Ежедневно')

    @property
    def cron(self) -> str:
        return self.value.cron

    @property
    def title(self) -> str:
        return self.value.title

    @classmethod
    def by_cron(cls, cron_string: str) -> 'CronDay':
        """ Return `CronDay` instance filtered by `cron` attribute.
                :param cron_string: A string by which filtered.
        """
        pattern = re.compile('^(\*|[0-6](-[0-6])?)(,(\*|[0-7](-[0-7])?))*$')
        if not pattern.match(cron_string):
            log.error(f'Can\'t parse cron string: {cron_string}.')
            raise ValueError()
        try:
            return next(t.value for t in cls if t.value.cron == cron_string)
        except StopIteration:
            log.warning(f'Can\'t find constant for cron string: {cron_string}.')
            return cls.__parse_cron(cron_string)

    @classmethod
    def __parse_cron(cls, cron_string: str) -> 'CronDay':
        titles = list()
        separator = re.findall(r'[^\d\s]', cron_string)[0]
        for num in cron_string.split(separator):
            titles.append(cls.by_cron(num).title)
        return CronDay(cron=cron_string, title=separator.join(titles))
