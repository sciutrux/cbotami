# Chatbot

Chatbot functionalities using ChatterBot dialog engine (https://github.com/gunthercox/ChatterBot.)

## Requirements

Python 3, pip, chatterbot, chatterbot-corpus, spacy

Created originally with chatterbot version 1.0.8.

## Use instructions

chatbot.py

Configuration file for language independency, example configuration using SQLite database. Internal / external terminal input / output only. Call me Amelia! (or what ever you like ...)

Use included list trainer or corpus trainer by changing configuration 
"trainer": "none" -> "list" or "corpus"

learning_chatbot.py

Train chatbot from Chatterbot Corpus, create SQLite database.

run_chatbot.py

Run basic chatbot from SQLite database - read_only.

export_chatbot.py

Export training from SQLite database to JSON export file.

import_chatbot.py

Import training from YAML or JSON export file to SQLite database.

feedback_learning_chatbot.py

Feedback learning chatbot using SQLite database.