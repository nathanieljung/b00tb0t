#this script starts the bot and loads all plugins. Plugins are located under /home/discordbot/discord/plugins
import discord

from discord.ext import commands

from io import FileIO
import json

import subprocess

from random import random

CONFIG_FILE='/home/discordbot/discord/config.json'
SAVE_FILE='/home/discordbot/discord/save.json'

bot = commands.Bot(command_prefix='!', description='b00tbot')

channel_log = dict()

config = False

def loadConfig(keys):
    if not config:
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
async def save(ctx)
    data = dict()
    data['channel_log'] = channel_log
    io = open(SAVE_FILE, 'w')
    json.dump(data, io)
    io.close()

@bot.command()
async def restart(ctx):
    await ctx.send('Restarting...')
    await save()
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
    
    if not message.channel.id in channel_log:
        channel_log[message.channel.id] = dict()
    
    if message.author.id != 773745805227982910:
        
        if message.content == 'F':
            channel_log[message.channel.id]['Fs']++
            if channel_log[message.channel.id]['Fs'] == 3:
                await message.channel.send('F')
        else:
            channel_log[message.channel.id]['Fs'] = 0
        
        autoreplies = loadConfig(['autoreplies'])
        for autoreply_key in autoreplies[0].keys():
            if autoreply_key in message.content:
                autoreply_options = autoreplies[0][autoreply_key]
                autoreply = autoreply_options[int(random()*len(autoreply_options))]
                await message.channel.send(autoreply)
        
        autoreactions = loadConfig(['autoreactions'])
        for autoreaction in autoreactions[0].keys():
            if autoreaction in message.content:
                await message.add_reaction(autoreactions[0][autoreaction])
    
    if int(random()*12) == 0:
        sixtyninefourtwenty = ['6️⃣', '9️⃣', '4️⃣', '2️⃣', '0️⃣']
        for react in sixtyninefourtwenty:
            await message.add_reaction(react)
    if message.content == 'test':
        await message.channel.send('https://cdn.discordapp.com/attachments/775772474621165588/778466913872379924/EnEJNYbXcAUsBT8.png')

bot.run(TOKEN, bot=True, reconnect=True)
