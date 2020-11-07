#imports
import discord, random
from discord.ext import commands

class HangoutsCommands(commands.Cog):
    def __init(self, bot):
        self.bot = bot

    #Commands
    @commands.command()
    async def helloworld(self, ctx):
        '''replies with 'Hello World!' '''
        await ctx.send('Hello World!')

    @commands.command()
    async def geamswhen(self, ctx):
        choice = [
                    "games tonight for sure", 
                    "right after 'this thing' is finished", 
                    "crossing a river right now, one sec", 
                    "start it up, we'll join in a bit", 
                    "taking an indefinitely long test but will def play today", 
                    "you always flake, so I'll pass", 
                    "okay just pick a game that we all have", 
                    "not sure, lets ask John", 
                    "if Sam plays I'll play", 
                    "talking to grill, please wait", 
                    "okay, just wait for me", 
                    "sorry I unplugged the pie before I left town",
                    "*attempts to change subject",
                    "It's downloading, you should have told me yesterday",
                    "I deleted my games to save memory",
                    "my computer isn’t powerful enough to run that game",
                    "Let me take a quick nap first, I’ll set an alarm. *phone @ 5%",
                    "Yeah, let's play Street Fighter!... oh, you don't want to geam anymore?"
                 ]
        value = random.choice(choice)
        await ctx.send(value)

def setup(bot):
    bot.add_cog(HangoutsCommands(bot))
