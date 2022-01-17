import typing as tp
import requests

from urllib.parse import urljoin


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
