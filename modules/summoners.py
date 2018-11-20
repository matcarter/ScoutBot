# TODO Begin scouting report command

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


class Summoners:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='info')
    async def get_summoner(self, ctx, name: str):
        """Returns information on a summoner"""

        summoner = watcher.summoner.by_name(default_region, name)
        mastery_score = watcher.champion_mastery.scores_by_summoner(default_region, summoner['id'])
        ranked_stats = watcher.league.positions_by_summoner(default_region, summoner['id'])

        solo_rank = 'N/A'
        flex_rank = 'N/A'
        threes_rank = 'N/A'

        for stats in ranked_stats:
            queue_type = stats.get('queueType')

            if queue_type == 'RANKED_SOLO_5x5':
                solo_rank = rank_to_string(stats)
            elif queue_type == 'RANKED_FLEX_SR':
                flex_rank = rank_to_string(stats)
            else:
                threes_rank = rank_to_string(stats)

        ret = 'Name: ' + summoner.get('name') + '\n'
        ret += '\tLevel: ' + str(summoner.get('summonerLevel')) + '\n'
        ret += '\tMastery Score: ' + str(mastery_score) + '\n'
        ret += '\tRanked: \n'
        ret += '\t\tSolos - ' + solo_rank + '\n'
        ret += '\t\tFlex 5v5 - ' + flex_rank + '\n'
        ret += '\t\tFlex 3v3 - ' + threes_rank

        await ctx.send(ret)


def rank_to_string(ranked_stats):
    tier = ranked_stats.get('tier')
    rank = ranked_stats.get('rank')
    league_points = str(ranked_stats.get('leaguePoints'))

    ret = tier + ' ' + rank + ' (' + league_points + 'LP)'

    return ret


def setup(bot):
    bot.add_cog(Summoners(bot))
