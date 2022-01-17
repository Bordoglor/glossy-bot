import argparse
import typing as tp

from words_api import WordsApi
from telegram_glossy import TelegramGlossy


def parse_args():
    parser = argparse.ArgumentParser(description='Bot description')

    parser.add_argument('token', metavar='TOKEN', type=str,
                        help='telegram token')
    parser.add_argument('host', metavar='HOST', type=str,
                        help='words api host')
    parser.add_argument('key', metavar='KEY', type=str,
                        help='words api key')

    return parser.parse_args()


def run():
    args = parse_args()
    words_api = WordsApi(args.host, args.key)
    telegram_bot = TelegramGlossy(args.token, words_api)

    telegram_bot.run()


if __name__ == "__main__":
    run()
