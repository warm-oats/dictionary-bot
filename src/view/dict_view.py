import discord

class DictView:

    def __init__(self):
        super().__init__()
        self.value = None
        self.phonetics = []

    async def post_word_info(self, ctx, def_contexts, button_view):
        embeds = [] # List containing an embed for each definition context
        contexts_count = len(def_contexts)

        self.set_phonetics(def_contexts)

        for count, word_info in enumerate(def_contexts, start=1):
            embeds.append(self.create_embed(word_info, count, contexts_count))

        await ctx.channel.send(embed = embeds[0], view = button_view)
        await button_view.wait()

    async def edit_word_info(self, def_context, context_num, contexts_count, interaction):
        embed = self.create_embed(def_context, context_num, contexts_count)
        await interaction.response.edit_message(embed = embed)
 
    def create_embed(self, word_info, context_num, contexts_count):
        embed = discord.Embed(title = f"{word_info["word_name"].capitalize()}   `{context_num} of {contexts_count}`")

        embed.add_field(name = "Pronunciations", value = ' '.join(self.phonetics), inline = False)

        for count, definition in enumerate(word_info["definitions"], start = 1):
            embed.add_field(name = f"Definition {count}", value = definition.capitalize(), inline = False)

        embed.add_field(name = "Stem Set", value =  " ".join(word_info["stem_set"]), inline = False)
        embed.add_field(name = "Part of Speech", value = word_info["part_of_speech"].capitalize(), inline = False)

        embed.footer

        return embed
    
    def set_phonetics(self, def_contexts):
        phonetics = []

        for context in def_contexts:
            phonetics.extend(context["phonetics"])

        self.phonetics = phonetics
