import random
import json
import html

import requests
import discord
from discord.ext import commands


class TriviaGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.categories = {
            "general": 9,
            "film": 11,
            "music": 12,
            "art": 25,
            "history": 23,
            "geography": 22,
            "sports": 21,
        }
        self.questions = None

    @commands.command()
    async def trivia_cog(self, ctx, category: str, num_questions: int):
        """
        Command: trivia category number_of_questions. \nWill start a game of trivia.
        """

        if category not in self.categories:
            await ctx.send(f'Invalid category!\nCategories are:\n - ' + '\n - '.join(self.categories.keys()))

        URL = f'https://opentdb.com/api.php?amount={num_questions}&category={self.categories[category]}'

        res = requests.get(URL)
        response = res.json()

        questions = response['results']