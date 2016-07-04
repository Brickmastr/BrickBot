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
    def game(self, incluce_tw='No', blacklist='Yes'):
        """Have RNG select a Splatoon Map and Mode.

        include_tw: 'Yes' to include turf war as a mode option
        blacklist: 'No' to include all map mode combinations, (default excludes rotations like RM Blackbelly)
        """
        splatoon = self.bot.get_cog('Splatoon')
        if splatoon is None:
            yield from self.bot.say('Splatoon cog is not loaded.')
            return
        mp = rng.choice(splatoon.maps)
        md = rng.choice(splatoon.modes)
        while incluce_tw == 'No' and md == 'Turf War' or [md, mp] in splatoon.blacklist and blacklist == 'Yes':
            mp = rng.choice(splatoon.maps)
            md = rng.choice(splatoon.modes)
        yield from self.bot.say('{} on {}'.format(md, mp))

    @random.command(invoke_without_command=True)
    @asyncio.coroutine
    def scrim(self, matches=9, blacklist='Yes'):
        """Have RNG select a number of Splatoon matches to play out.

        matches: number of matches to generate
        blacklist: 'No' to include all map mode combinations, (default excludes rotations like RM Blackbelly)
        """
        splatoon = self.bot.get_cog('Splatoon')
        if splatoon is None:
            yield from self.bot.say('Splatoon cog is not loaded.')
            return
        match_list = []
        modes = list(splatoon.modes)
        modes.remove('Turf War')
        rng.shuffle(splatoon.modes)
        used_maps = []
        for match in range(matches):
            md = modes[match % 3]
            mp = rng.choice(splatoon.maps)
            while [md, mp] in splatoon.blacklist and blacklist.lower() == 'yes' or mp in used_maps:
                mp = rng.choice(splatoon.maps)
            used_maps.append(mp)
            match_list.append('{} on {}'.format(md, mp))
        yield from self.bot.say('\n'.join(match_list))

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
    def mode(self, incluce_tw: str='No'):
        """Have RNG select a Splatoon Mode.

        Pass the optional argument as "yes" to include turf war.
        """
        splatoon = self.bot.get_cog('Splatoon')
        if splatoon is None:
            yield from self.bot.say('Splatoon cog is not loaded.')
            return
        choice = rng.choice(splatoon.modes)
        while incluce_tw == 'No' and choice == 'Turf War':
            choice = rng.choice(splatoon.modes)
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
    def number(self, minimum: int=0, maximum: int=100):
        """Displays a random number within an optional range"""
        if minimum >= maximum:
            yield from self.bot.say('Maximum is smaller than minimum')
            return
        yield from self.bot.say(rng.randint(minimum, maximum))

    @random.command()
    @asyncio.coroutine
    def pin(self, digits: int=4):
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


def setup(bot):
    bot.add_cog(RNG(bot))
