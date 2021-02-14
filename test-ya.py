from bs4 import BeautifulSoup
from urllib import parse
import requests

url = 'https://yandex.ru/maps/-/CCUMf0bhoD'
headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
items = soup.find('div', class_='auto-route-snippet-view__route-title-primary')
print('time', items.text)
# trf = soup.find('div', _class='traffic-raw-icon__text')
# print('probki', trf.text)
canonical = soup.find('link', rel='canonical')['href']
location = parse.parse_qs(parse.urlparse(canonical).query)['ll'][0]
rtext = parse.parse_qs(parse.urlparse(canonical).query)['rtext'][0].split('~')
swaprf = ','.join(reversed(rtext[0].split(',')))
swaprl = ','.join(reversed(rtext[-1].split(',')))
rfirst = f'{swaprf},flag'
rlast = f'{swaprl},flag'
print('location', location)
static_map_url = f'https://static-maps.yandex.ru/1.x/?l=map,trf&size=650,450&bbox={swaprf}~{swaprl}'
print('static_map_url', static_map_url)
