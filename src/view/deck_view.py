import discord
from view.button_view import DecksButtonView

class DeckView:
    async def post_decks_info(self, decks_info: list[list[str, int]], user_name: str, ctx: discord.Interaction):
        # List containing an embed for each deck context
        embeds = []

        if (not decks_info):
            await ctx.followup.send(f"No decks for user {user_name}")
            return

        start_i = 0
        end_i = min(5, len(decks_info))
        copy_deck = decks_info[start_i:end_i]

        # Each deck embed should only contain 5 decks at most
        while (copy_deck):
            embeds.append(self.create_decks_embed(decks_info[start_i:end_i], user_name))
            start_i = end_i
            end_i = start_i + 5
            copy_deck = decks_info[start_i:end_i]
        
        button_view = DecksButtonView(embeds, self.edit_deck_info)

        await ctx.followup.send(embed = embeds[0], view = button_view)
        await button_view.wait()

    async def edit_deck_info(self, deck_embed: discord.Embed, interaction: discord.Interaction, button_view):
        await interaction.response.edit_message(embed = deck_embed, view = button_view)
 
    def create_decks_embed(self, decks_info: list[list[str, int]], user_name: str):
        # Create embed
        embed = discord.Embed(title = f"Decks for {user_name}")

        # Add field for each deck
        for deck_name, vocab_count in decks_info:
            embed.add_field(name = f"{deck_name} - {vocab_count} vocabularies", value = '', inline = False)

        return embed