from discord.ext import commands
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from model.pos_tag_model import PosTagModel
from view.pos_tag_view import PosTagView

class PosTagController(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.pos_tag_model = PosTagModel()
        self.pos_tag_view = PosTagView()

async def setup(bot):
    print("Inside pos tag controller setup function")
    await bot.add_cog(PosTagController(bot))