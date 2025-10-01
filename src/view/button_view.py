import discord

class ButtonView(discord.ui.View):

    def __init__(self, contexts, edit_func, context_i = 0, context_num = 1):
        super().__init__()
        self.contexts = contexts
        self.edit_func = edit_func
        self.context_i = context_i
        self.context_num = context_num

    @discord.ui.button(label = "<<", style = discord.ButtonStyle.blurple)
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        contexts_len = len(self.contexts)

        if self.is_valid_index(self.context_i - 1, contexts_len):
            context = self.contexts[self.context_i - 1]
            self.context_num -= 1

            await self.edit_func(context, self.context_num, contexts_len, interaction)

            self.context_i -= 1

    @discord.ui.button(label = ">>", style = discord.ButtonStyle.blurple)
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