from abc import ABC, abstractmethod
from app.types import GeoPoint


class NoWeatherContent(Exception):
    """ Raised when no weather cast text return. """

    pass


class AbstractWeather(ABC):
    """Abstract weather class.

    Implement your own subclass of web scraping or get by API weather
    data and return current temperature and forecast by properties
    temp and fact.

    Type Point is a named Tuple with keys: lat, lon and their float
    values representing geo coordinates for collect local weather
    data at this location.

    Property ``temp`` must return string with current temperature.

    Property ``fact`` must return string with current forecast.
    """

    @abstractmethod
    def __init__(self, position: GeoPoint) -> None:
        ...

    def __new__(cls, *_args, **_kargs):
        required_class_attributes = ['ENDPOINT', 'HEADERS', 'PARSER']
        for attr in required_class_attributes:
            if not hasattr(cls, attr):
                raise NotImplementedError(
                    f'Class {cls} lacks required {attr} class attribute'
                ) from None
        return object.__new__(cls)

    @abstractmethod
    def temp(self) -> str:
        ...

    @abstractmethod
    def fact(self) -> str:
        ...

    @classmethod
    def __str__(cls) -> str:
        return f'{cls.temp} {cls.fact}.'
