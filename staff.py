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
import dialogs
import game
import money
import news
import structures


class Staff:
    def __init__(self, staff_type):
        if staff_type == 0:
            self.staffid = game.coachid
            game.coachid += 1
        elif staff_type == 1:
            self.staffid = game.scoutid
            game.scoutid += 1

        self.name = self.name()
        self.age = self.age()
        self.ability = self.ability()
        self.wage = self.wage()
        self.contract = self.contract()

        if staff_type == 0:
            self.speciality = self.speciality()

        self.morale = 9
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
        keys = tuple(constants.ability.keys())
        ability = random.choice(keys)

        return ability

    def speciality(self):
        keys = tuple(constants.speciality.keys())
        speciality = random.choice(keys)

        return speciality

    def contract(self):
        period = random.randint(24, 260)

        return period

    def hire(self):
        '''
        Hire the staff member.
        '''
        state = False

        if dialogs.hire_staff(0, self.name):
            state = True

        return state

    def fire(self):
        '''
        Fire the staff member and payout remainder of the contract.
        '''
        state = False

        payout = self.wage * self.contract

        if dialogs.fire_staff(index=0, name=self.name, payout=payout):
            money.withdraw(payout, 11)

            del game.clubs[game.teamid].coaches_hired[self.staffid]

            state = True

        return state

    def renew_contract(self):
        '''
        Renew the contract of the staff member.
        '''
        state = False

        if self.retiring:
            dialogs.renew_staff_contract_error(self)
        else:
            year = random.randint(2, 4)
            amount = round(self.wage * 1.055)

            if dialogs.renew_staff_contract(self.name, year, amount):
                self.wage = amount
                self.contract = year * 52
                self.morale += random.randint(1, 3)

                state = True

        return state

    def improve_wage(self):
        '''
        Offer a pay increase to the staff member.
        '''
        amount = round(self.wage * 1.025)

        state = False

        if dialogs.improve_wage(self.name, amount):
            self.wage = amount
            self.morale += 1

            state = True

        return state

    def staff_morale(self):
        status = constants.morale[self.morale]

        return status


def check_morale():
    '''
    Check workload of other coaches and decrease morale if overworked.
    '''
    counts = {}

    club = game.clubs[game.teamid]

    for playerid, training in club.individual_training.items():
        if training.coachid in counts:
            counts[training.coachid] += 1
        else:
            counts[training.coachid] = 1

    average = 0

    for value in counts.values():
        average += value

    if len(counts) > 1:
        average = average / len(counts)
    else:
        for coachid, count in counts.items():
            if count > 9:
                coach = club.coaches_hired[coachid]
                news.publish("IT01", coach=coach.name)
