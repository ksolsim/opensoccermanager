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

import calculator
import game


class Overdraft:
    def __init__(self):
        self.amount = 0
        self.rate = random.randint(4, 15)
        self.timeout = random.randint(12, 20)

    def get_maximum(self):
        '''
        Return the maximum allowed overdraft.
        '''
        club = game.clubs[game.teamid]
        amount = ((club.accounts.balance * 0.5) * 0.05) * club.reputation
        amount = calculator.value_rounder(amount)

        return amount

    def update_interest_rate(self):
        '''
        Adjust the interest rate when the timeout hits zero.
        '''
        if self.timeout > 0:
            self.timeout -= 1
        else:
            self.rate = random.randint(4, 15)
            self.timeout = random.randint(12, 20)

    def pay_overdraft(self):
        '''
        Pay charge on current overdraft in use.
        '''
        if self.amount > 0:
            charge = self.amount * 0.01
            interest = 0

            if game.clubs[game.teamid].accounts.balance < 0:
                interest = self.amount * self.rate

            amount = charge + interest

            if amount > 0:
                game.clubs[game.teamid].accounts.withdraw(amount, "overdraft")
