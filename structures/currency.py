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


import data


class Currency:
    def __init__(self):
        self.currency = {0: ("British Pound", "£", 1),
                         1: ("US Dollar", "$", 1.6),
                         2: ("Euro", "€", 1.25)}

    def get_amount(self, amount):
        '''
        Return converted amount to currency preference value.
        '''
        return amount * self.currency[data.preferences.currency][2]

    def get_currency(self, amount, integer=False):
        '''
        Return amount argument in converted currency.
        '''
        value = self.get_amount(amount)

        if integer:
            amount = "%s%i" % (self.currency[data.preferences.currency][1], value)
        else:
            amount = "%s%.2f" % (self.currency[data.preferences.currency][1], value)

        return amount

    def get_currency_names(self):
        '''
        Return the names of the currencies supported.
        '''
        names = [(key, item[0]) for key, item in self.currency.items()]

        return names

    def get_currency_symbol(self):
        '''
        Return the symbol for the given currency index.
        '''
        return self.currency[data.preferences.currency][1]

    def get_rounded_amount(self, amount):
        '''
        Round passed amount for displaying.
        '''
        if amount >= 1000000:
            amount = "%s%.1fM" % (self.get_currency_symbol(), amount / 1000000)
        elif amount >= 1000:
            amount = "%s%.1fK" % (self.get_currency_symbol(), amount / 1000)
        else:
            amount = "%s%i" % (self.get_currency_symbol(), amount)

        return amount

    def get_rounded_value(self, amount):
        '''
        Round passed amount for accessing.
        '''
        return int(5 * round(float(amount) / 5))

    def get_comma_value(self, amount):
        '''
        Return value formatted with commas.
        '''
        return "{:,}".format(amount)
