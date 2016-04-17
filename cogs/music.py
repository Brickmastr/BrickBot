from discord.ext import commands
from cogs.utils import playlist
from cogs.utils.yt_downloader import extract_info
import discord
import asyncio
import os
import config

if not discord.opus.is_loaded():
    discord.opus.load_opus('opus')


class Music:
    """Commands relating to playing music over Discord"""

    def __init__(self, bot):
        self.bot = bot
        self.auto_songs = asyncio.Queue()
        self.play_next_song = asyncio.Event()
        self.player = None
        self.current = None
        self.auto_play_list = playlist.PlayList()
        self.songs = asyncio.Queue()
        self.play_list = playlist.PlayList(False)

    def is_playing(self):
        return self.player is not None and self.player.is_playing()

    def toggle_next_song(self):
        self.bot.loop.call_soon_threadsafe(self.play_next_song.set)

    def get_next_auto_song(self):
        while len(self.auto_play_list.playlist) == 0:
            self.auto_play_list.shuffle()
        song = self.auto_play_list.playlist.popleft()
        yield from self.auto_songs.put(song)

    def get_next_song(self):
        song = self.play_list.playlist.popleft()
        yield from self.songs.put(song)

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

    @dj.command(name='auto-play')
    @asyncio.coroutine
    def auto_play(self):
        """Start playing music from the stored playlist!"""
        if self.is_playing():
            yield from self.bot.say('I\'m already playing a song!')
            return
        while True:
            yield from self.get_next_song()
            if not self.bot.is_voice_connected():
                yield from self.bot.say('I\'m not connected to a voice channel!')
                return
            self.play_next_song.clear()
            self.current = yield from self.auto_songs.get()
            print('"{0[title]}"'.format(self.current))
            self.player = yield from self.bot.voice.create_ytdl_player(self.current['url'], after=self.toggle_next_song)
            self.player.start()
            yield from self.bot.say('Playing "{0[title]}" added by {0[adder]}.'.format(self.current))
            yield from self.play_next_song.wait()

    @dj.command()
    @asyncio.coroutine
    def play(self):
        """Start playing music!"""
        if self.is_playing():
            yield from self.bot.say('I\'m already playing a song!')
            return
        while True:
            yield from self.get_next_song()
            if not self.bot.is_voice_connected():
                yield from self.bot.say('I\'m not connected to a voice channel!')
                return
            self.play_next_song.clear()
            self.current = yield from self.songs.get()
            print('"{0[title]}"'.format(self.current))
            self.player = yield from self.bot.voice.create_ytdl_player(self.current['url'], after=self.toggle_next_song)
            self.player.start()
            yield from self.bot.say('Playing "{0[title]}" added by {0[adder]}.'.format(self.current))
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

    @dj.command(pass_context=True)
    @asyncio.coroutine
    def next(self, ctx, url: str):
        """Adds a song to the playlist

        Pass a YouTube video link to add the song.
        """
        info = yield from extract_info(self.bot.loop, url, download=False)
        if not info:
            yield from self.bot.say('Unable to access a video from that link!')
            return

        msg = self.play_list.add_song(info['title'], url, ctx.message.author.name)
        yield from self.bot.say(msg)

    @dj.command(pass_context=True)
    @asyncio.coroutine
    def add(self, ctx, url: str):
        """Adds a song to the playlist for auto play

        Pass a YouTube video link to add the song.
        """
        info = yield from extract_info(self.bot.loop, url, download=False)
        if not info:
            yield from self.bot.say('Unable to access a video from that link!')
            return

        msg = self.auto_play_list.add_song(info['title'], url, ctx.message.author.name)
        yield from self.bot.say(msg)

    @dj.command()
    @asyncio.coroutine
    def remove(self, url: str):
        """Removes a song from the playlist for auto play

        Pass a YouTube video link to remove the song.
        """
        yield from self.bot.say(self.auto_play_list.remove_song(url))

    @dj.command()
    @asyncio.coroutine
    def shuffle(self):
        """Shuffles the songs in the auto playlist."""
        self.auto_play_list.shuffle()
        yield from self.bot.say('Playlist Shuffled.')

    @dj.command(aliases=['current', 'video'])
    @asyncio.coroutine
    def source(self):
        """Looks up the source video of the current song."""
        if self.current is None:
            yield from self.bot.say('No song currently playing.')
            return

        yield from self.bot.say('Currently playing: {0[url]}'.format(self.current))
        yield from self.bot.say('Added by {0[adder]}'.format(self.current))

    @dj.command()
    @asyncio.coroutine
    def skip(self):
        if self.player is not None:
            self.player.stop()
            self.player = None


def setup(bot):
    bot.add_cog(Music(bot))
