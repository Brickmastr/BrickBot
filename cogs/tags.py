from discord.ext import commands
import asyncio
from cogs.utils import tag


class Tags:
    """Commands to manage tags"""

    def __init__(self, bot):
        self.bot = bot
        self.tag_handler = tag.TagHandler()

    @commands.group(pass_context=True, invoke_without_command=True)
    @asyncio.coroutine
    def tag(self, ctx, *, name: str):
        """Tags text for later use.

        If a subcommand is not called, this will search for the tag and return it's text.
        """
        if ctx.invoked_subcommand is None:
            yield from self.bot.say(self.tag_handler.read_tag(name))

    @tag.command(name='create', aliases=['add'])
    @asyncio.coroutine
    def _create(self, t: str, content: str):
        """Create a new tag."""
        yield from self.bot.say(self.tag_handler.create_tag(t, content))

    @tag.command(name='remove')
    @asyncio.coroutine
    def _remove(self, t: str):
        """Remove an existing tag."""
        yield from self.bot.say(self.tag_handler.remove_tag(t))
