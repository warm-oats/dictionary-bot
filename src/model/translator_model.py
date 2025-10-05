import asyncio
from googletrans import Translator as GoogleTranslator
import nest_asyncio
nest_asyncio.apply()

class TranslatorModel:

    def translate_word(self, word, src='en', dest='ko'):
        async def sync_translate():
            async with GoogleTranslator() as translator:
                return await translator.translate(word, src=src, dest=dest)

        return asyncio.run(sync_translate())
    
if __name__ == '__main__':
    translator = TranslatorModel()

    print(translator.translate_word("가").text)

    print(translator.translate_word("가").text)

    

