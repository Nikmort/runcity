from re import match, I
from requests import get as requests_get
from bs4 import BeautifulSoup

main_cite = 'http://www.mosopen.ru/streets'
digits = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')


# Извлечь из страницы a-тэги, содержащие определенные подстроки в ссылке.
# Возвращается генератор по этим тэгам.
def get_tags(link, keyword):
    res = requests_get(link)
    soup = BeautifulSoup(res.text, 'html.parser')
    for tag in soup.find_all('a'):
        if keyword in tag.get('href'):
            yield tag


# Получить словарь, где ключами будут районы Москвы,
# а значениями - словари с ключами-улицами (см. ниже).
def get_regions():
    regions = {}
    for tag in get_tags(main_cite, 'region/'):
        region_name = tag.get_text()
        print('***{}***'.format(region_name))
        if region_name not in regions:
            regions[region_name] = get_streets(tag.get('href'))
    return regions


# Получить словарь, где ключами улицы района,
# а значениями - списки домов (см. ниже).
# На вход подается ссылка на район.
def get_streets(region_link):
    streets = {}
    for tag in get_tags(region_link, 'street/'):
        street_parser = tag.get_text().replace(',', '').split()
        street_type = street_parser[-1]
        street_name = ' '.join(street_parser[:-1])
        street_tuple = (street_name, street_type)
        streets[street_tuple] = get_houses(tag.get('href'))
    return streets


# Получить список, элементами которого будет словари,
# характеризующий дом (см. ниже).
# На вход подается ссылка на улицу.
def get_houses(street_link):
    houses = []
    for tag in get_tags(street_link, 'address.'):
        houses.append(house_parser(tag.get_text()))
    return houses


# Получить словарь со следующими ключами:
# ind - номер дома,
# / - дробь,
# с - строение,
# к - корпус
# ft - полная адресная строка дома с сайта mosopen.
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


# Вспомогательная функция для парсинга номера дома.
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
