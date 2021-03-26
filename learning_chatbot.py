#!/usr/bin/env python
# -*- coding: utf-8 -*-
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer

# override Chatterbot PosLemmaTagger
from tagging import CustomPosLemmaTagger

import os.path

import logging
# logging.basicConfig(level=logging.ERROR)
logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.DEBUG)

print('Train chatbot from Chatterbot Corpus')

database_file = input('SQLite database: ')
if '.sqlite3' not in database_file:
    database_file = database_file + '.sqlite3'

if os.path.isfile('./' + database_file):
    logging.error("* Database file %s already exists", database_file)
    exit(1)

# storageAdapter = input('storageAdapter: ')
storageAdapter = 'SQLStorageAdapter'

bot = ChatBot(
    'Learning Bot',
    storage_adapter = 'chatterbot.storage.' + storageAdapter,
    database_uri = "sqlite:///" + database_file)

# override Chatterbot PosLemmaTagger get_bigram_pair_string function
# POS tags were not suitable for how conversations are processed
custom_tagger = CustomPosLemmaTagger()
bot.storage.tagger.get_bigram_pair_string = custom_tagger.get_bigram_pair_string
trainer = ChatterBotCorpusTrainer(bot)

trainer.train(
    'chatterbot.corpus.english.ai',
    'chatterbot.corpus.english.botprofile',
    'chatterbot.corpus.english.computers',
    'chatterbot.corpus.english.conversations',
    'chatterbot.corpus.english.emotion',
    'chatterbot.corpus.english.greetings',
    # 'chatterbot.corpus.english'
)

print('SQLite database ' + database_file + ' created')