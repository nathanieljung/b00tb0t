#imports
import discord, random
from discord.ext import commands

class AceAttorney(commands.Cog):
    def __init(self, bot):
        self.bot = bot

    #Commands
    @commands.command()
    async def lastmessages(self, ctx, num_comments):
        to_send = ''
        history = ctx.channel.history(limit=int(num_comments))
        await history.next()
        async for message in history:
            to_send += message.author.name + ': ' + message.content + '\n'
        await ctx.send(to_send)

def setup(bot):
    bot.add_cog(AceAttorney(bot))
