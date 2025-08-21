from discord.ext import commands
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from model.dict_model.dict_logic import DictLogic
from view.dict_view import DictView

class DictController(commands.Cog):

    dict_model = DictLogic()
    dict_view = DictView()

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "defineword")
    async def define_word(self, ctx, word):
        word_info = self.dict_model.get_word(word)

        await ctx.channel.send(word_info['word_name'])

async def setup(bot):
    print("Inside dictionary controller setup function")
    await bot.add_cog(DictController(bot))