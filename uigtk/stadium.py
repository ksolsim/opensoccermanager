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
import structures.stadiums
import uigtk.widgets


class Stadium(Gtk.Grid):
    __name__ = "stadium"

    class Details(uigtk.widgets.CommonFrame):
        def __init__(self):
            uigtk.widgets.CommonFrame.__init__(self, "Details")

            label = uigtk.widgets.Label("Name", leftalign=True)
            self.grid.attach(label, 0, 0, 1, 1)
            self.labelName = uigtk.widgets.Label(leftalign=True)
            self.grid.attach(self.labelName, 1, 0, 1, 1)

            label = uigtk.widgets.Label("Capacity", leftalign=True)
            self.grid.attach(label, 0, 1, 1, 1)
            self.labelCapacity = uigtk.widgets.Label(leftalign=True)
            self.grid.attach(self.labelCapacity, 1, 1, 1, 1)

            label = uigtk.widgets.Label("Condition", leftalign=True)
            self.grid.attach(label, 0, 2, 1, 1)
            self.labelCapacity = uigtk.widgets.Label(leftalign=True)
            self.grid.attach(self.labelCapacity, 1, 2, 1, 1)

        def set_details(self, name, capacity, condition):
            '''
            Set stadium details.
            '''
            self.labelName.set_label(name)
            self.labelCapacity.set_label(capacity)
            self.labelCondition.set_label(condition)

    def __init__(self):
        Gtk.Grid.__init__(self)

        self.details = self.Details()
        self.attach(self.details, 0, 0, 1, 1)

        frame = uigtk.widgets.CommonFrame("Stands")
        self.attach(frame, 0, 1, 1, 1)

        names = structures.stadiums.Names()

        for count, name in enumerate(names.get_names()):
            label = uigtk.widgets.Label(name, leftalign=True)
            frame.grid.attach(label, 0, count, 1, 1)

        self.main_stands = []
        self.corner_stands = []

        for count in range(0, 4):
            stand = MainStand()
            self.main_stands.append(stand)

            spinbutton = Gtk.SpinButton()
            spinbutton.set_range(0, 15000)
            spinbutton.set_increments(1000, 1000)
            spinbutton.set_value(0)
            spinbutton.set_snap_to_ticks(True)
            spinbutton.set_numeric(True)
            spinbutton.connect("value-changed", stand.on_capacity_changed)
            frame.grid.attach(spinbutton, 1, count, 1, 1)
            stand.capacity = spinbutton

            checkbutton = Gtk.CheckButton("Roof")
            checkbutton.set_sensitive(False)
            checkbutton.connect("toggled", stand.on_roof_changed)
            frame.grid.attach(checkbutton, 2, count, 1, 1)
            stand.roof = checkbutton

            radiobuttonStanding = Gtk.RadioButton("Standing")
            radiobuttonStanding.set_sensitive(False)
            frame.grid.attach(radiobuttonStanding, 3, count, 1, 1)
            stand.standing = radiobuttonStanding
            radiobuttonSeating = Gtk.RadioButton("Seating")
            radiobuttonSeating.set_sensitive(False)
            radiobuttonSeating.join_group(radiobuttonStanding)
            frame.grid.attach(radiobuttonSeating, 4, count, 1, 1)
            stand.seating = radiobuttonSeating

            label = uigtk.widgets.Label("Box", leftalign=True)
            frame.grid.attach(label, 5, count, 1, 1)

            spinbutton = Gtk.SpinButton()
            spinbutton.set_range(0, 500)
            spinbutton.set_increments(250, 250)
            spinbutton.set_value(0)
            spinbutton.set_snap_to_ticks(True)
            spinbutton.set_numeric(True)
            spinbutton.set_sensitive(False)
            frame.grid.attach(spinbutton, 6, count, 1, 1)
            stand.box = spinbutton

        # Populate adjacent main stands for corner stands
        for count in range(0, 4):
            stand = CornerStand()
            self.corner_stands.append(stand)

            stand.main.append(self.main_stands[count])

            if count + 1 == len(self.main_stands):
                stand.main.append(self.main_stands[0])
            else:
                stand.main.append(self.main_stands[count + 1])

            spinbutton = Gtk.SpinButton()
            spinbutton.set_range(0, 3000)
            spinbutton.set_increments(1000, 1000)
            spinbutton.set_value(0)
            spinbutton.set_snap_to_ticks(True)
            spinbutton.set_numeric(True)
            spinbutton.set_sensitive(False)
            spinbutton.connect("value-changed", stand.on_capacity_changed)
            frame.grid.attach(spinbutton, 1, count + 4, 1, 1)
            stand.capacity = spinbutton

            checkbutton = Gtk.CheckButton("Roof")
            checkbutton.set_sensitive(False)
            checkbutton.connect("toggled", stand.on_roof_changed)
            frame.grid.attach(checkbutton, 2, count + 4, 1, 1)
            stand.roof = checkbutton

            radiobuttonStanding = Gtk.RadioButton("Standing")
            radiobuttonStanding.set_sensitive(False)
            frame.grid.attach(radiobuttonStanding, 3, count + 4, 1, 1)
            stand.standing = radiobuttonStanding
            radiobuttonSeating = Gtk.RadioButton("Seating")
            radiobuttonSeating.set_sensitive(False)
            radiobuttonSeating.join_group(radiobuttonStanding)
            frame.grid.attach(radiobuttonSeating, 4, count + 4, 1, 1)
            stand.seating = radiobuttonSeating

        for count, stand in enumerate(self.main_stands):
            stand.corners.append(self.corner_stands[count])
            stand.corners.append(self.corner_stands[count - 1 % len(self.corner_stands)])

    def run(self):
        self.show_all()


class MainStand:
    def __init__(self):
        self.corners = []

    def add_adjacent_corner(self, stand):
        self.corners.append(stand)

    def on_capacity_changed(self, spinbutton):
        sensitive = spinbutton.get_value_as_int() > 0
        self.roof.set_sensitive(sensitive)
        self.standing.set_sensitive(sensitive)
        self.seating.set_sensitive(sensitive)

        self.update_box_status()
        self.update_adjacent_status()

    def update_adjacent_status(self):
        for stand in self.corners:
            stand.check_adjacent_capacity()

    def on_roof_changed(self, *args):
        self.update_box_status()

    def update_box_status(self):
        sensitive = self.capacity.get_value_as_int() >= 4000 and self.roof.get_active()

        if not self.roof.get_active():
            self.box.set_value(0)

        self.box.set_sensitive(sensitive)


class CornerStand:
    def __init__(self):
        self.main = []

    def check_adjacent_capacity(self):
        '''
        Determine whether adjacent main stand capacities are enough.
        '''
        if self.main[0].capacity.get_value_as_int() < 8000 and self.main[1].capacity.get_value_as_int() < 8000:
            self.capacity.set_sensitive(False)
        else:
            self.capacity.set_sensitive(True)
        '''
        print(self.main)

        for stand in self.main:
            if stand.capacity.get_value_as_int() < 8000:
                self.capacity.set_sensitive(False)
        '''

    def on_capacity_changed(self, spinbutton):
        pass

    def on_roof_changed(self, checkbutton):
        pass


class UpgradeStadium(Gtk.MessageDialog):
    '''
    Confirm specified improvements to stadium construction.
    '''
    def __init__(self, cost):
        Gtk.MessageDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_modal(True)
        self.set_title("Upgrade Stadium")
        self.set_property("message-type", Gtk.MessageType.QUESTION)
        self.set_markup("Begin the construction of upgrades to the stadium at cost of %s?" % (cost))
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Upgrade", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.CANCEL)

    def show(self):
        self.run()
        self.destroy()
