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


class Coaches:
    class Coach:
        def __init__(self):
            self.name = ""
            self.age = 0
            self.ability = 0
            self.speciality = 0
            self.wage = 0
            self.contract = 0
            self.morale = 7
            self.retiring = False

            self.generate_name()
            self.generate_age()
            self.generate_ability()
            self.generate_speciality()
            self.generate_contract()

        def generate_name(self):
            '''
            Generate name of the coach.
            '''
            letters = list(string.ascii_letters[26:])
            initial = random.choice(letters)
            surname = random.choice(game.surnames)
            self.name = "%s. %s" % (initial, surname)

        def generate_age(self):
            '''
            Select random age for the coach.
            '''
            self.age = random.randint(43, 61)

        def generate_ability(self):
            '''
            Determine ability of coach.
            '''
            keys = tuple(constants.ability.keys())
            self.ability = random.choice(keys)

            self.generate_wage()

        def generate_speciality(self):
            '''
            Pick speciality for coach.
            '''
            keys = tuple(constants.speciality.keys())
            self.speciality = random.choice(keys)

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

        def get_morale_string(self):
            '''
            Return the morale for display.
            '''
            morale = constants.morale[self.morale]

            return morale

    def __init__(self):
        self.coachid = 0

        self.available = {}
        self.hired = {}

    def get_coach_id(self):
        self.coachid += 1

        return self.coachid

    def generate_initial_coaches(self):
        '''
        Select the first five coaches to start the game.
        '''
        self.available = {}

        for count in range(0, 5):
            coachid = self.get_coach_id()
            coach = self.Coach()
            self.available[coachid] = coach

    def get_number_of_coaches(self):
        '''
        Return the number of coaches on staff.
        '''
        number = len(self.hired)

        return number
