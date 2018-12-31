import datetime
import json
from riotwatcher import RiotWatcher

# Load the config file
with open('config.json') as json_data_file:
    data = json.load(json_data_file)

# Store config details
key = data['key']

watcher = RiotWatcher(key)
default_region = 'na1'


class Player:
    def __init__(self, name):
        summoner = watcher.summoner.by_name(default_region, name)

        # Main account information
        self.name = summoner['name']
        self.summoner_level = str(summoner['summonerLevel'])
        self.revision_date = summoner['revisionDate']
        self.id = summoner['id']
        self.account_id = summoner['accountId']

        # Ranked information
        self.solo_rank = 'N/A'
        self.flex_rank = 'N/A'
        self.threes_rank = 'N/A'
        self.solo_duo_tier = 'N/A'
        self.flex_tier = 'N/A'
        self.threes_tier = 'N/A'

        # Match statistics
        self.participant_id = None
        self.team_id = None
        self.champion = None
        self.kills = None
        self.deaths = None
        self.assists = None
        self.largest_multi_kill = None
        self.total_damage_to_champions = None
        self.magic_damage_to_champions = None
        self.physical_damage_to_champions = None
        self.true_damage_to_champions = None
        self.vision_score = None
        self.time_ccing_others = None
        self.total_damage_taken = None
        self.magic_damage_taken = None
        self.physical_damage_taken = None
        self.true_damage_taken = None
        self.gold_earned = None
        self.total_minions_killed = None
        self.champion_level = None

        self.get_ranked_stats()

    def to_string(self):
        ret = 'Name: ' + self.name + '\n'
        ret += '\tSummoner Level: ' + self.summoner_level + '\n'
        ret += '\tRevision Date: ' + datetime.datetime.fromtimestamp(self.revision_date/1000.0).strftime('%m-%d-%Y %H:%M:%S') + '\n'
        ret += '\tID: ' + str(self.id) + '\n'
        ret += '\tAccount ID: ' + str(self.account_id) + '\n'
        ret += '\tRanked: \n'
        ret += '\t\tSolo/Duo - ' + self.solo_rank + '\n'
        ret += '\t\tFlex 5v5 - ' + self.flex_rank + '\n'
        ret += '\t\tFlex 3v3 - ' + self.threes_rank

        return ret

    def print_match_stats(self):
        print(self.participant_id)
        print(self.team_id)
        print(self.champion)
        print(self.kills)
        print(self.deaths)
        print(self.assists)
        print(self.largest_multi_kill)
        print(self.total_damage_to_champions)
        print(self.magic_damage_to_champions)
        print(self.physical_damage_to_champions)
        print(self.true_damage_to_champions)
        print(self.vision_score)
        print(self.time_ccing_others)
        print(self.total_damage_taken)
        print(self.magic_damage_taken)
        print(self.physical_damage_taken)
        print(self.true_damage_taken)
        print(self.gold_earned)
        print(self.total_minions_killed)
        print(self.champion_level)

    def get_ranked_stats(self):
        ranked_stats = watcher.league.positions_by_summoner(default_region, self.id)

        for stats in ranked_stats:
            queue_type = stats.get('queueType')

            if queue_type == 'RANKED_SOLO_5x5':
                self.solo_rank = rank_to_string(stats)
                self.solo_duo_tier = stats.get('tier').lower().capitalize()
            elif queue_type == 'RANKED_FLEX_SR':
                self.flex_rank = rank_to_string(stats)
                self.flex_tier = stats.get('tier').lower().capitalize()
            else:
                self.threes_rank = rank_to_string(stats)
                self.threes_tier = stats.get('tier').lower().capitalize()


def rank_to_string(ranked_stats):
    tier = ranked_stats.get('tier').lower().capitalize()
    rank = ranked_stats.get('rank')
    league_points = str(ranked_stats.get('leaguePoints'))

    ret = tier + ' ' + rank + ' (' + league_points + 'LP)'

    return ret
