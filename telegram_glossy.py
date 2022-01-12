import typing as tp

import telebot


class ClientStatus:
    pass


class TelegramGlossy:
    def __init__(self, token: str, dictionary):
        self.bot = telebot.TeleBot(token)
        self.history = {}
        self.dictionary = dictionary

        self.clients: tp.Mapping[str, ClientStatus] = dict()

    def run(self):
        self.bot.infinity_polling()
