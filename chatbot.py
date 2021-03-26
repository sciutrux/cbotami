#!/usr/bin/env python
# -*- coding: utf-8 -*-
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from chatterbot.comparisons import LevenshteinDistance, JaccardSimilarity
from chatterbot.response_selection import get_first_response, get_most_frequent_response
from chatterbot.filters import get_recent_repeated_responses

import json
from collections import namedtuple

# override Chatterbot PosLemmaTagger
from tagging import CustomPosLemmaTagger

# Read configuration file
with open("configuration.json") as json_file:
        config_data = json.load(json_file, object_hook = lambda d: namedtuple('X', d.keys())(*d.values()))

read_only = False
if config_data.read_only: 
            read_only = True

import logging
# logging.basicConfig(level = logging.ERROR)
logging.basicConfig(level = logging.INFO)

# Setup chatbot
bot = ChatBot(
    config_data.bot_name,
    storage_adapter = 'chatterbot.storage.' + config_data.storage_adapter,
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
            'import_path': 'chatterbot.logic.SpecificResponseAdapter',
            'input_text': config_data.specificResponseAdapter.input_text,
            'output_text': config_data.specificResponseAdapter.output_text
        },
        # {
        #     'import_path': 'chatterbot.logic.BestMatch',
        #     'default_response': config_data.bestMatch.default_response,
        #     'maximum_similarity_threshold': config_data.bestMatch.maximum_similarity_threshold
        # },
        {
            'import_path': 'best_match.CustomBestMatch',
            'default_response': config_data.bestMatch.default_response,
            'maximum_similarity_threshold': config_data.bestMatch.maximum_similarity_threshold
        }
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

# override Chatterbot PosLemmaTagger get_bigram_pair_string function
# POS tags were not suitable for how conversations are processed
custom_tagger = CustomPosLemmaTagger()
bot.storage.tagger.get_bigram_pair_string = custom_tagger.get_bigram_pair_string

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

name = input(config_data.bot_name + ': ' + config_data.name_inquiry + ' ')
print(config_data.bot_name + ': ' + config_data.initial_greeting)

while True:
    try:
        sentence = input(name + ': ')
        response = bot.get_response(sentence)
        print(config_data.bot_name + ': ' + response.text)

    except (KeyboardInterrupt, EOFError, SystemExit):
        break
