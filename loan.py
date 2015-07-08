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


import math
import random

import calculator
import game


class Loan:
    def __init__(self):
        self.amount = 0
        self.rate = random.randint(4, 15)
        self.timeout = random.randint(12, 20)

    def get_maximum(self):
        '''
        Get the maximum permissible amount to borrow.
        '''
        club = game.clubs[game.teamid]
        amount = club.reputation ** 2 * 10000
        maximum = calculator.value_rounder(amount)

        return maximum

    def update_interest_rate(self):
        if self.timeout > 0:
            self.timeout -= 1
        else:
            self.rate = random.randint(4, 15)
            self.timeout = random.randint(4, 20)


    def get_repayment(self, amount, weeks):
        '''
        Return the repayment amount.
        '''
        repayment = amount * (self.rate * 0.01 + 1) / weeks
        repayment = math.ceil(repayment)

        return repayment


    def repay_loan(self):
        '''
        Repayment of outstanding loan balance.
        '''
        if self.amount > 0:
            if self.get_repayment() > self.amount:
                repayment = self.amount
            else:
                repayment = self.get_repayment()

            game.bankloan.amount -= repayment

            game.clubs[game.teamid].accounts.withdraw(repayment, "loan")
