#!/usr/bin/env python
# -*- coding: utf-8 -*-
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

import os.path

import logging
# logging.basicConfig(level=logging.ERROR)
logging.basicConfig(level=logging.INFO)

print('Import training from YAML or JSON export file to SQLite database')

import_file = input('Import file: ')
if not os.path.isfile('./' + import_file):
    logging.error("* Import file %s not found", import_file)
    exit(1)

database_file = input('SQLite database: ')
if '.sqlite3' not in database_file:
    database_file = database_file + '.sqlite3'

# storageAdapter = input('storageAdapter: ')
storageAdapter = 'SQLStorageAdapter'

bot = ChatBot(
    'Import Bot',
    storage_adapter = 'chatterbot.storage.' + storageAdapter,
    database_uri = "sqlite:///" + database_file)

trainer = ChatterBotCorpusTrainer(bot)

trainer.train(
   "./" + import_file
)

print('Import file ' + import_file + ' imported into ' + database_file)