from discord.ext import commands
import asyncio
import config
from cogs.utils import gear_finder, schedule, squad


class Splatoon:
    """Splatoon related commands."""
    def __init__(self, bot):
        self.bot = bot
        self.gear_finder = gear_finder.GearFinder()
        self.scheduler = schedule.Schedule()
        self.squad_maker = squad.Squad()
        self.maps = []
        with open(config.HOME + 'maps.txt', 'r') as f:
            for line in f:
                self.maps.append(line.rstrip())
        self.modes = []
        with open(config.HOME + 'modes.txt', 'r') as f:
            for line in f:
                self.modes.append(line.rstrip())

    @commands.command(aliases=['maps', 'rotation'])
    @asyncio.coroutine
    def current(self):
        """Fetches the current map rotation in Splatoon."""
        yield from self.bot.say(self.scheduler.maps(0))

    @commands.command(aliases=['nextmaps'])
    @asyncio.coroutine
    def next(self):
        """Fetches the upcoming map rotation in Splatoon."""
        yield from self.bot.say(self.scheduler.maps(1))

    @commands.command(hidden=True, aliases=['lastmaps'])
    @asyncio.coroutine
    def future(self):
        """Fetches the future map rotation in Splatoon"""
        yield from self.bot.say(self.scheduler.maps(2))

    @commands.command()
    @asyncio.coroutine
    def schedule(self):
        """Fetches the current Splatoon rotation schedule."""
        yield from self.bot.say(self.scheduler.maps())

    @commands.command(aliases=['find', 'findgear'])
    @asyncio.coroutine
    def gear(self, *desired: str):
        """Find all gear with the specified perks.

        Use quotes around each perk name and the full text used in-game ("Ink Saver (Sub)").
        Up to 6 perks can be queried.
        """
        yield from self.bot.say(self.gear_finder.find_abilities(desired))

    @commands.command()
    @asyncio.coroutine
    def define(self, desired: str):
        """Look up information on gear and weapons."""
        yield from self.bot.say(self.gear_finder.define_gear(desired))

    @commands.group(pass_context=True)
    @asyncio.coroutine
    def squad(self, ctx):
        """Generate random teams of four from a give pool.

        Use the "create" subcommand to initialize a new squad,
        then use "next" to generate new squads.
        """
        if ctx.invoked_subcommand is None:
            yield from self.bot.say('No subcommand provided!')

    @squad.command(name='new', aliases=['create'])
    @asyncio.coroutine
    def _new_squad(self, *members: str):
        """Generate a new squad with the provided members.

        Members can have spaces when using quotes around each member.
        """
        yield from self.bot.say(self.squad_maker.new_squad(members))

    @squad.command(name='add')
    @asyncio.coroutine
    def _add_squad(self, member: str):
        """Add a member to the existing squad member pool."""
        yield from self.bot.say(self.squad_maker.add_member(member))

    @squad.command(name='remove', help='Remove a player from the pool')
    @asyncio.coroutine
    def _remove_squad(self, member: str):
        """Remove a member from the existing squad member pool."""
        yield from self.bot.say(self.squad_maker.remove_member(member))

    @squad.command(name='next', help='Generate the next team')
    @asyncio.coroutine
    def _next_squad(self):
        """Generate the next squad using the current pool."""
        yield from self.bot.say(self.squad_maker.refresh_team())


def setup(bot):
    bot.add_cog(Splatoon(bot))
