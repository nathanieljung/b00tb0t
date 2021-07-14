#imports
import discord, random
from discord.ext import commands

class AceAttorney(commands.Cog):
    def __init(self, bot):
        self.bot = bot

    #Commands
    @commands.command()
    async def lastcommands(ctx, num_comments):
        test = ""

def setup(bot):
    bot.add_cog(AceAttorney(bot))
