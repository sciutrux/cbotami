#!/usr/bin/env python
# -*- coding: utf-8 -*-
from chatterbot import ChatBot
from chatterbot.conversation import Statement
from chatterbot.comparisons import LevenshteinDistance, JaccardSimilarity
from chatterbot.response_selection import get_first_response, get_most_frequent_response
from chatterbot.filters import get_recent_repeated_responses

import os.path

"""
Learn from feedback.
Base from ChatterBot/examples/learning_feedback_example.py
"""

import logging
# logging.basicConfig(level=logging.ERROR)
logging.basicConfig(level=logging.INFO)

print('Run feedback learning chatbot using SQLite database')

database_file = input('SQLite database: ')
if '.sqlite3' not in database_file:
    database_file = database_file + '.sqlite3'

if not os.path.isfile('./' + database_file):
    logging.error("* Database file %s not found", database_file)
    exit(1)

# storageAdapter = input('storageAdapter: ')
storageAdapter = 'SQLStorageAdapter'

bot = ChatBot(
    'Feedback Learning Bot',
    storage_adapter = 'chatterbot.storage.' + storageAdapter,
    database_uri = "sqlite:///" + database_file,
    preprocessors = [
        'chatterbot.preprocessors.clean_whitespace'
    ],
    logic_adapters = [
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, but I do not understand.',
            'maximum_similarity_threshold': 0.90
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
)

def get_feedback():

    text = input()

    if 'y' in text.lower():
        return True
    elif 'n' in text.lower():
        return False
    else:
        print('Please type either "y = Yes" or "n = No"')
        return get_feedback()


print('Hello. Type something to begin ...')

while True:
    try:
        input_statement = Statement(text=input())
        response = bot.generate_response(
            input_statement
        )

        print('\n Is "{}" a coherent response to "{}" (y/n)? \n'.format(
            response.text,
            input_statement.text
        ))
        if get_feedback() is False:
            print('please input the correct one')
            correct_response = Statement(text=input())
            bot.learn_response(correct_response, input_statement)
            print('Responses added to bot!')

    # Press ctrl-c or ctrl-d on the keyboard to exit
    except (KeyboardInterrupt, EOFError, SystemExit):
        break