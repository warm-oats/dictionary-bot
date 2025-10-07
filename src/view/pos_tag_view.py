import discord
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))   

class PosTagView:

    async def post_tag_info(self, ctx, translation_package):
        
        embeds = []
        sentence = f"```ansi\n\u001b[1;40;32m{translation_package['text']}\u001b[0m\n```"
        sentence_translation = translation_package['translation']
        content = f"""{sentence}\n\n{sentence_translation}\n_ _"""

        # Remove text and translation field: no longer needed in pos mapping
        translation_package.pop('text')
        translation_package.pop('translation')

        # Iterate through each part of speech words mapping
        for pos, meaning_map in translation_package.items():
            single_pos_map = {pos: meaning_map}

            # Check if a part of speech has no words
            if (single_pos_map[pos] != []): 
                embed = self.create_embed(single_pos_map, pos, False)

                embeds.append(embed)

        # Post embed to discord
        await ctx.response.send_message(content = content, embeds = embeds)

    def create_embed(self, pos_meaning_map, sentence, put_pos_title = True):
        embed = discord.Embed(title = f"{sentence}")

        for pos, words_map in pos_meaning_map.items():
            if (words_map != []):
                formatted_words = ""

                for word_map in words_map:
                    formatted_words += self.word_formatter(word_map)

                if (put_pos_title): # If creating a single embed for all pos, attach all pos names, else not
                    embed.add_field(name = f"**{pos.capitalize()}**", value = formatted_words, inline = False)
                else:
                    embed.add_field(name = "", value = formatted_words, inline = False)

        return embed
    
    def word_formatter(self, word_map):

        for key, value in word_map.items():
            word = key
            meaning = value
        
        return f"({word}: {meaning})"