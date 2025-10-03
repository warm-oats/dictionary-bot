import discord
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

class PosTagView:

    async def post_tag_info(self, ctx, pos_tag_map, phrase):

        embed = self.create_embed(pos_tag_map, phrase)

        await ctx.channel.send(embed = embed)

    def create_embed(self, pos_tag_map, phrase):
        embed = discord.Embed(title = f"{phrase}")

        for pos, words in pos_tag_map.items():
            if (words != []):
                embed.add_field(name = f"**{pos.capitalize()}**", value = words, inline = False)

        return embed