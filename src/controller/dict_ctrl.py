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
        button_controller = ButtonController(def_contexts)
        await DictController.dict_view.post_word_info(ctx, def_contexts, button_controller)

class ButtonController(discord.ui.View):
    def __init__(self, def_contexts):
        super().__init__()
        self.value = None
        self.def_contexts = def_contexts
        self.def_context_i = 0

    @discord.ui.button(label="<<", style=discord.ButtonStyle.blurple)
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message('CLICKED PREV!')

    @discord.ui.button(label=">>", style=discord.ButtonStyle.blurple)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message('CLICKED NEXT!')

    def is_valid_index(self, index, lst_len):
        if index < 0 or index >= lst_len:
            return False
        
        return True

async def setup(bot):
    print("Inside dict controller setup function")
    await bot.add_cog(DictController(bot))