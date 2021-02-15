from bs4 import BeautifulSoup
from urllib import parse
import requests


class BaseParser:
    """
    Base parser class
    """
    PARSER = 'html.parser'
    HEADERS = {'User-Agent': 'Mozilla/5.0'}  # headers for requests

    _defaults = {}

    def __init__(self, url: str) -> None:
        self.url = url
        self.soup = None
        self.time = None

    def parse(self):
        html = self._get_http_response(self.url)
        self.soup = BeautifulSoup(html, self.PARSER)
        return self

    def _get_http_response(self, url: str):
        """
        Helper method, sends HTTP request and returns response payload.
        """
        try:
            request = requests.get(url, headers=self.HEADERS)
            html = request.text
            return html
        except Exception:
            return None


class YAMParser(BaseParser):
    """
    Parser class for Yandex Maps.
    """

    MAP_PROVIDER = 'Yandex'

    def __init__(self, url: str) -> None:
        BaseParser.__init__(self, url)
        self.static_map: str = None

    def _parse_time(self, **kwargs):
        params = {
            'time_tag': 'div',
            'time_class': 'auto-route-snippet-view__route-title-primary',
        }
        params.update(kwargs)
        self.time = self.soup.find(
            params['time_tag'], class_=params['time_class']).text

    def get_time(self):
        """
        Return route time left.
        """
        self._parse_time()
        return self.time


test = YAMParser('https://yandex.ru/maps/-/CCUMf0bhoD').parse()
print(test.get_time())
