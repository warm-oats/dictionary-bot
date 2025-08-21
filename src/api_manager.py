import os
import requests
import asyncio
from googletrans import Translator as GoogleTranslator
from dotenv import load_dotenv

# f-strings make OOP for this very hard, so using separate classes

class PapagoAPIManager():

    google_translator = GoogleTranslator()

    def translate_word(self, word):
        async def sync_translate():
            async with self.google_translator:
                #result = await google_translator.translate('안녕하세요.')
                #print(result)  # <Translated src=ko dest=en text=Good evening. pronunciation=Good evening.>
                    
                return await self.google_translator.translate(word, dest='ko')
        
                #result = await google_translator.translate('veritas lux mea', src='la')
                #print(result)  # <Translated src=la dest=en text=The truth is my light pronunciation=The truth is my light>

        return asyncio.run(sync_translate())

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
    papago = PapagoAPIManager()

    print(papago.translate_word('get'))