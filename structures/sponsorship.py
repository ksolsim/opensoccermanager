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
import uigtk.sponsorship


class Sponsorship:
    class Offer:
        def __init__(self):
            self.company = None
            self.period = 0
            self.amount = 0

    def __init__(self):
        self.offer = None

        self.timeout = 3
        self.status = 0

        self.date = None

    def generate_sponsorship(self):
        '''
        Create sponsorship offer details and announce to user.
        '''
        club = data.clubs.get_club_by_id(data.user.team)

        self.status = 1
        self.timeout = random.randint(6, 10)

        self.offer = self.Offer()
        self.offer.company = random.choice(data.companies.get_companies())
        self.offer.period = random.randint(1, 5)
        self.offer.amount = (club.reputation * random.randrange(950, 1100, 10)) * club.reputation ** 2

        club.news.publish("BS01")

    def update_sponsorship(self):
        self.timeout -= 1

        if self.timeout == 0:
            if self.status == 0:
                self.generate_sponsorship()
            elif self.status == 1:
                self.missed_offer()
            elif self.status == 2:
                self.offer.period -= 1

    def accept_offer(self):
        '''
        Update sponsorship to acceptance of offer.
        '''
        self.status = 2
        self.offer.period = self.offer.period * 52

        club = data.clubs.get_club_by_id(data.user.team)

        club.accounts.deposit(self.offer.amount, "sponsorship")

    def reject_offer(self):
        '''
        Update sponsorship to rejection of offer.
        '''
        self.status = 0
        self.timeout = random.randint(6, 10)

        self.offer = None

    def missed_offer(self):
        '''
        Reset sponsorship is offer timeout has passed.
        '''
        self.status = 0
        self.timeout = random.randint(6, 10)

        self.offer = None

        club = data.clubs.get_club_by_id(data.user.team)

        club.news.publish("BS03")

    def display_sponsorship_dialog(self):
        '''
        Determine which message dialog to display to the user.
        '''
        if self.status == 0:
            uigtk.sponsorship.NoOffer()
        elif self.status == 1:
            dialog = uigtk.sponsorship.NegotiateOffer()
            response = dialog.show()

            if response == 1:
                self.accept_offer()
            elif response == 0:
                self.reject_offer()
        else:
            uigtk.sponsorship.CurrentOffer()
