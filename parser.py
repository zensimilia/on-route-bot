from urllib import parse

import requests
from bs4 import BeautifulSoup


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
            print(e)
        return 'Что-то пошло не так!'

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
            if response.status_code != 200:
                return ''
        except Exception as e:
            print(e)
        return response.text

    @property
    def canonical(self) -> str:
        """
        Returns full page link from tiny.
        """
        return self.soup.find('link', rel='canonical')['href']

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
