#this script starts the bot and loads all plugins. Plugins are located under /home/discordbot/discord/plugins
import discord

from discord.ext import commands

from io import FileIO
import json

CONFIG_FILE='/home/discordbot/discord/config.json'
TOKEN = 'NzczNzQ1ODA1MjI3OTgyOTEw.X6Ns7w.6FTnUEgypxB0OeCmLei2PBqcyGY'

bot = commands.Bot(command_prefix='!', description='b00tbot')

def loadPlugins():
    if __name__ == '__main__':
        io = FileIO(CONFIG_FILE)
        plugins = json.load(io)['plugins']
        for plugin in plugins:
            bot.load_extension('plugins.{}'.format(plugin))
            print('Loaded extension: {}'.format(plugin))

@bot.event
async def on_ready():
    print('\nLoading plugins...\n')
    loadPlugins()
    print('\nPlugins loaded!\n')
    print('Logged in as: {} - {}\nVersion: {}\n'.format(bot.user.name, bot.user.id, discord.__version__))
    await bot.change_presence(activity=discord.Game(name='N00by\'s Hentai Collection', type=1, url='https://twitch.tv/paymoneywubby'))
    print('Successfully logged in and booted!\n')

bot.run(TOKEN, bot=True, reconnect=True)
