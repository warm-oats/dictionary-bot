import discord

class CustomButton(discord.ui.Button):

    def __init__(self, callback_func, style: discord.ButtonStyle, label: str, **callback_params):
        super().__init__(label = label, style = style, disabled = False)
        self.callback_func = callback_func
        self.callback_params = callback_params

    async def callback(self, interaction: discord.Interaction):

        # All callback functions need interaction argument
        self.callback_params['interaction'] = interaction

        # Call callback function that modifies button with passed in params for said function
        return await self.callback_func(**self.process_params(self.callback_params))
    
    # Maps parameters to name: parameter pairs
    def process_params(self, params):

        result = {}
        
        for key, value in params.items():
            if isinstance(value, dict):
                result.update(value)
            else:
                result[key] = value

        return result