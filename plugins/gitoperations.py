#imports
import discord, random
from discord.ext import commands
import subprocess

class GitOperations(commands.Cog):
    def __init(self, bot):
        self.bot = bot

    #Commands
    @commands.command()
    async def grive(self, ctx):
        await ctx.send('s\ny\nn\nc\ni\nn\ng\n\nl\ni\nb\ns')
        output = subprocess.run('~/b00tb0t/grive.sh',encoding='ascii',check=True, stdout=subprocess.PIPE).stdout
        if 'ERROR: git not clean. Can\'t pull' in output:
            await ctx.send('GRIVE FAILED. UNCOMMITTED CHANGES ON PI.')
        else:
            await ctx.send('GRIVE SUCCESS')

#cog setup
def setup(bot):
    bot.add_cog(GitOperations(bot))
