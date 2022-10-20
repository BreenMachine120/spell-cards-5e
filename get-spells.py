import csv
import json
from time import sleep

import requests

import secrets

header = {'authorization': secrets.discord_auth_key}
url = f'https://discord.com/api/v9/channels/{secrets.avrae_channel_id}/messages'
spell_data_header = ['name', 'lvl_school', 'availability', 'casting_time', 'range_area',
                     'components', 'duration', 'description', 'source']


def send_bot_command(_spell):
    payload = {
        'content': f'!spell {_spell}'
    }
    r = requests.post(url, data=payload, headers=header)
    return 0


def retrieve_spell_data():
    r = requests.get(url, headers=header)
    json_data = json.loads(r.text)

    msg_count = 0
    while json_data[msg_count]['author']['id'] == secrets.avrae_user_id:
        msg_count += 1

    name = json_data[msg_count - 1]['embeds'][0]['title']
    lvl_school = json_data[msg_count - 1]['embeds'][0]['description'].split('. ')[0].strip('*')
    availability = json_data[msg_count - 1]['embeds'][0]['description'].split('. ')[1].strip('()*')
    casting_time = json_data[msg_count - 1]['embeds'][0]['fields'][0]['value'].split('\n')[0].split(': ')[1]
    range_area = json_data[msg_count - 1]['embeds'][0]['fields'][0]['value'].split('\n')[1].split(': ')[1]
    components = json_data[msg_count - 1]['embeds'][0]['fields'][0]['value'].split('\n')[2].split(': ')[1]
    duration = json_data[msg_count - 1]['embeds'][0]['fields'][0]['value'].split('\n')[3].split(': ')[1]

    description = ''
    for msg in range(msg_count - 1, -1, -1):
        if msg == (msg_count - 1):
            description += json_data[msg]['embeds'][0]['fields'][1]['value']
        else:
            description += '\n' + json_data[msg]['embeds'][0]['description']
    description = description.replace('\n\n', '\n')
    if len(json_data[msg_count-1]['embeds'][0]['fields']) > 2:
        description += '\nAt Higher Levels: ' + json_data[msg_count-1]['embeds'][0]['fields'][2]['value']
    elif 'fields' in json_data[0]['embeds'][0]:
        if json_data[0]['embeds'][0]['fields'][0]['name'] == 'At Higher Levels':
            description += '\nAt Higher Levels: ' + json_data[0]['embeds'][0]['fields'][0]['value']

    source = json_data[0]['embeds'][0]['footer']['text'].split(' | ')[1]

    return [name, lvl_school, availability, casting_time, range_area,
            components, duration, description, source]


def write_to_csv(_spell_list):
    with open('spell-data.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(spell_data_header)
        for spell in _spell_list:
            send_bot_command(spell)
            sleep(1.5)
            try:
                writer.writerow(retrieve_spell_data())
            except:
                print("Exception occurred: " + spell)


write_to_csv(secrets.spell_list)
