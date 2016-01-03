#!/usr/bin/env python3

from gi.repository import Gtk

import uigtk.widgets


class Catering(uigtk.widgets.Grid):
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

    def run(self):
        self.show_all()
