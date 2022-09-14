#imports
import discord, random, os
from discord.ext import commands

class PictureCommands(commands.Cog):
    def __init(self, bot):
        self.bot = bot

    #Commands
    @commands.command()
    async def LFG(self, ctx):
        '''replies with 'LET'S FUCKING GO!' pic '''
        await ctx.send('https://media.discordapp.net/attachments/775772474621165588/778466913872379924/EnEJNYbXcAUsBT8.png?width=249&height=375')

    @commands.command()
    async def delet(self, ctx):
        '''replies with a random delet image'''
        picture = discord.File('./plugins/delet/{}'.format(random.choice(os.listdir('./plugins/delet'))))
        await ctx.send(file=picture)
def setup(bot):
    bot.add_cog(PictureCommands(bot))
