import typing as tp

from telebot import types
import telebot

class TelegramGlossy:
    def __init__(self, token: str, dictionary):
        self.bot = telebot.TeleBot(token)
        self.dictionary = dictionary

        self.bot.set_update_listener(lambda messages: self._handle_messages(messages))
        self.bot.register_callback_query_handler(lambda reply: self._query_handler(reply), lambda reply: True)

    def _query_handler(self, reply):
        command, word = reply.data.split(":")

        answer = None
        if command == "info":
            answer = self._get_definitions(word)
        if command == "pro":
            answer = self._get_pronunciation(word)
        if command == "part":
            answer = self._get_part_of_speech(word)
        if command == "syn":
            answer = self._get_synonyms(word)
        if command == "ant":
            answer = self._get_antonyms(word)
        if command == "exm":
            answer = self._get_examples(word)
        keyboard = self._make_keyboard(word)

        self.bot.send_message(reply.message.chat.id, answer, reply_markup=keyboard, parse_mode='Markdown')

    def _handle_messages(self, messages):
        for message in messages:
            self._handle_message(message)

    def _handle_message(self, message):
        # print(message)
        if message.content_type != "text":
            self.bot.send_message(message.chat.id, "Only text content is allowed")
            return

        if not self.dictionary._try_fetch(message.text.lower()):
            print("here")
            self.bot.send_message(message.chat.id, "No such word")
            return

        keyboard = self._make_keyboard(message.text.lower())

        self.bot.send_message(message.chat.id, text="Choose the option!", reply_markup=keyboard)

    def _make_keyboard(self, word: str) -> types.InlineKeyboardMarkup:
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        buttons = [
            types.InlineKeyboardButton(text='Definitions', callback_data='info:' + word),
            types.InlineKeyboardButton(text='Pronunciation', callback_data='pro:' + word),
            types.InlineKeyboardButton(text="Parts of speech", callback_data="part:" + word),
            types.InlineKeyboardButton(text="Synonyms", callback_data="syn:" + word),
            types.InlineKeyboardButton(text="Antonyms", callback_data="ant:" + word),
            types.InlineKeyboardButton(text="Examples", callback_data="exm:" + word)
        ]

        keyboard.add(*buttons)
        return keyboard

    def _get_definitions(self, word: str) -> str:
        if self.dictionary.definition(word) == "":
            return f'*{word.upper()}*' + '\n'+"No information about definition"
        answer = f'*{word.upper()}*'+'\nDefinitions:'+'\n⦁ '+'\n⦁ '.join(self.dictionary.definition(word))
        return answer

    def _get_pronunciation(self, word: str) -> str:
        if self.dictionary.pronunciation(word) == "":
            return f'*{word.upper()}*' + '\n'+"No information about pronunciation"
        answer = f'*{word.upper()}*' + '\nPronunciation:'+ '\n⦁ '+self.dictionary.pronunciation(word)
        return answer

    def _get_part_of_speech(self, word: str) -> str:
        if self.dictionary.part_of_speech(word) == "":
            return f'*{word.upper()}*' + '\n'+"No information about part of speech"
        answer = f'*{word.upper()}*' + '\nParts of speech:' + '\n⦁ ' + '\n⦁ '.join(self.dictionary.part_of_speech(word))
        return answer

    def _get_synonyms(self, word: str) -> str:
        if self.dictionary.synonyms(word) == "":
            return f'*{word.upper()}*' + '\n'+"No information about synonyms"
        answer = f'*{word.upper()}*' + '\nSynonyms:' + '\n⦁ ' + '\n⦁ '.join(self.dictionary.synonyms(word))
        return answer

    def _get_antonyms(self, word: str) -> str:
        if self.dictionary.antonyms(word) == "":
            return f'*{word.upper()}*' + '\n'+"No information about antonyms"
        answer = f'*{word.upper()}*' + '\nAntonyms:' + '\n⦁ ' + '\n⦁ '.join(self.dictionary.antonyms(word))
        return answer

    def _get_examples(self, word: str) -> str:
        if self.dictionary.examples(word) == "":
            return f'*{word.upper()}*' + '\n'+"No information about examples"
        answer = f'*{word.upper()}*'+ '\nExamples:' + '\n⦁ ' + '\n⦁ '.join(self.dictionary.examples(word))
        return answer

    def run(self):
        self.bot.infinity_polling()
