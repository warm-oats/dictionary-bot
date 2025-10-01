import asyncio
from googletrans import Translator as GoogleTranslator

class TranslatorApiManager():

    translator = GoogleTranslator()

    def translate_word(self, word, src='en', dest='ko'):
        async def sync_translate():
            async with TranslatorApiManager.translator:
                return await TranslatorApiManager.translator.translate(word, src=src, dest=dest)

        return asyncio.run(sync_translate())
    
if __name__ == '__main__':
    translator = TranslatorApiManager()
    print(translator.translate_word('hey'))