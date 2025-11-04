import asyncio
from googletrans import Translator as GoogleTranslator
import nest_asyncio
nest_asyncio.apply()

class TranslatorModel:

    def translate_word(self, word: str, src: str, dest: str):
        async def sync_translate():
            async with GoogleTranslator() as translator:
                return await translator.translate(word, src = src, dest = dest)

        return asyncio.run(sync_translate())