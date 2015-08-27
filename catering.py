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

import constants
import game


class Catering:
    def __init__(self):
        self.percentages = [100] * len(constants.catering)

        self.sales = []

    def calculate_sales(self, attendance):
        '''
        Determine sales of merchandise for the given attendance.
        '''
        club = user.get_user_club()

        self.reset_sales()

        for count, profit_percentage in enumerate(self.percentages):
            multiplier = constants.catering[count][2]
            multiplier += random.randint(-3, 3)

            potential_sales = attendance * (multiplier * 0.01)
            sale_percentage = 200 - profit_percentage

            if sale_percentage < 0:
                sale_percentage = 0

            sales = int((potential_sales * 0.25 * 0.01) * sale_percentage)

            income = sales * (constants.catering[count][1] + (constants.catering[count][1] * (profit_percentage * 0.01)))
            profit = income - (sales * constants.catering[count][1])
            cost = income - profit

            self.sales.append([sales, income, profit])

            club.accounts.deposit(amount=income, category="catering")
            club.accounts.withdraw(amount=cost, category="catering")

    def reset_sales(self):
        '''
        Reset sales data list back to empty.
        '''
        self.sales = []
