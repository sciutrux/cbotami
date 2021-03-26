# Chatbot

Chatbot functionalities using ChatterBot dialog engine (https://github.com/gunthercox/ChatterBot.)

## Requirements

Python 3, pip, chatterbot, chatterbot-corpus, spacy

Created originally with chatterbot version 1.0.8.

## Use instructions

__chatbot.py__

Configuration file for language independency, example configuration using SQLite database. Internal / external terminal input / output only. Call me Amelia! (or what ever you like ...)

Use included list trainer or corpus trainer by changing configuration 
"trainer": "none" -> "list" or "corpus"

__learning_chatbot.py__

Train chatbot from Chatterbot Corpus, create SQLite database.

__run_chatbot.py__

Run basic chatbot from SQLite database - read_only.

__export_chatbot.py__

Export training from SQLite database to JSON export file.

__import_chatbot.py__

Import training from YAML or JSON export file to SQLite database.

__feedback_learning_chatbot.py__

Feedback learning chatbot using SQLite database.

Notice: not updated to work with new configuration - depreciated

__cbotami.py__

Class implementation of a chatbot.

__run_cbotami.py__

Run chatbot class implementation using SQLite database.

__teach_cbotami.py__

Feedback learning using cbotami class and defined SQLite DB.
Create conversation from sentence and response similarly as with
Chatterbot Corpus trainer, including POS tagging.

## Notice

Includes own logic adapter and some function overrides.
