#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from collections import namedtuple

from cbotami import CBotAmI

from chatterbot.conversation import Statement

def get_feedback():

    text = input()

    if 'y' in text.lower():
        return True
    elif 'n' in text.lower():
        return False
    else:
        print('Please type either "y = Yes" or "n = No"')
        return get_feedback()

# Read configuration file
with open("configuration.json") as json_file:
        config_data = json.load(json_file, object_hook = lambda d: namedtuple('X', d.keys())(*d.values()))

read_only = False
if config_data.read_only: 
    read_only = True

import logging
logging.basicConfig(level = logging.ERROR)
# logging.basicConfig(level = logging.INFO)
# logging.basicConfig(level = logging.DEBUG)

# SQLAlchemy DEBUG logging - displays connection handling, SQL statements
# logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
# logging.getLogger('sqlalchemy.pool').setLevel(logging.DEBUG)

bot = CBotAmI(config_data)

name = input(config_data.bot_name + ': ' + config_data.name_inquiry + ' ')
print(config_data.bot_name + ': ' + config_data.initial_greeting)

while True:
    try:
        sentence = input(name + ': ')
        response = bot.get_response(sentence)
        print(config_data.bot_name + ': ' + response.text)

        print('\n Is "{}" a coherent response to "{}" (y/n)? \n'.format(
            response.text,
            sentence
        ))

        if get_feedback() is False:

            print('\n Please input the correct one \n')

            correct_response = Statement(text=input(config_data.bot_name + ': '))
            bot.learn_response(correct_response, sentence)

            print('\n Responses added')
            print(' Please continue with next sentence \n')
        else:
            print('\n Please continue with next sentence \n')

    except (KeyboardInterrupt, EOFError, SystemExit):
        break