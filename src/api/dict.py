import os
import requests
from dotenv import load_dotenv

class DictAPI():
    def __init__(self):
        load_dotenv()
        DictAPI.API_KEY = os.getenv('DICTIONARY_API')

    def request_json(self, word):
        response = requests.get(f"https://dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={DictAPI.API_KEY}")

        return response.json()