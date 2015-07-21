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


import calculator
import club
import constants
import display
import evaluation
import game
import nation
import player
import preferences


class Player:
    def __init__(self):
        self.common_name = None
        self.fitness = 100
        self.training_points = 0
        self.morale = 20
        self.injury_type = 0
        self.injury_period = 0
        self.suspension_points = 0
        self.suspension_type = 0
        self.suspension_period = 0
        self.yellow_cards = 0
        self.red_cards = 0
        self.transfer = [False, False]
        self.not_for_sale = False
        self.appearances = 0
        self.substitute = 0
        self.missed = 0
        self.goals = 0
        self.assists = 0
        self.man_of_the_match = 0
        self.rating = []
        self.history = player.History()

    def get_skills(self):
        '''
        Return tuple of skill attributes for the player.
        '''
        values = (self.keeping,
                  self.tackling,
                  self.passing,
                  self.shooting,
                  self.heading,
                  self.pace,
                  self.stamina,
                  self.ball_control,
                  self.set_pieces,
                 )

        return values

    def get_name(self, mode=0):
        '''
        Return the player name in the requested format.
        '''
        if self.common_name:
            name = self.common_name
        else:
            if mode == 0:
                name = "%s, %s" % (self.second_name, self.first_name)
            elif mode == 1:
                name = "%s %s" % (self.first_name, self.second_name)

        return name

    def get_age(self):
        '''
        Determine the player age relative to current in-game date.
        '''
        year, month, day = self.date_of_birth.split("-")
        age = game.date.year - int(year)

        if (game.date.month, game.date.day) < (int(month), int(day)):
            age -= 1

        return age

    def get_club(self):
        '''
        Return the club name, or none if player is without a contract.
        '''
        if self.club:
            name = club.clubitem.clubs[self.club].name
        else:
            name = ""

        return name

    def get_nationality(self):
        '''
        Return the player nationality.
        '''
        name = nation.get_nation(self.nationality)

        return name

    def get_value(self):
        '''
        Retrieve the player value formatted with currency.
        '''
        value = calculator.value_rounder(self.value)
        currency, exchange = constants.currency[preferences.preferences.currency]

        if value >= 1000000:
            amount = (value / 1000000) * exchange
            value = "%s%.1fM" % (currency, amount)
        elif value >= 1000:
            amount = (value / 1000) * exchange
            value = "%s%iK" % (currency, amount)

        return value

    def get_wage(self):
        '''
        Fetch the player wage and return with appropriate currency.
        '''
        wage = calculator.wage_rounder(self.wage)
        currency, exchange = constants.currency[preferences.preferences.currency]

        if wage >= 1000:
            amount = (wage / 1000) * exchange
            wage = "%s%.1fK" % (currency, amount)
        elif wage >= 100:
            amount = wage * exchange
            wage = "%s%i" % (currency, amount)

        return wage

    def get_contract(self):
        '''
        Format the number of weeks on the contract remaining and return.
        '''
        if self.contract > 1:
            contract = "%i Weeks" % (self.contract)
        elif self.contract == 1:
            contract = "%i Week" % (self.contract)
        elif self.contract == 0:
            contract = "Out of Contract"

        return contract

    def set_morale(self, amount):
        '''
        Set the morale of the player between -100 and 100.
        '''
        self.morale += amount

        if self.morale > 100:
            self.morale = 100
        elif self.morale < -100:
            self.morale = -100

    def get_morale(self):
        '''
        Return the string indicating the players morale value.
        '''
        status = ""

        if self.morale >= 85:
            status = constants.morale[8]
        elif self.morale >= 70:
            status = constants.morale[7]
        elif self.morale >= 45:
            status = constants.morale[6]
        elif self.morale >= 20:
            status = constants.morale[5]
        elif self.morale >= 0:
            status = constants.morale[4]
        elif self.morale >= -25:
            status = constants.morale[3]
        elif self.morale >= -50:
            status = constants.morale[2]
        elif self.morale >= -75:
            status = constants.morale[1]
        elif self.morale >= -100:
            status = constants.morale[0]

        return status

    def get_appearances(self):
        '''
        Get number of appearances and substitute appearances.
        '''
        appearances = "%i (%i)" % (self.appearances, self.substitute)

        return appearances

    def get_cards(self):
        '''
        Get number of yellow and red cards.
        '''
        cards = "%i/%i" % (self.yellow_cards, self.red_cards)

        return cards

    def get_injury(self):
        '''
        Return number of weeks out injured.
        '''
        if self.injury_period == 1:
            injury = "%i Week" % (self.injury_period)
        else:
            injury = "%i Weeks" % (self.injury_period)

        return injury

    def get_suspension(self):
        '''
        Return number of matches out suspended.
        '''
        if self.suspension_period == 1:
            suspension = "%i Match" % (self.suspension_period)
        else:
            suspension = "%i Matches" % (self.suspension_period)

        return suspension

    def get_rating(self):
        '''
        Display the average player rating.
        '''
        if self.rating != []:
            average = sum(self.rating) / float(len(self.rating))
            rating = "%.1f" % (average)
        else:
            rating = "0.0"

        return rating

    def renew_contract(self):
        '''
        Determine whether player will agree on a contract renewal.
        '''
        points = self.morale

        overall = evaluation.calculate_overall()
        points += overall - 25

        state = points >= 0

        return state


class Team:
    def __init__(self):
        self.teamid = None
        self.name = ""
        self.team = {}
        self.substitutes = {}
        self.shots_on_target = 0
        self.shots_off_target = 0
        self.throw_ins = 0
        self.corner_kicks = 0
        self.free_kicks = 0
        self.penalty_kicks = 0
        self.fouls = 0
        self.yellow_cards = 0
        self.red_cards = 0
        self.possession = 0


class Cards:
    def __init__(self):
        self.yellow_cards = 0
        self.red_cards = 0
        self.points = 0
