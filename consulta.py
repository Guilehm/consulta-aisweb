import requests

from bs4 import BeautifulSoup
from datetime import datetime


url = 'https://www.aisweb.aer.mil.br/?i=aerodromos&p=sol'
today = datetime.now().date().strftime('%d/%m/%Y')


def get_search_value():
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')
    return soup.find('input', {'name': 'busca'})['value']


def get_sunrise_and_sunset(icaocode='SBMT', date=today):
    data = {
        'icaocode': icaocode,
        'dt_i': date,
        'dt_f': date,
        'busca': get_search_value()
    }
    r_post = requests.post(url, data=data)
    soup = BeautifulSoup(r_post.content, 'html.parser')
    tds = soup.find_all('tr')[1:2][0].find_all('td')
    sr, st = (td.text for td in tds if td.text.endswith('UTC'))
    return sr, st


sunrise, sunset = get_sunrise_and_sunset()
