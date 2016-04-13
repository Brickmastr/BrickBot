import asyncio
import time
import config
from discord.ext import commands


description = 'Brickmastr\'s personal Discord Bot.'

initial_extensions = [
    'cogs.meta'
    'cogs.splatoon'
    'cogs.rng'
    'cogs.tags'
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


while True:
    try:
        bot.run(config.TOKEN)
    except KeyboardInterrupt:
        print('Interrupted. Signing out.')
        break
    except TimeoutError:
        print('Connection Timed Out. Reconnecting in 15 seconds...')
        time.sleep(15)
