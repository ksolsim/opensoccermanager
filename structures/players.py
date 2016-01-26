#!/usr/bin/env python3

#  This file is part of OpenSoccerManager.
#
#  OpenSoccerManager is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by the
#  Free Software Foundation, either version 3 of the License, or (at your
#  option) any later version.
#
#  OpenSoccerManager is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
#  or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
#
#  You should have received a copy of the GNU General Public License along with
#  OpenSoccerManager.  If not, see <http://www.gnu.org/licenses/>.


import random

import data
import structures.contract
import structures.history
import structures.morale
import structures.value
import structures.wage


class Players:
    class Player:
        def __init__(self):
            self.first_name = ""
            self.second_name = ""
            self.common_name = None
            self.date_of_birth = [0, 0, 0]
            self.squad = structures.squad.Squad()
            self.nationality = None
            self.position = ""
            self.morale = 20
            self.keeping = 0
            self.tackling = 0
            self.passing = 0
            self.shooting = 0
            self.heading = 0
            self.pace = 0
            self.stamina = 0
            self.set_pieces = 0
            self.ball_control = 0
            self.fitness = 100
            self.value = None
            self.wage = None
            self.contract = None
            self.transfer = [False, False]
            self.appearances = 0
            self.substitute = 0
            self.goals = 0
            self.assists = 0
            self.yellow_cards = 0
            self.red_cards = 0
            self.man_of_the_match = 0
            self.rating = Rating()
            self.injury = Injury()
            self.suspension = Suspension()
            self.training_value = 0
            self.training_points = 0
            self.history = None
            self.retiring = False

        def get_name(self, mode=0):
            '''
            Return player name for display.
            '''
            if self.common_name:
                name = self.common_name
            else:
                if mode == 0:
                    name = "%s, %s" % (self.second_name, self.first_name)
                else:
                    name = "%s %s" % (self.first_name, self.second_name)

            return name

        def get_age(self):
            '''
            Return age of player.
            '''
            age = data.date.year - self.date_of_birth[0]

            if (data.date.month, data.date.day) < (self.date_of_birth[1], self.date_of_birth[2]):
                age -= 1

            return age

        def get_date_of_birth(self):
            '''
            Return string containing date of birth.
            '''
            return "%i/%i/%i" % tuple(self.date_of_birth)

        def get_club_name(self):
            '''
            Return club name player is contracted to.
            '''
            club = data.clubs.get_club_by_id(self.squad)

            if club:
                return club.name
            else:
                return ""

        def get_nationality_name(self):
            '''
            Return nationality country name.
            '''
            nation = data.nations.get_nation_by_id(self.nationality)

            return nation.name

        def get_skills(self):
            '''
            Return tuple of the nine skills.
            '''
            skills = (self.keeping,
                      self.tackling,
                      self.passing,
                      self.shooting,
                      self.heading,
                      self.pace,
                      self.stamina,
                      self.set_pieces,
                      self.ball_control)

            return skills

        def get_skill_by_index(self, index):
            '''
            Return single skill value for given index.
            '''
            skills = self.get_skills()

            return skills[index]

        def get_morale(self):
            '''
            Return the string indicating the players morale value.
            '''
            morale = structures.morale.PlayerMorale()
            status = morale.get_morale(self.morale)

            return status

        def get_appearances(self):
            '''
            Get number of appearances and substitute appearances.
            '''
            return "%i (%i)" % (self.appearances, self.substitute)

        def get_cards(self):
            '''
            Get number of yellow and red cards.
            '''
            return "%i/%i" % (self.yellow_cards, self.red_cards)

        def get_rating(self):
            '''
            Display the average player rating.
            '''
            return ""

    def __init__(self, season):
        self.players = {}
        self.season = season

        self.populate_data()

    def get_players(self):
        '''
        Return all player items.
        '''
        return self.players.items()

    def get_player_by_id(self, playerid):
        '''
        Return player for given player id.
        '''
        return self.players[playerid]

    def update_contracts(self):
        for playerid, player in self.players.items():
            player.contract.decrement_contract_period()

    def populate_data(self):
        data.database.cursor.execute("SELECT * FROM player \
                                     JOIN playerattr \
                                     ON player.id = playerattr.player \
                                     WHERE year = ?",
                                     (self.season,))

        for item in data.database.cursor.fetchall():
            if item[9] in data.clubs.get_club_keys():
                player = self.Player()
                playerid = item[0]
                self.players[playerid] = player

                player.playerid = playerid
                player.first_name = item[1]
                player.second_name = item[2]

                if item[3] != "":
                    player.common_name = item[3]

                player.date_of_birth = list(map(int, item[4].split("-")))
                player.nationality = item[5]
                player.squad = item[9]
                player.position = item[10]

                player.keeping = item[11]
                player.tackling = item[12]
                player.passing = item[13]
                player.shooting = item[14]
                player.heading = item[15]
                player.pace = item[16]
                player.stamina = item[17]
                player.ball_control = item[18]
                player.set_pieces = item[19]
                player.training_value = item[20]

                # Add player to squad
                club = data.clubs.get_club_by_id(player.squad)
                club.squad.add_to_squad(playerid)

                # Add player to nation
                nation = data.nations.get_nation_by_id(player.nationality)
                nation.add_to_nation(playerid)

                # Add history object
                player.history = structures.history.History(playerid)

                # Set value, wage and contract values
                player.value = structures.value.Value(player)
                player.wage = structures.wage.Wage(player)
                player.contract = structures.contract.Contract(player)


class Rating:
    def __init__(self):
        self.rating = []

    def add_rating(self, score):
        '''
        Prepend passed score value to rating list.
        '''
        self.rating.insert(0, score)

    def get_rating(self, number):
        '''
        Return rating score for last passed games amount.
        '''
        return self.rating[:number]

    def get_average_rating(self, number):
        '''
        Return average rating for last passed games amount.
        '''


class Injury:
    def __init__(self):
        self.injuryid = None
        self.period = 0

    def get_injured(self):
        '''
        Return whether player is currently injured.
        '''
        return self.injuryid is not None

    def get_injury_type(self):
        '''
        Get type of injury player has received.
        '''
        if self.injuryid:
            injury = data.injuries.get_injury_by_id(self.injuryid)

            return injury.name

        return "None"

    def get_injury_period(self):
        '''
        Return injury period with weeks string affix.
        '''
        return "%i Weeks" % (self.period)


class Suspension:
    def __init__(self):
        self.suspensionid = None
        self.period = 0

    def get_suspended(self):
        '''
        Return whether player is currently suspended.
        '''
        return self.suspensionid is not None

    def get_suspension_type(self):
        '''
        Get type of suspension player has received.
        '''
        if self.suspensionid:
            suspension = data.suspensions.get_suspension_by_id(self.suspensionid)

            return suspension.name

        return "None"

    def suspension_period(self):
        '''
        Return suspension period with matches string affix.
        '''
        return "%i Matches" % (self.period)
