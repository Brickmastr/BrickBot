from discord.ext import commands
import discord
import asyncio

if not discord.opus.is_loaded():
    discord.opus.load_opus('opus')


class Music:
    """Commands relating to playing music over Discord"""

    def __init__(self, bot):
        self.bot = bot
        self.songs = asyncio.Queue()
        self.play_next_song = asyncio.Event()
        self.player = None
        self.current = None

    def is_playing(self):
        return self.player is not None and self.player.is_playing()

    def toggle_next_song(self):
        self.bot.loop.call_soon_threadsafe(self.play_next_song.set)

    @commands.group(pass_context=True)
    @asyncio.coroutine
    def dj(self, ctx):
        """Base music player command."""
        if ctx.invoked_subcommand is None:
            yield from self.bot.say('You need to pass a valid subcommand! See `!help dj`')

    @dj.command(aliases=['connect'], pass_context=True)
    @asyncio.coroutine
    def join(self, ctx, channel: str):
        """Join a voice channel."""
        if self.bot.is_voice_connected():
            yield from self.bot.say('Already connected to a voice channel! Can\'t connect to another.')
            return
        check = lambda c: c.name == channel and c.type == discord.ChannelType.voice
        channel = discord.utils.find(check, ctx.message.server.channels)
        try:
            yield from self.bot.join_voice_channel(channel)
        except Exception as e:
            yield from self.bot.say('Cannot connect to that voice channel.')
            print(e)

    @dj.command(aliases=['disconnect'])
    @asyncio.coroutine
    def leave(self):
        """Leave a voice channel."""
        yield from self.bot.voice.disconnect()

    @dj.command()
    @asyncio.coroutine
    def play(self):
        """Start playing music!"""
        if self.is_playing():
            yield from self.bot.say('I\'m already playing a song!')
            return
        while True:
            if not self.bot.is_voice_connected():
                yield from self.bot.say('I\'m not connected to a voice channel!')
                return
            self.play_next_song.clear()
            self.current = yield from self.songs.get()
            self.player = self.bot.voice.create_ffmpeg_player(self.current, after=self.toggle_next_song)
            self.player.start()
            yield from self.bot.say('Playing "{}"'.format(self.current))
            yield from self.play_next_song.wait()

    @dj.command()
    @asyncio.coroutine
    def pause(self):
        """Pause any currently playing music."""
        if self.is_playing():
            self.player.pause()

    @dj.command()
    @asyncio.coroutine
    def resume(self):
        """Resume playing music after pausing."""
        if self.player is not None and not self.is_playing():
            self.player.resume()

    @dj.command()
    @asyncio.coroutine
    def next(self, filename: str):
        """Adds a song to the playlist queue"""
        yield from self.songs.put(filename)
        yield from self.bot.say('Sucessfully registered {}'.format(filename))


def setup(bot):
    bot.add_cog(Music(bot))
