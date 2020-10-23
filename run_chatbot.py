#!/usr/bin/env python
# -*- coding: utf-8 -*-
from chatterbot import ChatBot

import os.path

import logging
logging.basicConfig(level=logging.ERROR)
# logging.basicConfig(level=logging.INFO)

print('Run chatbot from SQLite database - read_only')

database_file = input('SQLite database: ')
if '.sqlite3' not in database_file:
    database_file = database_file + '.sqlite3'

if not os.path.isfile('./' + database_file):
    logging.error("* Database file %s not found", database_file)
    exit(1)

# storageAdapter = input('storageAdapter: ')
storageAdapter = 'SQLStorageAdapter'

bot = ChatBot(
    'Basic Bot',
    storage_adapter = 'chatterbot.storage.' + storageAdapter,
    database_uri = "sqlite:///" + database_file,
    read_only = True)

# print('Begin')

while True:
    try:
        sentence = input()
        response = bot.get_response(sentence)
        print(response.text)

    except (KeyboardInterrupt, EOFError, SystemExit):
        break