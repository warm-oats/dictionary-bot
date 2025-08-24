import os
from discord import Intents
from bot import Bot
from dotenv import load_dotenv

intents = Intents.all()
intents.message_content = True
bot = Bot(command_prefix = ">", intents = intents)

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Runs as soon as script is run, setup once
@bot.event
async def setup_hook():
    for filename in os.listdir("src/controller"):
        if filename.endswith(".py"):
            await bot.load_extension(f"controller.{filename[:-3]}")
    
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} commands(s)")

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency * 1000, 1)}ms")

if __name__ == "__main__":
    bot.run(f"{BOT_TOKEN}")