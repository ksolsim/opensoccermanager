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

import calculator
import constants
import dialogs
import display
import game
import stadium
import user
import widgets


class Stadium(Gtk.Grid):
    __name__ = "stadium"

    def __init__(self):
        self.main_stand_widget = []
        self.corner_stand_widget = []
        self.roof_widget = []
        self.standing_widget = []
        self.box_widget = []

        Gtk.Grid.__init__(self)
        self.set_vexpand(True)
        self.set_hexpand(True)
        self.set_border_width(5)
        self.set_row_spacing(5)
        self.set_column_spacing(5)

        # Details
        frame = widgets.CommonFrame("Details")
        self.attach(frame, 0, 0, 1, 1)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        frame.insert(grid)

        label = widgets.AlignedLabel("Current Capacity")
        grid.attach(label, 0, 1, 1, 1)
        self.labelCurrentCapacity = widgets.AlignedLabel()
        grid.attach(self.labelCurrentCapacity, 1, 1, 1, 1)
        label = widgets.AlignedLabel("Upgraded Capacity")
        grid.attach(label, 0, 2, 1, 1)
        self.labelUpgradeCapacity = widgets.AlignedLabel("0")
        grid.attach(self.labelUpgradeCapacity, 1, 2, 1, 1)
        label = widgets.AlignedLabel("Upgrade Cost")
        grid.attach(label, 3, 1, 1, 1)
        self.labelCost = widgets.AlignedLabel()
        grid.attach(self.labelCost, 4, 1, 1, 1)
        label = widgets.AlignedLabel("Stadium Condition")
        grid.attach(label, 3, 2, 1, 1)
        self.labelCondition = widgets.AlignedLabel()
        grid.attach(self.labelCondition, 4, 2, 1, 1)

        notebook = Gtk.Notebook()
        notebook.set_vexpand(True)
        notebook.set_hexpand(True)
        self.attach(notebook, 0, 2, 1, 1)

        # Capacity
        grid = Gtk.Grid()
        grid.set_border_width(5)
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        label = widgets.Label("_Capacity")
        notebook.append_page(grid, label)

        # Stand labels
        for count, text in enumerate(constants.stands):
            label = widgets.AlignedLabel("%s Stand" % (text))
            grid.attach(label, 0, count, 1, 1)

        # Main stands
        for count in range(0, 4):
            spinbutton = Gtk.SpinButton.new_with_range(0, 15000, 1000)
            spinbutton.set_snap_to_ticks(True)
            spinbutton.connect("value-changed", self.main_changed, count)
            grid.attach(spinbutton, 1, count, 1, 1)
            self.main_stand_widget.append(spinbutton)

        # Corner stands
        for count in range(4, 8):
            spinbutton = Gtk.SpinButton.new_with_range(0, 3000, 1000)
            spinbutton.set_snap_to_ticks(True)
            spinbutton.set_sensitive(False)
            spinbutton.connect("value-changed", self.corner_changed, count)
            grid.attach(spinbutton, 1, count, 1, 1)
            self.corner_stand_widget.append(spinbutton)

        # Roof
        for count in range(0, 8):
            checkbutton = Gtk.CheckButton("Roof")
            checkbutton.set_sensitive(False)
            checkbutton.connect("toggled", self.roof_changed, count)
            grid.attach(checkbutton, 2, count, 1, 1)
            self.roof_widget.append(checkbutton)

        # Standing / Seating
        for count in range(0, 8):
            radiobutton1 = Gtk.RadioButton("Standing")
            radiobutton1.set_sensitive(False)
            radiobutton1.connect("toggled", self.standing_changed, count)
            grid.attach(radiobutton1, 3, count, 1, 1)
            radiobutton2 = Gtk.RadioButton("Seating", group=radiobutton1)
            radiobutton2.set_sensitive(False)
            radiobutton2.connect("toggled", self.standing_changed, count)
            grid.attach(radiobutton2, 4, count, 1, 1)
            self.standing_widget.append([radiobutton1, radiobutton2])

        # Boxes
        for count in range(0, 4):
            label = widgets.AlignedLabel("Executive Box")
            grid.attach(label, 5, count, 1, 1)
            spinbutton = Gtk.SpinButton.new_with_range(0, 500, 250)
            spinbutton.set_snap_to_ticks(True)
            spinbutton.set_sensitive(False)
            spinbutton.connect("value-changed", self.box_changed, count)
            grid.attach(spinbutton, 6, count, 1, 1)
            self.box_widget.append(spinbutton)

        buttonbox = Gtk.ButtonBox()
        buttonbox.set_spacing(5)
        buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
        grid.attach(buttonbox, 0, 8, 2, 1)
        self.buttonRevert = widgets.Button("_Revert")
        self.buttonRevert.connect("clicked", self.revert_upgrade)
        buttonbox.add(self.buttonRevert)
        self.buttonConfirm = widgets.Button("_Build")
        self.buttonConfirm.connect("clicked", self.confirm_upgrade)
        buttonbox.add(self.buttonConfirm)

        grid = Gtk.Grid()
        grid.set_border_width(5)
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        label = widgets.Label("_Maintenance")
        notebook.append_page(grid, label)

        label = widgets.AlignedLabel("Stadium Upkeep Percentage:")
        grid.attach(label, 0, 0, 1, 1)
        self.spinbuttonMaintenance = Gtk.SpinButton.new_with_range(0, 110, 1)
        self.spinbuttonMaintenance.connect("value-changed", self.maintenance_changed)
        grid.attach(self.spinbuttonMaintenance, 1, 0, 1, 1)
        label = widgets.AlignedLabel("Cost Per Month:")
        grid.attach(label, 0, 1, 1, 1)
        self.labelMaintenanceCost = widgets.AlignedLabel()
        grid.attach(self.labelMaintenanceCost, 1, 1, 1, 1)

    def run(self):
        clubobj = user.get_user_club()
        stadiumobj = stadium.get_stadium(clubobj.stadium)

        self.update_capacity()
        self.revert_upgrade()

        self.cost = 0
        cost = display.currency(self.cost)
        self.labelCost.set_label("%s" % (cost))

        self.spinbuttonMaintenance.set_value(stadiumobj.condition)

        '''
        cost = stadiumobj.get_maintenance()
        cost = display.currency(cost)
        self.labelMaintenanceCost.set_label("%s" % (cost))
        '''

        self.labelCondition.set_label("%i%%" % (stadiumobj.condition))

        self.show_all()

    def maintenance_changed(self, spinbutton):
        club = user.get_user_club()
        stadiumObject = stadium.get_stadium(club.stadium)

        stadiumObject.maintenance = spinbutton.get_value_as_int()

        '''
        cost = calculator.maintenance()
        cost = display.currency(cost)
        self.labelMaintenanceCost.set_label("%s" % (cost))
        '''

    def update_capacity(self):
        clubobj = user.get_user_club()
        stadiumobj = stadium.get_stadium(clubobj.stadium)

        capacity = 0

        for stand in stadiumobj.main:
            capacity += stand.capacity
            capacity += stand.box

        for stand in stadiumobj.corner:
            capacity += stand.capacity

        stadiumobj.capacity = capacity

        self.labelCurrentCapacity.set_label("%i" % (capacity))

    def main_changed(self, spinbutton, index):
        capacity = spinbutton.get_value_as_int()

        if capacity > 0:
            if not self.roof_widget[index].get_active():
                self.roof_widget[index].set_sensitive(True)

            if self.standing_widget[index][0].get_active():
                self.standing_widget[index][0].set_sensitive(True)
                self.standing_widget[index][1].set_sensitive(True)
        else:
            self.roof_widget[index].set_active(False)
            self.roof_widget[index].set_sensitive(False)
            self.standing_widget[index][0].set_active(True)
            self.standing_widget[index][0].set_sensitive(False)
            self.standing_widget[index][1].set_sensitive(False)
            self.box_widget[index].set_sensitive(False)

        if index < 4:
            if self.roof_widget[index].get_active() and capacity >= 5000:
                self.box_widget[index].set_sensitive(True)
            else:
                self.box_widget[index].set_value(0)
                self.box_widget[index].set_sensitive(False)

        # Corner stand availability
        club = user.get_user_club()
        stadiumObject = stadium.get_stadium(club.stadium)

        # (0, 1), (2, 0), (1, 3), (3, 2)
        adjacent = stadiumObject.main[index].adjacent

        if spinbutton.get_value_as_int() < 8000:
            if self.main_stand_widget[adjacent[0]].get_value_as_int() < 8000:
                self.corner_stand_widget[adjacent[0]].set_sensitive(False)

            if self.main_stand_widget[adjacent[1]].get_value_as_int() < 8000:
                self.corner_stand_widget[adjacent[1]].set_sensitive(False)
        else:
            self.corner_stand_widget[adjacent[0]].set_sensitive(True)
            self.corner_stand_widget[adjacent[1]].set_sensitive(True)

        self.update_cost()

    def corner_changed(self, spinbutton, index):
        capacity = spinbutton.get_value_as_int()

        if capacity > 0:
            if not self.roof_widget[index].get_active():
                self.roof_widget[index].set_sensitive(True)

            if self.standing_widget[index][0].get_active():
                self.standing_widget[index][0].set_sensitive(True)
                self.standing_widget[index][1].set_sensitive(True)
        else:
            self.roof_widget[index].set_active(False)
            self.roof_widget[index].set_sensitive(False)
            self.standing_widget[index][0].set_active(True)
            self.standing_widget[index][0].set_sensitive(False)
            self.standing_widget[index][1].set_sensitive(False)

        self.update_cost()

    def box_changed(self, spinbutton, index):
        self.update_cost()

    def standing_changed(self, radiobutton, index):
        self.update_cost()

    def roof_changed(self, checkbutton, index):
        if index < 4:
            if self.roof_widget[index].get_active() and self.main_stand_widget[index].get_value_as_int() >= 5000:
                self.box_widget[index].set_sensitive(True)
            else:
                self.box_widget[index].set_sensitive(False)
                self.box_widget[index].set_value(0)

        self.update_cost()

    def update_cost(self):
        self.cost = 0
        upgrade_capacity = 0

        club = user.get_user_club()
        stadiumObject = stadium.get_stadium(club.stadium)

        for count, widget in enumerate(self.main_stand_widget):
            capacity = stadiumObject.main[count].capacity
            new_capacity = widget.get_value_as_int()
            upgrade_capacity += new_capacity

            self.cost += ((new_capacity - capacity) / 1000) * 1200000

        for count, widget in enumerate(self.corner_stand_widget):
            capacity = stadiumObject.corner[count].capacity
            new_capacity = widget.get_value_as_int()
            upgrade_capacity += new_capacity

            self.cost += ((new_capacity - capacity) / 1000) * 750000

        for count, widget in enumerate(self.box_widget):
            capacity = stadiumObject.main[count].box
            new_capacity = widget.get_value_as_int()
            upgrade_capacity += new_capacity

            self.cost += ((new_capacity - capacity) / 250) * 450000

        for count, widget in enumerate(self.standing_widget):
            if count < 4:
                if not stadiumObject.main[count].seating:
                    if widget[1].get_active():
                        self.cost += 525000
            else:
                if not stadiumObject.corner[count - 4].seating:
                    if widget[1].get_active():
                        self.cost += 350000

        for count, widget in enumerate(self.roof_widget):
            if count < 4:
                if not stadiumObject.main[count].roof:
                    if widget.get_active():
                        self.cost += 1200000
            else:
                if not stadiumObject.corner[count - 4].roof:
                    if widget.get_active():
                        self.cost += 800000

        cost = display.currency(self.cost)
        self.labelCost.set_label("%s" % (cost))

        self.labelUpgradeCapacity.set_label("%i" % (upgrade_capacity))

        if self.cost > 0:
            self.buttonConfirm.set_sensitive(True)
            self.buttonRevert.set_sensitive(True)
        else:
            self.buttonConfirm.set_sensitive(False)
            self.buttonRevert.set_sensitive(False)

    def confirm_upgrade(self, button):
        stadiumid = game.clubs[game.teamid].stadium
        stadium = game.stadiums[stadiumid]

        club = game.clubs[game.teamid]

        if club.accounts.request(amount=self.cost):
            if dialogs.confirm_stadium(self.cost):
                game.clubs[game.teamid].accounts.withdraw(amount=self.cost, category="stadium")

                for count, widget in enumerate(self.main_stand_widget):
                    stadium.main[count].capacity = widget.get_value_as_int()

                for count, widget in enumerate(self.corner_stand_widget):
                    stadium.corner[count].capacity = widget.get_value_as_int()

                for count, widget in enumerate(self.box_widget):
                    stadium.main[count].box = widget.get_value_as_int()

                for count, widget in enumerate(self.standing_widget):
                    if widget[0].get_active():
                        if count < 4:
                            stadium.main[count].seating = False
                        else:
                            stadium.corner[count - 4].seating = False
                    elif widget[1].get_active():
                        if count < 4:
                            stadium.main[count].seating = True
                        else:
                            stadium.corner[count - 4].seating = True

                        widget[0].set_sensitive(False)
                        widget[1].set_sensitive(False)

                for count, widget in enumerate(self.roof_widget):
                    if count < 4:
                        stadium.main[count].roof = widget.get_active()
                    else:
                        stadium.corner[count - 4].roof = widget.get_active()

                    if widget.get_active():
                        widget.set_sensitive(False)

                self.revert_upgrade()
                self.update_capacity()

                self.cost = 0
                cost = display.currency(self.cost)
                self.labelCost.set_label("%s" % (cost))

                self.buttonConfirm.set_sensitive(False)

    def revert_upgrade(self, button=None):
        '''
        This function is also used to load the starting data set.
        '''
        clubobj = user.get_user_club()
        stadiumobj = stadium.get_stadium(clubobj.stadium)

        # Main stand
        for count, widget in enumerate(self.main_stand_widget):
            capacity = stadiumobj.main[count].capacity
            widget.set_value(capacity)
            widget.set_range(capacity, 15000)

            if capacity > 0:
                self.roof_widget[count].set_sensitive(True)
                self.standing_widget[count][0].set_sensitive(True)
                self.standing_widget[count][1].set_sensitive(True)

        # Corner stand
        for count, widget in enumerate(self.corner_stand_widget, start=4):
            capacity = stadiumobj.corner[count - 4].capacity
            widget.set_value(capacity)
            widget.set_range(capacity, 3000)

            if capacity > 0:
                self.roof_widget[count].set_sensitive(True)
                self.standing_widget[count][0].set_sensitive(True)
                self.standing_widget[count][1].set_sensitive(True)

                if capacity == 3000:
                    widget.set_sensitive(False)

        # Roof
        for count, widget in enumerate(self.roof_widget):
            if count < 4:
                roof = stadiumobj.main[count].roof

                # Main stands
                if self.main_stand_widget[count].get_value_as_int() > 0:
                    widget.set_active(roof)

                    if roof:
                        widget.set_sensitive(False)
            else:
                roof = stadiumobj.corner[count - 4].roof

                # Corner stands
                if self.corner_stand_widget[count - 4].get_value_as_int() > 0:
                    widget.set_active(roof)

                    if roof:
                        widget.set_sensitive(False)

        # Standing / Seating
        for count, widget in enumerate(self.standing_widget):
            if count < 4:
                seating = stadiumobj.main[count].seating
                capacity = stadiumobj.main[count].capacity
            else:
                seating = stadiumobj.corner[count - 4].seating
                capacity = stadiumobj.corner[count - 4].capacity

            if capacity > 0:
                widget[1].set_active(True)
            else:
                widget[0].set_active(True)

            if seating:
                widget[0].set_sensitive(False)
                widget[1].set_sensitive(False)

        # Executive boxes
        for count, widget in enumerate(self.box_widget):
            if count < 4:
                capacity = stadiumobj.main[count].box
                stand_capacity = stadiumobj.main[count].capacity
                roof_status = stadiumobj.main[count].roof

                if stand_capacity >= 5000 and roof_status:
                    widget.set_value(capacity)
                    widget.set_range(capacity, 500)

                    if capacity < 500:
                        widget.set_sensitive(True)


