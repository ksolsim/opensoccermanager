#!/usr/bin/env python3

import random
import string

import data


class Staff:
    surnames = []

    def __init__(self):
        self.available = {}
        self.hired = {}

        self.populate_surnames()

    def populate_surnames(self):
        data.database.cursor.execute("SELECT * FROM staff")

        for name in data.database.cursor.fetchall():
            self.surnames.append(name[0])

    def get_staff_count(self):
        '''
        Return the number of staff which have been hired.
        '''
        return len(self.hired)

    def get_total_wage(self):
        '''
        Return wages for all staff members contracted to the club.
        '''
        wage = 0

        for itemid, item in self.hired.items():
            wage += item.wage

        return wage


class Member(Staff):
    '''
    Base member object for use by scouts and coaches.
    '''
    def __init__(self):
        super(Staff, self).__init__()

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
        surname = random.choice(Staff.surnames)
        name = "%s. %s" % (initial, surname)

        return name

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
            contract = "%i Weeks" % (self.contract)
        else:
            contract = "%i Week" % (self.contract)

        return contract

    def get_payout(self):
        '''
        Return payout for firing the coach.
        '''
        return self.contract * self.wage
