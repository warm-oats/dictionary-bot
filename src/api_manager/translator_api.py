import asyncio
from googletrans import Translator as GoogleTranslator

class TranslatorAPIManager():

    translator = GoogleTranslator()

    def translate_word(self, word, src='en', dest='ko'):
        async def sync_translate():
            async with TranslatorAPIManager.translator:
                return await TranslatorAPIManager.translator.translate(word, src=src, dest=dest)

        return asyncio.run(sync_translate())
    
if __name__ == '__main__':
    translator = TranslatorAPIManager()
    translator.translate_word('hey')