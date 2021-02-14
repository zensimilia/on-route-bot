from bs4 import BeautifulSoup
import requests

url = 'https://go.2gis.com/rewrj'
headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
items = soup.find('div', class_='_mfyskr')
print(items.div.text)
