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
        self.scores = {}
        self._last_q_content = None
        self.key = None
        self._last_q_msg = None

    @commands.command()
    async def trivia(self, ctx, category: str, num_questions: int):
        """Will start a game of trivia.
        """
        #store context in state
        self.ctx = ctx

        #check for valid category
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
        #bot should not respond to its own reactions
        if reaction.message.id == self._last_q_msg.id and user != self.bot.user:
            #handle "next" button
            if str(reaction) == '⏭':
                #TODO:check answers and award points

                #ask next question or end game
                if self.questions:
                    await self.ask_question()
                else:
                    await self.ctx.send('Out of questions! Game over!')


    async def ask_question(self):
        
        self._last_q_content = self.questions.pop()

        #initialize how many answer choices
        if self._last_q_content['type'] == 'multiple':
            choices = ['\na) ','\nb) ','\nc) ','\nd) ']
        elif self._last_q_content['type'] == 'boolean':
            choices = ['\na) ','\nb) ']

        #generate a key
        random.shuffle(choices)
        answers = self._last_q_content['incorrect_answers'] + [self._last_q_content['correct_answer']]
        key = [{'option':choices[idx][1], 'prefix':choices[idx], 'answer':answer, 'correct':answer==self._last_q_content['correct_answer'],} for idx, answer in enumerate(answers)]

        #store the key in object state
        key.sort(key=lambda item: item['option'])
        self.key = key

        #generate and send message containing question
        message = self._last_q_content['question'] + ''.join([answer['prefix']+answer['answer'] for answer in self.key])
        message = html.unescape(message)
        self._last_q_msg = await self.ctx.send(message)

        #add reactions for controls
        emojis = {
            'a':'🇦',
            'b':'🇧',
            'c':'🇨',
            'd':'🇩',
            'next': '⏭'
            }

        for answer in self.key:
            await self._last_q_msg.add_reaction(emojis[answer['option']])

        await self._last_q_msg.add_reaction(emojis['next'])
