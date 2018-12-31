import discord
import json
from discord.ext import commands
from requests import HTTPError
from riotwatcher import RiotWatcher
from objects.player import Player
from .champions import Champions

# Load the config file
with open('config.json') as json_data_file:
    data = json.load(json_data_file)

# Store config details
key = data['key']

watcher = RiotWatcher(key)
default_region = 'na1'


class Scouter:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='scout')
    async def scout(self, ctx, name: str):
        """Display a scouting report for given summoner(s)"""

        ret = self.scout_summoner(name)

        if ret is None:
            ret = 'Failed to scout summoner!'

        await ctx.send(ret)

    @staticmethod
    def scout_summoner(name: str):
        try:
            player = Player(name)
        except HTTPError:
            return None
        champion_mastery = Champions.get_champion_mastery(name)

        ret = ''

        """
        Name (Main Role) - Solo/Duo Rank
            OTP: [Champ] (if they otp a champ)
            Most Played: Top 5 played champs in ranked
            Recently Played: Top 5 recently played champs
            Most Mastery: Top 5 mastery on champs
        """

        ret += player.name + ' (Role) - ' + player.solo_rank + '\n'
        ret += '\tOTP: ' + '\n'
        ret += '\tMost Played: ' + '\n'
        ret += '\tRecently Played: ' + '\n'
        ret += '\tMost Mastery: '

        length = len(champion_mastery)
        for i in range(length):
            ret += champion_mastery[i].get('name')

            if i != (length - 1):
                ret += ', '

        ret += '\n'

        return ret


def setup(bot):
    bot.add_cog(Scouter(bot))
