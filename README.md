# K-Learn: Discord Korean Language Learning Bot

<img src="https://github.com/warm-oats/dictionary-bot/blob/main/src/assets/k_learn_pfp.png" width="64" align="left"></img>
K-Learn is a Korean language learning bot that helps you learn Korean more efficiently. It combines different language learning tools into one to make your life easier. It can translate Korean sentences, highlighting and extracting parts of speech from them. It even features a robust flashcard system to help you save your vocabulary! K-Learn utilizes tools such as ChatGPT, KoNLPy NLP library, and the Merriam-Webster dictionary.

## Invite K-Learn

[Invite K-Learn to your server!](https://discord.com/oauth2/authorize?client_id=1427409639439466547&permissions=277025446912&integration_type=0&scope=bot)

## Features

### English Dictionary

Defines English words using the Merriam-Webster dictionary API.

| Command | Description |
| --- | --- |
|`define <word>`|Define an English word|

### Korean Parts of Speech Extraction and Translation

Given a Korean word, phrase, or sentence, extracts all parts of speech from it, translating it to English, and optionally color-codes all verbs, nouns, and adjectives in that Korean word, phrase, or sentence.

| Command | Description |
| --- | --- |
|`extract-pos <sentence> <(optional) colorize>`|Extracts Korean parts of speech|

### Flashcard System

A robust flashcard system as a studying tool to save and manage vocabulary. A flashcard is double-sided: front and back. Users can create decks and flashcards, and modify them with full CRUD functionality. 

| Commands | Description |
| --- | --- |
|`create-deck <deck_name>`|Create a flashcard deck|
|`delete-deck <deck_name>`|Delete a flashcard deck|
|`update-deck-name <new_deck_name> <deck_name`|Update a deck's name|
|`get-deck-list`|Get names of all decks created by user|
|`study-deck <deck_name>`|Fetch deck's flashcards to study|
|`add-flashcard <deck_name> <flashcard_front> <flashcard_back>`|Create a flashcard|
|`delete-flashcard <flashcard_name> <deck_name>`|Delete a flashcard|
|`update-flashcard <flashcard_name> <deck_name> <(optional) flashcard_front> <(optional) flashcard_back>`|Update a flashcard|

### Miscellaneous 

Utility commands for miscellaneous use

| Command | Description |
| --- | --- |
|`ping`|Check bot response time (ping)|


