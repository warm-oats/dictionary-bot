import discord

class CustomButton(discord.ui.Button):

    def __init__(self, callback_func, style, label, **callback_params):
        super().__init__(label = label, style = style)
        self.callback_func = callback_func
        self.callback_params = callback_params

    async def callback(self, interaction):

        self.callback_params['interaction'] = interaction

        return await self.callback_func(**self.process_params(self.callback_params))
    
    def process_params(self, params):

        result = {}
        
        for key, value in params.items():
            if isinstance(value, dict):
                result.update(value)
            else:
                result[key] = value

        return result

class ButtonView(discord.ui.View):

    def __init__(self, contexts, edit_func, context_i = 0, context_num = 1):
        super().__init__()
        self.contexts = contexts
        self.edit_func = edit_func
        self.context_i = context_i
        self.context_num = context_num
        self.test_button = CustomButton(callback_func=self.next_button, label="Test", style=discord.ButtonStyle.blurple)

        self.add_item(item = self.test_button)

    async def prev_button(self, interaction: discord.Interaction):

        contexts_len = len(self.contexts)

        if self.is_valid_index(self.context_i - 1, contexts_len):
            context = self.contexts[self.context_i - 1]
            self.context_num -= 1

            await self.edit_func(context, self.context_num, contexts_len, interaction)

            self.context_i -= 1

    async def next_button(self, interaction: discord.Interaction, j, i):

        contexts_len = len(self.contexts)

        print(j + i)

        if self.is_valid_index(self.context_i + 1, contexts_len):
            context = self.contexts[self.context_i + 1]
            self.context_num += 1

            await self.edit_func(context, self.context_num, contexts_len, interaction)

            self.context_i += 1

    def is_valid_index(self, index, lst_len):
        if index < 0 or index >= lst_len:
            return False
        
        return True