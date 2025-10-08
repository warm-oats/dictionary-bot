import discord
from pathlib import Path
import sys
import asyncio
sys.path.insert(0, str(Path(__file__).parent.parent))   

class PosTagView:

    async def post_tag_info(self, ctx, translation_package, no_stem_words):
        
        embeds = []
        sentence = self.sentence_colorizer(translation_package["text"], no_stem_words)
        sentence_translation = translation_package["translation"]
        content = f"""{sentence}\n\n{sentence_translation}\n_ _"""

        # Remove text and translation field: no longer needed in pos mapping
        translation_package.pop("text")
        translation_package.pop("translation")

        # Iterate through each part of speech words mapping
        for pos, meaning_map in translation_package.items():
            single_pos_map = {pos: meaning_map}

            # Check if a part of speech has no words
            if (single_pos_map[pos] != []): 
                embed = self.create_embed(single_pos_map, pos, False)

                embeds.append(embed)

        # Post embed
        await ctx.followup.send(content = content, embeds = embeds)

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
    
    def sentence_colorizer(self, sentence, no_stem_words):
        # nouns: blue, adjectives: green, verbs: red
        POS_MAP = {"nouns": "\u001b[0;34m", "adjectives": "\u001b[0;32m", "verbs": "\u001b[0;31m"}
        COLOR_END= "\u001b[0;0m"
        ANSI_HEAD = "```ansi\n"
        ANSI_TAIL = "\n```"

        for pos, words in no_stem_words.items():
            for word in words:
                sentence = sentence.replace(word, f"{POS_MAP[pos]}{word}{COLOR_END}")

        colorized_sentence = f"{ANSI_HEAD}{sentence}{ANSI_TAIL}"

        return colorized_sentence
    
if __name__ == "__main__":
    pos_tag_view = PosTagView()
    sentence = "‘곶감이 뭐지? 크고 무서운 게 분명해.’ 호랑이는 생각했다. ‘곶감을 피해야 해. 그렇지 않으면 나는 죽을 지 몰라.’"
    no_stem_words = {'nouns': ['나', '곶감', '게', '호랑이', '뭐', '해', '죽', '생각', '피해'], 'verbs': ['않으면', '지', '크고', '했다', '몰라'], 'adjectives': ['그렇지', '분명해', '무서운']}

    print(pos_tag_view.sentence_colorizer(sentence, no_stem_words))