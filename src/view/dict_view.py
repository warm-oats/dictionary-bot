class DictView:
    def __init__(self):
        pass
    
    async def post_word_info(self, ctx, word):
        await ctx.channel.send(word)
