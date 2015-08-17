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
import stadium
import user
import widgets


class Buildings(Gtk.Grid):
    __name__ = "buildings"

    def __init__(self):
        self.plots = 0
        self.total = 0            # Total cost
        self.futureplots = 0

        self.spins = []           # Store number spinbuttons
        self.labels = []          # Store subtotal labels
        self.display = []         # Labels for building and plot size
        self.buildings = []       # Number of buildings
        self.subtotals = [0] * 8  # Subtotal of all buildings

        Gtk.Grid.__init__(self)
        self.set_border_width(5)
        self.set_row_spacing(5)
        self.set_column_spacing(5)
        self.set_vexpand(True)
        self.set_hexpand(True)

        label = Gtk.Label("<b>Size</b>")
        label.set_use_markup(True)
        self.attach(label, 1, 0, 1, 1)
        label = Gtk.Label("<b>Cost</b>")
        label.set_use_markup(True)
        self.attach(label, 2, 0, 1, 1)
        label = Gtk.Label("<b>Quantity</b>")
        label.set_use_markup(True)
        self.attach(label, 3, 0, 1, 1)
        label = Gtk.Label("<b>Subtotal</b>")
        label.set_use_markup(True)
        self.attach(label, 4, 0, 1, 1)

        for count in range(0, 8):
            label1 = widgets.AlignedLabel()
            self.attach(label1, 0, count + 1, 1, 1)
            label2 = widgets.AlignedLabel()
            self.attach(label2, 1, count + 1, 1, 1)
            label3 = widgets.AlignedLabel()
            self.attach(label3, 2, count + 1, 1, 1)
            self.display.append([label1, label2, label3])

            spinbutton = Gtk.SpinButton.new_with_range(0, 8, 1)
            self.attach(spinbutton, 3, count + 1, 1, 1)
            self.spins.append(spinbutton)

            label = Gtk.Label()
            self.attach(label, 4, count + 1, 1, 1)
            self.labels.append(label)

        self.labelTotal = Gtk.Label()
        self.labelTotal.set_use_markup(True)
        self.attach(self.labelTotal, 4, 9, 1, 1)

        buttonbox = Gtk.ButtonBox()
        buttonbox.set_spacing(5)
        buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
        self.attach(buttonbox, 0, 10, 5, 1)
        self.buttonRevert = widgets.Button("_Revert")
        self.buttonRevert.connect("clicked", self.revert_building)
        buttonbox.add(self.buttonRevert)
        self.buttonConfirm = widgets.Button("_Build")
        self.buttonConfirm.set_sensitive(False)
        self.buttonConfirm.connect("clicked", self.confirm_building)
        buttonbox.add(self.buttonConfirm)

        self.labelFuturePlots = widgets.AlignedLabel()
        self.attach(self.labelFuturePlots, 0, 11, 1, 1)
        self.labelCurrentPlots = widgets.AlignedLabel()
        self.attach(self.labelCurrentPlots, 0, 12, 1, 1)

    def value_changed(self, spinbutton, index):
        self.futureplots = 0

        stadiumid = game.clubs[game.teamid].stadium
        stadium = game.stadiums[stadiumid]

        amount = spinbutton.get_value_as_int()
        buildings = self.buildings[index]
        difference = amount - buildings
        unitcost = constants.buildings[index][2]

        # Calculate construction or demolition cost
        if amount > self.buildings[index]:
            subtotal = difference * unitcost
            self.subtotals[index] = subtotal
        elif amount < self.buildings[index]:
            subtotal = (unitcost * 0.25) * (self.buildings[index] - amount)
            self.subtotals[index] = subtotal
        else:
            subtotal = 0
            self.subtotals[index] = subtotal

        for count, widget in enumerate(self.spins):
            value = widget.get_value_as_int()
            difference = value - self.buildings[count]
            plot_size = difference * constants.buildings[count][1]

            self.futureplots += plot_size

        self.futureplots += self.plots

        # Update total
        self.total = sum(self.subtotals)

        # Update labels
        subtotal = display.currency(subtotal)
        total = display.currency(self.total)
        self.labels[index].set_label("%s" % (subtotal))
        self.labelTotal.set_markup("<b>%s</b>" % (total))
        self.labelFuturePlots.set_label("Planned number of plots: %i" % (self.futureplots))

        if self.total > 0:
            self.buttonConfirm.set_sensitive(True)
        else:
            self.buttonConfirm.set_sensitive(False)

        if self.futureplots > stadium.plots:
            self.buttonConfirm.set_sensitive(False)

    def confirm_building(self, button):
        if dialogs.confirm_building(self.total):
            game.clubs[game.teamid].accounts.withdraw(amount=self.total, category="stadium")

            # Update stadium related values
            stadiumid = game.clubs[game.teamid].stadium
            stadium = game.stadiums[stadiumid]

            for count, widget in enumerate(self.spins):
                self.buildings[count] = widget.get_value_as_int()

            for count, item in enumerate(self.buildings):
                self.plots += self.buildings[count]
                stadium.buildings[count] = self.buildings[count]

            # Reset total labels and variables back to zero
            self.plots = self.futureplots
            self.futureplots = 0
            self.total = 0
            self.subtotals = [0] * 8
            self.buttonConfirm.set_sensitive(False)

            cost = display.currency(self.total)
            self.labelTotal.set_markup("<b>%s</b>" % (cost))
            self.labelFuturePlots.set_label("Planned number of plots: %i" % (self.futureplots))
            self.labelCurrentPlots.set_label("Used %i out of total %i plots available" % (self.plots, stadium.plots))

            for item in self.labels:
                cost = display.currency(0)
                item.set_label("%s" % (cost))

    def revert_building(self, button):
        for count, item in enumerate(self.buildings):
            self.spins[count].set_value(item)

    def run(self):
        club = user.get_user_club()

        stadium = stadiums.stadiumitem.stadiums[club.stadium]

        self.buildings = []
        self.plots = 0

        # Populate buildings, plot sizes and costs
        for count, item in enumerate(constants.buildings):
            self.display[count][0].set_label(item[0])
            self.display[count][1].set_label(str(item[1]))

            cost = display.currency(item[2])
            self.display[count][2].set_label(cost)

            cost = display.currency(0)
            self.labels[count].set_label("%s" % (cost))

            self.buildings.append(stadium.buildings[0 + count])
            self.spins[count].set_value(stadium.buildings[0 + count])
            self.spins[count].connect("value-changed", self.value_changed, count)

            # Total number of plots in use
            self.plots += stadium.buildings[0 + count] * item[1]

        self.labelFuturePlots.set_label("Planned number of plots: %i" % (self.futureplots))
        self.labelCurrentPlots.set_label("Used %i out of total %i plots available" % (self.plots, stadium.plots))

        cost = display.currency(0)
        self.labelTotal.set_markup("<b>%s</b>" % (cost))

        self.show_all()
