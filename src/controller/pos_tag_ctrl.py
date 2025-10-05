from discord.ext import commands
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from model.pos_tag_model import PosTagModel
from view.pos_tag_view import PosTagView
from view.button_view import DirectionalButtonView

class PosTagController(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.pos_tag_model = PosTagModel()
        self.pos_tag_view = PosTagView()

        pass

    @commands.command(name = "extract-pos")
    async def async_define_word(self, ctx, *, phrase):
        pos_tag_map = self.pos_tag_model.extract_pos(phrase)
        pos_meaning_map = self.pos_tag_model.map_pos_meaning(pos_tag_map)

        await self.pos_tag_view.post_tag_info(ctx, phrase, pos_meaning_map)

async def setup(bot):
    print("Inside pos tag controller setup function")
    await bot.add_cog(PosTagController(bot))