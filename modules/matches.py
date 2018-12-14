import datetime
import discord
import json
from discord.ext import commands
from riotwatcher import RiotWatcher
from .summoners import Summoners
from .champions import Champions

# Load the config file
with open('config.json') as json_data_file:
    data = json.load(json_data_file)

# Store config details
key = data['key']

watcher = RiotWatcher(key)
default_region = 'na1'


class Matches:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='history')
    async def get_match_history(self, ctx, name: str):
        """Display the match history for a given summoner"""

        self.get_recent_matches(name)

    @staticmethod
    def get_recent_matches(name: str, champion: str = None, queue: str = None, season: str = None):
        account = Summoners.get_account_info(name)
        account_id = account.get('account_id')

        match_history = watcher.match.matchlist_by_account(default_region, account_id, end_index=20)

        print(match_history)

        for match in match_history.get('matches'):
            print(convert_match_reference(match))


def convert_match_reference(match_reference):
    champion_id = str(match_reference.get('champion'))
    champion_name = Champions.get_champ_name_by_id(champion_id)

    match = {
        "region": match_reference.get('platformId'),
        "gameId": match_reference.get('gameId'),
        "champion": champion_name,
        "queue": match_reference.get('queue'),
        "season": match_reference.get('season'),
        "date": datetime.datetime.fromtimestamp(match_reference.get('timestamp')/1000.0).strftime('%m-%d-%Y %H:%M:%S'),
        "role": match_reference.get('role'),
        "lane": match_reference.get('lane')
    }

    return match


def setup(bot):
    bot.add_cog(Matches(bot))
