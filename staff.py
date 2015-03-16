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


def generate(role, number):
    '''
    Generates names for use as scouts and coaches. Takes a number, as in
    the number of staff names to generate when run.

    On first run, the game will request five coaches and five scouts. When staff
    are hired, the game will request a five minus the current number in the
    list.

    Periodically the game will request new scouts and coaches to be generated,
    around every three months.
    '''
    def name():
        letters = list(string.ascii_letters[26:])
        initial = random.choice(letters)
        surname = random.choice(game.surnames)
        name = "%s. %s" % (initial, surname)

        return name

    def age():
        age = random.randint(43, 61)

        return age

    def salary(level):
        if level == 0:
            lower = 335
            upper = 380
        elif level == 1:
            lower = 370
            upper = 555
        elif level == 2:
            lower = 545
            upper = 730

        wage = random.randrange(lower, upper, 5)

        return wage

    def ability():
        keys = list(constants.ability.keys())
        level = random.choice(keys)

        return level

    def speciality():
        keys = list(constants.speciality.keys())
        speciality = random.choice(keys)

        return speciality

    def contract():
        period = random.randint(24, 260)

        return period

    members = {}

    for count in range(0, number):
        staff = structures.Staff()
        staff.name = name()
        staff.age = age()
        staff.ability = ability()
        staff.wage = salary(staff.ability)
        staff.contract = contract()
        staff.retiring = False

        if role == 0:
            staff.speciality = speciality()
            members[game.coachid] = staff
            game.coachid += 1
        else:
            members[game.scoutid] = staff
            game.scoutid += 1

    return members
