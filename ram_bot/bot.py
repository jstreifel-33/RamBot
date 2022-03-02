import os

import random
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


#-- TRIVIA COMMAND --
@bot.command(
    help = "Command: trivia category number_of_questions. \nWill start a game of trivia.",
    brief = "Play a game of trivia."
)
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

        embed_msg = await ctx.send(message)

        emojis = {
            'a':'\U0001F1E6',
            'b':'\U0001F1E7',
            'c':'\U0001F1E8',
            'd':'\U0001F1E9',
            'next': '\U000023ED'
            }
        await embed_msg.add_reaction(emojis['a'])
        await embed_msg.add_reaction(emojis['b'])
        await embed_msg.add_reaction(emojis['c'])
        await embed_msg.add_reaction(emojis['d'])
        await embed_msg.add_reaction(emojis['next'])

    #execute ask_sequence for each question returned
    #NOTE: Might be better to must pop questions while keeping score? Sequence of events needs to depend on players. Create trivia class?

    for q in questions:
        await ask_sequence(q)
        

#-- ERROR HANDLING --
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')


#-- RUN --
bot.run(TOKEN)
