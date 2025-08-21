import asyncio
from googletrans import Translator as GoogleTranslator

class TranslatorAPIManager():
    def __init__(self):
        TranslatorAPIManager.translator = GoogleTranslator()

    def translate_word(self, word, src='en', dest='ko'):
        async def sync_translate():
            async with self.translator:
                return await self.translator.translate(word, src=src, dest=dest)

        return asyncio.run(sync_translate())
    
if __name__ == '__main__':
    translator = TranslatorAPIManager()
    translator.translate_word('hey')