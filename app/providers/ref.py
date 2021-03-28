import logging
from typing import Dict, List, Union, Optional

import requests
from bs4 import BeautifulSoup
from cached_property import cached_property
from requests.exceptions import RequestException

from .weather import AbstractWeather, NoWeatherContent, Point

log = logging.getLogger(__name__)


class YandexWeather(AbstractWeather):
    """ Class for parsing info about weather from Yandex Weather.

    :param coords: Geo coordinates for collect local weather data at
     this location.
    """

    PARSER: str = 'html.parser'
    HEADERS: Dict[str, str] = {'User-Agent': 'Mozilla/5.0'}
    ENDPOINT: str = 'https://yandex.ru/pogoda/maps/nowcast'
    CLASSES: Dict = {
        'temp': 'temp__value_with-unit',
        'fact': [
            'weather-maps-fact__nowcast-alert',
            'weather-maps-fact__condition'
        ]
    }

    def __init__(self, coords: Point) -> None:
        self.coords = coords
        self.url = f'{self.ENDPOINT}?lat={coords.lat}&lon={coords.lon}'

    @cached_property
    def temp(self) -> str:
        """ Get value of current temperature. """
        return self._get_element_text(class_=self.CLASSES['temp'])

    @cached_property
    def fact(self) -> str:
        """ Get fact about current weather cast. """
        return self._get_element_text(class_=self.CLASSES['fact'])

    def _get_element_text(self, class_: Union[List, str], tag: Optional[str] = None) -> str:
        """ Return text from first founded element by given criteria.

        :param tag: What HTML tag to find.
        :param class_: What class or list of classes to find.
        """
        try:
            element = self.soup.find_all(tag, class_=class_)[0]
            return element.text
        except IndexError:
            log.error(f'Can\'t find tags with class attribute: {class_}.')
            raise NoWeatherContent('Weather forecast not available.')

    @cached_property
    def soup(self) -> BeautifulSoup:
        """ Returns cached soup data structure from raw HTML. """
        return self.parse()

    def parse(self) -> BeautifulSoup:
        """ Update request and return new soup data. """
        if self.__dict__.get('soup'):
            del self.__dict__['soup']
        raw_html = self._get_http_response(self.url)
        return BeautifulSoup(raw_html, self.PARSER).body

    def _get_http_response(self, url: str) -> str:
        """ Helper method, sends HTTP request and returns response payload.

        :param url: The URL to make request for.
        """
        try:
            response = requests.get(url, headers=self.HEADERS)
            return response.text
        except RequestException:
            log.error(f'Request can\'t be done! URL: {url}')
            return str('')
