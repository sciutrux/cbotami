#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from collections import namedtuple

from cbotami import CBotAmI

import pyttsx3

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

# set up text-to-speech
tts_engine = pyttsx3.init()

tts_voices = tts_engine.getProperty('voices')
tts_engine.setProperty('voice', tts_voices[0].id)   # Microsoft Hazel Desktop - English (Great Britain)
tts_engine.setProperty('rate', 150)             # lower rate, default = 200

tts_engine.say(config_data.name_inquiry)
tts_engine.runAndWait()

name = input(config_data.bot_name + ': ' + config_data.name_inquiry + ' ')

print(config_data.bot_name + ': ' + config_data.initial_greeting)

tts_engine.say(config_data.initial_greeting)
tts_engine.runAndWait()

while True:
    try:
        sentence = input(name + ': ')
        response = bot.get_response(sentence)
        print(config_data.bot_name + ': ' + response.text)

        tts_engine.say(response.text)
        tts_engine.runAndWait()

    except (KeyboardInterrupt, EOFError, SystemExit):
        break