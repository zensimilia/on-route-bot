from enum import Enum
from typing import TypeVar, Type

T = TypeVar('T', bound='DayOfWeek')


class DayOfWeek(Enum):
    """ Day of week data type.

    Attributes:
        cron  (str) : Day in cron string format.
        title (str) : Title of week day or week period.
    """
    SUN = ('0', 'Воскресенье')
    MON = ('1', 'Понедельник')
    TUE = ('2', 'Вторник')
    WED = ('3', 'Среда')
    THU = ('4', 'Четверг')
    FRI = ('5', 'Пятница')
    SAT = ('6', 'Суббота')
    WRK = ('1-5', 'Рабочие дни')
    WND = ('6,0', 'Выходные дни')
    ALL = ('*', 'Ежедневно')

    @property
    def cron(self) -> str:
        return self.value[0]

    @property
    def title(self) -> str:
        return self.value[1]

    @classmethod
    def by_cron(cls: Type[T], cron_string: str) -> T:
        """ Return class instance filtered by `cron` attribute.
        :param cron_string: A string by which filtered.
        """
        # todo:
        # [ ] catch StopIteration exception and return something (?)
        return next(t for t in cls if t.cron == cron_string)
