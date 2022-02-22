import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents().all()
# client = discord.Bot(prefix = '', intents=intents)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)

    print(
        f'{bot.user.name} has connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
        )

    # members = '\n - '.join([member.name for member in guild.members])
    # print(f'Guild Members:\n - {members}')

#proof of life command
@bot.command(name='rambot', help='hello world command')
async def hello_world(ctx):
    response = 'Hello world!'
    await ctx.send(response)

@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

bot.run(TOKEN)