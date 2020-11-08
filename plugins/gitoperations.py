#imports
import discord, random
from discord.ext import commands

class GitOperations(commands.Cog):
    def __init(self, bot):
        self.bot = bot

    #Commands
    @commands.command()
    async def grive(self, ctx)
        await ctx.send('s\ny\nn\nc\ni\nn\ng\n\nl\ni\nb\ns')
    @commands.command()
    async def helloworld(self, ctx):
        '''replies with 'Hello World!' '''
        await ctx.send('Hello World!')

#cog setup
def setup(bot):
    bot.add_cog(GitOperations(bot))
