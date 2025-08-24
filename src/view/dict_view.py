import discord

class DictView:

    def __init__(self):
        super().__init__()
        self.value = None

    async def post_word_info(self, ctx, def_contexts):
        embeds = [] # List containing an embed for each definition context
        contexts_count = len(def_contexts)

        for count, word_info in enumerate(def_contexts, start=1):
            embeds.append(self.create_embed(word_info, count, contexts_count))

        await ctx.channel.send(embed=embeds[0], view=ButtonView())
        await ButtonView().wait()

    @discord.ui.button(label=">", style = discord.ButtonStyle.blurple)
    async def next_button(self, interaction, button):
        pass
 
    def create_embed(self, word_info, context_num, contexts_count):
        embed = discord.Embed(title = f"{word_info["word_name"].capitalize()}   `{context_num} of {contexts_count}`")

        for count, definition in enumerate(word_info["definitions"], start = 1):
            embed.add_field(name = f"Definition {count}", value = definition.capitalize(), inline = False)

        embed.add_field(name = "Stem Set", value =  " ".join(word_info["stem_set"]), inline = False)
        embed.add_field(name = "Part of Speech", value = word_info["part_of_speech"].capitalize(), inline = False)

        embed.footer

        return embed

class ButtonView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label=">", style=discord.ButtonStyle.blurple)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('CLICKED!')
        button.disabled = True
