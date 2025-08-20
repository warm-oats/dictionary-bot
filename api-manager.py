import os
import requests
from dotenv import load_dotenv

class WordAPIManager:

    URL = None

    def __init__(self):
        pass

    def request(self):
        dict_response = requests.get(eval(f'f"{self.URL}"')) 

        return dict_response

class RandomAPIManager(WordAPIManager):

    URL = "https://random-word-api.herokuapp.com/word?number={amount}?length={word_length}"

    def __init__(self):
        super()

    def request(self, amount=1, word_length=4):
        dict_response = super().request_word()

class MerriamAPIManager(WordAPIManager):

    load_dotenv()

    DICT_API = os.getenv('DICTIONARY_API')
    URL = "https://dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={MerriamAPIManager.DICT_API}"

    def __init__(self):
        super()
        load_dotenv()

    def request(self, word):
        dict_response = super().request_word(word)
        word_name = dict_response.json()[0]["meta"]["id"].lower().strip()
        stem_set = set(map(lambda stem: stem.split(" ")[0], dict_response.json()[0]["meta"]["stems"]))

        print(dict_response.json())

if __name__ == "__main__":
    api_manager = MerriamAPIManager()

    api_manager.request('voluminous')