from discord.ext import commands
import discord
from discord import app_commands
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from model.deck_model import DeckModel
from view.deck_view import DeckView
from view.button_view import DirectionalButtonView

class DeckController(commands.Cog):

    def __init__(self, bot: commands.Bot):
        super().__init__()
        self._bot = bot
        self._deck_model = DeckModel()
        self._deck_view = DeckView()

    @app_commands.command(name = "get-deck-list", description = "Get list of all decks")
    async def define_word(self, ctx: discord.Interaction):
        user_id = ctx.user.id
        user_name = ctx.user.name
        decks_info = self._deck_model.get_decks(user_id)

        # Defer due to fetching definitions can take long
        await ctx.response.defer(ephemeral = True, thinking = True)

        await self._deck_view.post_decks_info(decks_info, user_name, ctx)

async def setup(bot: commands.Bot):
    print("Inside deck controller setup function")
    await bot.add_cog(DeckController(bot))