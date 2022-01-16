import typing as tp
import requests

from urllib.parse import urljoin


# Класс, который позволяет получить информацию о слове, запрашивая информацию у сайта
# Также для уменьшения сетевого взаимодействия, класс имеет локальный кеш, в котором записаны уже полученные данные о словах.
class WordsApi:
    URL = "https://wordsapiv1.p.rapidapi.com/words/"

    def __init__(self, host, key):
        self.headers = {
            'x-rapidapi-host': host,
            'x-rapidapi-key': key
        }
        self.cache = dict()
        self.pro = dict()

    def definition(self, word) -> tp.Optional[list]:
        if not self.contains(word):
            return ""
        definitions = []
        for result in self.cache[word]:
            try:
                definitions.append(result["definition"].replace(f'{word.lower()}', f'*{word.lower()}*').capitalize())
            except:
                pass
        if len(definitions) == 0:
            return ""
        return definitions

    def pronunciation(self, word) -> tp.Optional[list]:
        if not self.contains(word):
            return ""
        if len(self.pro[word]) == 0:
            return ""
        return self.pro[word]

    def part_of_speech(self, word) -> tp.Optional[list]:
        if not self.contains(word):
            return ""
        parts = []
        for result in self.cache[word]:
            try:
                parts.append(result["partOfSpeech"].capitalize())
            except:
                pass
        if len(parts) == 0:
            return ""
        return set(parts)

    def synonyms(self, word) -> tp.Optional[list]:
        if not self.contains(word):
            return ""
        synonyms = []
        for result in self.cache[word]:
            if "synonyms" in result.keys():
                synonyms += result["synonyms"]
        if len(synonyms) == 0:
            return ""
        return set(synonyms)

    def antonyms(self, word) -> tp.Optional[list]:
        if not self.contains(word):
            return ""
        antonyms = []
        for result in self.cache[word]:
            if "antonyms" in result.keys():
                antonyms += result["antonyms"]
        if len(antonyms) == 0:
            return ""
        return set(antonyms)

    def examples(self, word) -> tp.Optional[list]:
        if not self.contains(word):
            return ""
        tmp_examples = []
        for result in self.cache[word]:
            if "examples" in result.keys():
                tmp_examples += result["examples"]
        examples = []
        for exm in tmp_examples:
            examples.append(exm.replace(f'{word.lower()}', f'*{word.lower()}*').capitalize())
        if len(examples) == 0:
            return ""
        return examples

    def contains(self, word) -> bool:
        # Если слова нет в ловкальной бд, то оно запрашивается с сайта. Если и там его нет, то возвращается false
        if word in self.cache:
            return True

        return self._try_fetch(word)

    def _try_fetch(self, word) -> bool:
        url = urljoin(self.URL, word)

        response = requests.request("GET", url, headers=self.headers)

        if response.status_code != 200:
            return False

        word_info = response.json()
        if "results" not in word_info or not word_info["results"]:
            return False

        self.cache[word] = word_info["results"]
        self.pro[word] = word_info["pronunciation"]["all"]
        return True


# class WordsApiLocal:
#
#     def __init__(self):
#         self.database = {"definitions": ["def line1 ", "def line2 ", "def line3 "],
#                          "pronunciation": "This is pronunciation of ",
#                          "synonyms": ["syn1", "syn2", "syn3"], "antonyms": ["ant1", "ant2", "ant3"],
#                          "partOfSpeech": ["part1", "part2", "part2", "part3"], "examples": ["ex1", "ex2", "ex3"]}
#
#         self.definitions = self._get_definitions(self.database)
#         self.pronunciation = self._get_pronunciation(self.database)
#         self.synonyms = self._get_synonyms(self.database)
#         self.antonyms = self._get_antonyms(self.database)
#         self.partOfSpeech = self._get_part_of_speech(self.database)
#         self.examples = self._get_examples(self.database)
#
#     def _get_definitions(self, database):
#         if "definitions" in database.keys():
#             return database["definitions"]
#
#     def _get_pronunciation(self, database):
#         if "pronunciation" in database.keys():
#             return database["pronunciation"]
#         else:
#             return None
#
#     def _get_synonyms(self, database):
#         if "synonyms" in database.keys():
#             return database["synonyms"]
#         else:
#             return None
#
#     def _get_antonyms(self, database):
#         if "antonyms" in database.keys():
#             return database["antonyms"]
#         else:
#             return None
#
#     def _get_part_of_speech(self, database):
#         if "partOfSpeech" in database.keys():
#             return set(database["partOfSpeech"])
#         else:
#             return None
#
#     def _get_examples(self, database):
#         if "examples" in database.keys():
#             return database["examples"]
#         else:
#             return None
