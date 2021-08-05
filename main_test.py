import unittest

class TestingClass(unittest.TestCase):
    def test_first(self):
        testvar = 9 + 1
        self.assertEqual(10, testvar)

    def test_aceattorney_plugin(self):
        from plugins import aceattorney

    def test_hangoutscommands_plugin(self):
        from plugins import hangoutscommands

    def test_picturecommands_plugin(self):
        from plugins import picturecommands

    def test_aceattorney_animation(self):
        import anim

        class DiscordAuthor:
            def __init__(self, name):
                self.name = name

        class DiscordComment(object):
            def __init__(self, username: str, text: str, score: int = 0, img: str = None):
                self.author = DiscordAuthor(username)
                self.body = text
                self.score = score
                self.img = img

        most_common = ['a', 'b', 'c'] # usernames in order of freq
        characters = anim.get_characters(most_common) # returns a dict where key = character, val = username
        comments = [
            DiscordComment('a', 'Hello as I am the most common I will be Phoenix'),
            DiscordComment('b', 'wassup I\'m edgyboy', score=-1),
            DiscordComment('c', 'I\'m someone random and I\'m angry')
        ]
        anim.comments_to_scene(comments, characters, output_filename="hello.mp4")
    
unittest.main()