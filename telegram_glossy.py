import typing as tp

from telebot import types
import telebot

class TelegramGlossy:
    def __init__(self, token: str, dictionary):
        self.bot = telebot.TeleBot(token)
        self.history = {}
        self.dictionary = dictionary

        self.bot.set_update_listener(lambda messages: self._handle_messages(messages))
        self.bot.register_callback_query_handler(lambda reply: self._query_handler(reply), lambda reply: True)

    def _query_handler(self, reply):
        command, word = reply.data.split(":")
        self.bot.send_message(reply.message.chat.id, "The word was " + word + "\nAnd command was " + command)

        # reply = None
        # if command == "syn":
        #     reply = self._get_synonyms(word)
        # if command == not ""...
        #
        #

    def _handle_messages(self, messages):
        for message in messages:
            self._handle_message(message)

    def _handle_message(self, message):
        print(message)

        if message.content_type != "text":
            self.bot.send_message(message.chat.id, "Only text content is allowed")

        word = message.text

        keyboard = types.InlineKeyboardMarkup(row_width=2)
        buttons = [
            types.InlineKeyboardButton(text='Значение', callback_data='info:' + word),
            types.InlineKeyboardButton(text='Произношение', callback_data='pro:' + word),
            types.InlineKeyboardButton(text="Часть речи", callback_data="part:" + word),
            types.InlineKeyboardButton(text="Синонимы", callback_data="syn:" + word),
            types.InlineKeyboardButton(text="Антонимы", callback_data="ant:" + word),
            types.InlineKeyboardButton(text="Примеры", callback_data="exm:" + word)
        ]

        keyboard.add(*buttons)

        self.bot.send_message(message.chat.id, text="Выбирай", reply_markup=keyboard)

    def _make_keyboard(self, word: str) -> types.InlineKeyboardMarkup:
        pass

    def _get_synonyms(self, word: str) -> str:
        pass

    def run(self):
        self.bot.infinity_polling()
