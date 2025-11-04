from discord.ext import commands
import discord
from discord import app_commands
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from model.deck_model import DeckModel
from view.deck_view import DeckView
from database.service import Db

class DeckController(commands.Cog):

    def __init__(self, bot: commands.Bot):
        super().__init__()
        self._bot = bot
        self._deck_model = DeckModel()
        self._deck_view = DeckView()
        self._db = Db()

    @app_commands.command(name = "get-deck-list", description = "Get list of all decks")
    async def get_deck_list(self, ctx: discord.Interaction):
        user_id = ctx.user.id
        user_name = ctx.user.name
        decks_info = self._deck_model.get_decks(user_id)

        # Defer due to fetching definitions can take long
        await ctx.response.defer(ephemeral = True, thinking = True)

        await self._deck_view.post_decks_info(decks_info, user_name, ctx)
    
    @app_commands.command(name = "create-deck", description = "Create new deck")
    @app_commands.describe(deck_name = "Name of new deck")
    async def add_deck(self, ctx: discord.Interaction, deck_name: str):
        
        # Defer due to fetching definitions can take long
        await ctx.response.defer(ephemeral = True, thinking = True)
        
        try:
            user_id = ctx.user.id

            self._db.create_deck(user_id, deck_name)


            ctx.followup.send(content = f"Added deck '{deck_name}'")
        except ValueError as e:
            ctx.followup.send(content = e)

    @app_commands.command(name = "delete-deck", description = "Delete a deck")
    @app_commands.describe(deck_name = "Deck name to be deleted")
    async def delete_deck(self, ctx: discord.Interaction, deck_name: str):
        
        # Defer due to fetching definitions can take long
        await ctx.response.defer(ephemeral = True, thinking = True)
        
        try:
            user_id = ctx.user.id

            self._db.delete_deck(user_id, deck_name)


            ctx.followup.send(content = f"Deleted deck '{deck_name}'")
        except ValueError as e:
            ctx.followup.send(content = e)

    @app_commands.command(name = "update-deck-name", description = "Change deck name")
    @app_commands.describe(deck_name = "Current deck name", new_deck_name = "New name of deck")
    async def update_deck(self, ctx: discord.Interaction, new_deck_name: str, deck_name: str):

        # Defer due to fetching definitions can take long
        await ctx.response.defer(ephemeral = True, thinking = True)

        try:
            user_id = ctx.user.id

            self._db.update_deck_name(user_id, deck_name, new_deck_name)

            ctx.followup.send(content = f"Changed deck '{deck_name}' to '{new_deck_name}'")
        except ValueError as e:
            ctx.followup.send(content = e)

    @app_commands.command(name = "add-flashcard", description = "Add new flashcard")
    @app_commands.describe(deck_name = "Deck to add flashcard to", flashcard_front = "Front description of flashcard", flashcard_back = "Back description of flashcard")
    async def add_flashcard(self, ctx: discord.Interaction, deck_name: str, flashcard_front: str, flashcard_back: str):

        # Defer due to fetching definitions can take long
        await ctx.response.defer(ephemeral = True, thinking = True)

        try:
            user_id = ctx.user.id

            self._db.add_flashcard(user_id, flashcard_front, flashcard_back)

            ctx.followup.send(content = f"Added flashcard '{flashcard_front}' to deck '{deck_name}'")
        except ValueError as e:
            ctx.followup.send(content = e)

async def setup(bot: commands.Bot):
    print("Inside deck controller setup function")
    await bot.add_cog(DeckController(bot))