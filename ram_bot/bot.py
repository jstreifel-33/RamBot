import os

import random
import html

import requests
import discord
from discord.ext import commands
from dotenv import load_dotenv

from ram_bot.trivia import TriviaGame

intents = discord.Intents().all()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!', intents=intents)

bot.add_cog(TriviaGame(bot))

#-- START UP ROUTINE --
@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)

    print(
        f'{bot.user.name} has connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
        )

    # members = '\n - '.join([member.name for member in guild.members])
    # print(f'Guild Members:\n - {members}')


#-- PROOF OF LIFE COMMAND --
@bot.command(name='rambot', help='hello world command')
async def hello_world(ctx):
    response = 'Hello world!'
    await ctx.send(response)


#-- DICE ROLLING COMMAND --
@bot.command(name='roll_dice', help='simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))


#-- ROLE PERMISSION TEST --
@bot.command(name='bot-thing')
@commands.has_role('bot-person')
async def bot_thing(ctx):
    response = 'bot-thing successful!'
    await ctx.send(response)
        

#-- ERROR HANDLING --
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')


#-- RUN --
bot.run(TOKEN)
