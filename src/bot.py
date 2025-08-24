from discord.ext import commands
import os

class Bot(commands.Bot):
    async def setup_hook(self) -> None:
        for f in os.listdir("./controller"):
	        if f.endswith(".py"):
		        await self.load_extension("controller." + f[:-3])