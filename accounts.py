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


import collections

import game


class Accounts:
    class Item:
        def __init__(self):
            self.week = 0
            self.season = 0

    def __init__(self):
        incomes = (("prize", self.Item()),
                   ("sponsorship", self.Item()),
                   ("advertising", self.Item()),
                   ("merchandise", self.Item()),
                   ("catering", self.Item()),
                   ("tickets", self.Item()),
                   ("transfers", self.Item()),
                   ("loan", self.Item()),
                   ("television", self.Item()),
                  )

        self.incomes = collections.OrderedDict(incomes)

        expenditures = (("fines", self.Item()),
                        ("stadium", self.Item()),
                        ("staffwage", self.Item()),
                        ("playerwage", self.Item()),
                        ("transfers", self.Item()),
                        ("merchandise", self.Item()),
                        ("catering", self.Item()),
                        ("loan", self.Item()),
                        ("overdraft", self.Item()),
                        ("training", self.Item()),
                       )

        self.expenditures = collections.OrderedDict(expenditures)

        self.income = 0
        self.expenditure = 0
        self.balance = 0

    def deposit(self, amount, category):
        '''
        Deposit the specified amount of money.
        '''
        self.incomes[category].week += amount
        self.incomes[category].season += amount

        self.income += amount
        self.balance += amount

    def withdraw(self, amount, category):
        '''
        Withdraw the specified amount of money.
        '''
        self.expenditures[category].week += amount
        self.expenditures[category].season += amount

        self.expenditure += amount
        self.balance -= amount

    def request(self, amount):
        '''
        Verify whether the withdrawal amount is permitted against the balance.
        '''
        if (self.balance + game.overdraft.amount) - amount >= 0:
            #self.withdraw(amount, category)
            state = True
        else:
            state = False

        return state

    def reset_accounts(self):
        '''
        Reset the weekly and season ledgers back to zero.
        '''
        for item in self.incomes.values():
            item.week = 0
            item.season = 0

        for item in self.expenditures.values():
            item.week = 0
            item.season = 0

        self.income = 0
        self.expenditure = 0

    def reset_weekly(self):
        '''
        Reset the weekly ledger back to zero.
        '''
        for item in self.incomes.values():
            item.week = 0

        for item in self.expenditures.values():
            item.week = 0
