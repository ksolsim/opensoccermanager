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

import data


class Advertising:
    class Advert:
        def __init__(self, name):
            self.name = name
            self.quantity = random.randint(1, 6)
            self.period = random.randint(1, 12)
            self.amount = (data.user.club.reputation + random.randint(-5, 5)) * 100

        def get_period(self):
            '''
            Return period string for display.
            '''
            if self.period > 1:
                return "%i Weeks" % (self.period)
            else:
                return "%i Week" % (self.period)

    def __init__(self):
        self.advertid = 0

        self.available = {}
        self.current = {}
        self.maximum = 0

    def get_advertid(self):
        '''
        Return a unique advert id.
        '''
        self.advertid += 1

        return self.advertid

    def generate_adverts(self, number):
        '''
        Generate given number of adverts and add to available dictionary.
        '''
        self.regenerate = number

        companies = data.companies.get_companies()
        random.shuffle(companies)

        for name in companies[:number]:
            advert = self.Advert(name)
            advertid = self.get_advertid()
            self.available[advertid] = advert

    def get_advert_count(self):
        '''
        Return number of current advertisements.
        '''
        return sum(advert.quantity for advert in self.current.values())

    def move(self, advertid):
        '''
        Accept advertisement and add to current dictionary.
        '''
        advert = self.available[advertid]

        if self.get_advert_count() + advert.quantity <= self.maximum:
            self.current[advertid] = advert

            data.user.club.accounts.deposit(advert.amount, "advertising")

            del self.available[advertid]
