from re import match, I
from requests import get as requests_get
from bs4 import BeautifulSoup
from utils import *

main_cite = 'http://www.mosopen.ru/streets'
alphabet = ('А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й',
            'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф',
            'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я')
digits = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')


def get_a_tags(link):
    res = requests_get(link)
    soup = BeautifulSoup(res.text, 'html.parser')
    return soup.find_all('a')


def get_regions():
    a_tags = get_a_tags(main_cite)
    regions = {}
    for t in a_tags:
        region_link = t.get('href')
        if 'region/' in region_link:
            region_name = t.get_text()
            print('***{}***'.format(region_name))
            if region_name not in regions:
                regions[region_name] = get_streets(region_link)
    return regions


def get_streets(region_link):
    a_tags = get_a_tags(region_link)
    streets = {}
    for t in a_tags:
        street_link = t.get('href')
        if 'street/' in street_link:
            street_parser = t.get_text().replace(',', '').split()
            street_type = street_parser[-1]
            street_name = ' '.join(street_parser[:-1])
            street_tuple = (street_name, street_type)
            streets[street_tuple] = get_houses(street_link)
    return streets


def get_houses(street_link):
    a_tags = get_a_tags(street_link)
    houses = []
    for t in a_tags:
        house_link = t.get('href')
        if 'address' in house_link:
            houses.append(house_parser(t.get_text()))
    return houses


def house_parser(house_text):
    full_text = house_text.replace('\xa0', ' ')
    parser = full_text.split(' ')
    if not parser[0].startswith(digits):
        house = {'ind': None}
        attributes = parser
    else:
        house = index_parser(parser[0])
        attributes = parser[1:]
    for attribute in attributes:
        house[attribute[0]] = attribute[1:]
    house['ft'] = full_text
    return house

def index_parser(index_text):
    index = {}
    parser = index_text.split('/')
    if len(parser) > 1:
        index['/'] = parser[1]
    items = match(r"([0-9]+)([А-Я]*)", parser[0], I).groups()
    index['ind'] = items[0]
    if items[1] != '':
        index['lit'] = items[1]
    return index
