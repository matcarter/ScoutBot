import discord
from discord.ext import commands
import json
from objects.player import Player
from requests import HTTPError
from riotwatcher import RiotWatcher

# Load the config file
with open('config.json') as json_data_file:
    data = json.load(json_data_file)

# Store config details
key = data['key']

watcher = RiotWatcher(key)
default_region = 'na1'


class Summoners:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='info')
    async def get_summoner(self, ctx, name: str):
        """Display information on a summoner"""
        try:
            player = Player(name)
        except HTTPError as err:
            await ctx.send('Failed to fetch summoner! Error code {}'.format(err.response.status_code))
            return

        ret = 'Name: ' + player.name + '\n'
        ret += '\tLevel: ' + player.summoner_level + '\n'
        ret += '\tRanked: \n'
        ret += '\t\tSolo/Duo - ' + player.solo_rank + '\n'
        ret += '\t\tFlex 5v5 - ' + player.flex_rank + '\n'
        ret += '\t\tFlex 3v3 - ' + player.threes_rank

        await ctx.send(ret)


def setup(bot):
    bot.add_cog(Summoners(bot))
