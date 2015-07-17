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
import string

import constants
import game


class Scouts:
    class Scout:
        def __init__(self):
            self.name = ""
            self.age = 0
            self.ability = 0
            self.wage = 0
            self.contract = 0
            self.morale = 7
            self.retiring = False

            self.generate_name()
            self.generate_age()
            self.generate_ability()
            self.generate_contract()

        def generate_name(self):
            '''
            Generate name of the scout.
            '''
            letters = list(string.ascii_letters[26:])
            initial = random.choice(letters)
            surname = random.choice(game.surnames)
            self.name = "%s. %s" % (initial, surname)

        def generate_age(self):
            '''
            Select random age for the scout.
            '''
            self.age = random.randint(43, 61)

        def generate_ability(self):
            '''
            Determine ability of scout.
            '''
            keys = tuple(constants.ability.keys())
            self.ability = random.choice(keys)

            self.generate_wage()

        def generate_wage(self):
            '''
            Generate wage based on ability.
            '''
            if self.ability == 0:
                lower = 335
                upper = 435
            elif self.ability == 1:
                lower = 425
                upper = 535
            elif self.ability == 2:
                lower = 525
                upper = 635

            self.wage = random.randrange(lower, upper, 5)

        def generate_contract(self):
            '''
            Pick contract period for scout.
            '''
            self.contract = random.randint(24, 260)

        def get_ability_string(self):
            '''
            Return the ability for display.
            '''
            ability = constants.ability[self.ability]

            return ability

        def get_contract_string(self):
            '''
            Return the contract period for display.
            '''
            period = "%s Weeks" % (self.contract)

            return period

    def __init__(self):
        self.scoutid = 0

        self.available = {}
        self.hired = {}

    def get_player_recommendations(self):
        '''
        Retrieve the list of scout recommended players for display.
        '''
        recommended = {}

        return recommended

    def get_scout_report(self, scoutid, playerid):
        '''
        Return a report for the given player using the given scout.
        '''

    def get_scout_id(self):
        self.scoutid += 1

        return self.scoutid

    def generate_initial_scouts(self):
        '''
        Select the first five scouts to start the game.
        '''
        for count in range(0, 5):
            scoutid = self.get_scout_id()
            scout = self.Scout()
            self.available[scoutid] = scout


def individual(shortlist_playerid):
    '''
    Analyses each individual player to match suitability
    '''
    shortlist_position = game.players[shortlist_playerid].position

    equivalents = []

    for playerid in game.clubs[game.teamid].squad:
        player = game.players[playerid]

        if player.position:
            if shortlist_position == "GK":
                equivalents.append(playerid)
            elif shortlist_position in ("DL", "DR", "DC", "D"):
                equivalents.append(playerid)
            elif shortlist_position in ("ML", "MR", "MC", "M"):
                equivalents.append(playerid)
            elif shortlist_position in ("AF", "AS"):
                equivalents.append(playerid)

    averages = []

    for playerid in equivalents:
        player = game.players[playerid]
        skills = player.get_skills()

        average = sum(skills[0:6]) + (skills[8] * 1.5) + (skills[5] * 0.2) + (skills[6] * 0.2) + (skills[7] * 1.5)
        average = average / 9

        averages.append(average)

    position_average = sum(averages) / len(averages)

    player = game.players[shortlist_playerid]
    skills = player.get_skills()

    average = sum(skills[0:6]) + (skills[8] * 1.5) + (skills[5] * 0.2) + (skills[6] * 0.2) + (skills[7] * 1.5)
    average = average / 9

    status = average < position_average

    return status


def recommends():
    '''
    Iterates through all players and displays those which are suitable.
    '''
    recommended = {}

    for playerid, player in game.players.items():
        if individual(playerid):
            recommended[playerid] = player

    return recommended
