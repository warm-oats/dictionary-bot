from discord.ext import commands
import discord
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

    @commands.command(name = "define")
    async def async_define_word(self, ctx, word):
        def_contexts = DictController.dict_model.get_word_info(word) 
        button_controller = ButtonController()
        await DictController.dict_view.post_word_info(ctx, def_contexts, ButtonController())

class ButtonController(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="<<", style=discord.ButtonStyle.blurple)
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('CLICKED PREV!')

    @discord.ui.button(label=">>", style=discord.ButtonStyle.blurple)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('CLICKED NEXT!')

async def setup(bot):
    print("Inside dict controller setup function")
    await bot.add_cog(DictController(bot))