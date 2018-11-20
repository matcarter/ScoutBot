import discord
from discord.ext import commands
import json
from riotwatcher import RiotWatcher
import time

# Load the config file
with open('config.json') as json_data_file:
    data = json.load(json_data_file)

# Store config details
key = data['key']

watcher = RiotWatcher(key)
default_region = 'na1'

# Load the config file
with open('data/static_champions.json') as json_data_file:
    champions = json.load(json_data_file)


class Champions:
    def __init__(self, bot):
        self.bot = bot
        update_champions()

    @commands.command(name='mastery')
    async def get_champion_mastery(self, ctx, name: str, champ: str = None):
        """Returns a players champion mastery details"""

        summoner = watcher.summoner.by_name(default_region, name)
        summoner_id = summoner['id']

        if champ is None:
            mastery = watcher.champion_mastery.by_summoner(default_region, summoner_id)

            ret = ''

            for i in range(0, 5):
                champ_id = mastery[i].get('championId')

                champ_name = get_champ_name(str(champ_id))
                champ_level = mastery[i].get('championLevel')
                champ_points = mastery[i].get('championPoints')

                ret += 'Champion: ' + champ_name + '\n'
                ret += '\tLevel: ' + str(champ_level) + '\n'
                ret += '\tPoints: ' + str(champ_points) + '\n'

        else:
            champ_id = get_champ_id(champ)
            mastery = watcher.champion_mastery.by_summoner_by_champion(default_region, summoner_id, champ_id)

            champ_name = champ.lower().capitalize()
            champ_level = mastery.get('championLevel')
            champ_points = mastery.get('championPoints')

            ret = 'Champion: ' + champ_name + '\n'
            ret += '\tLevel: ' + str(champ_level) + '\n'
            ret += '\tPoints: ' + str(champ_points)

        await ctx.send(ret)

    @commands.command(name='champion')
    async def get_champion(self, ctx, name: str):
        """Returns information on a champion"""

        name = name.lower()
        name = name.capitalize()

        champ = 'Name: ' + champions['data'][name]['name'] + '\n'
        champ += '\tTitle: ' + champions['data'][name]['title'] + '\n'
        champ += '\tBlurb: ' + champions['data'][name]['blurb']

        await ctx.send(champ)

    @commands.command(name='rotation')
    async def get_champion_rotation(self, ctx):
        """Returns the current champion rotation"""

        rotation = watcher.champion.rotations(default_region)

        free_champ_ids = rotation['freeChampionIds']
        free_champ_ids_new_players = rotation['freeChampionIdsForNewPlayers']
        max_new_player_level = rotation['maxNewPlayerLevel']

        free_champs = 'Free Champions: '
        free_champs_new_players = 'Free Champions for New Players: '

        for i in range(0, len(free_champ_ids)):
            if i < len(free_champ_ids) - 1:
                free_champs += get_champ_name(str(free_champ_ids[i])) + ', '
            else:
                free_champs += get_champ_name(str(free_champ_ids[i]))

        for i in range(0, len(free_champ_ids_new_players)):
            if i < len(free_champ_ids_new_players) - 1:
                free_champs_new_players += get_champ_name(str(free_champ_ids_new_players[i])) + ', '
            else:
                free_champs_new_players += get_champ_name(str(free_champ_ids_new_players[i]))

        ret = free_champs + '\n\n'
        ret += free_champs_new_players + '\n\n'
        ret += 'Max New Player level: ' + str(max_new_player_level)

        await ctx.send(ret)


def update_champions():
    version_data = watcher.data_dragon.versions_for_region(default_region)

    current_version = int(version_data.get('v').replace('.', ''))
    version = int(champions['version'].replace('.', ''))

    if current_version > version:
        champs = watcher.data_dragon.champions(version_data.get('v'))

        with open('data/static_champions.json', 'w') as outfile:
            json.dump(champs, outfile)

        print('Updated static_champions file to latest version')


def get_champ_id(name: str):
    name = name.lower()
    name = name.capitalize()

    champ_id = champions['data'][name]['key']

    return int(champ_id)


def get_champ_name(champ_id: str):
    for champ in champions['data']:
        champ_key = champions['data'][champ]['key']
        if champ_key == champ_id:
            return champions['data'][champ]['name']


def setup(bot):
    bot.add_cog(Champions(bot))
