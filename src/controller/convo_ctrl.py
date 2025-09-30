from discord.ext import commands
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from api_manager.convo_api import ConvoAPIManager

class DictController(commands.Cog):

    convo_manager = ConvoAPIManager()

    def __init__(self, bot):
        self.bot = bot



async def setup(bot):
    print("Inside dict controller setup function")
    await bot.add_cog(DictController(bot))

