#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from collections import namedtuple

from cbotami import CBotAmI

# Read configuration file
with open("configuration.json") as json_file:
        config_data = json.load(json_file, object_hook = lambda d: namedtuple('X', d.keys())(*d.values()))

read_only = False
if config_data.read_only: 
    read_only = True

import logging
# logging.basicConfig(level = logging.ERROR)
logging.basicConfig(level = logging.INFO)
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

    except (KeyboardInterrupt, EOFError, SystemExit):
        break