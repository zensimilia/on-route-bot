from urllib import parse

import requests
from bs4 import BeautifulSoup


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


class YAWParser:
    """
    Class form parsing info about weather from Yandex Weather.

    :param float lat: Coordinates latitude.
    :param float lon: Coordinates longitude.
    """

    PARSER = 'html.parser'  # parser for soup
    HEADERS = {'User-Agent': 'Mozilla/5.0'}  # headers for requests
    WEATHER_PROVIDER = 'Yandex'
    ENDPOINT = 'https://yandex.ru/pogoda/maps/nowcast'

    def __init__(self, lat: float, lon: float) -> None:
        self.lat = lat
        self.lon = lon
        self.url = self.ENDPOINT + f'?lat={self.lat}&lon={self.lon}'

    @property
    def temp(self) -> str:
        """
        Get value of current temperature.
        """
        if not hasattr(self, '_temp'):
            setattr(
                self,
                '_temp',
                self.get_text('span', class_='temp__value_with-unit'),
            )
        return getattr(self, '_temp')

    @property
    def fact(self) -> str:
        """
        Get fact about current weather cast.
        """
        classes = [
            'weather-maps-fact__nowcast-alert',
            'weather-maps-fact__condition',
        ]
        if not hasattr(self, '_fact'):
            # todo: check `weather-maps-fact__condition` if exception
            setattr(self, '_fact', self.get_text('div', class_=classes))
        return getattr(self, '_fact')

    def get_text(self, tag: str, class_: str) -> str:
        """
        Return parsed text from found element by parameters.

        :param str tag: What HTML-tag to parse.
        :param str class_: What class to parse.
        """
        try:
            if class_.__class__.__name__ in ('list', 'tuple'):
                return self.soup.find_all(tag, class_=class_)[0].text
            else:
                return self.soup.find(tag, class_=class_).text
        except Exception as e:
            raise YAParseError('Что-то пошло не так!') from e

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
            raise YARequestError(
                'Возникли проблемы с получением данных!'
            ) from e
        return response.text


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

    def get_time(
        self,
        tag: str = 'div',
        class_: str = 'auto-route-snippet-view__route-title-primary',
    ) -> str:
        """
        Return route time left.

        :param str tag: What HTML-tag to parse.
        :param str class_: What class to parse.
        """
        try:
            return self.soup.find(tag, class_=class_).text
        except Exception as e:
            raise YAParseError('Что-то пошло не так!') from e

    @property
    def coords(self) -> dict:
        try:
            coords = parse.parse_qs(parse.urlparse(self.canonical).query)['ll'][
                0
            ].split(',')
        except Exception as e:
            raise YAParseError('Что-то пошло не так!') from e
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
            raise YARequestError(
                'Возникли проблемы с получением данных!'
            ) from e
        return response.text

    @property
    def canonical(self) -> str:
        """
        Returns full page link from short URL.
        """
        try:
            return parse.unquote(
                self.soup.find('link', rel='canonical')['href']
            )
        except Exception as e:
            raise YARequestError(
                'Возникли проблемы с получением данных!'
            ) from e

    @property
    def map(self) -> str:
        """
        Returns URL of static map image with traffic layer.
        """
        rtext = parse.parse_qs(parse.urlparse(self.canonical).query)['rtext'][
            0
        ].split('~')
        swaprf = ','.join(reversed(rtext[0].split(',')))
        swaprl = ','.join(reversed(rtext[-1].split(',')))
        map_url = (
            'https://static-maps.yandex.ru/1.x/?'
            f'l=map,trf&size=650,450&bbox={swaprf}~{swaprl}'
        )
        return map_url
