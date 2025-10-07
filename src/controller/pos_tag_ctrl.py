from discord.ext import commands
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from model.pos_tag_model import PosTagModel
from view.pos_tag_view import PosTagView

class PosTagController(commands.Cog):

    def __init__(self, bot):
        self._bot = bot
        self._pos_tag_model = PosTagModel()
        self._pos_tag_view = PosTagView()

    @commands.command(name = "extract-pos")
    async def async_define_word(self, ctx, *, phrase):
        pos_tag_map = self._pos_tag_model.extract_pos(phrase)
        translation_package = self._pos_tag_model.map_pos_meaning(phrase, pos_tag_map)

        await self._pos_tag_view.post_tag_info(ctx, translation_package)

async def setup(bot):
    print("Inside pos tag controller setup function")
    await bot.add_cog(PosTagController(bot))