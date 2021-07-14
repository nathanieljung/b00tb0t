import anim

class DiscordAuthor:
    def __init__(self, name):
        self.name = name

class DiscordComment(object):
    def __init__(self, username: str, text: str, score: int = 0):
        self.author = DiscordAuthor(username)
        self.body = text
        self.score = score

most_common = ['a', 'b', 'c'] # usernames in order of freq
characters = anim.get_characters(most_common) # returns a dict where key = character, val = username
comments = [
    DiscordComment('a', 'Hello as I am the most common I will be Phoenix'),
    DiscordComment('b', 'wassup I\'m edgyboy', score=-1),
    DiscordComment('c', 'I\'m someone random and I\'m angry')
]
anim.comments_to_scene(comments, characters, output_filename="hello.mp4")
