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

import display
import game


class Advertising:
    class Advert:
        def __init__(self, name):
            club = game.clubs[game.teamid]

            self.name = name
            self.amount = random.randint(1, 6)
            self.period = random.randint(4, 12)
            self.cost = (club.reputation + random.randint(-5, 5)) * 100

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
        self.alert = 0

    def initialise(self):
        self.companies = [item[0] for item in game.companies]

        self.generate()

    def generate(self):
        '''
        Regenerate the advertising on offer.
        '''
        club = game.clubs[game.teamid]

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

        club = game.clubs[game.teamid]
        cost = self.current[advertid].cost

        club.accounts.deposit(amount=cost, category="advertising")

    def assistant(self):
        '''
        Have assistant manager handle advertising dealings.
        '''
        pass

    def update(self):
        '''
        Countdown for alerts and regeneration of adverts.
        '''
        if self.alert > 0:
            self.alert -= 1
        else:
            if self.get_count() < 12:
                game.news.publish("BS04")

            self.alert = random.randint(10, 16)

        if self.timeout > 0:
            self.timeout -= 1
        else:
            self.generate()
            self.timeout = random.randint(8, 12)

    def get_count(self):
        '''
        Return number of adverts currently set.
        '''
        amount = 0

        for advert in self.current.values():
            amount += advert.amount

        return amount
