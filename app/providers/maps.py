from abc import ABC, abstractmethod

from app.types import GeoPoint


class NoMapContent(Exception):
    """Raised when impossible to get information about route."""


class AbstractMaps(ABC):
    """Abstract map class.

    Implement your own subclass of web scraping or get by API map
    data and return information about route.
    """

    @abstractmethod
    def __init__(self, url: str) -> None: ...

    def __new__(cls, *_args, **_kargs):
        required_class_attributes = ["HEADERS", "PARSER"]
        for attr in required_class_attributes:
            if not hasattr(cls, attr):
                raise NotImplementedError(
                    f"Class {cls} lacks required {attr} class attribute"
                ) from None
        return object.__new__(cls)

    @abstractmethod
    def time(self) -> str: ...

    @abstractmethod
    def coords(self) -> GeoPoint: ...

    @abstractmethod
    def map(self) -> str: ...

    def __str__(self) -> str:
        return str(self.time)
