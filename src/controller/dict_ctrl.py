from discord.ext import commands
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from model.dict_model import DictModel
from view.dict_view import DictView

class DictController(commands.Cog):

    dict_model = DictModel()
    dict_view = DictView()

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "defineword")
    async def define_word(self, ctx, word):
        word_info = DictController.dict_model.get_word_info(word)
        DictController.dict_view.post_word_info(word_info)

async def setup(bot):
    print("Inside dict controller setup function")
    await bot.add_cog(DictController(bot))