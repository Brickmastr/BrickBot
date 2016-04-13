import asyncio
import random
import time
import gear_finder
import schedule
import squad as s_maker
import tag as t_handler
import config
import discord
from discord.ext import commands


version = '7.0.4'

description = 'Brickmastr\'s personal Discord Bot.'
bot = commands.Bot(command_prefix='!', description=description)

gear_list = gear_finder.GearFinder()
tags = t_handler.TagHandler()
rotations = schedule.Schedule()
squad_maker = s_maker.Squad()

maps = []
with open(config.HOME + 'maps.txt', 'r') as f:
    for line in f:
        maps.append(line.rstrip())
modes = []
with open(config.HOME + 'modes.txt', 'r') as f:
    for line in f:
        modes.append(line.rstrip())


@bot.event
@asyncio.coroutine
def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


# --- HELLO COMMAND --- #

@bot.command()
@asyncio.coroutine
def hello():
    """Greets the user and displays current version."""
    msg = 'Greetings from BrickBot! My current version is **{}**'.format(version)
    yield from bot.say(msg)


# --- SCHEDULING COMMANDS --- #

@bot.command()
@asyncio.coroutine
def current():
    """Fetches the current map rotation in Splatoon."""
    yield from bot.say(rotations.maps(0))


@bot.command(name='next')
@asyncio.coroutine
def s_next():
    """Fetches the upcoming map rotation in Splatoon."""
    yield from bot.say(rotations.maps(1))


@bot.command()
@asyncio.coroutine
def future():
    """Fetches the future map rotation in Splatoon"""
    yield from bot.say(rotations.maps(2))


@bot.command()
@asyncio.coroutine
def schedule():
    """Fetches the current Splatoon rotation schedule."""
    yield from bot.say(rotations.maps())


# --- CHOOSE AND RANDOM --- #

@bot.command(help='Randomly select an entry from a list')
@asyncio.coroutine
def choose(*choices: str):
    """Randomly select an entry from multiple choices.

    You can use quotes to separate choices with spaces in them.
    """
    yield from bot.say(random.choice(choices))


@bot.group(name='random', pass_context=True)
@asyncio.coroutine
def shuffle(ctx):
    """Use an RNG to make choices."""
    if ctx.invoked_subcommand is None:
        yield from bot.say(random.randint(0, 101))


@shuffle.command(name='game')
@asyncio.coroutine
def _game():
    """Have RNG select a Splatoon Map and Mode."""
    md = random.choice(modes)
    mp = random.choice(maps)
    yield from bot.say('{} on {}'.format(md, mp))


@shuffle.command(name='map')
@asyncio.coroutine
def _map():
    """Have RNG select a Splatoon Map."""
    yield from bot.say(random.choice(maps))


@shuffle.command(name='mode')
@asyncio.coroutine
def _mode():
    """Have RNG select a Splatoon Mode."""
    yield from bot.say(random.choice(modes))


@shuffle.command(name='weapon')
@asyncio.coroutine
def _weapon():
    """Have RNG select a Splatoon Weapon"""
    w = [wpn[0] for wpn in gear_list.weapons]
    yield from bot.say(random.choice(w))


@shuffle.command(help='Generate a random number')
@asyncio.coroutine
def _number(minimum=0, maximum=100):
    """Displays a random number within an optional range"""
    if minimum >= maximum:
        yield from bot.say('Maximum is smaller than minimum')
    yield from bot.say(random.randint(minimum, maximum))


@shuffle.command(name='pin')
@asyncio.coroutine
def _pin(digits=4):
    """Have RNG generate a pin number.

    Defaults to four digits, but can be set. Maximum number of digits is 10.
    """
    if digits > 10:
        yield from bot.say('Too many digits! Max is 10.')
    else:
        yield from bot.say('{0:0{1}d}'.format(random.randint(0, 10**digits), digits))


# --- GEAR --- #

@bot.group(pass_context=True)
@asyncio.coroutine
def gear(ctx):
    """Look up information on gear in Splatoon."""
    if ctx.invoked_subcommand is None:
        yield from bot.say('Subcommand not found!')


@gear.command()
@asyncio.coroutine
def find(*desired: str):
    """Find all gear with the specified perks.

    Use quotes around each perk name and the full text used in-game ("Ink Saver (Sub)").
    Up to 6 perks can be queried.
    """
    yield from bot.say(gear_list.find_abilities(desired))


@gear.command()
@asyncio.coroutine
def define(desired: str):
    """Look up information on gear and weapons."""
    yield from bot.say(gear_list.define_gear(desired))


# --- TAG --- #

@bot.group(pass_context=True)
@asyncio.coroutine
def tag(ctx):
    """Tags text for later use.

    If a subcommand is not called, this will search for the tag and return it's text.
    """
    if ctx.invoked_subcommand is None:
        yield from bot.say(tags.read_tag(ctx.args[0]))


@tag.command(name='create', aliases=['add'])
@asyncio.coroutine
def _create(t: str, content: str):
    """Create a new tag."""
    yield from bot.say(tags.create_tag(t, content))


@tag.command(name='remove')
@asyncio.coroutine
def _remove(t: str):
    """Remove an existing tag."""
    yield from bot.say(tags.remove_tag(t))


# --- SQUAD --- #

@bot.group(pass_context=True)
@asyncio.coroutine
def squad(ctx):
    """Generate random teams of four from a give pool.

    Use the "create" subcommand to initialize a new squad,
    then use "next" to generate new squads.
    """
    if ctx.invoked_subcommand is None:
        yield from bot.say('No subcommand provided!')


@squad.command(name='new', help='Create a new pool of players to pick from')
@asyncio.coroutine
def _new_squad(*members: str):
    """Generate a new squad with the provided members.

    Members can have spaces when using quotes around each member.
    """
    yield from bot.say(squad_maker.new_squad(members))


@squad.command(name='add')
@asyncio.coroutine
def _add_squad(member: str):
    """Add a member to the existing squad member pool."""
    yield from bot.say(squad_maker.add_member(member))


@squad.command(name='remove', help='Remove a player from the pool')
@asyncio.coroutine
def _remove_squad(member: str):
    """Remove a member from the existing squad member pool."""
    yield from bot.say(squad_maker.remove_member(member))


@squad.command(name='next', help='Generate the next team')
@asyncio.coroutine
def _next_squad():
    """Generate the next squad using the current pool."""
    yield from bot.say(squad_maker.refresh_team())


# --- UTILITY FUNCTIONS --- #

@bot.command()
@asyncio.coroutine
def join(url: str):
    """Pass a Discord Invite URL to invite BrickBot to a new server!

    NOTE: This function currently does not work.
    """
    try:
        yield from bot.accept_invite(url)
    except discord.NotFound:
        yield from bot.say('The invite provided has expired or is invalid! Please try again.')
    except discord.HTTPException:
        yield from bot.say('The link provided did not work! Please try again.')
    else:
        yield from bot.say('Joined!')


while True:
    try:
        bot.run(config.TOKEN)
    except KeyboardInterrupt:
        print('Interrupted. Signing out.')
        bot.close()
        break
    except TimeoutError:
        print('Connection Timed Out. Reconnecting in 15 seconds...')
        time.sleep(15)
