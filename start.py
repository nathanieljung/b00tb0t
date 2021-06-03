#this script starts the bot and loads all plugins. Plugins are located under ./plugins
import discord

from discord.ext import commands

from io import FileIO
import json

import subprocess

from random import random
import os

#setup and config file variable setting
CONFIG_FILE='config.json'
SAVE_FILE='save.json'
config = False
channel_log = dict()
bot = commands.Bot(command_prefix='!', description='b00tbot')

def loadConfig(keys):
    #This function loads values from the main config file based on keys. It checks if there is a cached config to avoid unnecessary file reading
    global config
    if not config:
        io = FileIO(CONFIG_FILE)
        config = json.load(io)
    
    returnList = []
    for key in keys:
        returnList.append(config[key])
    return returnList

def loadPlugins():
    #This function gets the functions to load from the config file and adds them as extensions to the bot
    if __name__ == '__main__':
        plugins = loadConfig(['plugins'])[0]
        for plugin in plugins:
            bot.load_extension('plugins.{}'.format(plugin))
            print('\tLoaded extension: {}'.format(plugin))

@bot.command()
async def save(ctx, suppressOutput):
    #This function saves the state of the chats that the bot is in
    if not suppressOutput:
        await ctx.send('Saving...')
    data = dict()
    data['channel_log'] = channel_log
    io = open(SAVE_FILE, 'w')
    json.dump(data, io)
    io.close()
    
    io = open(CONFIG_FILE, 'w')
    json.dump(config, io)
    io.close()

    if not suppressOutput:
        await ctx.send('Saved')

@bot.command()
async def restart(ctx):
    #This function quits the bot and reloads it
    await ctx.send('Restarting...')
    await save(ctx, True)
    subprocess.run('./restart.sh')

def getPluginList():
    potentialplugins = os.listdir('./plugins')
    returnPlugins = []
    for pp in potentialplugins:
        if ".py" in pp:
            returnPlugins.append(pp[0:len(pp)-3])
        else: continue
    return returnPlugins

@bot.command()
async def listplugins(ctx):
    #This function gets all available plugins
    str ='```\n'
    loaded = []
    unloaded = []
    potentialplugins = getPluginList()
    for pp in potentialplugins:
        if pp in loadConfig(['plugins'])[0]:
            loaded.append(pp)
        else:
            unloaded.append(pp)
    str += 'Loaded Plugins:\n'
    for lp in loaded:
        str += '\t- ' + lp + '\n'
    str += 'Unloaded Plugins:\n'
    for up in unloaded:
        str += '\t- ' + up + '\n'
    str += '```'
    await ctx.send(str)

@bot.command()
async def loadplugins(ctx, *args):
    potentialplugins = getPluginList()
    loaded = []
    alreadyLoaded = []
    notLoaded = []
    for arg in args:
        if arg in potentialplugins:
            if arg not in loadConfig(['plugins'])[0]:
                config['plugins'].append(arg) #probably should make a setter for this
                bot.load_extension('plugins.{}'.format(arg))
                print('\tLoaded extension: {}'.format(arg))
                loaded.append(arg)
            else:
                alreadyLoaded.append(arg)
        else:
            notLoaded.append(arg)
    await save(ctx, True)
    returnString = ''
    if len(loaded) > 0:
        returnString += '**Loaded:** ' + ', '.join(loaded) + '\n'
    if len(alreadyLoaded) > 0:
        returnString += '**Not Loaded (already loaded):** ' + ', '.join(alreadyLoaded) + '\n'
    if len(notLoaded) > 0:
        returnString += '**Not Loaded (plugin does not exist):** ' + ', '.join(notLoaded) + '\n'
    await ctx.send(returnString)

@bot.event
async def on_ready():
    #This is the main startup function for the bot
    print('\n\nLoading save state...')
    io = open(SAVE_FILE, 'r')
    data = json.load(io)
    channel_log = data['channel_log']
    print('Save file loaded!\n')
    
    print('Loading plugins...')
    loadPlugins()
    print('Plugins loaded!\n')
    
    print('Logged in as: {} - {}\nVersion: {}\n'.format(bot.user.name, bot.user.id, discord.__version__))
    await bot.change_presence(activity=discord.Game(name='With My Emotions', type=1, url='https://twitch.tv/paymoneywubby'))
    print('Successfully logged in and booted!\n')

@bot.event
async def on_message(message):
    #This is the primary message handler for the bot. Default functionality not included in plugins is included here.
    await bot.process_commands(message)
    
    #The bot will respond with an 'F' (to pay respects) after three consecutive 'F's in a channel.
    if not message.channel.id in channel_log:
        channel_log[message.channel.id] = dict()
        channel_log[message.channel.id]['Fs'] = 0
    
    if message.author.id != 773745805227982910:
        
        if message.content == 'F':
            channel_log[message.channel.id]['Fs'] +=1
            if channel_log[message.channel.id]['Fs'] == 3:
                await message.channel.send('F')
        else:
            channel_log[message.channel.id]['Fs'] = 0
        
        #This causes the bot to auto-reply to messages containing certain keywords that are added to the main configuration file.
        autoreplies = loadConfig(['autoreplies'])
        for autoreply_key in autoreplies[0].keys():
            if autoreply_key in message.content:
                autoreply_options = autoreplies[0][autoreply_key]
                autoreply = autoreply_options[int(random()*len(autoreply_options))]
                await message.channel.send(autoreply)
        
        #This causes the bot to auto-react to messages containing certain keywords that are added to the main configuration file.
        autoreactions = loadConfig(['autoreactions'])
        for autoreaction in autoreactions[0].keys():
            if autoreaction in message.content:
                await message.add_reaction(autoreactions[0][autoreaction])
    
        #The bot has a 1 in 30 chance of reacting with 69420 to any given message because I am very mature.
        if int(random()*30) == 0:
            sixtyninefourtwenty = ['6️⃣', '9️⃣', '4️⃣', '2️⃣', '0️⃣']
            for react in sixtyninefourtwenty:
                await message.add_reaction(react)

#Getting the bot up and running
TOKEN = loadConfig(['TOKEN'])[0]
bot.run(TOKEN, bot=True, reconnect=True)
