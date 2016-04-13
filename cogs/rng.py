from discord.ext import commands
import asyncio
import random as rng


class RNG:
    """Utilities that provide RNG"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @asyncio.coroutine
    def choose(self, *choices: str):
        """Randomly select an entry from multiple choices.

        You can use quotes to separate choices with spaces in them.
        """
        yield from self.bot.say(rng.choice(choices))

    @commands.group(pass_context=True)
    @asyncio.coroutine
    def random(self, ctx):
        """Use an RNG to make choices."""
        if ctx.invoked_subcommand is None:
            yield from self.bot.say(rng.randint(0, 101))

    @random.command()
    @asyncio.coroutine
    def game(self):
        """Have RNG select a Splatoon Map and Mode."""
        splatoon = self.bot.get_cog('Splatoon')
        if splatoon is None:
            yield from self.bot.say('Splatoon cog is not loaded.')
            return
        md = rng.choice(splatoon.modes)
        mp = rng.choice(splatoon.maps)
        yield from self.bot.say('{} on {}'.format(md, mp))

    @random.command(name='map')
    @asyncio.coroutine
    def _map(self):
        """Have RNG select a Splatoon Map."""
        splatoon = self.bot.get_cog('Splatoon')
        if splatoon is None:
            yield from self.bot.say('Splatoon cog is not loaded.')
            return
        yield from self.bot.say(rng.choice(splatoon.maps))

    @random.command()
    @asyncio.coroutine
    def mode(self):
        """Have RNG select a Splatoon Mode."""
        splatoon = self.bot.get_cog('Splatoon')
        if splatoon is None:
            yield from self.bot.say('Splatoon cog is not loaded.')
            return
        yield from self.bot.say(rng.choice(splatoon.modes))

    @random.command()
    @asyncio.coroutine
    def weapon(self):
        """Have RNG select a Splatoon Weapon"""
        splatoon = self.bot.get_cog('Splatoon')
        if splatoon is None:
            yield from self.bot.say('Splatoon cog is not loaded.')
            return
        w = [wpn[0] for wpn in splatoon.gear_finder.weapons]
        yield from self.bot.say(rng.choice(w))

    @random.command()
    @asyncio.coroutine
    def number(self, minimum=0, maximum=100):
        """Displays a random number within an optional range"""
        if minimum >= maximum:
            yield from self.bot.say('Maximum is smaller than minimum')
            return
        yield from self.bot.say(rng.randint(minimum, maximum))

    @random.command()
    @asyncio.coroutine
    def pin(self, digits=4):
        """Have RNG generate a pin number.

        Defaults to four digits, but can be set. Maximum number of digits is 10.
        """
        if digits > 10:
            yield from self.bot.say('Too many digits! Max is 10.')
        else:
            yield from self.bot.say('{0:0{1}d}'.format(rng.randint(0, 10**digits), digits))

    @random.command()
    @asyncio.coroutine
    def tag(self):
        """Displays a random tag."""
        tags = self.bot.get_cog('Tags')
        if tags is None:
            yield from self.bot.say('Tags cog not loaded!')
            return

        name = rng.choice(tags.tag_handler.tags.keys())
        t = tags.tag_handler.tags[name]
        yield from self.bot.say('Random tag: {}\n{}'.format(name, t))
