import discord
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from util.custom_button import CustomButton

class DirectionalButtonView(discord.ui.View):

    def __init__(self, contexts: list, edit_func, context_i: int = 0, context_num: int = 1):
        super().__init__()
        self.contexts = contexts
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

        contexts_len = len(self.contexts)

        if self.is_valid_index(self.context_i + direction, contexts_len):
            context = self.contexts[self.context_i + direction]
            self.context_num += direction

            self.context_i += direction
            self.toggle_buttons()

            await self.edit_func(context, self.context_num, contexts_len, interaction, self)

    def is_valid_index(self, index: int, lst_len: int):
        if index < 0 or index >= lst_len:
            return False
        
        return True
    
    def toggle_buttons(self):
        if (self.context_i == len(self.contexts) - 1):
            self._forward_button.disabled = True
        else:
            self._forward_button.disabled = False
        
        if (self.context_i == 0):
            self._prev_button.disabled = True
        else:
            self._prev_button.disabled = False

class DecksButtonView(DirectionalButtonView):

    def __init__(self, embeds: list, edit_func, context_i: int = 0, context_num: int = 1):
        super().__init__(embeds, edit_func, context_i, context_num)

    async def change_button_dir(self, interaction: discord.Interaction, direction: int):

        contexts_len = len(self.contexts)

        if self.is_valid_index(self.context_i + direction, contexts_len):
            context = self.contexts[self.context_i + direction]
            self.context_num += direction

            self.context_i += direction
            self.toggle_buttons()

            await self.edit_func(context, interaction, self)

class FlashcardButtonView(DecksButtonView):
    def __init__(self, embeds: list, edit_func, flip_func, context_i: int = 0, context_num: int = 1):
        super().__init__(embeds, edit_func, context_i, context_num)
        self.side = "front"
        self.flip_func = flip_func

        self._flip_button = CustomButton(
            callback_func = self.flip_flashcard, 
            label = "FLIP", 
            style = discord.ButtonStyle.blurple
        )

        self.add_item(item = self._flip_button)

    async def change_button_dir(self, interaction: discord.Interaction, direction: int):

        self.side = "front"

        await super().change_button_dir(interaction, direction)

    async def flip_flashcard(self, interaction: discord.Interaction):

        if (self.side == "front"):
            self.side = "back"
        else:
            self.side = "front"

        cur_flashcard = self.contexts[self.context_i]

        await self.flip_func(cur_flashcard, interaction, self.side, self)