# GlossyBot
*This is a student project for MIPT course "
Computer network architecture".*

### This Telegram Bot provides english dictionary with different information:

1. Definitions 
2. Pronunciation (transcription)
3. Parts fo speech
4. Synonyms
5. Antonyms 
6. Examples 

To interact with GlossyBot use [Link](https://t.me/NandCBot)

### How to install and run GlossyBot local

1. Clone the repository: `git clone https://github.com/Bordoglor/glossy-bot.git`
2. Install libraries via command: `pip install -r requirements.txt`
4. Run with command: `python run.py TOKEN HOST KEY`
   - TOKEN: a unique telegram bot token needed for connection with Telegram server
   - HOST and KEY: unique identifiers needed for connection with WordsApi

### More about GlossyBot development

This bot works with API of [WordsAPI](https://www.wordsapi.com/).

The bot uses and develops local database Cache to answer users' requests.
If the word not in the Cache, bot makes the request to [WordsAPI](https://www.wordsapi.com/) to get words info and add it to the Cache.

GlossyBot supports independent work with multiple users.
