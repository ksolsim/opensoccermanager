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


class Stadium(uigtk.widgets.Grid):
    __name__ = "stadium"

    class Details(uigtk.widgets.CommonFrame):
        def __init__(self):
            uigtk.widgets.CommonFrame.__init__(self, "Details")
            self.set_vexpand(False)

            label = uigtk.widgets.Label("Name", leftalign=True)
            self.grid.attach(label, 0, 0, 1, 1)
            self.labelName = uigtk.widgets.Label(leftalign=True)
            self.grid.attach(self.labelName, 1, 0, 1, 1)

            label = uigtk.widgets.Label("Capacity", leftalign=True)
            self.grid.attach(label, 0, 1, 1, 1)
            self.labelCapacity = uigtk.widgets.Label(leftalign=True)
            self.grid.attach(self.labelCapacity, 1, 1, 1, 1)

        def set_details(self, capacity=0):
            '''
            Set stadium details.
            '''
            self.labelName.set_label(data.user.club.stadium.name)
            self.labelCapacity.set_label("%i" % (data.user.club.stadium.get_capacity()))

    class Maintenance(uigtk.widgets.CommonFrame):
        def __init__(self):
            uigtk.widgets.CommonFrame.__init__(self, "Maintenance")

            label = uigtk.widgets.Label("Current Stadium Condition", leftalign=True)
            self.grid.attach(label, 0, 0, 1, 1)
            self.labelCondition = uigtk.widgets.Label(leftalign=True)
            self.grid.attach(self.labelCondition, 1, 0, 1, 1)

            label = uigtk.widgets.Label("Estimated Maintenance Percentage", leftalign=True)
            self.grid.attach(label, 0, 1, 1, 1)
            spinbutton = Gtk.SpinButton()
            spinbutton.set_range(0, 110)
            spinbutton.set_increments(1, 10)
            spinbutton.set_value(100)
            spinbutton.set_snap_to_ticks(True)
            spinbutton.set_tooltip_text("Percentage amount of required budget to spend on maintenance.")
            spinbutton.connect("value-changed", self.on_maintenance_changed)
            spinbutton.connect("output", self.on_maintenance_output)
            self.grid.attach(spinbutton, 1, 1, 1, 1)

            label = uigtk.widgets.Label("Stadium Maintenance Cost", leftalign=True)
            self.grid.attach(label, 0, 2, 1, 1)
            self.labelCost = uigtk.widgets.Label(leftalign=True)
            self.labelCost.connect("activate-link", self.on_maintenance_information_clicked)
            self.grid.attach(self.labelCost, 1, 2, 1, 1)

        def set_details(self):
            '''
            Update label for stadium condition and maintenance cost.
            '''
            self.labelCondition.set_label("%i%%" % (data.user.club.stadium.condition))

            self.labelCost.set_label("<a href=''>%s</a>" % (data.currency.get_currency(data.user.club.stadium.get_maintenance_cost(), integer=True)))

        def on_maintenance_information_clicked(self, *args):
            '''
            Display message about cost of maintenance.
            '''
            messagedialog = Gtk.MessageDialog()
            messagedialog.set_transient_for(data.window)
            messagedialog.set_modal(True)
            messagedialog.set_title("Maintenance Information")
            messagedialog.set_property("message-type", Gtk.MessageType.INFO)
            messagedialog.set_markup("The total maintenance cost is charged weekly, and is calculated from the total stadium capacity and number of shop buildings.")
            messagedialog.add_button("_Close", Gtk.ResponseType.CLOSE)
            messagedialog.run()
            messagedialog.destroy()

            return True

        def on_maintenance_changed(self, spinbutton):
            '''
            Store updated maintenance percentage value.
            '''
            data.user.club.stadium.maintenance = spinbutton.get_value_as_int()

            self.set_details()

        def on_maintenance_output(self, spinbutton):
            '''
            Format percentage sign into maintenance spinbutton output.
            '''
            spinbutton.set_text("%i%%" % (spinbutton.get_value_as_int()))

            return True

    class Attendances(uigtk.widgets.CommonFrame):
        def __init__(self):
            uigtk.widgets.CommonFrame.__init__(self, "Attendances")
            self.set_vexpand(True)

    def __init__(self):
        Gtk.Grid.__init__(self)

        self.details = self.Details()
        self.attach(self.details, 0, 0, 1, 1)

        Stadium.upgrades = Upgrades()
        self.attach(Stadium.upgrades, 0, 1, 1, 1)

        self.maintenance = self.Maintenance()
        self.attach(self.maintenance, 0, 2, 1, 1)

        self.attendances = self.Attendances()
        self.attach(self.attendances, 0, 3, 2, 1)

        frame = uigtk.widgets.CommonFrame("Stands")
        self.attach(frame, 1, 0, 1, 3)

        names = structures.stadiums.Names()

        for count, name in enumerate(names.get_names()):
            label = uigtk.widgets.Label(name, leftalign=True)
            frame.grid.attach(label, 0, count, 1, 1)

        Stadium.main_stands = []
        Stadium.corner_stands = []

        for count in range(0, 4):
            stand = MainStand()
            Stadium.main_stands.append(stand)

            stand.capacity.connect("value-changed", stand.on_capacity_changed)
            frame.grid.attach(stand.capacity, 1, count, 1, 1)

            stand.roof.connect("toggled", stand.on_roof_toggled)
            frame.grid.attach(stand.roof, 2, count, 1, 1)

            stand.standing.connect("toggled", stand.on_seating_toggled)
            frame.grid.attach(stand.standing, 3, count, 1, 1)
            stand.seating.connect("toggled", stand.on_seating_toggled)
            frame.grid.attach(stand.seating, 4, count, 1, 1)

            label = uigtk.widgets.Label("Executive Box", leftalign=True)
            frame.grid.attach(label, 5, count, 1, 1)
            stand.box.connect("value-changed", stand.on_box_changed)
            frame.grid.attach(stand.box, 6, count, 1, 1)

        for count in range(0, 4):
            stand = CornerStand()
            Stadium.corner_stands.append(stand)

            stand.main.append(self.main_stands[count])

            if count + 1 == len(self.main_stands):
                stand.main.append(self.main_stands[0])
            else:
                stand.main.append(self.main_stands[count + 1])

            stand.capacity.connect("value-changed", stand.on_capacity_changed)
            frame.grid.attach(stand.capacity, 1, count + 4, 1, 1)

            stand.roof.connect("toggled", stand.on_roof_toggled)
            frame.grid.attach(stand.roof, 2, count + 4, 1, 1)

            stand.standing.connect("toggled", stand.on_seating_toggled)
            frame.grid.attach(stand.standing, 3, count + 4, 1, 1)
            stand.seating.connect("toggled", stand.on_seating_toggled)
            frame.grid.attach(stand.seating, 4, count + 4, 1, 1)

        for count, stand in enumerate(self.main_stands):
            stand.corners.append(Stadium.corner_stands[count])
            stand.corners.append(Stadium.corner_stands[count - 1 % len(Stadium.corner_stands)])

        buttonbox = uigtk.widgets.ButtonBox()
        buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
        frame.grid.attach(buttonbox, 0, 12, 7, 1)

        buttonReset = uigtk.widgets.Button("_Reset")
        buttonReset.set_tooltip_text("Reset any adjusted values to initial starting values.")
        buttonReset.connect("clicked", self.on_reset_clicked)
        buttonbox.add(buttonReset)
        buttonConstruct = uigtk.widgets.Button("_Construct")
        buttonConstruct.set_tooltip_text("Begin construction of stadium upgrades.")
        buttonConstruct.connect("clicked", self.on_construct_clicked)
        buttonbox.add(buttonConstruct)

    def on_construct_clicked(self, *args):
        '''
        Store values and update interface when user clicks to build.
        '''
        dialog = UpgradeStadium(cost=Stadium.upgrades.get_cost())

        if dialog.show():
            self.save_data()

    def on_reset_clicked(self, *args):
        '''
        Reset any changed values back to default.
        '''
        self.populate_data()

    def update_interface(self):
        '''
        Update interface by changing sensitivity of unchangeable widgets.
        '''
        for stands in (Stadium.main_stands, Stadium.corner_stands):
            for stand in stands:
                if stand.seating.get_active():
                    stand.standing.set_sensitive(False)
                    stand.seating.set_sensitive(False)

                if stand.roof.get_active():
                    stand.roof.set_sensitive(False)

        for stand in Stadium.main_stands:
            stand.capacity.set_range(stand.capacity.get_value_as_int(), 15000)

            stand.box.set_range(stand.box.get_value_as_int(), 500)

            if stand.box.get_value_as_int() == 500:
                stand.box.set_sensitive(False)

        for stand in Stadium.corner_stands:
            stand.capacity.set_range(stand.capacity.get_value_as_int(), 3000)

        self.details.set_details()
        self.maintenance.set_details()
        Stadium.upgrades.update_cost()

    def save_data(self):
        '''
        Save stadium data into data structure.
        '''
        for count, item in enumerate(Stadium.main_stands):
            stand = data.user.club.stadium.main_stands[count]

            stand.capacity = item.capacity.get_value_as_int()
            stand.seating = not item.standing.get_active()
            stand.roof = item.roof.get_active()
            stand.box = item.box.get_value_as_int()

        for count, item in enumerate(Stadium.corner_stands):
            stand = data.user.club.stadium.corner_stands[count]

            stand.capacity = item.capacity.get_value_as_int()
            stand.seating = not item.standing.get_active()
            stand.roof = item.roof.get_active()

        self.update_interface()

    def populate_data(self):
        # Main stand data
        for count, item in enumerate(data.user.club.stadium.main_stands):
            stand = Stadium.main_stands[count]
            stand.data = item

            stand.capacity.set_value(item.capacity)
            stand.capacity.set_range(item.capacity, 15000)

            if item.capacity > 0:
                stand.roof.set_active(item.roof)

                if item.roof:
                    stand.roof.set_sensitive(False)

                if item.seating:
                    stand.seating.set_active(True)
                    stand.seating.set_sensitive(False)
                    stand.standing.set_sensitive(False)
            else:
                stand.standing.set_active(True)

            stand.box.set_value(item.box)
            stand.box.set_range(item.box, 500)

        # Corner stand data
        for count, item in enumerate(data.user.club.stadium.corner_stands):
            stand = Stadium.corner_stands[count]
            stand.data = item

            stand.capacity.set_value(item.capacity)
            stand.capacity.set_range(item.capacity, 3000)

            if item.capacity > 0:
                stand.roof.set_active(item.roof)

                if item.roof:
                    stand.roof.set_sensitive(False)

                if item.seating:
                    stand.seating.set_active(True)
                    stand.seating.set_sensitive(False)
                    stand.standing.set_sensitive(False)
            else:
                stand.standing.set_active(True)

        self.update_interface()

    def run(self):
        self.details.set_details()
        self.maintenance.set_details()
        self.populate_data()

        self.show_all()


class Stand:
    '''
    Base stand interface for main and corner stands.
    '''
    def __init__(self):
        self.capacity = Gtk.SpinButton()
        self.capacity.set_range(0, 15000)
        self.capacity.set_increments(1000, 1000)
        self.capacity.set_value(0)
        self.capacity.set_snap_to_ticks(True)
        self.capacity.set_numeric(True)

        self.roof = Gtk.CheckButton("Roof")
        self.roof.set_sensitive(False)

        self.standing = Gtk.RadioButton("Standing")
        self.standing.set_sensitive(False)
        self.seating = Gtk.RadioButton("Seating")
        self.seating.set_sensitive(False)
        self.seating.join_group(self.standing)

    def on_seating_toggled(self, *args):
        Stadium.upgrades.update_cost()


class MainStand(Stand):
    def __init__(self):
        Stand.__init__(self)

        self.corners = []

        self.box = Gtk.SpinButton()
        self.box.set_range(0, 500)
        self.box.set_increments(125, 125)
        self.box.set_value(0)
        self.box.set_snap_to_ticks(True)
        self.box.set_numeric(True)
        self.box.set_sensitive(False)

    def add_adjacent_corner(self, stand):
        '''
        Add passed stand to corners list.
        '''
        self.corners.append(stand)

    def on_capacity_changed(self, *args):
        '''
        Update widgets on change of capacity.
        '''
        if not self.roof.get_active():
            self.roof.set_sensitive(True)
            self.box.set_value(0)
            self.box.set_sensitive(False)

        if not self.seating.get_active():
            self.standing.set_sensitive(True)
            self.seating.set_sensitive(True)

        if not self.capacity.get_value_as_int() > 0:
            self.roof.set_active(False)
            self.roof.set_sensitive(False)
            self.standing.set_active(True)
            self.standing.set_sensitive(False)
            self.seating.set_sensitive(False)
            self.box.set_value(0)
            self.box.set_sensitive(False)

        self.update_box_status()
        self.update_adjacent_status()

        Stadium.upgrades.update_cost()
        Stadium.upgrades.update_capacity()

    def update_adjacent_status(self):
        '''
        Update adjacent stand status for capacity change.
        '''
        for stand in self.corners:
            stand.check_adjacent_capacity()

    def on_roof_toggled(self, *args):
        '''
        Update box status when roof widget is toggled.
        '''
        self.update_box_status()

        Stadium.upgrades.update_cost()
        Stadium.upgrades.update_capacity()

    def on_box_changed(self, *args):
        Stadium.upgrades.update_cost()
        Stadium.upgrades.update_capacity()

    def update_box_status(self):
        '''
        Update box widget based on capacity and roof status.
        '''
        if not self.roof.get_active():
            self.box.set_value(0)

        if self.capacity.get_value_as_int() < 4000:
            self.box.set_value(0)

        sensitive = self.capacity.get_value_as_int() >= 4000 and self.roof.get_active()
        self.box.set_sensitive(sensitive)


class CornerStand(Stand):
    def __init__(self):
        Stand.__init__(self)

        self.main = []

        self.capacity.set_range(0, 3000)

    def check_adjacent_capacity(self):
        '''
        Determine whether adjacent main stand capacities are enough.
        '''
        if self.main[0].capacity.get_value_as_int() < 8000 and self.main[1].capacity.get_value_as_int() < 8000:
            self.capacity.set_sensitive(False)
        else:
            self.capacity.set_sensitive(True)

    def on_capacity_changed(self, *args):
        '''
        Update sensitivity of widgets and roof/standing values.
        '''
        if not self.roof.get_active():
            self.roof.set_sensitive(True)

        if not self.seating.get_active():
            self.standing.set_sensitive(True)
            self.seating.set_sensitive(True)

        if not self.capacity.get_value_as_int() > 0:
            self.roof.set_active(False)
            self.roof.set_sensitive(False)
            self.standing.set_active(True)
            self.standing.set_sensitive(False)
            self.seating.set_sensitive(False)

        Stadium.upgrades.update_cost()
        Stadium.upgrades.update_capacity()

    def on_roof_toggled(self, *args):
        '''
        Update box status when roof widget is toggled.
        '''
        Stadium.upgrades.update_cost()
        Stadium.upgrades.update_capacity()


class Upgrades(uigtk.widgets.CommonFrame):
    '''
    Labels displaying upgrade cost and capacity.
    '''
    def __init__(self):
        uigtk.widgets.CommonFrame.__init__(self, "Upgrades")

        label = uigtk.widgets.Label("Upgrade Cost", leftalign=True)
        self.grid.attach(label, 0, 0, 1, 1)
        self.labelUpgradeCost = uigtk.widgets.Label(leftalign=True)
        self.grid.attach(self.labelUpgradeCost, 1, 0, 1, 1)

        label = uigtk.widgets.Label("Upgrade Capacity", leftalign=True)
        self.grid.attach(label, 0, 1, 1, 1)
        self.labelUpgradeCapacity = uigtk.widgets.Label(leftalign=True)
        self.grid.attach(self.labelUpgradeCapacity, 1, 1, 1, 1)

    def get_cost(self):
        '''
        Get cost of stadium modifications.
        '''
        cost = 0

        for stands in (Stadium.main_stands, Stadium.corner_stands):
            for stand in stands:
                capacity = stand.capacity.get_value_as_int()
                seating = stand.seating.get_active()
                roof = stand.roof.get_active()

                if hasattr(stand, "data"):
                    cost += stand.data.get_upgrade_cost(capacity=capacity,
                                                        seating=seating,
                                                        roof=roof)

        return cost

    def update_cost(self):
        '''
        Set the upgrade cost for current amendments.
        '''
        amount = int(self.get_cost())
        amount = data.currency.get_amount(amount)
        amount = data.currency.get_comma_value(amount)
        cost = "%s%s" % (data.currency.get_currency_symbol(), amount)
        self.labelUpgradeCost.set_label(cost)

    def get_capacity(self):
        '''
        Get capacity of stadium modifications.
        '''
        capacity = sum(stand.capacity.get_value_as_int() for stand in Stadium.main_stands)
        capacity += sum(stand.box.get_value_as_int() for stand in Stadium.main_stands)
        capacity += sum(stand.capacity.get_value_as_int() for stand in Stadium.corner_stands)

        return capacity

    def update_capacity(self):
        '''
        Set the upgrade capacity for the current amendments.
        '''
        self.labelUpgradeCapacity.set_label("%s" % (self.get_capacity()))


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
        self.set_markup("<span size='12000'><b>Begin the construction of upgrades to the stadium at cost of %s?</b></span>" % (data.currency.get_currency(cost, integer=True)))
        self.format_secondary_text("Once construction begins, no features of the stadium can be downgraded.")
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Upgrade", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.CANCEL)

    def show(self):
        response = self.run() == Gtk.ResponseType.OK
        self.destroy()

        return response
