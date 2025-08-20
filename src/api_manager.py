import os
import requests
from dotenv import load_dotenv

# f-strings make OOP for this very hard, so using separate classes

class RandomAPIManager():
    def __init__(self):
        super()

    def request_json(self, amount=1, word_length=4):
        dict_response = requests.get(f"https://random-word-api.herokuapp.com/word?number={amount}&length={word_length}")
        words = dict_response.json()
        
        return words # Output is a list of words

class MerriamAPIManager():

    load_dotenv()

    MERRIAM_API = os.getenv('DICTIONARY_API')

    def __init__(self):
        super()
        load_dotenv()

    def request_json(self, word):
        dict_response = requests.get(f"https://dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={MerriamAPIManager.MERRIAM_API}")
        word_name = dict_response.json()[0]["meta"]["id"].lower().strip()
        stem_set = set(map(lambda stem: stem.split(" ")[0], dict_response.json()[0]["meta"]["stems"]))

if __name__ == "__main__":
    random = RandomAPIManager()
    merriam = MerriamAPIManager()

    random.request_json()
    merriam.request_json('hey')