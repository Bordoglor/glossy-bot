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

    def __call__(self, word) -> tp.Optional[dict]:
        url = urljoin(URL, word)

        response = requests.request("GET", url, headers=headers)

        return response.json() if response.status_code == 200 else None
