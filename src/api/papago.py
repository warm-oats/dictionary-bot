import asyncio
from googletrans import Translator as GoogleTranslator

class PapagoAPIManager():
    def __init__(self):
        PapagoAPIManager.google_translator = GoogleTranslator()

    def translate_word(self, word, src='en', dest='ko'):
        async def sync_translate():
            async with self.google_translator:
                #result = await google_translator.translate('안녕하세요.')
                #print(result)  # <Translated src=ko dest=en text=Good evening. pronunciation=Good evening.>
                    
                return await self.google_translator.translate(word, src=src, dest=dest)
        
                #result = await google_translator.translate('veritas lux mea', src='la')
                #print(result)  # <Translated src=la dest=en text=The truth is my light pronunciation=The truth is my light>

        return asyncio.run(sync_translate())