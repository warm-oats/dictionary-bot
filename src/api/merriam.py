import os
import requests
from dotenv import load_dotenv

class MerriamAPIManager():
    def __init__(self):
        load_dotenv()
        MerriamAPIManager.MERRIAM_API = os.getenv('DICTIONARY_API')

    def request_json(self, word):
        dict_response = requests.get(f"https://dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={MerriamAPIManager.MERRIAM_API}")

        return dict_response.json()