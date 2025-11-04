import discord

class DictView:

    def __init__(self):
        super().__init__()
        self.phonetics = []

    async def post_word_info(self, ctx: discord.Interaction, pos_contexts: list[dict], button_view):
        embeds = [] # List containing an embed for each definition context
        contexts_count = len(pos_contexts)

        self.set_phonetics(pos_contexts)

        for count, word_info in enumerate(pos_contexts, start=1):
            embeds.append(self.create_embed(word_info, count, contexts_count))

        await ctx.followup.send(embed = embeds[0], view = button_view)
        await button_view.wait()

    async def edit_word_info(self, pos_context: dict, context_num: int, contexts_count: int, interaction: discord.Interaction, button_view):
        embed = self.create_embed(pos_context, context_num, contexts_count)
        
        await interaction.response.edit_message(embed = embed, view = button_view)
 
    def create_embed(self, word_info: dict, context_num: int, contexts_count: int):
        # Create embed
        embed = discord.Embed(title = f"{word_info["word_name"].capitalize()}   `{context_num} of {contexts_count}`")

        # Add field for pronunciation
        embed.add_field(name = "Pronunciations", value = ' '.join(self.phonetics), inline = False)

        # Add fields for each definition
        for count, definition in enumerate(word_info["definitions"], start = 1):
            embed.add_field(name = f"Definition {count}", value = definition.capitalize(), inline = False)

        # Add additional fields stem set and parts of speech
        embed.add_field(name = "Stem Set", value =  " ".join(word_info["stem_set"]), inline = False)
        embed.add_field(name = "Part of Speech", value = word_info["part_of_speech"].capitalize(), inline = False)

        return embed
    
    def set_phonetics(self, pos_contexts: dict):
        phonetics = []

        for context in pos_contexts:
            phonetics.extend(context["phonetics"])

        self.phonetics = phonetics
