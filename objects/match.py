import datetime
import json
from modules.champions import Champions
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


class Match:
    def __init__(self, match_id: int):
        self.match_id = match_id
        self.raw_match = watcher.match.by_id(default_region, self.match_id)

        # Information on the match
        self.season = self.raw_match['seasonId']
        self.queue = self.raw_match['queueId']
        self.game_duration = self.raw_match['gameDuration']
        self.game_creation = datetime.datetime.fromtimestamp(self.raw_match['gameCreation']/1000.0).strftime('%m-%d-%Y %H:%M:%S')

        # List of players for each team - consider updating to Team object
        self.players = list()
        self.blue_side = list()
        self.red_side = list()

        self.blue_side_win = None

        # Parse the data and create objects
        self.initialize_match()
        self.copy_player_stats()
        self.set_player_teams()

    def to_string(self):
        minutes, seconds = divmod(self.game_duration, 60)
        time_str = str(minutes) + ':'
        if seconds < 10:
            time_str += '0' + str(seconds)
        else:
            time_str += str(seconds)

        header = self.game_creation + ' - ' + self.queue + ' - ' + time_str + '\n'
        header += 'Champion\t\tPlayer\t\tRank\t\tK/D/A\t\tDamage\t\tVision\t\tCS\n\n'

        blue = 'Blue Side - ' + ('Victory' if self.blue_side_win else 'Defeat') + '\n'
        for player in self.blue_side:
            kda_str = str(player.kills) + '/' + str(player.deaths) + '/' + str(player.assists)

            blue += '\t\t{}\t\t{}\t\t{}\t\t{}\t\t{}\t\t{}\t\t{}\n'.format(player.champion, player.name,
                                                                          player.solo_duo_tier, kda_str,
                                                                          str(player.total_damage_to_champions),
                                                                          str(player.vision_score),
                                                                          str(player.total_minions_killed))

        red = '\nRed Side - ' + ('Defeat' if self.blue_side_win else 'Victory') + '\n'
        for player in self.red_side:
            kda_str = str(player.kills) + '/' + str(player.deaths) + '/' + str(player.assists)

            red += '\t\t{}\t\t{}\t\t{}\t\t{}\t\t{}\t\t{}\t\t{}\n'.format(player.champion, player.name,
                                                                         player.solo_duo_tier, kda_str,
                                                                         str(player.total_damage_to_champions),
                                                                         str(player.vision_score),
                                                                         str(player.total_minions_killed))

        return header + blue + red

    def initialize_match(self):
        from modules.matches import Matches
        self.season = Matches.get_season_by_id(self.raw_match['seasonId'])
        self.queue = Matches.get_queue_by_id(self.raw_match['queueId'])

        participant_identities = self.raw_match['participantIdentities']

        for pid in participant_identities:
            try:
                player = Player(pid['player']['summonerName'])

                player.participant_id = pid['participantId']
                self.players.append(player)
            except HTTPError as err:
                if err.response.status_code == 429:
                    print('We should retry in {} seconds.')
                    print('this retry-after is handled by default by the RiotWatcher library')
                    print('future requests wait until the retry-after time passes')
                elif err.response.status_code == 404:
                    print('Failed to fetch summoner!')
                else:
                    raise

    def copy_player_stats(self):
        participants = self.raw_match['participants']

        for participant in participants:
            cur_id = participant['participantId']
            stats = participant['stats']
            cur_player = self.players[cur_id - 1]

            cur_player.team_id = participant['teamId']
            if cur_player.team_id == 100:
                self.blue_side.append(cur_player)
            else:
                self.red_side.append(cur_player)

            cur_player.champion = Champions.get_champ_name_by_id(str(participant['championId']))
            cur_player.kills = stats['kills']
            cur_player.deaths = stats['deaths']
            cur_player.assists = stats['assists']
            cur_player.largest_multi_kill = stats['largestMultiKill']
            cur_player.total_damage_to_champions = stats['totalDamageDealtToChampions']
            cur_player.magic_damage_to_champions = stats['magicDamageDealtToChampions']
            cur_player.physical_damage_to_champions = stats['physicalDamageDealtToChampions']
            cur_player.true_damage_to_champions = stats['trueDamageDealtToChampions']
            cur_player.vision_score = stats['visionScore']
            cur_player.time_ccing_others = stats['timeCCingOthers']
            cur_player.total_damage_taken = stats['totalDamageTaken']
            cur_player.magic_damage_taken = stats['magicalDamageTaken']
            cur_player.physical_damage_taken = stats['physicalDamageTaken']
            cur_player.true_damage_taken = stats['trueDamageTaken']
            cur_player.gold_earned = stats['goldEarned']
            cur_player.total_minions_killed = stats['totalMinionsKilled']
            cur_player.champion_level = stats['champLevel']

    def set_player_teams(self):
        teams = self.raw_match['teams']

        if teams[0]['win'] == 'Win':
            self.blue_side_win = True
        else:
            self.blue_side_win = False
