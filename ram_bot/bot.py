import os

import random
import json
import html

import requests
import discord
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents().all()

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


@bot.command(name='roll_dice', help='simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))


@bot.command(name='bot-thing')
@commands.has_role('bot-person')
async def bot_thing(ctx):
    response = 'bot-thing successful!'
    await ctx.send(response)


@bot.command()
async def trivia(ctx, category: str, num_questions: int):

    categories = {
        "general":9,
        "film":11,
        "music":12,
        "art":25,
        "history":23,
        "geography":22,
        "sports":21
    }

    if category not in categories:
        await ctx.send(f'Invalid category!\nCategories are:\n - ' + '\n - '.join(categories.keys()))

    URL = f'https://opentdb.com/api.php?amount={num_questions}&category={categories[category]}'

    res = requests.get(URL)
    response = res.json()

    questions = response['results']

    #function for question sequence
    async def ask_sequence(question):
        choices = ['\na: ','\nb: ','\nc: ','\nd: ']

        answers = question['incorrect_answers'] + [question['correct_answer']]
        random.shuffle(answers)

        message = question['question'] + ''.join([choices[idx]+answer for idx, answer in enumerate(answers)])

        message = html.unescape(message)

        await ctx.send(message)

    #execute ask_sequence for each question returned
    for q in questions:
        ask_sequence(q)
        




@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')


bot.run(TOKEN)