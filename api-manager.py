import os
import requests
from dotenv import load_dotenv

class APIManager:

    load_dotenv()

    DICT_API = os.getenv('DICTIONARY_API')

    def __init__(self):
        load_dotenv()

    def request_word(self, word):
        api_request = requests.get(f"https://dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={APIManager.DICT_API}")
        
        print(api_request.json()[0])

if __name__ == "__main__":
    api_manager = APIManager()

    api_manager.request_word('hello')