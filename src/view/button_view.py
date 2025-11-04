import discord
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from util.custom_button import CustomButton

class DirectionalButtonView(discord.ui.View):

    def __init__(self, pos_contexts: list[dict], edit_func, context_i: int = 0, context_num: int = 1):
        super().__init__()
        self.pos_contexts = pos_contexts
        self.edit_func = edit_func
        self.context_i = context_i
        self.context_num = context_num
        
        self._forward_button = CustomButton(
            callback_func = self.change_button_dir, 
            label = ">>", 
            style = discord.ButtonStyle.blurple,
            direction = 1
            )
        self._prev_button = CustomButton(
            callback_func = self.change_button_dir, 
            label = "<<", 
            style = discord.ButtonStyle.blurple,
            direction = -1
            )
        
        # Enable or disable buttons toggle when scrolling to end
        self.toggle_buttons()

        self.add_item(item = self._prev_button)
        self.add_item(item = self._forward_button)

    async def change_button_dir(self, interaction: discord.Interaction, direction: int):

        contexts_len = len(self.pos_contexts)

        if self.is_valid_index(self.context_i + direction, contexts_len):
            context = self.pos_contexts[self.context_i + direction]
            self.context_num += direction

            self.context_i += direction
            self.toggle_buttons()

            await self.edit_func(context, self.context_num, contexts_len, interaction, self)

    def is_valid_index(self, index: int, lst_len: int):
        if index < 0 or index >= lst_len:
            return False
        
        return True
    
    def toggle_buttons(self):
        if (self.context_i == len(self.pos_contexts) - 1):
            self._forward_button.disabled = True
        else:
            self._forward_button.disabled = False
        
        if (self.context_i == 0):
            self._prev_button.disabled = True
        else:
            self._prev_button.disabled = False