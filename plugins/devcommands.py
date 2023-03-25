#imports
import json
import os
from discord.ext import commands

config = {'Details': 'Config cannot currently be loaded.'}

class DevCommands(commands.Cog):
    def __init(self, bot):
        self.bot = bot

    def verifyDevChannel(ctx):
        return ctx.channel.id == 778654436909776906

    
    @commands.command()
    async def viewconfig(self, ctx):
        stritem = '```json\n'
        stritem += json.dumps(config, indent=4)
        stritem += '\n```'
        await ctx.send(stritem)

    @commands.command()
    async def grive(self, ctx):
        os.system('git checkout main && git pull')

def setup(bot):
    bot.add_cog(DevCommands(bot))