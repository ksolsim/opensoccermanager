#!/usr/bin/env python3

import data


class Currency:
    def __init__(self):
        self.currency = {0: ("British Pound", "£", 1),
                         1: ("US Dollar", "$", 1.6),
                         2: ("Euro", "€", 1.25)}

    def get_currency(self, amount, integer=False):
        '''
        Return amount argument in converted currency.
        '''
        value = (amount * self.currency[data.preferences.currency][2])

        if not integer:
            amount = "%s%.2f" % (self.currency[data.preferences.currency][1], value)
        else:
            amount = "%s%i" % (self.currency[data.preferences.currency][1], value)

        return amount

    def get_currency_names(self):
        '''
        Return the name of the currency.
        '''
        names = [(key, item[0]) for key, item in self.currency.items()]

        return names

    def get_currency_symbol(self):
        '''
        Return the symbol for the given currency index.
        '''
        index = data.preferences.currency

        return self.currency[index][1]

    def get_rounded_amount(self, amount):
        '''
        Round passed amount for displaying.
        '''
        if amount >= 1000000:
            amount = "£%.1fM" % (amount / 1000000)
        elif amount >= 1000:
            amount = "£%iK" % (amount / 1000)
        else:
            amount = "£%i" % (amount)

        return amount
