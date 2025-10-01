import os
import requests
from dotenv import load_dotenv

class DictApiManager():

    load_dotenv()
    
    API_KEY = os.getenv('DICTIONARY_API')

    def request_json(self, word):
        response = requests.get(f"https://dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={DictApiManager.API_KEY}")

        return response.json()
    
if __name__ == '__main__':
    print(DictApiManager().request_json('what'))