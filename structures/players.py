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
            self.contract = structures.contract.Contract()
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
            self.history = structures.history.History()
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
            skills = self.get_skills()

            return skills[index]

        def get_value(self):
            '''
            Return current market value of player.
            '''
            return self.calculate_value()

        def get_value_as_string(self):
            '''
            Retrieve the player value formatted with currency.
            '''
            value = self.calculate_value()

            if value >= 1000000:
                value = "£%.1fM" % (value / 1000000)
            elif value >= 1000:
                value = "£%iK" % (value / 1000)

            return value

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

        def calculate_value(self):
            age = self.get_age()
            skills = self.get_skills()

            if self.position in ("GK"):
                primary = skills[0]
            elif self.position in ("DL", "DR", "DC", "D"):
                primary = skills[1]
            elif self.position in ("ML", "MR", "MC", "M"):
                primary = skills[2]
            elif self.position in ("AS", "AF"):
                primary = skills[3]

            average = sum(skills[0:6]) + (skills[8] * 1.5) + (skills[5] * 0.2) + (skills[6] * 0.2) + (skills[7] * 1.5)
            average += primary * 2
            average = average / 9

            if primary > 95:
                value_multiplier = 5.25
            elif primary >= 90:
                value_multiplier = 3.5
            elif primary > 85:
                value_multiplier = 2.5
            elif primary > 80:
                value_multiplier = 1.8
            elif primary > 75:
                value_multiplier = 1.5
            elif primary > 70:
                value_multiplier = 1.25
            elif primary > 60:
                value_multiplier = 0.9
            elif primary > 50:
                value_multiplier = 0.55
            elif primary > 40:
                value_multiplier = 0.25
            else:
                value_multiplier = 0.12

            # Age modifier
            if age >= 37:
                age_multiplier = 0.1
            elif age >= 34:
                age_multiplier = 0.25
            elif age >= 32:
                age_multiplier = 0.5
            elif age >= 30:
                age_multiplier = 0.75
            elif age == 29:
                age_multiplier = 0.9
            elif age >= 26:
                age_multiplier = 1
            elif age >= 24:
                age_multiplier = 0.9
            elif age >= 21:
                age_multiplier = 0.8
            elif age >= 18:
                age_multiplier = 0.7
            else:
                age_multiplier = 0.5

            value = ((average * 1000) * average) * value_multiplier * 0.25
            value = value * age_multiplier
            value = self.value_rounder(value)

            return value

        def value_rounder(self, value):
            if value >= 1000000:
                divisor = 100000
            elif value >= 10000:
                divisor = 1000

            value = int(value - (value % divisor))

            return value

        def calculate_wage(self):
            skills = self.get_skills()

            value = self.calculate_value()

            if self.position in ("GK"):
                primary = skills[0]
            elif self.position in ("DL", "DR", "DC", "D"):
                primary = skills[1]
            elif self.position in ("ML", "MR", "MC", "M"):
                primary = skills[2]
            elif self.position in ("AS", "AF"):
                primary = skills[3]

            average = sum(skills[0:6]) + (skills[8] * 1.5) + (skills[5] * 0.2) + (skills[6] * 0.2) + (skills[7] * 1.5)
            average += primary
            average = average / 9

            if primary >= 95:
                wage_divider = 390
                value_multiplier = 5
            elif primary >= 90:
                wage_divider = 310
                value_multiplier = 3.25
            elif primary >= 85:
                wage_divider = 255
                value_multiplier = 2
            elif primary >= 80:
                wage_divider = 225
                value_multiplier = 1.25
            elif primary >= 75:
                wage_divider = 195
                value_multiplier = 1
            elif primary >= 70:
                wage_divider = 165
                value_multiplier = 0.75
            elif primary >= 60:
                wage_divider = 140
                value_multiplier = 0.55
            elif primary >= 50:
                wage_divider = 120
                value_multiplier = 0.35
            elif primary >= 40:
                wage_divider = 100
                value_multiplier = 0.22
            else:
                wage_divider = 100
                value_multiplier = 0.12

            value = (((average * 1000) * average) * value_multiplier) * 0.25
            wage = value / wage_divider
            wage = self.wage_rounder(wage)

            return wage

        def wage_rounder(self, wage):
            if wage >= 10000:
                divisor = 100
            else:
                divisor = 10

            wage = int(wage - (wage % divisor))

            return wage

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

                # Set wage and bonus values
                wage = player.calculate_wage()
                player.contract.set_initial_wage(wage)

                # Add player to squad
                club = data.clubs.get_club_by_id(player.squad)
                club.squad.add_to_squad(playerid)

                # Add player to nation
                nation = data.nations.get_nation_by_id(player.nationality)
                nation.add_to_nation(playerid)


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
        self.injury_type = None
        self.injury_period = 0

    def get_injured(self):
        return self.injury_type is not None

    def get_injury_type(self):
        if self.injury_type:
            injury = data.injuries.get_injury_by_id(self.injury_type)

            return injury.name
        else:
            return "None"


class Suspension:
    def __init__(self):
        self.suspension_type = None
        self.suspension_period = 0

    def get_suspended(self):
        return self.suspension_type is not None

    def get_suspension_type(self):
        if self.suspension_type:
            suspension = data.suspension.get_suspension_by_id(self.suspension_type)

            return suspension.name
        else:
            return "None"
