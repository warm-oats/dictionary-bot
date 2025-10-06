from discord.ext import commands
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from model.groq_model import GroqModel
from view.convo_view import ConvoView

class ConvoController(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.convo_model = GroqModel("Korean")
        self.convo_view = ConvoView()

async def setup(bot):
    print("Inside convo controller setup function")
    await bot.add_cog(ConvoController(bot))

