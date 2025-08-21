from discord.ext import commands
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from service.translator import Translator

class WordDictionary(commands.Cog):

    translator = Translator()

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "defineword")
    async def define_word(self, ctx, word):
        word_info = self.translator.get_word(word)

        await ctx.channel.send(word_info['word_name'])

async def setup(bot):
    print("Inside word dictionary setup function")
    await bot.add_cog(WordDictionary(bot))