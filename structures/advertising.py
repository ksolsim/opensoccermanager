#!/usr/bin/env python3

import random

import data


class Advertising:
    class Advert:
        def __init__(self, name):
            club = data.clubs.get_club_by_id(data.user.team)

            self.name = name
            self.quantity = random.randint(1, 6)
            self.period = random.randint(1, 12)
            self.amount = (club.reputation + random.randint(-5, 5)) * 100

        def get_item(self):
            '''
            Return list containing advertisement details.
            '''
            item = [self.name, self.quantity, self.period, self.amount]

            return item

        def get_period(self):
            '''
            Return period string for display.
            '''
            if self.period > 1:
                period = "%i Weeks" % (self.period)
            else:
                period = "%i Week" % (self.period)

            return period

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
        Generate given number of advertisements and add to available list.
        '''
        self.regenerate = number

        companies = data.companies.get_companies()
        random.shuffle(companies)

        for name in companies[:number]:
            advert = self.Advert(name)
            advertid = self.get_advertid()
            self.available[self.advertid] = advert

    def get_advert_count(self):
        '''
        Return number of current advertisements.
        '''
        count = 0

        for advert in self.current.values():
            count += advert.quantity

        return count

    def move(self, advertid):
        '''
        Purchase advertisement and add to current list.
        '''
        advert = self.available[advertid]

        if self.get_advert_count() + advert.quantity <= self.maximum:
            self.current[advertid] = advert

            del self.available[advertid]