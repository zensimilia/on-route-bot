from app.providers.ref import YandexWeather, Point, NoWeatherContent
from app.utils.log import configure_logging
configure_logging()


test = YandexWeather(Point(45.028488, 38.967086))
# test.ENDPOINT = 'https://yandex.ru/pogoda/maps/nowcast'
# test.CLASSES['fact'] = ['sdfsdfsf', 'sdfsdfsdf']
try:
    print(test.temp, test.fact)
except NoWeatherContent:
    print('No weather content.')
