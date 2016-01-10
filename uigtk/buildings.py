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


class Buildings(uigtk.widgets.Grid):
    __name__ = "buildings"

    def __init__(self):
        uigtk.widgets.Grid.__init__(self)

        grid = uigtk.widgets.Grid()
        grid.set_vexpand(True)
        grid.set_row_homogeneous(True)
        grid.set_column_homogeneous(True)
        self.attach(grid, 0, 0, 1, 1)

        self.totals = Totals()

        row = 0
        column = 0

        for count, shop in enumerate(data.buildings.get_buildings()):
            shop = Shop(count)
            shop.total = self.totals
            grid.attach(shop, column, row, 1, 1)

            if column == 3:
                row += 1
                column = 0
            else:
                column += 1

        grid = uigtk.widgets.Grid()
        self.attach(grid, 1, 0, 1, 1)

        grid.attach(self.totals, 0, 1, 1, 1)

    def set_building_count(self):
        for building in data.buildings.get_buildings():
            pass

    def run(self):
        self.set_building_count()

        self.totals.update_grant_status()
        self.totals.update_maximum_plots()

        self.totals.update_used_plots()

        self.show_all()


class Shop(uigtk.widgets.Grid):
    def __init__(self, index):
        uigtk.widgets.Grid.__init__(self)

        building = data.buildings.get_building_by_index(index)

        self.labelName = uigtk.widgets.Label("<b>_%s</b>" % (building.name))
        self.attach(self.labelName, 0, 0, 2, 1)
        self.labelSize = Gtk.Label("Size %i" % (building.size))
        self.attach(self.labelSize, 0, 1, 1, 1)
        self.labelCost = Gtk.Label("Cost %s" % (data.currency.get_currency(building.cost, integer=True)))
        self.attach(self.labelCost, 1, 1, 1, 1)

        filepath = os.path.join("resources", "%s.png" % (building.filename))
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
        spinbutton.get_value_as_int()

        self.total.update_used_plots()


class Totals(uigtk.widgets.CommonFrame):
    plots = 0

    def __init__(self):
        uigtk.widgets.CommonFrame.__init__(self, "Totals")

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

        label = uigtk.widgets.Label("Upgrade Cost", leftalign=True)
        self.grid.attach(label, 0, 3, 1, 1)
        self.labelUpgradeCost = uigtk.widgets.Label(leftalign=True)
        self.grid.attach(self.labelUpgradeCost, 1, 3, 1, 1)

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
        club = data.clubs.get_club_by_id(data.user.team)
        stadium = data.stadiums.get_stadium_by_id(club.stadium)

        self.labelUsedPlots.set_label("%i" % stadium.buildings.get_used_plots())

    def update_maximum_plots(self):
        '''
        Display maximum allowable building plots.
        '''
        club = data.clubs.get_club_by_id(data.user.team)
        stadium = data.stadiums.get_stadium_by_id(club.stadium)

        self.labelMaximumPlots.set_label("%i" % (stadium.buildings.maximum_plots))

    def update_grant_status(self):
        '''
        Update upgrade status and total costs.
        '''
        club = data.clubs.get_club_by_id(data.user.team)

        if not club.finances.grant.get_grant_available():
            self.labelAvailableGrant.set_label("Grant unavailable")

    def on_apply_clicked(self, *args):
        '''
        Get plot size and ask to confirm upgrade.
        '''
        plots = 0

        for shop in Buildings.shops:
            plots += shop.size * shop.spinbutton.get_value_as_int()

        dialog = ConfirmBuilding()
        dialog.show()

    def on_reset_clicked(self, button):
        '''
        Reset changed building count spinbuttons and labels.
        '''
        button.set_sensitive(False)


class ConfirmBuilding(Gtk.MessageDialog):
    def __init__(self):
        Gtk.MessageDialog.__init__(self)
        self.set_modal(True)
        self.set_title("Confirm Building Upgrades")
        self.set_markup("<span size='12000'><b>Do you want to build the specified new shops?</b></span>")
        self.format_secondary_text("The cost to upgrade will be %s" % (cost))
        self.add_button("_Cancel Upgrade", Gtk.ResponseType.CANCEL)
        self.add_button("Confirm _Upgrade", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.CANCEL)

    def show(self):
        self.run()
        self.destroy()
