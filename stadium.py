#!/usr/bin/env python3

from gi.repository import Gtk

import calculator
import constants
import game
import money
import dialogs
import display
import widgets


class Stadium(Gtk.Grid):
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
        notebook.append_page(grid, Gtk.Label("Capacity"))

        # Stand labels
        for count, text in enumerate(("North", "West", "South", "East", "North West", "North East", "South West", "South East")):
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
        notebook.append_page(grid, Gtk.Label("Maintenance"))

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
        club = game.clubs[game.teamid]
        stadium = game.stadiums[club.stadium]

        self.revert_upgrade()
        self.update_capacity()

        self.cost = 0
        cost = display.currency(self.cost)
        self.labelCost.set_text("%s" % (cost))

        self.spinbuttonMaintenance.set_value(stadium.maintenance)

        cost = calculator.maintenance()
        cost = display.currency(cost)
        self.labelMaintenanceCost.set_text("%s" % (cost))

        self.labelCondition.set_text("%i%%" % (stadium.condition))

        self.show_all()

    def maintenance_changed(self, spinbutton):
        stadiumid = game.clubs[game.teamid].stadium
        stadium = game.stadiums[stadiumid]

        stadium.maintenance = spinbutton.get_value_as_int()

        cost = calculator.maintenance()
        cost = display.currency(cost)
        self.labelMaintenanceCost.set_text("%s" % (cost))

    def update_capacity(self):
        stadiumid = game.clubs[game.teamid].stadium
        stadium = game.stadiums[stadiumid]

        capacity = 0

        for stand in stadium.main:
            capacity += stand.capacity
            capacity += stand.box

        for stand in stadium.corner:
            capacity += stand.capacity

        stadium.capacity = capacity

        self.labelCurrentCapacity.set_text("%i" % (capacity))

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
        stadiumid = game.clubs[game.teamid].stadium
        stadium = game.stadiums[stadiumid]

        # (0, 1), (2, 0), (1, 3), (3, 2)
        adjacent = stadium.main[index].adjacent

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

        stadiumid = game.clubs[game.teamid].stadium
        stadium = game.stadiums[stadiumid]

        for count, widget in enumerate(self.main_stand_widget):
            capacity = stadium.main[count].capacity
            new_capacity = widget.get_value_as_int()
            upgrade_capacity += new_capacity

            self.cost += ((new_capacity - capacity) / 1000) * 1200000

        for count, widget in enumerate(self.corner_stand_widget):
            capacity = stadium.corner[count].capacity
            new_capacity = widget.get_value_as_int()
            upgrade_capacity += new_capacity

            self.cost += ((new_capacity - capacity) / 1000) * 750000

        for count, widget in enumerate(self.box_widget):
            capacity = stadium.main[count].box
            new_capacity = widget.get_value_as_int()
            upgrade_capacity += new_capacity

            self.cost += ((new_capacity - capacity) / 250) * 450000

        for count, widget in enumerate(self.standing_widget):
            if count < 4:
                if stadium.main[count].seating is False:
                    if widget[1].get_active():
                        self.cost += 525000
            else:
                if stadium.corner[count - 4].seating is False:
                    if widget[1].get_active():
                        self.cost += 350000

        for count, widget in enumerate(self.roof_widget):
            if count < 4:
                if stadium.main[count].roof is False:
                    if widget.get_active():
                        self.cost += 1200000
            else:
                if stadium.corner[count - 4].roof is False:
                    if widget.get_active():
                        self.cost += 800000

        cost = display.currency(self.cost)
        self.labelCost.set_text("%s" % (cost))

        self.labelUpgradeCapacity.set_text("%i" % (upgrade_capacity))

        if self.cost > 0:
            self.buttonConfirm.set_sensitive(True)
            self.buttonRevert.set_sensitive(True)
        else:
            self.buttonConfirm.set_sensitive(False)
            self.buttonRevert.set_sensitive(False)

    def confirm_upgrade(self, button):
        stadiumid = game.clubs[game.teamid].stadium
        stadium = game.stadiums[stadiumid]

        state = money.request(self.cost)

        if state:
            state = dialogs.confirm_stadium(self.cost)

            if state:
                money.withdraw(self.cost, 10)

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
                self.labelCost.set_text("%s" % (cost))

                self.buttonConfirm.set_sensitive(False)

    def revert_upgrade(self, button=None):
        '''
        This function is also used to load the starting data set.
        '''
        stadiumid = game.clubs[game.teamid].stadium
        stadium = game.stadiums[stadiumid]

        # Main stand
        for count, widget in enumerate(self.main_stand_widget):
            capacity = stadium.main[count].capacity
            widget.set_value(capacity)
            widget.set_range(capacity, 15000)

            if capacity > 0:
                self.roof_widget[count].set_sensitive(True)
                self.standing_widget[count][0].set_sensitive(True)
                self.standing_widget[count][1].set_sensitive(True)

        # Corner stand
        for count, widget in enumerate(self.corner_stand_widget, start=4):
            capacity = stadium.corner[count - 4].capacity
            widget.set_value(capacity)
            widget.set_range(capacity, 3000)

            if capacity > 0:
                self.roof_widget[count].set_sensitive(True)
                self.standing_widget[count][0].set_sensitive(True)
                self.standing_widget[count][1].set_sensitive(True)

        # Roof
        for count, widget in enumerate(self.roof_widget):
            if count < 4:
                roof = stadium.main[count].roof

                # Main stands
                if self.main_stand_widget[count].get_value_as_int() > 0:
                    widget.set_active(roof)

                    if roof:
                        widget.set_sensitive(False)
            else:
                roof = stadium.corner[count - 4].roof

                # Corner stands
                if self.corner_stand_widget[count - 4].get_value_as_int() > 0:
                    widget.set_active(roof)

                    if roof:
                        widget.set_sensitive(False)

        # Standing / Seating
        for count, widget in enumerate(self.standing_widget):
            if count < 4:
                seating = stadium.main[count].seating
                capacity = stadium.main[count].capacity
            else:
                seating = stadium.corner[count - 4].seating
                capacity = stadium.corner[count - 4].capacity

            if capacity > 0:
                widget[seating].set_active(True)
            else:
                widget[0].set_active(True)

            if seating:
                widget[0].set_sensitive(False)
                widget[1].set_sensitive(False)

        # Executive boxes
        for count, widget in enumerate(self.box_widget):
            if count < 4:
                capacity = stadium.main[count].box
                stand_capacity = stadium.main[count].capacity
                roof_status = stadium.main[count].roof

                if stand_capacity >= 5000 and roof_status is True:
                    widget.set_value(capacity)
                    widget.set_range(capacity, 500)

                    if capacity < 500:
                        widget.set_sensitive(True)


class Buildings(Gtk.Grid):
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
        self.labels[index].set_text("%s" % (subtotal))
        self.labelTotal.set_markup("<b>%s</b>" % (total))
        self.labelFuturePlots.set_text("Planned number of plots: %i" % (self.futureplots))

        if self.total > 0:
            self.buttonConfirm.set_sensitive(True)
        else:
            self.buttonConfirm.set_sensitive(False)

        if self.futureplots > stadium.plots:
            self.buttonConfirm.set_sensitive(False)

    def confirm_building(self, button):
        state = dialogs.confirm_building(self.total)

        if state:
            money.withdraw(self.total, 10)

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
            self.labelFuturePlots.set_text("Planned number of plots: %i" % (self.futureplots))
            self.labelCurrentPlots.set_text("Used %i out of total %i plots available" % (self.plots, stadium.plots))

            for item in self.labels:
                cost = display.currency(0)
                item.set_text("%s" % (cost))

    def revert_building(self, button):
        for count, item in enumerate(self.buildings):
            self.spins[count].set_value(item)

    def run(self):
        stadiumid = game.clubs[game.teamid].stadium
        stadium = game.stadiums[stadiumid]

        self.buildings = []
        self.plots = 0

        # Populate buildings, plot sizes and costs
        for count, item in enumerate(constants.buildings):
            self.display[count][0].set_text(item[0])
            self.display[count][1].set_text(str(item[1]))

            cost = display.currency(item[2])
            self.display[count][2].set_text(cost)

            cost = display.currency(0)
            self.labels[count].set_text("%s" % (cost))

            self.buildings.append(stadium.buildings[0 + count])
            self.spins[count].set_value(stadium.buildings[0 + count])
            self.spins[count].connect("value-changed", self.value_changed, count)

            # Total number of plots in use
            self.plots += stadium.buildings[0 + count] * item[1]

        self.labelFuturePlots.set_text("Planned number of plots: %i" % (self.futureplots))
        self.labelCurrentPlots.set_text("Used %i out of total %i plots available" % (self.plots, stadium.plots))

        cost = display.currency(0)
        self.labelTotal.set_markup("<b>%s</b>" % (cost))

        self.show_all()
