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

import data


class Staff:
    def __init__(self):
        self.surnames = []

        self.available = {}
        self.hired = {}

        self.populate_surnames()

    def get_staff_count(self):
        '''
        Return the number of staff which have been hired.
        '''
        return len(self.hired)

    def get_total_wage(self):
        '''
        Return wages for all staff members contracted to the club.
        '''
        return sum(staff.wage for staff in self.hired.values())

    def populate_surnames(self):
        data.database.cursor.execute("SELECT * FROM staff")

        for name in data.database.cursor.fetchall():
            self.surnames.append(name[0])


class Member(Staff):
    '''
    Base member object for use by scouts and coaches.
    '''
    def __init__(self):
        Staff.__init__(self)

        self.name = self.generate_name()
        self.age = random.randint(45, 60)
        self.ability = random.randint(0, 2)
        self.wage = self.generate_wage()
        self.contract = random.randint(24, 260)
        self.morale = 7
        self.retiring = False

        self.generate_name()

    def generate_name(self):
        '''
        Generate staff name in 'F. Second' format.
        '''
        letters = list(string.ascii_letters[26:])
        initial = random.choice(letters)
        surname = random.choice(self.surnames)

        return "%s. %s" % (initial, surname)

    def generate_wage(self):
        '''
        Return wage in range for given ability.
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

        wage = random.randrange(lower, upper, 5)

        return wage

    def get_contract_string(self):
        '''
        Grab string for displaying contract length.
        '''
        if self.contract > 1:
            return "%i Weeks" % (self.contract)
        else:
            return "%i Week" % (self.contract)

    def get_payout(self):
        '''
        Return payout for firing the coach.
        '''
        return self.contract * self.wage

    def get_renew_contract(self):
        '''
        Return whether coach is willing to new his contract.
        '''
        if self.retiring:
            return 1
        elif self.morale < 5:
            return 2
        else:
            return 0

    def get_contract_renewal_period(self):
        '''
        Get number of years staff member wishes to renew contract for.
        '''
        return random.randint(1, 3)

    def get_contract_renewal_amount(self):
        '''
        Get wage amount staff member wants for new contract.
        '''
        return int(self.wage * 1.05)

    def get_improve_wage_amount(self):
        '''
        Get improved wage amount for staff member.
        '''
        return int(self.wage * 1.01)
