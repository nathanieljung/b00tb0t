#imports
import discord, random
from discord.ext import commands

#Credentials
TOKEN = 'NzczNzQ1ODA1MjI3OTgyOTEw.X6Ns7w.6FTnUEgypxB0OeCmLei2PBqcyGY'

#Create bot
client = commands.Bot(command_prefix='!')

#Startup information
@client.event
async def on_ready():
    print('Connected to bot: {}'.format(client.user.name))
    print('Bot ID: {}'.format(client.user.id))

#Commands
@client.command()
async def helloworld(ctx):
    await ctx.send('Hello World!')

@client.command()
async def geamswhen(ctx):
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
                                                                                                                                                            "Yeah, let's play Street Fighter!... oh, you don't want to geam anymore?"]
    value = random.choice(choice)
    await ctx.send(value)
#Run the bot
client.run(TOKEN)                                                              
