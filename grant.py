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


import game


class Grant:
    def __init__(self):
        self.timeout = 0
        self.status = 0
        self.amount = 0

    def get_grant_allowed(self):
        club = game.clubs[game.teamid]

        state = club.reputation < 13

        # Determine current bank balance
        if state:
            state = club.accounts.balance <= (150000 * club.reputation)

        # Determine stadium capacity
        if state:
            capacity = game.stadiums[club.stadium].capacity

            state = capacity < (1500 * club.reputation + (club.reputation * 0.5))

        return state

    def get_grant_maximum(self):
        amount = club.reputation ** 2 * 10000
        diff = amount * 0.1
        amount += random.randint(-diff, diff)

        maximum = calculator.value_rounder(amount)

        return maximum

    def get_grant_response(self):
        '''
        Determine whether the grant request is accepted or rejected.
        '''
        response = random.choice((True, False))  # Replace with AI

        return response

    def update_grant(self):
        '''
        Update grant timeout.
        '''
        if self.status == 1:
            if self.timeout > 0:
                self.timeout -= 1
            else:
                if self.get_grant_response():
                    self.status = 2

                    club = game.clubs[game.teamid]
                    club.accounts.deposit(amount=self.amount, category="grant")
                    game.news.publish("SG01", amount=self.amount)
                else:
                    self.status = 3

                    self.timeout = random.randint(26, 78)
        elif self.status == 2:
            if self.timeout > 0:
                self.timeout -= 1
            else:
                print("Grant running")
        elif self.status == 3:
            if self.timeout > 0:
                self.timeout -= 1
            else:
                self.status = 0

    def set_grant_application(self, amount):
        '''
        Apply for grant with set amount.
        '''
        self.timeout = random.randint(6, 10)
        self.status = 1
        self.amount = amount
