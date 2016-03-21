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
import os

import data
import uigtk.widgets


class Totals(uigtk.widgets.CommonFrame):
    def __init__(self, shops):
        self.shops = shops

        uigtk.widgets.CommonFrame.__init__(self, "Details")

        label = uigtk.widgets.Label("Used Plots", leftalign=True)
        self.grid.attach(label, 0, 0, 1, 1)
        self.labelUsedPlots = uigtk.widgets.Label(leftalign=True)
        self.grid.attach(self.labelUsedPlots, 1, 0, 1, 1)

        label = uigtk.widgets.Label("Maximum Plots", leftalign=True)
        self.grid.attach(label, 0, 1, 1, 1)
        self.labelMaximumPlots = uigtk.widgets.Label(leftalign=True)
        self.grid.attach(self.labelMaximumPlots, 1, 1, 1, 1)

        label = uigtk.widgets.Label("Available Grant", leftalign=True)
        self.grid.attach(label, 0, 2, 1, 1)
        self.labelAvailableGrant = uigtk.widgets.Label(leftalign=True)
        self.grid.attach(self.labelAvailableGrant, 1, 2, 1, 1)

        label = uigtk.widgets.Label("Construction Cost", leftalign=True)
        self.grid.attach(label, 0, 3, 1, 1)
        self.labelConstructionCost = uigtk.widgets.Label(leftalign=True)
        self.grid.attach(self.labelConstructionCost, 1, 3, 1, 1)

        buttonbox = uigtk.widgets.ButtonBox()
        buttonbox.set_hexpand(True)
        buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
        self.grid.attach(buttonbox, 0, 5, 2, 1)

        buttonReset = uigtk.widgets.Button("_Reset")
        buttonReset.set_sensitive(False)
        buttonReset.set_tooltip_text("Reset changes made to building configuration.")
        buttonbox.add(buttonReset)
        buttonApply = uigtk.widgets.Button("_Apply")
        buttonApply.set_tooltip_text("Apply changes made to number of buildings.")
        buttonApply.connect("clicked", self.on_apply_clicked)
        buttonbox.add(buttonApply)

    def update_used_plots(self):
        '''
        Set number of used building plots.
        '''
        self.labelUsedPlots.set_label("%i" % (self.shops.get_building_count()))

    def update_maximum_plots(self):
        '''
        Set maximum allowable building plots.
        '''
        self.labelMaximumPlots.set_label("%i" % (data.user.club.stadium.buildings.maximum_plots))

    def update_grant_status(self):
        '''
        Update upgrade status and total costs.
        '''
        if not data.user.club.finances.grant.get_grant_available():
            self.labelAvailableGrant.set_label("Grant unavailable")

    def calculate_construction_cost(self):
        '''
        Calculate cost of construction works.
        '''
        cost = 0

        for shop in Buildings.shops:
            if shop.spinbutton.get_value_as_int() < shop.building.number:
                cost  += (shop.building.cost * 0.25) * (shop.building.number - shop.spinbutton.get_value_as_int())
            else:
                cost += shop.building.cost * (shop.spinbutton.get_value_as_int() - shop.building.number)

        return cost

    def update_construction_cost(self):
        '''
        Update label displaying cost of construction work.
        '''
        cost = self.calculate_construction_cost()
        cost = data.currency.get_currency(cost, integer=True)
        self.labelConstructionCost.set_label(cost)

    def on_apply_clicked(self, *args):
        '''
        Get plot size and ask to confirm upgrade.
        '''
        plots = sum(shop.building.size * shop.spinbutton.get_value_as_int() for shop in Buildings.shops)

        cost = self.calculate_construction_cost()
        dialog = ConfirmBuilding(cost)

        if dialog.show():
            if data.user.club.accounts.request(cost):
                for shop in Buildings.shops:
                    shop.building.number = shop.spinbutton.get_value_as_int()

                data.user.club.accounts.withdraw(cost, "stadium")
                self.update_construction_cost()

    def on_reset_clicked(self, button):
        '''
        Reset changed building count spinbuttons and labels.
        '''
        button.set_sensitive(False)


class Buildings(uigtk.widgets.Grid):
    __name__ = "buildings"

    shops = None
    totals = None

    def __init__(self):
        uigtk.widgets.Grid.__init__(self)

        grid = uigtk.widgets.Grid()
        grid.set_vexpand(True)
        grid.set_row_homogeneous(True)
        grid.set_column_homogeneous(True)
        self.attach(grid, 0, 0, 1, 1)

        Buildings.shops = Shops()
        self.attach(Buildings.shops, 0, 0, 1, 1)

        Buildings.totals = Totals(self.shops)
        self.attach(Buildings.totals, 1, 0, 1, 1)

    def run(self):
        self.shops.set_building_count()

        self.totals.update_used_plots()
        self.totals.update_maximum_plots()
        self.totals.update_grant_status()

        self.show_all()


class Shops(uigtk.widgets.Grid):
    def __init__(self):
        uigtk.widgets.Grid.__init__(self)

        self.shops = []

        row = 0
        column = 0

        for count, shop in enumerate(data.buildings.get_buildings()):
            shop = Shop(count)
            self.shops.append(shop)
            self.attach(shop, column, row, 1, 1)

            if column == 3:
                row += 1
                column = 0
            else:
                column += 1

    def set_building_count(self):
        '''
        Set number of buildings on to interface.
        '''
        for count, building in enumerate(data.user.club.stadium.buildings.get_buildings()):
            self.shops[count].spinbutton.set_value(building.number)

    def get_building_count(self):
        '''
        Return number of buildings on interface.
        '''
        plots = 0

        for count, shop in enumerate(self.shops):
            building = data.buildings.get_building_by_index(count)
            plots += building.size * shop.spinbutton.get_value_as_int()

        return plots


class Shop(uigtk.widgets.Grid):
    def __init__(self, index):
        uigtk.widgets.Grid.__init__(self)

        self.building = data.user.club.stadium.buildings.get_building_by_index(index)

        self.labelName = uigtk.widgets.Label("<b>_%s</b>" % (self.building.name))
        self.attach(self.labelName, 0, 0, 2, 1)
        self.labelSize = Gtk.Label("Size %i" % (self.building.size))
        self.attach(self.labelSize, 0, 1, 1, 1)
        self.labelCost = Gtk.Label("Cost %s" % (data.currency.get_currency(self.building.cost, integer=True)))
        self.attach(self.labelCost, 1, 1, 1, 1)

        filepath = os.path.join("resources", "%s.png" % (self.building.filename))
        image = Gtk.Image.new_from_file(filepath)
        self.attach(image, 0, 2, 2, 1)

        label = uigtk.widgets.Label("Number")
        self.attach(label, 0, 3, 1, 1)
        self.spinbutton = Gtk.SpinButton()
        self.spinbutton.set_range(0, 10)
        self.spinbutton.set_increments(1, 2)
        self.spinbutton.connect("value-changed", self.on_plots_changed)
        self.labelName.set_mnemonic_widget(self.spinbutton)
        self.attach(self.spinbutton, 1, 3, 1, 1)

    def on_plots_changed(self, spinbutton):
        '''
        Update number of used plots on spinbutton adjustment.
        '''
        Buildings.totals.update_used_plots()

        self.update_construction_cost(spinbutton)

    def update_construction_cost(self, spinbutton):
        '''
        Update cost of construction works.
        '''
        Buildings.totals.update_construction_cost()


class ConfirmBuilding(Gtk.MessageDialog):
    '''
    Message dialog to confirm whether new buildings should be built.
    '''
    def __init__(self, cost):
        Gtk.MessageDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_modal(True)
        self.set_title("Confirm Building Construction")
        self.set_markup("<span size='12000'><b>Do you want to build the specified new shops?</b></span>")
        self.format_secondary_text("The cost of construction will be %s." % (data.currency.get_currency(cost, integer=True)))
        self.add_button("_Cancel Construction", Gtk.ResponseType.CANCEL)
        self.add_button("C_onfirm Construction", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.CANCEL)

    def show(self):
        state = self.run() == Gtk.ResponseType.OK
        self.destroy()

        return state
