#!/usr/bin/env python
# -*- coding: utf-8 -*-
from chatterbot import ChatBot
from chatterbot.trainers import Trainer

import os.path

import logging
# logging.basicConfig(level=logging.ERROR)
logging.basicConfig(level=logging.INFO)

print('Export training from SQLite database to JSON export file')

database_file = input('SQLite database: ')
if '.sqlite3' not in database_file:
    database_file = database_file + '.sqlite3'

if not os.path.isfile('./' + database_file):
    logging.error("* Database file %s not found", database_file)
    exit(1)

# storageAdapter = input('storageAdapter: ')
storageAdapter = 'SQLStorageAdapter'

bot = ChatBot(
    'Export Bot',
    storage_adapter = 'chatterbot.storage.' + storageAdapter,
    database_uri = "sqlite:///" + database_file)

trainer = Trainer(bot)

export_file = './' + database_file[:database_file.find('.sqlite3')] + '.json'
trainer.export_for_training(export_file)

print('SQLite database ' + database_file + ' exported into ' + export_file)