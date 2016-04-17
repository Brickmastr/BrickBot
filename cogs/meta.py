from discord.ext import commands
import discord
import asyncio


class Meta:
    """Commands related to Discord or BrickBot itself"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @asyncio.coroutine
    def hello(self):
        """Greets the user and displays current version."""
        msg = 'Greetings from BrickBot! My current version is **8.1.0**'
        yield from self.bot.say(msg)

    @commands.command()
    @asyncio.coroutine
    def join(self, url: str):
        """Pass a Discord Invite URL to invite BrickBot to a new server!

        NOTE: This function currently does not work.
        """
        try:
            yield from self.bot.accept_invite(url)
        except discord.NotFound:
            yield from self.bot.say('The invite provided has expired or is invalid! Please try again.')
        except discord.HTTPException:
            yield from self.bot.say('The link provided did not work! Please try again.')
        else:
            yield from self.bot.say('Joined!')


def setup(bot):
    bot.add_cog(Meta(bot))
