#imports
import discord, random
from discord.ext import commands

class AceAttorney(commands.Cog):
    def __init(self, bot):
        self.bot = bot

    #Commands
    @commands.command()
    async def lastcommands(ctx, num_comments):
        to_send = ''
        async for message in ctx.channel.history(limit=int(num_comments)):
            to_send += message.author.name + ': ' + message.content + '\n'
        await ctx.send(to_send)

def setup(bot):
    bot.add_cog(AceAttorney(bot))
