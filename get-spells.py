import csv

import requests
from bs4 import BeautifulSoup

import secrets

# TODO: cache web results

search_page = 'https://www.dndbeyond.com/spells'
sources = [44, 4, 2, 80, 13, 67, 27]


def generate_search_url(filters):
    url = search_page + '?sort=level'
    for source in sources:
        url += f'&filter-source={source}'
    return url + filters


all_owned = generate_search_url('')
cleric_cantrips = generate_search_url('?filter-class=2&filter-level=0')
level_1 = generate_search_url('?filter-level=1')


def generate_spell_cards(search_list):

    all_spells = []
    url_list = retrieve_spell_list(search_list)

    for page in url_list:
        try:
            spell_details = retrieve_spell_details(page)
        except AttributeError:
            print('Inaccessible: ' + page)
        else:
            all_spells.append(spell_details)

    write_to_csv(all_spells)


def init_soup(url):
    headers = secrets.headers
    webpage = requests.get(url, headers=headers)
    soup = BeautifulSoup(webpage.content, 'html.parser')
    print('Webpage accessed: ' + url)
    return soup


def retrieve_spell_list(base_url):
    print('Retrieving spell list...')
    spell_url_list = []

    soup = init_soup(base_url)
    footer_elements = soup.find('div', class_='listing-footer').find_all('li')
    if len(footer_elements) > 0:
        pages = int(footer_elements[len(footer_elements) - 2].text)
    else:
        pages = 1

    for page in range(pages):

        soup = init_soup(base_url + '&page=' + str(page + 1))
        listing_body = soup.find('div', class_='listing-body')
        links = listing_body.find_all('a')
        for link in links:
            url = 'https://www.dndbeyond.com' + link.get('href')
            spell_url_list.append(url)

    print('Spell list retrieved')
    return spell_url_list


def retrieve_spell_details(spell_url):
    soup = init_soup(spell_url)

    name = soup.find('h1', class_='page-title').text.strip()
    statblock = soup.find('div', class_='ddb-statblock ddb-statblock-spell')

    level = statblock\
        .find('div', class_='ddb-statblock-item ddb-statblock-item-level')\
        .find('div', class_='ddb-statblock-item-value').text.strip()
    duration = ''
    for element in statblock\
            .find('div', class_='ddb-statblock-item ddb-statblock-item-duration')\
            .find('div', class_='ddb-statblock-item-value'):
        if element.text.strip() == 'Concentration':
            name += ' (Concentration)'
        else:
            duration += element.text.strip()
    casting_time = ''
    for element in statblock\
            .find('div', class_='ddb-statblock-item ddb-statblock-item-casting-time')\
            .find('div', class_='ddb-statblock-item-value'):
        if element.text.strip() == 'Ritual':
            name += ' (Ritual)'
        else:
            casting_time += element.text.strip()
    range_area = ''
    for element in statblock\
            .find('div', class_='ddb-statblock-item ddb-statblock-item-range-area')\
            .find('div', class_='ddb-statblock-item-value'):
        range_area += element.text.strip()
    range_area = range_area.replace('(', ' (').replace(' )', ')')

    components = statblock\
        .find('div', class_='ddb-statblock-item ddb-statblock-item-components')\
        .find('div', class_='ddb-statblock-item-value').text.strip()
    school = statblock\
        .find('div', class_='ddb-statblock-item ddb-statblock-item-school')\
        .find('div', class_='ddb-statblock-item-value').text.strip()
    attack_save = statblock\
        .find('div', class_='ddb-statblock-item ddb-statblock-item-attack-save')\
        .find('div', class_='ddb-statblock-item-value').text.strip()
    damage_effect = statblock\
        .find('div', class_='ddb-statblock-item ddb-statblock-item-damage-effect')\
        .find('div', class_='ddb-statblock-item-value').text.strip()

    description = ''
    for element in soup.find('div', class_='more-info-content'):
        if element.text.strip() != '':
            description += element.text.strip() + ' \n'
    description = description.replace('At Higher Levels. ', 'At Higher Levels: ')

    tags = ''
    for tag in soup.find('p', class_='tags spell-tags')\
            .findAll('span', class_='tag spell-tag'):
        if tags != '':
            tags += ', '
        tags += tag.text

    availability = ''
    for element in soup.find('p', class_='tags available-for')\
            .findAll('span', class_='tag class-tag'):
        if availability != '':
            availability += ', '
        availability += element.text.strip()

    source = soup.find('p', class_='source spell-source').text.strip()

    spell_details = {
        'URL': spell_url,
        'Name': name,
        'Level': level,
        'Casting Time': casting_time,
        'Range/Area': range_area,
        'Components': components,
        'Duration': duration,
        'School': school,
        'Attack/Save': attack_save,
        'Damage/Effect': damage_effect,
        'Description': description,
        'Tags': tags,
        'Availability': availability,
        'Source': source
    }

    return spell_details


def write_to_csv(spell_list):
    with open('spell-data.csv', 'w', newline='', encoding='utf-8') as f:
        fieldnames = spell_list[0].keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(spell_list)


generate_spell_cards(all_owned)
