# TODO Use DDragon to pull champion data and parse that with champion-masteries-by-summoner

import discord
from discord.ext import commands
import json
from riotwatcher import RiotWatcher

# Load the config file
with open('config.json') as json_data_file:
    data = json.load(json_data_file)

# Store config details
key = data['key']

watcher = RiotWatcher(key)
default_region = 'na1'

version = watcher.data_dragon.versions_for_region(default_region)
print(version)

champions = watcher.data_dragon.champions(version.get('v'))
print(champions.get('data'))


class Summoners:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='info')
    async def get_summoner(self, ctx, name: str):
        """Returns information on a summoner"""

        summoner = watcher.summoner.by_name(default_region, name)
        ranked_stats = watcher.league.positions_by_summoner(default_region, summoner['id'])

        ret = 'Name: ' + summoner.get('name') + '\n'
        ret += '\tLevel: ' + str(summoner.get('summonerLevel')) + '\n'
        ret += '\tRank: ' + rank_to_string(ranked_stats[0])

        await ctx.send(ret)


def rank_to_string(ranked_stats):
    tier = ranked_stats.get('tier')
    rank = ranked_stats.get('rank')
    league_points = str(ranked_stats.get('leaguePoints'))

    ret = tier + ' ' + rank + ' (' + league_points + 'LP)'

    return ret


def setup(bot):
    bot.add_cog(Summoners(bot))
