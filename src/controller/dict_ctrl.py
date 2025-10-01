from discord.ext import commands
import discord
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from model.dict_model import DictModel
from view.dict_view import DictView

class DictController(commands.Cog):

    def __init__(self, bot):
        self.dict_model = DictModel()
        self.dict_view = DictView()
        self.bot = bot

    @commands.command(name = "define")
    async def async_define_word(self, ctx, word):
        def_contexts = self.dict_model.get_word_info(word) 
        button_controller = DictButtonController(def_contexts, self.dict_view.edit_word_info)

        await self.dict_view.post_word_info(ctx, def_contexts, button_controller)

class DictButtonController(discord.ui.View):

    def __init__(self, contexts, edit_func, context_i = 0, context_num = 1):
        super().__init__()
        self.view = discord.ui.View()
        self.contexts = contexts
        self.edit_func = edit_func
        self.context_i = context_i
        self.context_num = context_num

    @discord.ui.button(label="<<", style = discord.ButtonStyle.blurple)
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        contexts_len = len(self.contexts)

        if self.is_valid_index(self.context_i - 1, contexts_len):
            context = self.contexts[self.context_i - 1]
            self.context_num -= 1

            await self.edit_func(context, self.context_num, contexts_len, interaction)

            self.context_i -= 1

    @discord.ui.button(label=">>", style = discord.ButtonStyle.blurple)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        contexts_len = len(self.contexts)

        if self.is_valid_index(self.context_i + 1, contexts_len):
            context = self.contexts[self.context_i + 1]
            self.context_num += 1

            await self.edit_func(context, self.context_num, contexts_len, interaction)

            self.context_i += 1

    def is_valid_index(self, index, lst_len):
        if index < 0 or index >= lst_len:
            return False
        
        return True

async def setup(bot):
    print("Inside dict controller setup function")
    await bot.add_cog(DictController(bot))