from abc import ABC, abstractmethod
from app.types import GeoPoint


class NoWeatherContent(Exception):
    """ Raised when no weather cast text return. """
    pass


class AbstractWeather(ABC):
    """ Abstract weather class.

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
        """Constructor with at least one required argument.

        :param position: A Point object representing geo coordinates.
        """
        ...

    @property
    @abstractmethod
    def temp(self) -> str:
        ...

    @property
    @abstractmethod
    def fact(self) -> str:
        ...

    @classmethod
    def __str__(cls) -> str:
        return f'{cls.temp} {cls.fact}.'
