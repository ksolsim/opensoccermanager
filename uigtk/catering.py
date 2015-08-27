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

import constants
import display
import game
import user
import widgets


class Catering(Gtk.Grid):
    __name__ = "catering"

    def __init__(self):
        self.display = []
        self.spins = []

        Gtk.Grid.__init__(self)
        self.set_vexpand(True)
        self.set_hexpand(True)
        self.set_border_width(5)
        self.set_row_spacing(5)
        self.set_column_spacing(5)

        label = Gtk.Label("<b>Production Cost</b>")
        label.set_use_markup(True)
        self.attach(label, 1, 0, 1, 1)
        label = Gtk.Label("<b>Profit Percentage</b>")
        label.set_use_markup(True)
        self.attach(label, 2, 0, 1, 1)
        label = Gtk.Label("<b>Sale Price</b>")
        label.set_use_markup(True)
        self.attach(label, 3, 0, 1, 1)

        separator = Gtk.Separator()
        separator.set_orientation(Gtk.Orientation.VERTICAL)
        self.attach(separator, 4, 1, 1, 12)

        label = Gtk.Label("<b>Quantity Sold</b>")
        label.set_use_markup(True)
        self.attach(label, 5, 0, 1, 1)
        label = Gtk.Label("<b>Income</b>")
        label.set_use_markup(True)
        self.attach(label, 6, 0, 1, 1)
        label = Gtk.Label("<b>Profit</b>")
        label.set_use_markup(True)
        self.attach(label, 7, 0, 1, 1)

        for index in range(0, 9):
            label1 = widgets.AlignedLabel()
            self.attach(label1, 0, index + 1, 1, 1)
            label2 = Gtk.Label()
            self.attach(label2, 1, index + 1, 1, 1)
            label3 = Gtk.Label()
            self.attach(label3, 3, index + 1, 1, 1)

            spinbutton = Gtk.SpinButton.new_with_range(-100, 1000, 10)
            spinbutton.set_snap_to_ticks(True)
            spinbutton.set_numeric(False)
            spinbutton.connect("output", self.format_output)
            spinbutton.connect("value-changed", self.value_changed, index)
            self.attach(spinbutton, 2, index + 1, 1, 1)
            self.spins.append(spinbutton)

            label4 = Gtk.Label()
            self.attach(label4, 5, index + 1, 1, 1)
            label5 = Gtk.Label()
            self.attach(label5, 6, index + 1, 1, 1)
            label6 = Gtk.Label()
            self.attach(label6, 7, index + 1, 1, 1)

            self.display.append([label1, label2, label3, label4, label5, label6])

    def format_output(self, spinbutton):
        value = spinbutton.get_value_as_int()
        spinbutton.set_text("%i%%" % (value))

        return True

    def value_changed(self, spinbutton, index):
        club = user.get_user_club()

        club.catering.percentages[index] = spinbutton.get_value()

        cost = constants.catering[index][1]

        profit = (self.spins[index].get_value() * 0.01) * cost + cost
        profit = display.currency(profit, mode=1)
        self.display[index][2].set_label("%s" % (profit))

    def run(self):
        club = user.get_user_club()

        for count, item in enumerate(constants.catering):
            self.display[count][0].set_label(item[0])
            cost = display.currency(item[1], mode=1)
            self.display[count][1].set_label("%s" % (cost))

            value = club.catering.percentages[count]
            self.spins[count].set_value(value)

            profit = (self.spins[count].get_value() * 0.01) * item[1] + item[1]
            profit = display.currency(profit, mode=1)
            self.display[count][2].set_label("%s" % (profit))

            if len(club.catering.sales) > 0:
                sales = "%i" % (club.catering.sales[count][0])

                revenue = club.catering.sales[count][1]
                cost = club.catering.sales[count][2]
                profit = revenue - cost

                revenue = display.currency(revenue)
                self.display[count][4].set_label(revenue)

                profit = display.currency(profit)
                self.display[count][5].set_label(profit)
            else:
                sales = "No Sales"

            self.display[count][3].set_label(sales)

        self.show_all()
