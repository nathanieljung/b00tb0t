#this script starts the bot and loads all plugins. Plugins are located under ./plugins
from botutils import literal_message
import discord

from discord.ext import commands

from discord_slash import SlashCommand
from discord_slash.utils import manage_commands
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.http import SlashCommandRequest

from io import FileIO
import json, pickle

import subprocess

from random import random
import os

def getPluginList():
    potentialplugins = os.listdir('./plugins')
    returnPlugins = []
    for pp in potentialplugins:
        if ".py" in pp:
            returnPlugins.append(pp[0:len(pp)-3])
        else: continue
    return returnPlugins

def loadConfig(keys):
    #This function loads values from the main config file based on keys. It checks if there is a cached config to avoid unnecessary file reading
    global config
    if not config:
        io = FileIO(CONFIG_FILE)
        config = json.load(io)
    
    returnList = []
    for key in keys:
        returnitem = config[key]
        if isinstance(returnitem, str) and returnitem[0:7]=='!secret':
            returnitem = loadSecret(returnitem[8:])
        returnList.append(returnitem)
    return returnList

#setup and config file variable setting
CONFIG_FILE='config.json'
SAVE_FILE='save.json'
SECRET_FILE='secrets.json'
config = False
channel_log = dict()
loadedPlugins = []
unloadedPlugins = []
bot = commands.Bot(command_prefix='!', description='b00tbot')


potentialplugins = getPluginList()
for pp in potentialplugins:
    if pp in loadConfig(['plugins'])[0]:
        loadedPlugins.append(create_choice(pp, pp))
    else:
        unloadedPlugins.append(create_choice(pp, pp))

slash = SlashCommand(bot, sync_commands=True)

def loadSecret(key):
    io = FileIO(SECRET_FILE)
    secrets = json.load(io)
    return secrets[key]

async def refreshPlugins():
    slash.commands.pop('unloadplugin')
    slash.commands.pop('loadplugin')
    await slash.sync_all_commands()
    slash.add_slash_command(unloadplugin, name="unloadplugin", 
                description="Allows you to remove any number of available plugins to the current instance of bot", 
                options=[create_option(name="plugin", description="This is the plugin to unload.", option_type=3, required=False, choices=loadedPlugins)], 
                guild_ids=guild_ids)
    slash.add_slash_command(loadplugin, name="loadplugin", 
                description="Allows you to add any number of available plugins to the current instance of bot", 
                options=[create_option(name="plugin", description="This is the plugin to load.", option_type=3, required=False, choices=unloadedPlugins)], 
                guild_ids=guild_ids)
    await slash.sync_all_commands()

def loadPlugins():
    #This function gets the functions to load from the config file and adds them as extensions to the bot
    if __name__ == '__main__':
        plugins = loadConfig(['plugins'])[0]
        for plugin in plugins:
            bot.load_extension('plugins.{}'.format(plugin))
            print('\tLoaded extension: {}'.format(plugin))


guild_ids = loadConfig(['slash_channels'])[0]
bot_id = loadConfig(['bot_id'])[0]

@bot.event
async def on_ready():
    #This is the main startup function for the bot
    try:
        print('\n\nLoading save state...')
        io = open(SAVE_FILE, 'r')
        data = json.load(io)
        channel_log = data['channel_log']
        print('Save file loaded!\n')
    except:
        print('No save file found. Either this is a first run or save file was deleted.')
    
    print('Loading plugins...')
    loadPlugins()
    print('Plugins loaded!\n')
    
    print('Logged in as: {} - {}\nVersion: {}\n'.format(bot.user.name, bot.user.id, discord.__version__))
    await bot.change_presence(activity=discord.Game(name='With My Emotions', type=1, url='https://twitch.tv/paymoneywubby'))
    print('Successfully logged in and booted!\n')

@slash.slash(name="listplugins", description="This function gets all available plugins", guild_ids=guild_ids)
async def listplugins(ctx):
    '''This function gets all available plugins'''
    stritem ='```\n'
    loaded = []
    unloaded = []
    potentialplugins = getPluginList()
    for pp in potentialplugins:
        if pp in loadConfig(['plugins'])[0]:
            loaded.append(pp)
        else:
            unloaded.append(pp)
    stritem += 'Loaded Plugins:\n'
    for lp in loaded:
        stritem += '\t- ' + lp + '\n'
    stritem += 'Unloaded Plugins:\n'
    for up in unloaded:
        stritem += '\t- ' + up + '\n'
    stritem += '```'
    await ctx.send(stritem)

@bot.command()
async def savestate(ctx, suppressOutput):
    '''This function saves the state of the chats that the bot is in'''
    if not suppressOutput:
        await ctx.send('Saving...')
    data = dict()
    data['channel_log'] = channel_log
    io = open(SAVE_FILE, 'w')
    json.dump(data, io, indent=4)
    io.close()
    
    io = open(CONFIG_FILE, 'w')
    json.dump(config, io, indent=4)
    io.close()

    if not suppressOutput:
        await ctx.send('Saved')

@slash.slash(name="restart", description="This function quits the bot and reloads it", guild_ids=guild_ids)
async def restart(ctx):
    '''This function quits the bot and reloads it'''
    with open('ctx.cfg', 'wb') as ctxfile:
        pickle.dump(ctx, ctxfile)
    await ctx.send('Restarting...')
    await savestate(ctx, True)
    subprocess.run('./restart.sh')

@slash.slash(   name="loadplugin", 
                description="Allows you to add any number of available plugins to the current instance of bot", 
                options=[create_option(name="plugin", description="This is the plugin to load.", option_type=3, required=False, choices=unloadedPlugins)], 
                guild_ids=guild_ids)
async def loadplugin(ctx, plugin: str):
    '''Allows you to add any number of available plugins to the current instance of bot'''
    potentialplugins = getPluginList()
    loaded = []
    alreadyLoaded = []
    notLoaded = []
    if plugin in potentialplugins:
        if plugin not in loadConfig(['plugins'])[0]:
            await ctx.send('Loading **{}**. Please have patience, this may take a while...'.format(plugin))
            config['plugins'].append(plugin) #probably should make a setter for this
            bot.load_extension('plugins.{}'.format(plugin))
            print('\tLoaded extension: {}'.format(plugin))
            loadedPlugins.append(create_choice(plugin, plugin))
            for i in range(len(unloadedPlugins)):
                if unloadedPlugins[i]['value'] == plugin:
                    unloadedPlugins.pop(i)
                    break
            loaded.append(plugin)
        else:
            alreadyLoaded.append(plugin)
    else:
        notLoaded.append(plugin)
    await savestate(ctx, True)
    returnString = ''
    if len(loaded) > 0:
        returnString += '**Loaded:** ' + ', '.join(loaded) + '\n'
    if len(alreadyLoaded) > 0:
        returnString += '**Not Loaded (already loaded):** ' + ', '.join(alreadyLoaded) + '\n'
    if len(notLoaded) > 0:
        returnString += '**Not Loaded (plugin does not exist):** ' + ', '.join(notLoaded) + '\n'
    await ctx.send(returnString)
    await refreshPlugins()

@slash.slash(   name="unloadplugin", 
                description="Allows you to remove any number of available plugins to the current instance of bot", 
                options=[create_option(name="plugin", description="This is the plugin to unload.", option_type=3, required=False, choices=loadedPlugins)], 
                guild_ids=guild_ids)
async def unloadplugin(ctx, plugin: str):
    '''Allows you to remove any number of available plugins to the current instance of bot'''
    potentialplugins = getPluginList()
    unloaded = []
    alreadyUnloaded = []
    notUnloaded = []
    if plugin in potentialplugins:
        if plugin in loadConfig(['plugins'])[0]:
            config['plugins'].remove(plugin) #this is terrible and naive
            bot.unload_extension('plugins.{}'.format(plugin))
            print('\tUnloaded extension: {}'.format(plugin))
            unloadedPlugins.append(create_choice(plugin, plugin))
            for i in range(len(loadedPlugins)):
                if loadedPlugins[i]['value'] == plugin:
                    loadedPlugins.pop(i)
                    break
            unloaded.append(plugin)
        else:
            alreadyUnloaded.append(plugin)
    else:
        notUnloaded.append(plugin)
    await savestate(ctx, True)
    returnString = ''
    if len(unloaded) > 0:
        returnString += '**Unloaded:** ' + ', '.join(unloaded) + '\n'
    if len(alreadyUnloaded) > 0:
        returnString += '**Not Unloaded (already unloaded):** ' + ', '.join(alreadyUnloaded) + '\n'
    if len(notUnloaded) > 0:
        returnString += '**Not Unloaded (plugin does not exist):** ' + ', '.join(notUnloaded) + '\n'

    await ctx.send(returnString)
    await refreshPlugins()
        
@slash.slash(name="viewconfig", description="Prints config.json", guild_ids=guild_ids)
async def viewconfig(ctx):
    stritem = '```json\n'
    stritem += json.dumps(config, indent=4)
    stritem += '\n```'
    await ctx.send(stritem)

@bot.event
async def on_message(message):
    #This is the primary message handler for the bot. Default functionality not included in plugins is included here.
    await bot.process_commands(message)
    
    if message.author.id != bot_id:
        message_literal_content = literal_message(message)
        last_three = await message.channel.history(limit=3).flatten()
        if len(last_three) >= 3:
            if last_three[0].content == last_three[1].content == last_three[2].content and last_three[0].author.id != bot_id and last_three[1].author.id != bot_id and last_three[2].author.id != bot_id:
                await message.channel.send(last_three[0].content)
        
        #This causes the bot to auto-reply to messages containing certain keywords that are added to the main configuration file.
        autoreplies = loadConfig(['autoreplies'])
        for autoreply_key in autoreplies[0].keys():
            if autoreply_key in message_literal_content:
                autoreply_options = autoreplies[0][autoreply_key]
                autoreply = autoreply_options[int(random()*len(autoreply_options))]
                await message.channel.send(autoreply)
        
        #This causes the bot to auto-react to messages containing certain keywords that are added to the main configuration file.
        autoreactions = loadConfig(['autoreactions'])
        for autoreaction in autoreactions[0].keys():
            if autoreaction in message_literal_content:
                await message.add_reaction(autoreactions[0][autoreaction])
    
        #The bot has a 1 in 30 chance of reacting with 69420 to any given message because I am very mature.
        if int(random()*30) == 0:
            sixtyninefourtwenty = ['6️⃣', '9️⃣', '4️⃣', '2️⃣', '0️⃣']
            for react in sixtyninefourtwenty:
                await message.add_reaction(react)

#Getting the bot up and running
TOKEN = loadConfig(['TOKEN'])[0]
bot.run(TOKEN, bot=True, reconnect=True)
