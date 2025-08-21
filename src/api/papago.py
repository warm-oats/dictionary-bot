import asyncio
from googletrans import Translator as GoogleTranslator

class PapagoAPIManager():
    def __init__(self):
        PapagoAPIManager.google_translator = GoogleTranslator()

    def translate_word(self, word, src='en', dest='ko'):
        async def sync_translate():
            async with self.google_translator:
                return await self.google_translator.translate(word, src=src, dest=dest)

        return asyncio.run(sync_translate())