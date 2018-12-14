import discord
from discord.ext import commands
import json
from riotwatcher import RiotWatcher
import re

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
        check_for_update()

    @commands.command(name='mastery')
    async def get_mastery(self, ctx, name: str, champ: str = None):
        """Display a players champion mastery details"""

        champion_mastery = self.get_champion_mastery(name, champ)
        length = len(champion_mastery)
        ret = 'Champion (Mastery Level) - Mastery Points\n\n'

        for i in range(length):
            ret += champion_mastery[i].get('name')
            ret += ' (' + champion_mastery[i].get('level') + ')'
            ret += ' - ' + champion_mastery[i].get('points') + '\n'

        await ctx.send(ret)

    @commands.command(name='champion')
    async def get_champion(self, ctx, name: str):
        """Display information on a champion"""

        name = name.lower().capitalize()

        champ = 'Name: ' + champions['data'][name]['name'] + '\n'
        champ += '\tTitle: ' + champions['data'][name]['title'] + '\n'
        champ += '\tBlurb: ' + champions['data'][name]['blurb']

        await ctx.send(champ)

    @commands.command(name='rotation')
    async def rotation(self, ctx):
        """Display the current champion rotation"""

        info = self.get_champion_rotation()

        ret = info.get('free_champs') + '\n\n'
        ret += info.get('free_champs_new_players') + '\n\n'
        ret += 'Max New Player level: ' + info.get('max_new_player_level')

        await ctx.send(ret)

    @commands.command(name='update')
    async def update_champions(self, ctx):
        """Display the static champion list to current patch"""

        version = update_static_champions()

        await ctx.send('Version: ' + version)

    @staticmethod
    def get_champion_mastery(name: str, champ: str = None):
        champion_mastery = []

        summoner = watcher.summoner.by_name(default_region, name)
        summoner_id = summoner['id']

        if champ is None:
            mastery = watcher.champion_mastery.by_summoner(default_region, summoner_id)

            for i in range(0, 5):
                champ_id = mastery[i].get('championId')

                champ_name = champion_name_by_id(str(champ_id))
                champ_level = mastery[i].get('championLevel')
                champ_points = mastery[i].get('championPoints')

                champ = {
                    "name": champ_name,
                    "level": str(champ_level),
                    "points": str(champ_points)
                }

                champion_mastery.append(champ)

        else:
            champ_id = champion_id_by_name(champ)
            mastery = watcher.champion_mastery.by_summoner_by_champion(default_region, summoner_id, champ_id)

            champ_name = champ.lower().capitalize()
            champ_level = mastery.get('championLevel')
            champ_points = mastery.get('championPoints')

            champ = {
                "name": champ_name,
                "level": str(champ_level),
                "points": str(champ_points)
            }

            champion_mastery.append(champ)

        return champion_mastery

    @staticmethod
    def get_champion_rotation():
        rotation = watcher.champion.rotations(default_region)

        free_champ_ids = rotation['freeChampionIds']
        free_champ_ids_new_players = rotation['freeChampionIdsForNewPlayers']
        max_new_player_level = rotation['maxNewPlayerLevel']

        free_champs = 'Free Champions: '
        free_champs_new_players = 'Free Champions for New Players: '

        for i in range(0, len(free_champ_ids)):
            if i < len(free_champ_ids) - 1:
                free_champs += champion_name_by_id(str(free_champ_ids[i])) + ', '
            else:
                free_champs += champion_name_by_id(str(free_champ_ids[i]))

        for i in range(0, len(free_champ_ids_new_players)):
            if i < len(free_champ_ids_new_players) - 1:
                free_champs_new_players += champion_name_by_id(str(free_champ_ids_new_players[i])) + ', '
            else:
                free_champs_new_players += champion_name_by_id(str(free_champ_ids_new_players[i]))

        info = {
            "free_champs": free_champs,
            "free_champs_new_players": free_champs_new_players,
            "max_new_player_level": str(max_new_player_level)
        }

        return info

    @staticmethod
    def get_champ_id_by_name(name: str):
        name = name.lower().capitalize()

        champ_id = champions['data'][name]['key']

        return int(champ_id)

    @staticmethod
    def get_champ_name_by_id(champ_id: str):
        for champ in champions['data']:
            champ_key = champions['data'][champ]['key']
            if champ_key == champ_id:
                return champions['data'][champ]['name']


def check_for_update():
    version_data = watcher.data_dragon.versions_for_region(default_region)

    current_version = list(map(int, re.findall('\d+', version_data.get('v'))))
    static_version = list(map(int, re.findall('\d+', champions['version'])))

    for i in range(3):
        if current_version[i] == static_version[i]:
            continue

        elif current_version[i] > static_version[i]:
            print("Updating to version " + version_data.get('v') + " from " + champions['version'])
            update_static_champions()
            break


def update_static_champions():
    version_data = watcher.data_dragon.versions_for_region(default_region)

    champs = watcher.data_dragon.champions(version_data.get('v'))

    with open('data/static_champions.json', 'w') as outfile:
        json.dump(champs, outfile)

    return champs.get('v')


def champion_id_by_name(name: str):
    name = name.lower().capitalize()

    champ_id = champions['data'][name]['key']

    return int(champ_id)


def champion_name_by_id(champ_id: str):
    for champ in champions['data']:
        champ_key = champions['data'][champ]['key']
        if champ_key == champ_id:
            return champions['data'][champ]['name']


def setup(bot):
    bot.add_cog(Champions(bot))
