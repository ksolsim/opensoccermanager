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
import structures


class Staff:
    def __init__(self, staff_type):
        self.name = self.name()
        self.age = self.age()
        self.ability = self.ability()
        self.wage = self.wage()
        self.contract = self.contract()

        if staff_type == 0:
            self.speciality = self.speciality()

        self.retiring = False

    def name(self):
        '''
        Generate name of scout or coach.
        '''
        letters = list(string.ascii_letters[26:])
        initial = random.choice(letters)
        surname = random.choice(game.surnames)
        name = "%s. %s" % (initial, surname)

        return name

    def age(self):
        '''
        Select random age for staff member.
        '''
        age = random.randint(43, 61)

        return age

    def wage(self):
        if self.ability == 0:
            lower = 335
            upper = 435
        elif self.ability == 1:
            lower = 425
            upper = 535
        elif self.ability == 2:
            lower = 525
            upper = 635

        wage = random.randrange(lower, upper, 5)

        return wage

    def ability(self):
        keys = list(constants.ability.keys())
        ability = random.choice(keys)

        return ability

    def speciality(self):
        keys = list(constants.speciality.keys())
        speciality = random.choice(keys)

        return speciality

    def contract(self):
        period = random.randint(24, 260)

        return period
