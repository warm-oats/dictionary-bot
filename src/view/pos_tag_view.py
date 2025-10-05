import discord
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

class PosTagView:

    async def post_tag_info(self, ctx, phrase, pos_meaning_map):
        
        embeds = []

        for pos, meaning_map in pos_meaning_map.items():
            single_pos_map = {pos: meaning_map}
            embed = self.create_embed(single_pos_map, pos, False)

            embeds.append(embed)

        await ctx.channel.send(content = f"**{phrase}**", embeds = embeds)

    def create_embed(self, pos_meaning_map, phrase, put_pos_title = True):
        embed = discord.Embed(title = f"{phrase}")

        for pos, words_map in pos_meaning_map.items():
            if (words_map != []):
                formatted_words = ""

                for word_map in words_map:
                    formatted_words += self.word_formatter(word_map)

                if (put_pos_title):
                    embed.add_field(name = f"**{pos.capitalize()}**", value = formatted_words, inline = False)
                else:
                    embed.add_field(name = "", value = formatted_words, inline = False)

        return embed
    
    def word_formatter(self, word_map):

        for key, value in word_map.items():
            word = key
            meaning = value
        
        return f"({word}: {meaning}) "