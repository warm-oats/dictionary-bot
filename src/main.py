import os
from discord import Intents
from bot import Bot
from dotenv import load_dotenv
import discord

intents = Intents.all()
intents.message_content = True
bot = Bot(command_prefix = ">", intents = intents)

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Sync cogs and cog commands, run once at setup
@bot.event
async def setup_hook():
    for filename in os.listdir("src/controller"):
        if filename.endswith(".py"):
            await bot.load_extension(f"controller.{filename[:-3]}")
    
    synced = await bot.tree.sync(guild = discord.Object(id = 520337076659421192))
    print(f"Synced {len(synced)} commands(s)")

@bot.tree.command(
    name = "ping",
    description = "Check bot ping",
    guild = discord.Object(id = 520337076659421192)
)
async def ping(ctx):
    await ctx.response.send_message(f"Pong! {round(bot.latency * 1000, 1)}ms")

if __name__ == "__main__":
    bot.run(f"{BOT_TOKEN}")