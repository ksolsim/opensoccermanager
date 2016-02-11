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


from gi.repository import Gtk

import data
import uigtk.products
import uigtk.widgets


class Catering(uigtk.products.Products):
    __name__ = "catering"

    def __init__(self):
        uigtk.products.Products.__init__(self)

        self.products = []
        self.profit = []

    def setup_display_widgets(self):
        '''
        Setup interface with appropriate widgets to display data.
        '''
        for count, product in enumerate(self.club.catering.get_catering(), start=1):
            item = uigtk.products.Item()

            item.labelProduct.set_label(product[0])
            self.pricing.attach(item.labelProduct, 0, count, 1, 1)
            self.pricing.attach(item.labelDescription, 1, count, 1, 1)
            item.labelCost.set_label("%s" % (data.currency.get_currency(product[1])))
            self.pricing.attach(item.labelCost, 2, count, 1, 1)
            self.pricing.attach(item.spinbuttonProfit, 3, count, 1, 1)

            self.pricing.attach(item.labelSalePrice, 4, count, 1, 1)

            item.spinbuttonProfit.connect("value-changed", self.on_profit_changed, count - 1)

            self.products.append(product)
            self.profit.append(item.labelSalePrice)

            profit = self.calculate_profit(100, count - 1)
            item.labelSalePrice.set_label(profit)

    def on_profit_changed(self, spinbutton, index):
        '''
        Update sale price of product on change of spin button percentage.
        '''
        profit = self.calculate_profit(spinbutton.get_value_as_int(), index)

        self.profit[index].set_label(profit)

    def calculate_profit(self, value, index):
        '''
        Determine profit of each item.
        '''
        cost = self.products[index][1]
        profit = (0.01 * value) * cost + cost

        return data.currency.get_currency(profit)

    def run(self):
        self.club = data.clubs.get_club_by_id(data.user.team)

        if self.products == []:
            self.setup_display_widgets()

        self.show_all()
