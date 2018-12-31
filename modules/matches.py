import datetime
import discord
import json
from discord.ext import commands
from modules.champions import Champions
from objects.match import Match
from objects.player import Player
from requests import HTTPError
from riotwatcher import RiotWatcher

# Load the config file
with open('config.json') as json_data_file:
    data = json.load(json_data_file)

# Load the game constants
with open('data/game_constants.json') as json_constants_file:
    game_constants = json.load(json_constants_file)

# Store config details
key = data['key']

watcher = RiotWatcher(key)
default_region = 'na1'


class Matches:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='history')
    async def get_match_history(self, ctx, name: str, champion: str = None):
        """Display the match history for a given summoner"""

        try:
            player = Player(name)
        except HTTPError:
            await ctx.send('Failed to fetch summoner!')
            return

        matches = self.get_recent_matches(name, champion)

        if matches is None:
            await ctx.send('Error getting matches... Please try again.\n')

        ret = player.name + ' - ' + player.solo_rank + '\n\n'

        for match in matches:
            game_id = str(match['gameId'])
            queue = match['queue']
            champ = match['champion']
            date = match['date']
            lane = match['lane']

            ret += "\t" + date + ' - ' + queue + '\n'
            ret += "\tGame ID: " + game_id + '\n'
            ret += "\t" + champ + ' (' + lane + ')\n\n'

        await ctx.send(ret)

    @commands.command(name='match')
    async def get_match(self, ctx, match_id: int):
        """Display information about a given match"""

        match = self.get_match_by_id(match_id)

        await ctx.send(match.to_string())

    @commands.command(name='highkills')
    async def get_high_kill_games(self, ctx, name: str):
        """Display recent matches where the summoner was hella fed"""

        await ctx.send("WIP")

    @commands.command(name="highdeaths")
    async def get_high_death_games(self, ctx, name: str):
        """Display recent matches where the summoner hella fed"""

        await ctx.send("WIP")

    @commands.command(name="highlights")
    async def get_highlight_games(self, ctx, name: str):
        """Display high performance matches"""

        await ctx.send("WIP")

    @staticmethod
    def get_recent_matches(name: str, champion: str = None):
        try:
            player = Player(name)
        except HTTPError:
            print("Shouldn't have gotten here! - matches.get_recent_matches()")
            return

        account_id = player.account_id

        if champion is not None:
            champ_id = Champions.get_champ_id_by_name(champion)

            if champ_id is None:
                return None

            match_history = watcher.match.matchlist_by_account(default_region, account_id, champion=champ_id, end_index=10)
        else:
            match_history = watcher.match.matchlist_by_account(default_region, account_id, end_index=10)

        matches = list()

        for match in match_history.get('matches'):
            matches.append(Matches.convert_match_reference(match))

        return matches

    @staticmethod
    def get_match_by_id(match_id: int):
        match = Match(match_id)

        return match

    @staticmethod
    def convert_match_reference(match_reference):
        champion_id = str(match_reference.get('champion'))
        champion_name = Champions.get_champ_name_by_id(champion_id)

        match = {
            "region": match_reference.get('platformId'),
            "gameId": match_reference.get('gameId'),
            "champion": champion_name,
            "queue": Matches.get_queue_by_id(match_reference.get('queue')),
            "season": Matches.get_season_by_id(match_reference.get('season')),
            "date": datetime.datetime.fromtimestamp(match_reference.get('timestamp')/1000.0).strftime('%m-%d-%Y %H:%M:%S'),
            "role": match_reference.get('role'),
            "lane": match_reference.get('lane')
        }

        return match

    @staticmethod
    def get_queue_by_id(queue: int):
        for q in game_constants['queues']:
            if str(queue) == q:
                ret = game_constants['queues'][q]['description'] + ' - ' + game_constants['queues'][q]['map']
                return ret

        return 'Special Mode'

    @staticmethod
    def get_season_by_id(season: int):
        for s in game_constants['seasons']:
            if str(season) == s:
                return game_constants['seasons'][s]['season']


def setup(bot):
    bot.add_cog(Matches(bot))
