#imports
from discord.ext.commands.core import command

from discord.ext import commands, Context as context

from collections import Counter

import anim, os, discord

class DiscordAuthor:
        def __init__(self, name):
            self.name = name

class DiscordComment:
    def __init__(self, username: str, text, str, score: int = 0):
        self.author = DiscordAuthor(username)
        self.body = text
        self.score = score

class AceAttorney(commands.Cog):
    def __init(self, bot):
        self.bot = bot

    #Commands
    @commands.command()
    async def lastmessages(self, ctx, num_comments):
        to_send = ''
        history = ctx.channel.history(limit=int(num_comments))
        await history.next()
        async for message in history:
            to_send += message.author.name + ': ' + message.content + '\n'
        await ctx.send(to_send)

    @commands.command()
    async def acecourt(self, ctx: context, num_comments: int):
        unames = []
        origcomments = []
        history = ctx.channel.history(limit=num_comments + 1)
        await history.next()
        async for message in history:
            unames.append(message.author.name)
            origcomments.append(message.content)
        cnt = Counter(unames)
        most_common_pair = cnt.most_common(len(cnt))
        most_common = []
        for a, b in most_common_pair:
            most_common.append(a)
        
        characters = anim.get_characters(most_common=most_common)
        comments = []
        for uname, comment in zip(unames, origcomments):
            comments.append(DiscordComment(uname, comment))
        comments.reverse()
        anim.comments_to_scene(comments, characters, output_filename="ace.mp4")
        fileSize = os.path.getsize("ace.mp4")
        if fileSize < ctx.channel.guild.filesize_limit:
            await ctx.send(content="", file=discord.File("ace.mp4"))
        else:
            ctx.send("The resulting filesize is too big to send.")

def setup(bot):
    bot.add_cog(AceAttorney(bot))
