import asyncio
import time
import config
from discord.ext import commands
from cogs.utils import checks


description = 'Brickmastr\'s personal Discord Bot.'

initial_extensions = [
    'cogs.meta',
    'cogs.splatoon',
    'cogs.rng',
    'cogs.tags',
    'cogs.music'
]

bot = commands.Bot(command_prefix='!', description=description)


@bot.event
@asyncio.coroutine
def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print('Failed to load extension {}\n{} {}'.format(extension, type(e).__name__, e))


@bot.command(pass_context=True, hidden=True)
@checks.is_owner()
@asyncio.coroutine
def debug(ctx, *, code: str):
    """Evaluates code."""
    code = code.strip('` ')
    python = '```py\n{}\n```'
    result = None

    try:
        result = eval(code)
    except Exception as e:
        yield from bot.say(python.format(type(e).__name__ + ': ' + str(e)))
        return

    if asyncio.iscoroutine(result):
        result = yield from result

    yield from bot.say(python.format(result))


while True:
    try:
        bot.run(config.TOKEN)
    except KeyboardInterrupt:
        print('Interrupted. Signing out.')
        break
    except (TimeoutError, RuntimeError):
        print('Connection Timed Out. Reconnecting in 15 seconds...')
        time.sleep(15)
