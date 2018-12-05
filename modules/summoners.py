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

        info = self.get_summoner_info(name)

        ret = 'Name: ' + info.get('name') + '\n'
        ret += '\tLevel: ' + info.get('level') + '\n'
        ret += '\tMastery Score: ' + info.get('mastery_score') + '\n'
        ret += '\tRanked: \n'
        ret += '\t\tSolo/Duo - ' + info.get('solo_duo') + '\n'
        ret += '\t\tFlex 5v5 - ' + info.get('flex_5v5') + '\n'
        ret += '\t\tFlex 3v3 - ' + info.get('flex_3v3')

        await ctx.send(ret)

    @staticmethod
    def get_summoner_info(name: str):
        summoner = watcher.summoner.by_name(default_region, name)
        mastery_score = watcher.champion_mastery.scores_by_summoner(default_region, summoner['id'])
        ranked_stats = watcher.league.positions_by_summoner(default_region, summoner['id'])

        solo_rank = 'N/A'
        flex_rank = 'N/A'
        threes_rank = 'N/A'
        solo_duo_tier = 'N/A'
        flex_tier = 'N/A'
        threes_tier = 'N/A'

        for stats in ranked_stats:
            queue_type = stats.get('queueType')

            if queue_type == 'RANKED_SOLO_5x5':
                solo_rank = rank_to_string(stats)
                solo_duo_tier = stats.get('tier').lower().capitalize()
            elif queue_type == 'RANKED_FLEX_SR':
                flex_rank = rank_to_string(stats)
                flex_tier = stats.get('tier').lower().capitalize()
            else:
                threes_rank = rank_to_string(stats)
                threes_tier = stats.get('tier').lower().capitalize()

        info = {
            "name": summoner.get('name'),
            "level": str(summoner.get('summonerLevel')),
            "mastery_score": str(mastery_score),
            "solo_duo": solo_rank,
            "flex_5v5": flex_rank,
            "flex_3v3": threes_rank,
            "solo_duo_tier": solo_duo_tier,
            "flex_5v5_tier": flex_tier,
            "flex_3v3_tier": threes_tier,
        }

        return info


def rank_to_string(ranked_stats):
    tier = ranked_stats.get('tier').lower().capitalize()
    rank = ranked_stats.get('rank')
    league_points = str(ranked_stats.get('leaguePoints'))

    ret = tier + ' ' + rank + ' (' + league_points + 'LP)'

    return ret


def setup(bot):
    bot.add_cog(Summoners(bot))
