#imports
import discord
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

#Run the bot
client.run(TOKEN)
