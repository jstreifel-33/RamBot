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
        self.ctx = None
        self.questions = None
        self.scores = None
        self._last_q_content = None
        self._last_q_msg = None

    @commands.command()
    async def trivia_cog(self, ctx, category: str, num_questions: int):
        """Will start a game of trivia.
        """

        self.ctx = ctx

        if category not in self.categories:
            await self.ctx.send(f'Invalid category!\nCategories are:\n - ' + '\n - '.join(self.categories.keys()))

        #get trivia info based on input
        URL = f'https://opentdb.com/api.php?amount={num_questions}&category={self.categories[category]}'
        res = requests.get(URL)
        response = res.json()
        self.questions = response['results']

        #ask first question
        await self.ask_question()

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.message.id == self._last_q_msg.id and user != self.bot:
            #handle checking answer and allocating points
            print('reaction detected: ', reaction)

    async def ask_question(self):
        
        if self.questions:
            self._last_q_content = self.questions.pop()
        else:
            #execute end game command?
            #This condition should eventually move to on_reaction_add
            return

        choices = ['\na: ','\nb: ','\nc: ','\nd: ']

        answers = self._last_q_content['incorrect_answers'] + [self._last_q_content['correct_answer']]

        random.shuffle(answers)

        message = self._last_q_content['question'] + ''.join([choices[idx]+answer for idx, answer in enumerate(answers)])

        message = html.unescape(message)

        self._last_q_msg = await self.ctx.send(message)

        emojis = {
            'a':'🇦',
            'b':'🇧',
            'c':'🇨',
            'd':'🇩',
            'next': '⏭'
            }
        await self._last_q_msg.add_reaction(emojis['a'])
        await self._last_q_msg.add_reaction(emojis['b'])
        await self._last_q_msg.add_reaction(emojis['c'])
        await self._last_q_msg.add_reaction(emojis['d'])
        await self._last_q_msg.add_reaction(emojis['next'])