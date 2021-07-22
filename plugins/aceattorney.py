#imports
from discord.ext.commands.core import command

from discord.ext import commands
from discord.ext.commands import Context as context


from collections import Counter

import anim, os, discord

class DiscordAuthor:
        def __init__(self, name):
            self.name = name

class DiscordComment:
    def __init__(self, username: str, text: str, score: int = 0, img: str = None):
        self.author = DiscordAuthor(username)
        self.body = text
        self.score = score
        self.img = img

def process_comment(message):
    img = None
    attachment = None
    if message.attachments:
        attachment = message.attachments.pop()
        type, extension = attachment.content_type.split('/')
        if type == 'image':
            if not message.content:
                message.content = 'Behold! My evidence.'
            img = attachment.filename
        elif not message.content:
            message.content = '{}s aren\'t supported, but I have evidence anyway...'.format(extension)
        else:
            message.content += ' <' + attachment.filename + '>'
    return message.author.name, message.content, img, attachment

def cleanupfiles(comment: str):
    if comment:
        os.remove(comment)

class AceAttorney(commands.Cog):
    def __init(self, bot):
        self.bot = bot

    #Commands
    @commands.command()
    async def acecourt(self, ctx: context, num_comments: int):
        basemessage = ctx.message.reference.resolved if ctx.message.reference else ctx.message
        unames = []
        origcomments = []
        imgs = []
        if not basemessage.id == ctx.message.id:
            num_comments -= 1
            uname, comment, img, attachment = process_comment(basemessage)
            if img:
                await attachment.save(attachment.filename)
            unames.append(uname)
            origcomments.append(comment)
            imgs.append(img)
        history = ctx.channel.history(limit=num_comments, oldest_first=False, before=basemessage)
        async for message in history:
            uname, comment, img, attachment = process_comment(message)
            if img:
                await attachment.save(attachment.filename)
            unames.append(uname)
            origcomments.append(comment)
            imgs.append(img)            

        cnt = Counter(unames)
        most_common_pair = cnt.most_common(len(cnt))
        most_common = []
        for a, b in most_common_pair:
            most_common.append(a)
        
        characters = anim.get_characters(most_common=most_common)
        comments = []
        for uname, comment, img in zip(unames, origcomments, imgs):
            comments.append(DiscordComment(uname, comment, img=img))
        comments.reverse()
        anim.comments_to_scene(comments, characters, output_filename="ace.mp4")
        fileSize = os.path.getsize("ace.mp4")
        if fileSize < ctx.channel.guild.filesize_limit:
            await ctx.send(content="", file=discord.File("ace.mp4"))
        else:
            ctx.send("The resulting filesize is too big to send.")
        for img in imgs:
            cleanupfiles(img)

def setup(bot):
    bot.add_cog(AceAttorney(bot))
