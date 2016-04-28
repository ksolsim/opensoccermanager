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

import data


class Categories:
    def __init__(self):
        self.categories = {0: (20000000, "Grandmother"),
                           1: (10000000, "Very Easy"),
                           2: (5000000, "Easy"),
                           3: (1000000, "Normal"),
                           4: (100000, "Hard"),
                           5: (0, "Very Hard")
                          }

    def get_categories(self):
        '''
        Return dictionary items for categories.
        '''
        return self.categories.items()

    def get_value_by_index(self, index):
        '''
        Return finance amount for given index value.
        '''
        return self.categories[index][0]


class Finances:
    class Loan:
        '''
        Bank loan class handling maximum allowed, interest rates, and repayment.
        '''
        def __init__(self):
            self.amount = 0
            self.period = 0

            self.interest = random.randint(3, 15)
            self.timeout = random.randint(12, 20)

            self.update_interest_rate()

        def get_loan_permitted(self):
            '''
            Return whether bank is willing to provide loan.
            '''
            return data.user.club.accounts.balance > 0

        def get_loan_active(self):
            '''
            Return if club currently has an active loan.
            '''
            return self.amount > 0

        def get_maximum_loan(self):
            '''
            Return maximum permissible loan club can receive.
            '''
            return data.user.club.reputation ** 2 * 10000

        def get_weekly_repayment(self, amount, period):
            '''
            Return amount to be paid weekly.
            '''
            amount = amount * (self.interest * 0.01 + 1) / (period * 52)
            amount = math.ceil(amount)

            return amount

        def update_interest_rate(self):
            '''
            Countdown timeout to update interest rate.
            '''
            self.timeout -= 1

            if self.timeout == 0:
                self.interest = random.randint(3, 15)
                self.timeout = random.randint(12, 20)

    class Overdraft:
        '''
        Overdraft class defining maximum overdraft and the interest rate.
        '''
        def __init__(self):
            self.amount = 0

            self.interest = random.randint(3, 15)
            self.timeout = random.randint(12, 20)

            self.update_interest_rate()

        def get_overdraft_active(self):
            '''
            Return whether an overdraft is currently set.
            '''
            return self.amount > 0

        def get_maximum_overdraft(self):
            '''
            Return the maximum allowed overdraft.
            '''
            return int(((data.user.club.accounts.balance * 0.5) * 0.05) * data.user.club.reputation)

        def update_interest_rate(self):
            '''
            Countdown timeout to update interest rate.
            '''
            self.timeout -= 1

            if self.timeout == 0:
                self.interest = random.randint(3, 15)
                self.timeout = random.randint(12, 20)

    class Grant:
        '''
        Grant structure dealing with whether a grant is permitted and the amount.
        '''
        def __init__(self):
            self.weeks = 24

        def decrement_grant_period(self):
            '''
            Decrement amount of time until grant money must be used.
            '''

        def get_maximum_grant(self):
            '''
            Return the maximum permitted stadium improvement grant.
            '''
            pass

        def get_grant_available(self):
            '''
            Return if club is able to receive the stadium improvement grant.
            '''
            available = False

            if data.user.club.reputation < 12:
                available = True

            return available

    class Flotation:
        '''
        Flotation class handling flotation and the amount which will be raised.
        '''
        def __init__(self):
            self.pending = False
            self.public = False

            self.timeout = 0

        def get_float_amount(self):
            '''
            Return amount of money available via flotation.
            '''
            return data.user.club.reputation ** 2 * 100000

        def set_initiate_float(self):
            '''
            Initialise timeout to countdown time until going public.
            '''
            self.timeout = random.randint(12, 18)
            self.pending = True

            data.user.club.news.publish("FL01")

        def set_float_public(self):
            '''
            Complete flotation of the club.
            '''
            self.public = True

            data.user.club.news.publish("FL02")

        def decrement_float_period(self):
            '''
            Countdown time until club goes on the stock market.
            '''
            if self.timeout > 0:
                self.timeout -= 1
            else:
                self.set_float_public()

    def __init__(self):
        self.loan = self.Loan()
        self.overdraft = self.Overdraft()
        self.grant = self.Grant()
        self.flotation = self.Flotation()
