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
        self.def_contexts = DictController.dict_model.get_word_info(word) 
        button_controller = ButtonController(self)
        await DictController.dict_view.post_word_info(ctx, self.def_contexts, button_controller)

class ButtonController(discord.ui.View):
    def __init__(self, dict_controller):
        super().__init__()
        self.value = None
        self.dict_controller = dict_controller
        self.def_context_i = 0
        self.cur_context_num = 1

    @discord.ui.button(label="<<", style = discord.ButtonStyle.blurple)
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        contexts_len = len(self.dict_controller.def_contexts)

        if self.is_valid_index(self.def_context_i - 1, contexts_len):
            def_context = self.dict_controller.def_contexts[self.def_context_i - 1]
            self.cur_context_num -= 1
            await self.dict_controller.dict_view.edit_word_info(def_context, self.cur_context_num, contexts_len, interaction)
            self.def_context_i -= 1

    @discord.ui.button(label=">>", style = discord.ButtonStyle.blurple)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        contexts_len = len(self.dict_controller.def_contexts)

        if self.is_valid_index(self.def_context_i + 1, contexts_len):
            def_context = self.dict_controller.def_contexts[self.def_context_i + 1]
            self.cur_context_num += 1
            await self.dict_controller.dict_view.edit_word_info(def_context, self.cur_context_num, contexts_len, interaction)
            self.def_context_i += 1

    def is_valid_index(self, index, lst_len):
        if index < 0 or index >= lst_len:
            return False
        
        return True

async def setup(bot):
    print("Inside dict controller setup function")
    await bot.add_cog(DictController(bot))