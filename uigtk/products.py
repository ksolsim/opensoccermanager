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

import uigtk.widgets


class Products(Gtk.Notebook):
    def __init__(self):
        Gtk.Notebook.__init__(self)
        self.set_vexpand(True)
        self.set_hexpand(True)

        self.pricing = Pricing()
        self.append_page(self.pricing, uigtk.widgets.Label("_Pricing"))

        self.sales = Sales()
        self.append_page(self.sales, uigtk.widgets.Label("_Sales"))


class Pricing(uigtk.widgets.Grid):
    '''
    Notebook tab displaying pricing adjustment widgets.
    '''
    def __init__(self):
        uigtk.widgets.Grid.__init__(self)
        self.set_border_width(5)

        label = uigtk.widgets.Label("<b>Product</b>")
        self.attach(label, 0, 0, 1, 1)
        label = uigtk.widgets.Label("<b>Description</b>")
        self.attach(label, 1, 0, 1, 1)
        label = uigtk.widgets.Label("<b>Production Cost</b>")
        label.set_tooltip_text("The amount it costs to manufacture, transport and market the item.")
        self.attach(label, 2, 0, 1, 1)
        label = uigtk.widgets.Label("<b>Profit Percentage</b>")
        label.set_tooltip_text("The amount of profit we want to make on this item.")
        self.attach(label, 3, 0, 1, 1)
        label = uigtk.widgets.Label("<b>Sale Price</b>")
        label.set_tooltip_text("The total price that the customer will pay in the shop.")
        self.attach(label, 4, 0, 1, 1)


class Sales(uigtk.widgets.Grid):
    '''
    Notebook tab displaying sales data from previous matches.
    '''
    def __init__(self):
        uigtk.widgets.Grid.__init__(self)
        self.set_border_width(5)


class Item:
    '''
    Combination labels and spinbutton for defining product pricing.
    '''
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
        self.labelProduct.set_mnemonic_widget(self.spinbuttonProfit)
        self.spinbuttonProfit.connect("output", self.on_percentage_output)

    def on_percentage_output(self, spinbutton):
        '''
        Format percentage sign into spinbutton output.
        '''
        spinbutton.set_text("%i%%" % (spinbutton.get_value_as_int()))

        return True
