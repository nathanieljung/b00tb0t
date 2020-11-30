#this script starts the bot and loads all plugins. Plugins are located under /home/discordbot/discord/plugins
import discord

from discord.ext import commands

from io import FileIO
import json

import subprocess

CONFIG_FILE='/home/discordbot/discord/config.json'

bot = commands.Bot(command_prefix='!', description='b00tbot')

def loadConfig(keys):
    returnList = []
    io = FileIO(CONFIG_FILE)
    config = json.load(io)
    for key in keys:
        returnList.append(config[key])
    return returnList
    

TOKEN = loadConfig(['TOKEN'])[0]

def loadPlugins():
    if __name__ == '__main__':
        io = FileIO(CONFIG_FILE)
        plugins = json.load(io)['plugins']
        for plugin in plugins:
            bot.load_extension('plugins.{}'.format(plugin))
            print('Loaded extension: {}'.format(plugin))

@bot.command()
async def restart(ctx):
    await ctx.send('Restarting...')
    subprocess.run('./restart.sh')

@bot.event
async def on_ready():
    print('\nLoading plugins...\n')
    loadPlugins()
    print('\nPlugins loaded!\n')
    print('Logged in as: {} - {}\nVersion: {}\n'.format(bot.user.name, bot.user.id, discord.__version__))
    await bot.change_presence(activity=discord.Game(name='N00by\'s Hentai Collection', type=1, url='https://twitch.tv/paymoneywubby'))
    print('Successfully logged in and booted!\n')

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    autoreplies = loadConfig(['autoreplies'])
    for autoreply_key in autoreplies[0].keys():
        if autoreply_key in message.content:
            await message.channel.send(autoreplies[0][autoreply_key])
    if message.content == 'test':
        await message.channel.send('Testing 1 2 3!')

bot.run(TOKEN, bot=True, reconnect=True)
