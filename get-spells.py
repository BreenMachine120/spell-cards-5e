import csv
import json

import requests

import secrets


spell_data_header = ['name', 'lvl_school', 'availability', 'casting_time', 'range_area',
                     'components', 'duration', 'description', 'upcasting', 'source']


def retrieve_last_message():
    headers = {
        'authorization': secrets.discord_auth_key
    }
    r = requests.get(f'https://discord.com/api/v9/channels/{secrets.avrae_channel_id}/messages', headers=headers)
    json_data = json.loads(r.text)

    msg_count = 0
    while json_data[msg_count]['author']['id'] != secrets.avrae_user_id:
        msg_count += 1

    return json_data[msg_count]


def format_spell_data(message):
    content = message['embeds'][0]

    name = content['title']
    lvl_school = content['description'].split('. ')[0].strip('*')
    availability = content['description'].split('. ')[1].strip('()*')
    casting_time = content['fields'][0]['value'].split('\n')[0].split(': ')[1]
    range_area = content['fields'][0]['value'].split('\n')[1].split(': ')[1]
    components = content['fields'][0]['value'].split('\n')[2].split(': ')[1]
    duration = content['fields'][0]['value'].split('\n')[3].split(': ')[1]
    description = content['fields'][1]['value']
    if len(content['fields']) > 2:
        upcasting = content['fields'][2]['value']
    else:
        upcasting = ''
    source = content['footer']['text'].split(' | ')[1]

    return [name, lvl_school, availability, casting_time, range_area,
            components, duration, description, upcasting, source]


with open('spell-data.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(spell_data_header)
    writer.writerow(format_spell_data(retrieve_last_message()))
