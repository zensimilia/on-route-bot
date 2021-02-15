from bs4 import BeautifulSoup
from urllib import parse
import requests


class Parser:
    """
    Parser class
    """

    def __init__(self, url) -> None:
        self.url = url
        self._headers = {'User-Agent': 'Mozilla/5.0'}  # headers for requests
        self._response = requests.get(self._url, headers=self._headers)
