from discord.ext.commands import Context
import re

def literal_message(message):
    message_string = message.content
    mentions = dict()
    if message.mentions:
        for mention in message.mentions:
            mentions[str(mention.id)] = mention.name
    if message.channel_mentions:
        for mention in message.channel_mentions:
            mentions[str(mention.id)] = mention.name
    if message.role_mentions:
        for mention in message.role_mentions:
            mentions[str(mention.id)] = mention.name
    if len(mentions) > 0:
        matches = re.finditer(r'<(@|#)(?:!|&|)(\d+)>', message_string)
        for match in matches:
            raw_mention = match.group(0)
            mention_type = match.group(1)
            mention_id = match.group(2)
            message_string = str.replace(message_string, raw_mention, '{}{}'.format(mention_type, mentions[mention_id]))
    return message_string