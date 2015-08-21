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

import club
import display
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


class Advertising:
    class Advert:
        def __init__(self, name):
            clubitem = club.clubs[game.teamid]

            self.name = name
            self.amount = random.randint(1, 6)
            self.period = random.randint(4, 12)
            self.cost = (clubitem.reputation + random.randint(-5, 5)) * 100

        def get_details(self):
            amount = display.currency(self.cost)

            item = [self.name, self.amount, self.period, self.cost, amount]

            return item

    def __init__(self):
        self.companies = []

        self.available = {}
        self.current = {}

        self.advertid = 0

        self.timeout = 0
        self.alert = random.randint(8, 16)

    def initialise(self):
        self.companies = [item[0] for item in game.companies]

        self.generate()

    def generate(self):
        '''
        Regenerate the advertising on offer.
        '''
        random.shuffle(self.companies)

        self.available = {}

        for name in self.companies[0:30]:
            advert = self.Advert(name)
            self.available[self.advertid] = advert

            self.advertid += 1

    def move(self, advertid):
        '''
        Move advert specified from available to current.
        '''
        self.current[advertid] = self.available[advertid]
        del self.available[advertid]

        self.timeout = random.randint(8, 12)

        club = user.get_user_club()
        cost = self.current[advertid].cost

        club.accounts.deposit(amount=cost, category="advertising")

    def update(self):
        '''
        Countdown for alerts and regeneration of adverts.
        '''
        if self.alert > 0:
            self.alert -= 1
        else:
            if self.get_advert_count() < 12:
                game.news.publish("BS04")

            self.alert = random.randint(10, 16)

        if self.timeout > 0:
            self.timeout -= 1
        else:
            self.generate()
            self.timeout = random.randint(8, 12)

        for advert in self.current.values():
            advert.period -= 1

    def get_advert_count(self):
        '''
        Return number of adverts currently set.
        '''
        amount = 0

        for advert in self.current.values():
            amount += advert.amount

        return amount
