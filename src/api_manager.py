import os
import requests
import asyncio
from dotenv import load_dotenv

# f-strings make OOP for this very hard, so using separate classes

class PapagoKoreanAPIManager():
    def __init__(self):
        pass

class RandomAPIManager():
    def __init__(self):
        pass

    def request_json(self, amount=1, word_length=4):
        dict_response = requests.get(f"https://random-word-api.herokuapp.com/word?number={amount}&length={word_length}")
        
        return dict_response.json() # Output is a list of words

class MerriamAPIManager():

    load_dotenv()

    MERRIAM_API = os.getenv('DICTIONARY_API')

    def __init__(self):
        pass

    def request_json(self, word):
        dict_response = requests.get(f"https://dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={MerriamAPIManager.MERRIAM_API}")

        return dict_response.json()

if __name__ == "__main__":
    random = RandomAPIManager()
    merriam = MerriamAPIManager()

    random.request_json()
    merriam.request_json('hey')