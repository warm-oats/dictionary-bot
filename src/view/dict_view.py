import discord

class DictView:
    def __init__(self):
        pass
    
    async def post_word_info(self, ctx, word_info):
        embed = self.create_embed(word_info)
        await ctx.channel.send(embed = embed)

    def create_embed(self, word_info):
        embed = discord.Embed(title = word_info["word_name"].capitalize())

        for count, definition in enumerate(word_info["definitions"], start = 1):
            embed.add_field(name = f"Definition {count}", value = definition.capitalize(), inline = False)

        embed.add_field(name = "Stem Set", value =  " ".join(word_info["stem_set"]).capitalize(), inline = False)
        embed.add_field(name = "Part of Speech", value = word_info["part_of_speech"].capitalize(), inline = False)

        return embed

        
