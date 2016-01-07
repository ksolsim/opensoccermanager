#!/usr/bin/env python3

from gi.repository import Gtk

import data
import uigtk.widgets


class Catering(uigtk.widgets.Grid):
    __name__ = "catering"

    class Item:
        def __init__(self, product=""):
            self.labelProduct = uigtk.widgets.Label(product, leftalign=True)
            self.labelDescription = uigtk.widgets.Label(leftalign=True)
            self.labelDescription.set_hexpand(True)
            self.labelCost = uigtk.widgets.Label(leftalign=True)
            self.labelSalePrice = uigtk.widgets.Label(leftalign=True)

            self.spinbuttonProfit = Gtk.SpinButton()
            self.spinbuttonProfit.set_range(-100, 1000)
            self.spinbuttonProfit.set_increments(10, 100)
            self.spinbuttonProfit.set_snap_to_ticks(True)
            self.spinbuttonProfit.set_numeric(False)
            self.spinbuttonProfit.set_value(100)
            self.spinbuttonProfit.connect("output", self.on_percentage_output)

        def on_percentage_output(self, spinbutton):
            '''
            Format percentage sign into spinbutton output.
            '''
            spinbutton.set_text("%i%%" % (spinbutton.get_value_as_int()))

            return True

    def __init__(self):
        uigtk.widgets.Grid.__init__(self)

        label = uigtk.widgets.Label("<b>Product</b>")
        self.attach(label, 0, 0, 1, 1)
        label = uigtk.widgets.Label("<b>Description</b>")
        self.attach(label, 1, 0, 1, 1)
        label = uigtk.widgets.Label("<b>Product Cost</b>")
        label.set_tooltip_text("The amount it costs to manufacture, transport and market the item.")
        self.attach(label, 2, 0, 1, 1)
        label = uigtk.widgets.Label("<b>Profit</b>")
        label.set_tooltip_text("The amount of profit we will make on the item sale.")
        self.attach(label, 3, 0, 1, 1)
        label = uigtk.widgets.Label("<b>Sale Cost</b>")
        label.set_tooltip_text("The total price that the customer will pay in the shop.")
        self.attach(label, 4, 0, 1, 1)

        self.products = []
        self.profit = []

    def setup_display_widgets(self):
        '''
        Setup interface with appropriate widgets to display data.
        '''
        for count, product in enumerate(self.club.catering.get_catering(), start=1):
            item = self.Item()

            item.labelProduct.set_label(product[0])
            self.attach(item.labelProduct, 0, count, 1, 1)
            self.attach(item.labelDescription, 1, count, 1, 1)
            item.labelCost.set_label("%s" % (data.currency.get_currency(product[1])))
            self.attach(item.labelCost, 2, count, 1, 1)
            self.attach(item.spinbuttonProfit, 3, count, 1, 1)

            self.attach(item.labelSalePrice, 4, count, 1, 1)

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
        cost = self.products[index][1]
        profit = (0.01 * value) * cost + cost

        return data.currency.get_currency(profit)

    def run(self):
        self.club = data.clubs.get_club_by_id(data.user.team)

        if self.products == []:
            self.setup_display_widgets()

        self.show_all()
