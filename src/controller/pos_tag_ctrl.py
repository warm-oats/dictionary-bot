from discord.ext import commands
from pathlib import Path
from discord import app_commands
import discord
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from model.pos_tag_model import PosTagModel
from view.pos_tag_view import PosTagView

class PosTagController(commands.Cog):

    def __init__(self, bot):
        self._bot = bot
        self._pos_tag_model = PosTagModel()
        self._pos_tag_view = PosTagView()

        self._bot.tree.command(
            name = 'extract-pos',
            description = 'Extract Korean sentence parts of speech in context',
            guild = discord.Object(id = '520337076659421192')
        )(self.extract_pos)

    @app_commands.describe(sentence = "Korean sentence", colorize = "Colorize all parts of speech?")
    async def extract_pos(self, ctx, *, sentence: str, colorize: bool = False):

        # Defer due to fetching translations can take long
        await ctx.response.defer(ephemeral = True, thinking = True)

        pos_tag_map = self._pos_tag_model.extract_pos(sentence)
        translation_package = self._pos_tag_model.map_pos_meaning(sentence, pos_tag_map)
        no_stem_words = self._pos_tag_model.extract_pos(sentence, False, False)

        await self._pos_tag_view.post_tag_info(ctx, translation_package, no_stem_words, colorize)

async def setup(bot):
    print("Inside pos tag controller setup function")
    await bot.add_cog(PosTagController(bot))