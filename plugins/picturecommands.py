#imports
import discord, random
from discord.ext import commands

class PictureCommands(commands.Cog):
    def __init(self, bot):
        self.bot = bot

    #Commands
    @commands.command()
    async def LFG(self, ctx):
        '''replies with 'LET'S FUCKING GO!' pic '''
        await ctx.send('https://media.discordapp.net/attachments/775772474621165588/778466913872379924/EnEJNYbXcAUsBT8.png?width=249&height=375')

def setup(bot):
    bot.add_cog(HangoutsCommands(bot))
