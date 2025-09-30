from discord.ext import commands
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from model.convo_model import ConvoModel
from view.convo_view import ConvoView

class ConvoController(commands.Cog):

    convo_model = ConvoModel()
    convo_view = ConvoView()

    def __init__(self, bot):
        self.bot = bot

async def setup(bot):
    print("Inside dict controller setup function")
    await bot.add_cog(ConvoController(bot))

