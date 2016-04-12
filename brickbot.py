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


version = '7.0.1'

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

@bot.command(help='Greets the user and displays current version')
@asyncio.coroutine
def hello():
    msg = 'Greetings from BrickBot! My current version is **{}**'.format(version)
    yield from bot.say(msg)


# --- SCHEDULING COMMANDS --- #

@bot.command(help='Gets the current maps and modes on Splatoon')
@asyncio.coroutine
def current():
    yield from bot.say(rotations.maps(0))


@bot.command(name='next', help='Gets the next maps and modes on Splatoon')
@asyncio.coroutine
def s_next():
    yield from bot.say(rotations.maps(1))


@bot.command(help='Gets the future maps and modes on Splatoon')
@asyncio.coroutine
def future():
    yield from bot.say(rotations.maps(2))


@bot.command(help='Gets the current Splatoon rotation forecast')
@asyncio.coroutine
def schedule():
    yield from bot.say(rotations.maps())


# --- CHOOSE AND RANDOM --- #

@bot.command(help='Randomly select an entry from a list')
@asyncio.coroutine
def choose(*choices: str):
    yield from bot.say(random.choice(choices))


@bot.group(name='random', pass_context=True, help='Randomly select from pre-defined lists or numbers')
@asyncio.coroutine
def shuffle(ctx):
    if ctx.invoked_subcommand is None:
        yield from bot.say(random.randint(0, 101))


@shuffle.command(name='game', help='Randomly select a map and mode combination in Splatoon')
@asyncio.coroutine
def _game():
    md = random.choice(modes)
    mp = random.choice(maps)
    yield from bot.say('{} on {}'.format(md, mp))


@shuffle.command(name='map', help='Randomly select a map in Splatoon')
@asyncio.coroutine
def _map():
    yield from bot.say(random.choice(maps))


@shuffle.command(name='mode', help='Randomly select a mode in Splatoon')
@asyncio.coroutine
def _mode():
    yield from bot.say(random.choice(maps))


@shuffle.command(name='weapon', help='Randomly select a weapon in Splatoon')
@asyncio.coroutine
def _weapon():
    w = [wpn[0] for wpn in gear_list.weapons]
    yield from bot.say(random.choice(w))


@shuffle.command(name='number', help='Randomly generate a random number between 0 and 100')
@asyncio.coroutine
def _number_a():
    yield from bot.say(random.randint(0, 101))


@shuffle.command(name='number1', help='Randomly generate a number less than the entered value')
@asyncio.coroutine
def _number_b(maximum: int):
    try:
        msg = random.randint(0, maximum)
    except (ValueError, TypeError):
        msg = 'Cannot evaluate "{}" as a number.'.format(maximum)
    yield from bot.say(msg)


@shuffle.command(name='number2', help='Randomly generate a number between two numbers')
@asyncio.coroutine
def _number_c(minimum: int, maximum: int):
    try:
        msg = random.randint(minimum, maximum)
    except (ValueError, TypeError):
        msg = 'Cannot evaluate "{}" or "{}" as a number.'.format(minimum, maximum)
    yield from bot.say(msg)


@shuffle.command(name='pin', help='Randomly generate a four-digit pin')
@asyncio.coroutine
def _pin():
    yield from bot.say('{:04d}'.format(random.randint(0, 10000)))


# --- GEAR --- #

@bot.group(pass_context=True, help='Look up information on gear in Splatoon')
@asyncio.coroutine
def gear(ctx):
    if ctx.invoked_subcommand is None:
        yield from bot.say('Subcommand not found!')


@gear.command(help='Find Splatoon gear with certain perk(s)')
@asyncio.coroutine
def find(*desired: str):
    yield from bot.say(gear_list.find_abilities(desired))


@gear.command(help='Learn about brand perks, gear abilities weapon kits')
@asyncio.coroutine
def define(desired: str):
    yield from bot.say(gear_list.define_gear(desired))


# --- TAG --- #

@bot.group(pass_context=True, help='Create shortcuts to links')
@asyncio.coroutine
def tag(ctx, t: str):
    if ctx.invoked_subcommand is None:
        yield from bot.say(tags.read_tag(t))


@tag.command(name='create', help='Create a shortcut to a link')
@asyncio.coroutine
def _create(t: str, content: str):
    yield from bot.say(tags.create_tag(t, content))


@tag.command(name='remove', help='Remove an existing shortcut to a link')
@asyncio.coroutine
def _remove(t: str):
    yield from bot.say(tags.remove_tag(t))


# --- SQUAD --- #

@bot.group(pass_context=True, help='Generate random teams of four from a given pool')
@asyncio.coroutine
def squad(ctx):
    if ctx.invoked_subcommand is None:
        yield from bot.say('No context provided!')


@squad.command(name='new', help='Create a new pool of players to pick from')
@asyncio.coroutine
def _new_squad(*members: str):
    yield from bot.say(squad_maker.new_squad(members))


@squad.command(name='add', help='Add a player to the pool')
@asyncio.coroutine
def _add_squad(member: str):
    yield from bot.say(squad_maker.add_member(member))


@squad.command(name='remove', help='Remove a player from the pool')
@asyncio.coroutine
def _remove_squad(member: str):
    yield from bot.say(squad_maker.remove_member(member))


@squad.command(name='next', help='Generate the next team')
@asyncio.coroutine
def _next_squad():
    yield from bot.say(squad_maker.refresh_team())


# --- UTILITY FUNCTIONS --- #

@bot.command(help='Tell the bot to join a new server')
@asyncio.coroutine
def join(url: str):
    try:
        bot.accept_invite(url)
    except discord.NotFound:
        bot.say('The invite provided has expired or is invalid! Please try again.')
    except discord.HTTPException:
        bot.say('The link provided did not work! Please try again.')
    else:
        bot.say('Joined!')


while True:
    try:
        bot.run(config.TOKEN)
    except KeyboardInterrupt:
        print('Interrupted. Signing out.')
        bot.logout()
        break
    except TimeoutError:
        print('Connection Timed Out. Reconnecting in 15 seconds...')
        time.sleep(15)
