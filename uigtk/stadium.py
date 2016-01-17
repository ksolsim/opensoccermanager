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
            self.labelCondition = uigtk.widgets.Label(leftalign=True)
            self.grid.attach(self.labelCondition, 1, 2, 1, 1)

        def set_details(self, capacity=0, condition=100):
            '''
            Set stadium details.
            '''
            club = data.clubs.get_club_by_id(data.user.team)
            stadium = data.stadiums.get_stadium_by_id(club.stadium)

            self.labelName.set_label(stadium.name)
            self.labelCapacity.set_label("%i" % (stadium.get_capacity()))
            self.labelCondition.set_label("%i%%" % (condition))

    class Maintenance(uigtk.widgets.CommonFrame):
        def __init__(self):
            uigtk.widgets.CommonFrame.__init__(self, "Maintenance")

            label = uigtk.widgets.Label("Estimated Maintenance Percentage", leftalign=True)
            self.grid.attach(label, 0, 0, 1, 1)
            spinbutton = Gtk.SpinButton()
            spinbutton.set_range(0, 110)
            spinbutton.set_increments(1, 10)
            spinbutton.set_value(100)
            spinbutton.set_snap_to_ticks(True)
            spinbutton.connect("output", self.on_maintenance_output)
            self.grid.attach(spinbutton, 1, 0, 1, 1)

            label = uigtk.widgets.Label("Stadium Maintenance Cost", leftalign=True)
            self.grid.attach(label, 0, 1, 1, 1)
            self.labelCost = uigtk.widgets.Label(leftalign=True)
            self.grid.attach(self.labelCost, 1, 1, 1, 1)

        def set_maintenance_cost(self):
            '''
            Update display label for cost of maintaining stadium and buildings.
            '''
            club = data.clubs.get_club_by_id(data.user.team)
            stadium = data.stadiums.get_stadium_by_id(club.stadium)

            self.labelCost.set_label(data.currency.get_currency(stadium.get_maintenance_cost(), integer=True))

        def on_maintenance_output(self, spinbutton):
            '''
            Format percentage sign into maintenance spinbutton output.
            '''
            spinbutton.set_text("%i%%" % (spinbutton.get_value_as_int()))

            return True

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

            stand.capacity = Gtk.SpinButton()
            stand.capacity.set_range(0, 15000)
            stand.capacity.set_increments(1000, 1000)
            stand.capacity.set_value(0)
            stand.capacity.set_snap_to_ticks(True)
            stand.capacity.set_numeric(True)
            stand.capacity.connect("value-changed", stand.on_capacity_changed)
            frame.grid.attach(stand.capacity, 1, count, 1, 1)

            stand.roof = Gtk.CheckButton("Roof")
            stand.roof.set_sensitive(False)
            stand.roof.connect("toggled", stand.on_roof_changed)
            frame.grid.attach(stand.roof, 2, count, 1, 1)

            stand.standing = Gtk.RadioButton("Standing")
            stand.standing.set_sensitive(False)
            frame.grid.attach(stand.standing, 3, count, 1, 1)
            stand.seating = Gtk.RadioButton("Seating")
            stand.seating.set_sensitive(False)
            stand.seating.join_group(stand.standing)
            frame.grid.attach(stand.seating, 4, count, 1, 1)

            label = uigtk.widgets.Label("Box", leftalign=True)
            frame.grid.attach(label, 5, count, 1, 1)
            stand.box = Gtk.SpinButton()
            stand.box.set_range(0, 500)
            stand.box.set_increments(250, 250)
            stand.box.set_value(0)
            stand.box.set_snap_to_ticks(True)
            stand.box.set_numeric(True)
            stand.box.set_sensitive(False)
            frame.grid.attach(stand.box, 6, count, 1, 1)

        # Populate adjacent main stands for corner stands
        for count in range(0, 4):
            stand = CornerStand()
            self.corner_stands.append(stand)

            stand.main.append(self.main_stands[count])

            if count + 1 == len(self.main_stands):
                stand.main.append(self.main_stands[0])
            else:
                stand.main.append(self.main_stands[count + 1])

            stand.capacity = Gtk.SpinButton()
            stand.capacity.set_range(0, 3000)
            stand.capacity.set_increments(1000, 1000)
            stand.capacity.set_value(0)
            stand.capacity.set_snap_to_ticks(True)
            stand.capacity.set_numeric(True)
            stand.capacity.set_sensitive(False)
            stand.capacity.connect("value-changed", stand.on_capacity_changed)
            frame.grid.attach(stand.capacity, 1, count + 4, 1, 1)

            stand.roof = Gtk.CheckButton("Roof")
            stand.roof.set_sensitive(False)
            frame.grid.attach(stand.roof, 2, count + 4, 1, 1)

            stand.standing = Gtk.RadioButton("Standing")
            stand.standing.set_sensitive(False)
            frame.grid.attach(stand.standing, 3, count + 4, 1, 1)
            stand.seating = Gtk.RadioButton("Seating")
            stand.seating.set_sensitive(False)
            stand.seating.join_group(stand.standing)
            frame.grid.attach(stand.seating, 4, count + 4, 1, 1)

        for count, stand in enumerate(self.main_stands):
            stand.corners.append(self.corner_stands[count])
            stand.corners.append(self.corner_stands[count - 1 % len(self.corner_stands)])

        self.maintenance = self.Maintenance()
        self.attach(self.maintenance, 0, 2, 1, 1)

    def on_build_clicked(self):
        '''
        Store values and update interface when user clicks to build.
        '''

    def on_reset_clicked(self):
        '''
        Reset any changed values back to default.
        '''

    def populate_data(self):
        club = data.clubs.get_club_by_id(data.user.team)
        stadium = data.stadiums.get_stadium_by_id(club.stadium)

        for count, item in enumerate(stadium.main_stands):
            stand = self.main_stands[count]

            stand.capacity.set_value(item.capacity)

            if item.capacity > 0:
                stand.roof.set_active(item.roof)

            if item.seating:
                if item.capacity > 0:
                    stand.seating.set_active(True)
            else:
                stand.standing.set_active(True)

            stand.box.set_value(item.box)

        for count, item in enumerate(stadium.corner_stands):
            stand = self.corner_stands[count]
            stand.capacity.set_value(item.capacity)

            if item.capacity > 0:
                stand.roof.set_active(item.roof)

            if item.seating:
                if item.capacity > 0:
                    stand.seating.set_active(True)
            else:
                stand.standing.set_active(True)

    def run(self):
        self.details.set_details()
        self.maintenance.set_maintenance_cost()
        self.populate_data()

        self.show_all()


class MainStand:
    def __init__(self):
        self.corners = []

    def add_adjacent_corner(self, stand):
        '''
        Add passed stand to corners list.
        '''
        self.corners.append(stand)

    def on_capacity_changed(self, spinbutton):
        '''
        Update widgets on change of capacity.
        '''
        sensitive = spinbutton.get_value_as_int() > 0
        self.roof.set_sensitive(sensitive)
        self.standing.set_sensitive(sensitive)
        self.seating.set_sensitive(sensitive)

        if not sensitive:
            self.roof.set_active(False)
            self.standing.set_active(True)

        self.update_box_status()
        self.update_adjacent_status()

    def update_adjacent_status(self):
        '''
        Update adjacent stand status for capacity change.
        '''
        for stand in self.corners:
            stand.check_adjacent_capacity()

    def on_roof_changed(self, *args):
        '''
        Update box status when roof widget is toggled.
        '''
        self.update_box_status()

    def update_box_status(self):
        '''
        Update box widget based on capacity and roof status.
        '''
        sensitive = self.capacity.get_value_as_int() >= 4000 and self.roof.get_active()

        if not self.roof.get_active():
            self.box.set_value(0)

        if self.capacity.get_value_as_int() < 4000:
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

    def on_capacity_changed(self, spinbutton):
        '''
        Update sensitivity of widgets and roof/standing values.
        '''
        sensitive = spinbutton.get_value_as_int() > 0
        self.roof.set_sensitive(sensitive)
        self.standing.set_sensitive(sensitive)
        self.seating.set_sensitive(sensitive)

        if not sensitive:
            self.roof.set_active(False)
            self.standing.set_active(True)


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
