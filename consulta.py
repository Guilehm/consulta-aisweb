import requests

from bs4 import BeautifulSoup
from collections import namedtuple
from datetime import datetime


today = datetime.now().date().strftime('%d/%m/%Y')


def get_search_value():
    url = 'https://www.aisweb.aer.mil.br/?i=aerodromos&p=sol'
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')
    return soup.find('input', {'name': 'busca'})['value']


def get_sunrise_and_sunset(icaocode='SBJD', date=today):
    url = 'https://www.aisweb.aer.mil.br/?i=aerodromos&p=sol'
    data = {
        'icaocode': icaocode,
        'dt_i': date,
        'dt_f': date,
        'busca': get_search_value(),
    }
    soup = BeautifulSoup(requests.post(url, data=data).content, 'html.parser')
    tds = soup.find_all('tr')[1:2][0].find_all('td')
    sr, st = (td.text for td in tds if td.text.endswith('UTC'))
    return sr, st


def get_letters(icaocode='SBJD'):
    Letter = namedtuple('Carta', 'local type code date')
    url = 'https://www.aisweb.aer.mil.br/?i=cartas'
    data = {
        'icaocode': icaocode,
        'tipo': 0,
        'carta': '',
        'pe': 0,
        'uso': 0,
        'busca': get_search_value(),
    }
    soup = BeautifulSoup(requests.post(url, data=data).content, 'html.parser')
    trs = soup.find('tbody').find_all('tr')
    letters = []
    for tr in trs:
        tr_data = [td.text.strip() for td in tr.find_all('td')]
        letters.append(Letter(tr_data[1], tr_data[2], tr_data[3], tr_data[4]))
    return letters


def get_temp_data(icaocode='SBJD', tipo='N'):
    url = 'https://www.aisweb.aer.mil.br/?i=notam'
    data = {
        'icaocode': icaocode,
        'tipo': tipo,
        'busca': 'localidade',
    }
    soup = BeautifulSoup(requests.post(url, data=data).content, 'html.parser')
    divs = soup.find_all('div', {'class': 'notam'})
    return [div.find('div').text for div in divs]


icao_code = input('Digite o código ICAO: ') or 'SBJD'

letters = get_letters(icaocode=icao_code)
print('CARTAS'.center(46))
print('CARTA'.ljust(30) + 'TIPO'.ljust(7) + 'DATA'.ljust(10))
print('-' * 46)
for letter in letters:
    print(f'{letter.code}'.ljust(30) + f'{letter.type}'.ljust(7) + f'{letter.date}'.ljust(10))


sunrise, sunset = get_sunrise_and_sunset(icaocode=icao_code)
print('\n')
print('NASCER / POR DO SOL'.center(30))
print('-' * 30)
print('NASCER DO SOL'.ljust(20), sunrise)
print('POR DO SOL'.ljust(20), sunset)


print('\n')
print('TAF / METAR'.center(50))
print('-' * 50)
temp_data = get_temp_data(icaocode=icao_code)
for number, data in enumerate(temp_data, 1):
    print(f'{number} - {data}')
