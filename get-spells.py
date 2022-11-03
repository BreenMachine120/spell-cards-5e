import requests
from bs4 import BeautifulSoup

import secrets


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
            d = {'URL': 'https://www.dndbeyond.com' + link.get('href')}     # should a dict be used here?
            spell_url_list.append(d)

    print('Spell list retrieved')
    return spell_url_list

    # with open('spell-data.csv', 'w', newline='') as f:    # move to different function
    #     w = csv.DictWriter(f, ['URL'])
    #     w.writeheader()
    #     w.writerows(spell_url_list)


def retrieve_spell_details(spell_url):  # redo this garbage entirely
    soup = init_soup(spell_url)
    spell_name = soup.find('h1', class_='page-title').text.strip()

    spell_level, spell_casting_time, spell_range_area, spell_components, spell_duration, spell_school, spell_attack_save, spell_damage_effect = '', '', '', '', '', '', '', ''
    statblock = soup.find('div', class_='ddb-statblock ddb-statblock-spell')
    for element in statblock.find('div', class_='ddb-statblock-item ddb-statblock-item-level').find('div', class_='ddb-statblock-item-value'): spell_level+= element.text.strip()
    for element in statblock.find('div', class_='ddb-statblock-item ddb-statblock-item-casting-time').find('div', class_='ddb-statblock-item-value'): spell_casting_time += element.text.strip()
    for element in statblock.find('div', class_='ddb-statblock-item ddb-statblock-item-range-area').find('div', class_='ddb-statblock-item-value'): spell_range_area += element.text.strip()
    for element in statblock.find('div', class_='ddb-statblock-item ddb-statblock-item-components').find('div', class_='ddb-statblock-item-value'): spell_components += element.text.strip()
    for element in statblock.find('div', class_='ddb-statblock-item ddb-statblock-item-duration').find('div', class_='ddb-statblock-item-value'): spell_duration += element.text.strip()
    for element in statblock.find('div', class_='ddb-statblock-item ddb-statblock-item-school').find('div', class_='ddb-statblock-item-value'): spell_school += element.text.strip()
    for element in statblock.find('div', class_='ddb-statblock-item ddb-statblock-item-attack-save').find('div', class_='ddb-statblock-item-value'): spell_attack_save += element.text.strip()
    for element in statblock.find('div', class_='ddb-statblock-item ddb-statblock-item-damage-effect').find('div', class_='ddb-statblock-item-value'): spell_damage_effect += element.text.strip()

    spell_description = ''
    for element in soup.find('div', class_='more-info-content'): spell_description += element.text.strip()

    print(spell_name, spell_level, spell_casting_time, spell_range_area, spell_components, spell_duration, spell_school, spell_attack_save, spell_damage_effect)
    print(spell_description)


search_url1 = 'https://www.dndbeyond.com/spells?filter-class=0&filter-search=&filter-source=1&filter-source=4&filter-source=2&filter-source=80&filter-source=13&filter-source=67&filter-source=27&sort=level'
search_url2 = 'https://www.dndbeyond.com/spells?filter-class=0&filter-class=2&filter-search=&filter-level=0&filter-verbal=&filter-somatic=&filter-material=&filter-concentration=&filter-ritual=&filter-sub-class='
retrieve_spell_list(search_url2)
# retrieve_spell_details('https://www.dndbeyond.com/spells/fireball')
