import os

import discord
from dotenv import load_dotenv

intents = discord.Intents().all()
# client = discord.Bot(prefix = '', intents=intents)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)

    print(
        f'{client.user} has connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
        )

    # members = '\n - '.join([member.name for member in guild.members])
    # print(f'Guild Members:\n - {members}')

@client.event
async def on_message(message):
    #avoid recursive loops
    if message.author == client.user:
        return

    #create response based on message
    if message.content == 'rambot':
        response = "Hello world!"

    #send response
    await message.channel.send(response)

client.run(TOKEN)