import discord

class CustomButton(discord.ui.Button):

    def __init__(self, callback_func, style, label, disabled = False, custom_id = None, url = None, emoji = None, row = None, sku_id = None, id = None):
        super().__init__(
            label = label, 
            style = style, 
            disabled = disabled, 
            custom_id = custom_id, 
            url = url, 
            emoji = emoji,
            row = row,
            sku_id = sku_id,
            id = id
        )
        self.callback = callback_func

class ButtonView(discord.ui.View):

    def __init__(self, contexts, edit_func, context_i = 0, context_num = 1):
        super().__init__()
        self.contexts = contexts
        self.edit_func = edit_func
        self.context_i = context_i
        self.context_num = context_num
        self.test_button = CustomButton(self.next_button, label="Test", style = discord.ButtonStyle.blurple)

        self.add_item(item = self.test_button)

    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        contexts_len = len(self.contexts)

        if self.is_valid_index(self.context_i - 1, contexts_len):
            context = self.contexts[self.context_i - 1]
            self.context_num -= 1

            await self.edit_func(context, self.context_num, contexts_len, interaction)

            self.context_i -= 1

    async def next_button(self, interaction: discord.Interaction):

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