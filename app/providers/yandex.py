import logging
from functools import cached_property  # https://stackoverflow.com/a/19979379
from typing import Optional, Union
from urllib import parse

import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from requests.models import Response

from app.providers.maps import AbstractMaps, NoMapContent
from app.providers.weather import AbstractWeather, NoWeatherContent
from app.types import GeoPoint
from app.utils import uchar

log = logging.getLogger(__name__)


class YandexWeather(AbstractWeather):
    """Class form parsing info about weather from Yandex Weather.

    :param float lat: Coordinates latitude.
    :param float lon: Coordinates longitude.
    """

    PARSER = 'html.parser'  # parser for soup
    HEADERS = {'User-Agent': 'Mozilla/5.0'}  # headers for requests
    ENDPOINT = 'https://yandex.ru/pogoda/maps/nowcast'
    CLASSES = [
        'weather-maps-fact__nowcast-alert',
        'weather-maps-fact__condition',
    ]

    def __init__(self, position: GeoPoint) -> None:
        self.lat = position.lat
        self.lon = position.lon
        self.url = self.ENDPOINT + f'?lat={self.lat}&lon={self.lon}'

    @cached_property
    def temp(self) -> str:
        """Get value of current temperature."""
        return (
            self.get_text(class_='temp__value_with-unit') + f'{uchar.DEGREE}C'
        )

    @cached_property
    def fact(self) -> str:
        """Get fact about current weather cast."""
        return self.get_text(class_=self.CLASSES)

    @cached_property
    def soup(self) -> BeautifulSoup:
        """Property, returns `soup` from raw HTML."""
        html = self._get_http_response(self.url).text
        return BeautifulSoup(html, self.PARSER)

    def get_text(
        self, class_: Union[str, list], tag: Optional[str] = None
    ) -> str:
        """Return parsed text from found element by parameters.

        :param str tag: What HTML-tag to parse.
        :param str class_: What class to parse.
        """
        result = self.soup.find(tag, class_=class_)
        if result is None:
            log.error(
                'Парсер не обнаружил элементы с классами %s на странице %s.',
                class_,
                self.url,
            )
            raise NoWeatherContent('Что-то пошло не так!') from None
        return result.text

    def _get_http_response(self, url: str) -> Response:
        """Helper method, sends HTTP request and returns response payload.

        :param str url: The URL to make request for.
        """
        try:
            return requests.get(url, headers=self.HEADERS)
        except RequestException as e:
            log.error('Возникли проблемы с получением данных по ссылке %s', url)
            raise NoWeatherContent(
                'Возникли проблемы с получением данных'
            ) from e


class YandexMaps(AbstractMaps):
    """Class for parsing info about routes from Yandex Maps.

    :param str url: The URL from which the HTML originated.
    """

    PARSER = 'html.parser'  # parser for soup
    HEADERS = {'User-Agent': 'Mozilla/5.0'}  # headers for requests
    CLASSES = ['auto-route-snippet-view__route-title-primary']
    ENDPOINT = 'https://static-maps.yandex.ru/1.x'

    def __init__(self, url: str) -> None:
        self.url = url

    @cached_property
    def time(self) -> str:
        """Alias for `get_time()` method but with caching and defaults."""
        return self.get_time()

    def get_time(
        self,
        class_: Optional[Union[str, list]] = None,
        tag: Optional[str] = None,
    ) -> str:
        """Return route time left. Get it by parsing page and find by tag and
        class names specified in fn attributes.

        :param str tag: What HTML-tag to parse.
        :param str class_: What class to parse. Defaults: self.CLASSES list.
        """
        class_ = class_ or self.CLASSES
        try:
            return self.soup.find(tag, class_=class_).text
        except AttributeError as e:
            log.warning(
                'Can\'t get time left for route from page %s.', self.url
            )
            raise NoMapContent('Информация о маршруте недоступна') from e

    @property
    def coords(self) -> GeoPoint:
        url_query = parse.urlparse(str(self.canonical)).query
        query_dict = parse.parse_qs(url_query)
        try:
            coords = query_dict['ll'][0].split(',')
            return GeoPoint(lat=float(coords[1]), lon=float(coords[0]))
        except KeyError:
            log.warning(
                'Can\'t parse canonical URL (%s) to get coordinates.',
                self.canonical,
            )
            raise NoMapContent(
                'Невозможно получить координаты маршрута'
            ) from None

    @cached_property
    def soup(self) -> BeautifulSoup:
        """Property, returns `soup` from raw HTML."""
        html = self._get_http_response(self.url)
        return BeautifulSoup(html, self.PARSER)

    def _get_http_response(self, url: str) -> str:
        """Helper method, sends HTTP request and returns response payload.

        :param str url: The URL to make request for.
        """
        try:
            response = requests.get(url, headers=self.HEADERS)
        except RequestException as e:
            log.error('Request error for URL %s.', url)
            raise NoMapContent('Возникли проблемы с получением данных!') from e
        return response.text

    @cached_property
    def canonical(self) -> Optional[str]:
        """Returns full link to map page from short URL."""
        link = self.soup.find('link', rel='canonical')
        if link is None:
            log.warning('Can\'t get canonical URL from %s.', self.url)
            return None
        return parse.unquote(link.get('href'))

    @property
    def map(self) -> Optional[str]:
        """Returns URL of static map image with traffic layer."""
        if self.canonical is None:
            return None
        url_query = parse.urlparse(self.canonical).query
        rtext = parse.parse_qs(url_query)['rtext'][0].split('~')
        swaprf = ','.join(reversed(rtext[0].split(',')))
        swaprl = ','.join(reversed(rtext[-1].split(',')))
        url_params = {
            'l': 'map,trf',
            'size': '650,450',
            'bbox': '%s~%s' % (swaprf, swaprl),
        }
        return self.ENDPOINT + '?' + parse.urlencode(url_params)
