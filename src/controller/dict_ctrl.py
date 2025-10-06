from discord import app_commands
from discord.ext import commands
import discord
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from model.dict_model import DictModel
from view.dict_view import DictView
from view.button_view import DirectionalButtonView
from main import bot

class DictController(commands.Cog):

    def __init__(self, bot):
        self.dict_model = DictModel()
        self.dict_view = DictView()
        self.bot = bot

        self.define_decorator()

    def define_decorator(self):
        self.bot.tree.command(
            name="define",
            description="Define English word definition",
            guild=discord.Object(id=520337076659421192)
        )(self.async_define_word)

    async def async_define_word(self, ctx, word: str):
        def_contexts = self.dict_model.get_word_info(word) 
        button_view = DirectionalButtonView(def_contexts, self.dict_view.edit_word_info)

        await self.dict_view.post_word_info(ctx, def_contexts, button_view)

async def setup(bot):
    print("Inside dict controller setup function")
    await bot.add_cog(DictController(bot))