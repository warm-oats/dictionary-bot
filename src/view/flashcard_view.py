import discord
from view.button_view import FlashcardButtonView

class FlashcardView:

    FLASHCARD_FRONT_i = 0
    FLASHCARD_BACK_i = 1

    async def post_flashcards_info(self, flashcards_info: list[tuple], deck_name: str, ctx: discord.Interaction):
        # List containing an embed for each flashcard
        embeds = []
        content = f"**Studying Deck '{deck_name.capitalize()}'**\n_ _"

        if (not flashcards_info):
            await ctx.followup.send(content = "No cards in this deck")
            return

        for flashcard in flashcards_info:
            embeds.append(self.create_flashcard_embed(flashcard))
        
        button_view = FlashcardButtonView(embeds, self.switch_flashcard, self.flip_flashcard)

        await ctx.followup.send(content = content, embed = embeds[0][0], view = button_view)
        await button_view.wait()

    async def switch_flashcard(self, new_flashcard: discord.Embed, interaction: discord.Interaction, button_view):
        await interaction.response.edit_message(embed = new_flashcard[self.FLASHCARD_FRONT_i], view = button_view)
        
    async def flip_flashcard(self, cur_flashcard: list, interaction: discord.Embed, side: str, button_view):

        if (side == "front"):
            embed = cur_flashcard[self.FLASHCARD_FRONT_i]
        else:
            embed = cur_flashcard[self.FLASHCARD_BACK_i]

        await interaction.response.edit_message(embed = embed, view = button_view)
 
    def create_flashcard_embed(self, flashcard: tuple) -> list[discord.Embed, discord.Embed]:

        # Create embeds
        embed_front = discord.Embed()
        embed_back = discord.Embed()

        embed_front.description = (
            "\u200b\n"
            f"# \u1CBC\u1CBC\u1CBC\u1CBC{flashcard[self.FLASHCARD_FRONT_i]}\u1CBC\u1CBC\u1CBC\u1CBC"
            "\n\n\u200b\u200b\u200b\n\n"
        )

        embed_back.description = (
            "\u200b\n"
            f"# \u1CBC\u1CBC\u1CBC\u1CBC{flashcard[self.FLASHCARD_BACK_i]}\u1CBC\u1CBC\u1CBC\u1CBC"
            "\n\n\u200b\u200b\u200b\n\n"
        )

        return [embed_front, embed_back]