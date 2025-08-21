import os
import requests
from dotenv import load_dotenv

class DictAPIManager():

    load_dotenv()
    
    API_KEY = os.getenv('DICTIONARY_API')

    def request_json(self, word):
        response = requests.get(f"https://dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={DictAPIManager.API_KEY}")

        return response.json()