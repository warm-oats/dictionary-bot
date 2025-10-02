import discord

class CustomButton(discord.ui.Button):

    def __init__(self, callback_func, style, label, **callback_params):
        super().__init__(label = label, style = style)
        self.callback_func = callback_func
        self.callback_params = callback_params

    async def callback(self, interaction):

        self.callback_params['interaction'] = interaction # All callback functions need interaction argument

        return await self.callback_func(**self.process_params(self.callback_params))
    
    def process_params(self, params):

        result = {}
        
        for key, value in params.items():
            if isinstance(value, dict):
                result.update(value)
            else:
                result[key] = value

        return result