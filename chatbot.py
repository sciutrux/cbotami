#!/usr/bin/env python
# -*- coding: utf-8 -*-
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from chatterbot.comparisons import LevenshteinDistance, JaccardSimilarity
from chatterbot.response_selection import get_first_response, get_most_frequent_response
from chatterbot.filters import get_recent_repeated_responses

import json
from collections import namedtuple

# Read configuration file
with open("configuration.json") as json_file:
        config_data = json.load(json_file, object_hook = lambda d: namedtuple('X', d.keys())(*d.values()))

read_only = False
if config_data.readOnly: 
    read_only = True

import logging
# logging.basicConfig(level = logging.ERROR)
logging.basicConfig(level = logging.INFO)

# Setup chatbot
bot = ChatBot(
    config_data.botName,
    storage_adapter = 'chatterbot.storage.' + config_data.storageAdapter,
    database_uri = config_data.database_uri,
    preprocessors = [
        'chatterbot.preprocessors.clean_whitespace'
    ],
    logic_adapters = [
        'chatterbot.logic.MathematicalEvaluation',
        # UnitConversion needs pint installed
        # 'chatterbot.logic.UnitConversion',
        # TimeLogic needs nltk installed
        # 'chatterbot.logic.TimeLogicAdapter',
        # 'chatterbot.logic.BestMatch',
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, but I do not understand.',
            'maximum_similarity_threshold': config_data.maximumSimilarityThreshold
        },
        {
            'import_path': 'chatterbot.logic.SpecificResponseAdapter',
            'input_text': config_data.specificResponseAdapter.input_text,
            'output_text': config_data.specificResponseAdapter.output_text
        },
    ],
    filters = [
        get_recent_repeated_responses
    ],
    # options for statement comparison:
    # - LevenshteinDistance
    # - SpacySimilarity
    # - JaccardSimilarity
    statement_comparison_function = JaccardSimilarity,
    # options for response selection:
    # - get_first_response
    # - get_most_frequent_response
    # - get_random_response
    response_selection_method = get_most_frequent_response,
    read_only = read_only
)

trainer_type = config_data.trainer_type

# Train chatbot with list, corpus or none
if trainer_type == 'list':

    trainer = ListTrainer(bot)

    conversation = [
        'Hi!',
        'Hello!',
        'How are you?',
        'I\'m fine, thank you',
        'Nice to meet you.',
        'Thank you.',
        'See you soon!'
    ]

    trainer.train(conversation)

elif trainer_type == 'corpus':

    # train from YAML or JSON data.
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

name = input(config_data.botName + ': ' + config_data.nameInquiry + ' ')
print(config_data.botName + ': ' + config_data.initialGreeting)

while True:
    try:
        sentence = input(name + ': ')
        response = bot.get_response(sentence)
        print(config_data.botName + ': ' + response.text)

    except (KeyboardInterrupt, EOFError, SystemExit):
        break
