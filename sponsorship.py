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

import game
import user


class Sponsorship:
    def __init__(self):
        self.company = None
        self.period = 0
        self.amount = 0

        self.timeout = 0
        self.status = 0

    def generate(self):
        '''
        Generate a new sponsorship offer.
        '''
        companies = random.choice(game.companies)
        self.company = companies[0]

        self.period = random.randint(1, 5)

        club = user.get_user_club()

        self.amount = (club.reputation * random.randrange(950, 1100, 10)) * club.reputation ** 2

        self.status = 1
        self.timeout = random.randint(4, 6)

        game.news.publish("BS01")

    def update(self):
        '''
        Decrement the remaining sponsorship period.
        '''
        if self.status == 0:
            if self.timeout > 0:
                self.timeout -= 1
            else:
                self.generate()
        elif self.status == 1:
            if self.timeout > 0:
                self.timeout -= 1
            else:
                self.status = 0
                self.timeout = random.randint(4, 6)
                game.news.publish("BS03")
        elif self.status == 2:
            if self.period > 0:
                self.period -= 1
            else:
                self.status = 0
                game.news.publish("BS02")

    def accept(self):
        '''
        Accept the specified sponsorship offer.
        '''
        self.status = 2

        club = user.get_user_club()
        club.accounts.deposit(amount=self.amount, category="sponsorship")

    def reject(self):
        '''
        Reject the tabled sponsorship offer.
        '''
        self.company = None
        self.timeout = random.randint(4, 6)
        self.amount = 0

        self.status = 0

    def get_details(self):
        '''
        Return tuple of sponsorship deal details.
        '''
        return self.company, self.period, self.amount
