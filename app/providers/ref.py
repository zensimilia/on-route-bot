from abc import ABC, abstractmethod
from typing import Dict, List, NamedTuple, Union
from urllib import parse

import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from typing_extensions import Final


class Point(NamedTuple):
    """ Data type for geo coordinates. """
    lat: float
    lon: float


class YAParseError(Exception):
    """
    Raised when parser can't return necessary result.
    """
    pass


class YARequestError(Exception):
    """
    Raised when parser have problems with request document.
    """
    pass


class AbstractWeather(ABC):
    """ Abstract weather class.

    Implement your own subclass of web scraping or get by API weather
    data and return current temperature and forecast by properties
    temp and fact.

    Type Point is a named Tuple with keys: lat, lon and their float
    values representing geo coordinates for collect local weather
    data at this location.

    Property temp must return string with current temperature.

    Property fact must return string with current forecast.
    """

    @abstractmethod
    def __init__(self, position: Point) -> None:
        """Constructor with at least one required argument.

        :param position: A Point object representing geo coordinates.
        """

    @property
    @abstractmethod
    def temp(self) -> str:
        ...

    @property
    @abstractmethod
    def fact(self) -> str:
        ...

    @classmethod
    def __str__(self) -> str:
        return f'{self.temp} {self.fact}.'


class YandexWeather(AbstractWeather):
    """
    Class form parsing info about weather from Yandex Weather.

    :param float lat: Coordinates latitude.
    :param float lon: Coordinates longitude.
    """

    PARSER: str = 'html.parser'
    HEADERS: Dict[str, str] = {
        'User-Agent': 'Mozilla/5.0'
    }
    PROVIDER: Final[str] = 'Yandex'
    ENDPOINT: str = 'https://yandex.ru/pogoda/maps/nowcast'

    def __init__(self, coords: Point) -> None:
        """ Constructor. """
        self.coords = coords
        self.url = self.ENDPOINT + f'?lat={coords.lat}&lon={coords.lon}'

    @property
    def temp(self) -> str:
        """ Get value of current temperature. """
        if not hasattr(self, '_temp'):
            setattr(self, '_temp', self.get_element_text(
                'span', class_='temp__value_with-unit'))
        return getattr(self, '_temp')

    @property
    def fact(self) -> str:
        """ Get fact about current weather cast. """
        classes = [
            'weather-maps-fact__nowcast-alert',
            'weather-maps-fact__condition'
        ]
        if not hasattr(self, '_fact'):
            # todo: check `weather-maps-fact__condition` if exception
            setattr(self, '_fact', self.get_element_text(
                    'div', class_=classes))
        return getattr(self, '_fact')

    def get_element_text(self, tag: str, class_: Union[List, str]) -> str:
        """ Return text from first found element by given criteria.

        :param tag: What HTML-tag to find.
        :param class_: What class or list of classes to find.
        """
        try:
            element = self.soup.find_all(tag, class_=class_)[0]
        except Exception:
            return 'Н/Д'
        return element.text

    @property
    def soup(self) -> BeautifulSoup:
        """ Returns soup data structure from raw HTML. """
        if not hasattr(self, '_soup'):
            html = self._get_http_response(self.url)
            soup = BeautifulSoup(html, self.PARSER)
            setattr(self, '_soup', soup)
        return getattr(self, '_soup')

    def _get_http_response(self, url: str) -> str:
        """ Helper method, sends HTTP request and returns response payload.

        :param url: The URL to make request for.
        """
        try:
            response = requests.get(url, headers=self.HEADERS)
        except RequestException as e:
            raise YARequestError('Возникли проблемы с получением данных!', e)
        return response.text


test = YandexWeather(Point(12345.028488, 12338.967086))
print(test.temp, test.fact)


class YAMParser:
    """
    Class for parsing info about routes from Yandex Maps.

    :param str url: The URL from which the HTML originated.
    """

    PARSER = 'html.parser'  # parser for soup
    HEADERS = {'User-Agent': 'Mozilla/5.0'}  # headers for requests
    MAP_PROVIDER = 'Yandex'

    def __init__(self, url: str) -> None:
        self.url = url

    @property
    def time(self) -> str:
        """
        Alias for `get_time()` method but with caching and defaults.
        """
        if not hasattr(self, '_time'):
            setattr(self, '_time', self.get_time())
        return getattr(self, '_time')

    def get_time(self,
                 tag: str = 'div',
                 class_: str = 'auto-route-snippet-view__route-title-primary') -> str:
        """
        Return route time left.

        :param str tag: What HTML-tag to parse.
        :param str class_: What class to parse.
        """
        try:
            return self.soup.find(
                tag, class_=class_).text
        except Exception as e:
            raise YAParseError('Что-то пошло не так!')

    @property
    def coords(self) -> dict:
        try:
            coords = parse.parse_qs(parse.urlparse(self.canonical).query)[
                'll'][0].split(',')
        except Exception as e:
            raise YAParseError('Что-то пошло не так!')
        return {
            'lon': float(coords[0]),
            'lat': float(coords[1]),
        }

    @property
    def soup(self) -> BeautifulSoup:
        """
        Property, returns `soup` from raw HTML.
        """
        if not hasattr(self, '_soup'):
            html = self._get_http_response(self.url)
            soup = BeautifulSoup(html, self.PARSER)
            setattr(self, '_soup', soup)
        return getattr(self, '_soup')

    def _get_http_response(self, url: str) -> str:
        """
        Helper method, sends HTTP request and returns response payload.

        :param str url: The URL to make request for.
        """
        try:
            response = requests.get(url, headers=self.HEADERS)
        except Exception as e:
            raise YARequestError('Возникли проблемы с получением данных!')
        return response.text

    @property
    def canonical(self) -> str:
        """
        Returns full page link from short URL.
        """
        try:
            return parse.unquote(self.soup.find('link', rel='canonical')['href'])
        except Exception as e:
            raise YARequestError('Возникли проблемы с получением данных!')

    @property
    def map(self) -> str:
        """
        Returns URL of static map image with traffic layer.
        """
        rtext = parse.parse_qs(parse.urlparse(self.canonical).query)[
            'rtext'][0].split('~')
        swaprf = ','.join(reversed(rtext[0].split(',')))
        swaprl = ','.join(reversed(rtext[-1].split(',')))
        map_url = f'https://static-maps.yandex.ru/1.x/?l=map,trf&size=650,450&bbox={swaprf}~{swaprl}'
        return map_url
