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
from gi.repository import Gdk
import random

import constants
import display
import game
import widgets


class Tickets(Gtk.Grid):
    __name__ = "tickets"

    def __init__(self):
        self.scales = []

        Gtk.Grid.__init__(self)
        self.set_vexpand(True)
        self.set_hexpand(True)
        self.set_border_width(5)
        self.set_row_spacing(5)

        commonframe = widgets.CommonFrame("Ticket Prices")
        self.attach(commonframe, 0, 0, 1, 1)

        grid1 = Gtk.Grid()
        grid1.set_row_spacing(5)
        grid1.set_column_spacing(5)
        commonframe.insert(grid1)

        label = Gtk.Label("<b>League</b>")
        label.set_use_markup(True)
        grid1.attach(label, 1, 1, 2, 1)
        label = Gtk.Label("<b>Cup</b>")
        label.set_use_markup(True)
        grid1.attach(label, 3, 1, 2, 1)
        label = Gtk.Label("<b>Season</b>")
        label.set_use_markup(True)
        grid1.attach(label, 5, 1, 2, 1)

        label = widgets.AlignedLabel("Standing")
        grid1.attach(label, 0, 2, 1, 1)
        label = widgets.AlignedLabel("Covered Standing")
        grid1.attach(label, 0, 3, 1, 1)
        label = widgets.AlignedLabel("Seating")
        grid1.attach(label, 0, 4, 1, 1)
        label = widgets.AlignedLabel("Covered Seating")
        grid1.attach(label, 0, 5, 1, 1)
        label = widgets.AlignedLabel("Corporate Box")
        grid1.attach(label, 0, 6, 1, 1)

        count = 0

        for row in range(1, 6):
            for column in range(1, 4):
                scale = Gtk.Scale()
                scale.set_hexpand(True)
                scale.set_orientation(Gtk.Orientation.HORIZONTAL)
                scale.set_value_pos(Gtk.PositionType.BOTTOM)
                scale.set_digits(0)
                scale.set_increments(1, 10)
                scale.connect("value-changed", self.value_changed, count)
                scale.connect("format-value", self.format_value_tickets)
                grid1.attach(scale, column * 2, row + 1, 1, 1)
                self.scales.append(scale)

                count += 1

        commonframe = widgets.CommonFrame("School Tickets")
        self.attach(commonframe, 0, 1, 1, 1)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        commonframe.insert(grid)

        label = widgets.AlignedLabel("Free School Tickets Available")
        grid.attach(label, 0, 1, 1, 1)
        self.spinbuttonSchoolTickets = Gtk.SpinButton()
        self.spinbuttonSchoolTickets.set_snap_to_ticks(True)
        self.spinbuttonSchoolTickets.connect("value-changed", self.school_tickets)
        grid.attach(self.spinbuttonSchoolTickets, 1, 1, 1, 1)

        commonframe = widgets.CommonFrame("School Tickets")
        self.attach(commonframe, 0, 2, 1, 1)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        commonframe.insert(grid)

        label = widgets.AlignedLabel("Season Ticket Allocation Percentage")
        grid.attach(label, 0, 1, 1, 1)
        self.spinbuttonSeasonTickets = Gtk.SpinButton.new_with_range(0, 100, 1)
        self.spinbuttonSeasonTickets.set_numeric(False)
        self.spinbuttonSeasonTickets.connect("value-changed", self.season_tickets)
        self.spinbuttonSeasonTickets.connect("output", self.format_value_season)
        grid.attach(self.spinbuttonSeasonTickets, 1, 1, 1, 1)
        self.labelStatus = widgets.AlignedLabel()
        grid.attach(self.labelStatus, 0, 2, 2, 1)

    def value_changed(self, scale, index):
        game.clubs[game.teamid].tickets.tickets[index] = int(scale.get_value())

    def format_value_tickets(self, scale, value):
        value = display.currency(value)

        return value

    def format_value_season(self, scale):
        value = "%i%%" % (scale.get_value_as_int())
        scale.set_text(value)

        return True

    def school_tickets(self, spinbutton):
        game.clubs[game.teamid].tickets.school_tickets = spinbutton.get_value_as_int()

    def season_tickets(self, spinbutton):
        game.clubs[game.teamid].tickets.season_tickets = spinbutton.get_value_as_int()

    def populate_data(self):
        club = game.clubs[game.teamid]
        stadium = game.stadiums[club.stadium]

        # Determine standing / seating configurations
        uncovered_standing = False
        uncovered_seating = False
        covered_standing = False
        covered_seating = False
        box = False

        for count, stand in enumerate(stadium.main):
            if stand.capacity > 0:
                if stand.seating and stand.roof:
                    covered_seating = True
                elif stand.seating and not stand.roof:
                    uncovered_seating = True
                elif not stand.seating and stand.roof:
                    covered_standing = True
                elif not stand.seating and not stand.roof:
                    uncovered_standing = True

                if stand.box > 0:
                    box = True

        for count, stand in enumerate(stadium.corner):
            if stand.capacity > 0:
                if stand.seating and stand.roof:
                    covered_seating = True
                elif stand.seating and not stand.roof:
                    uncovered_seating = True
                elif not stand.seating and stand.roof:
                    covered_standing = True
                elif not stand.seating and not stand.roof:
                    uncovered_standing = True

        count = 0

        # Set capacities and standing / seating of stand
        for row in range(1, 6):
            for column in range(1, 4):
                price = game.clubs[game.teamid].tickets.tickets[count]

                if column < 3:
                    self.scales[count].set_range(0, 99)
                else:
                    self.scales[count].set_range(0, 999)

                self.scales[count].set_value(price)

                if row == 1:
                    self.scales[count].set_sensitive(uncovered_standing)
                elif row == 2:
                    self.scales[count].set_sensitive(covered_standing)
                elif row == 3:
                    self.scales[count].set_sensitive(uncovered_seating)
                elif row == 4:
                    self.scales[count].set_sensitive(covered_seating)
                elif row == 5:
                    self.scales[count].set_sensitive(box)

                count += 1

        self.spinbuttonSchoolTickets.set_range(0, stadium.capacity)
        self.spinbuttonSchoolTickets.set_increments(100, 1000)
        self.spinbuttonSchoolTickets.set_value(club.tickets.school_tickets)

        self.spinbuttonSeasonTickets.set_value(club.tickets.season_tickets)

        if game.clubs[game.teamid].tickets.season_tickets_available:
            status = "Season tickets are currently on sale."
        else:
            status = "Season tickets can not be purchased at this time."

        self.spinbuttonSeasonTickets.set_sensitive(club.tickets.season_tickets_available)

        self.labelStatus.set_label(status)

    def run(self):
        self.populate_data()

        self.show_all()


class Advertising(Gtk.Grid):
    __name__ = "advertising"

    class Display(Gtk.Grid):
        def __init__(self, category):
            self.liststoreAvailable = Gtk.ListStore(int, str, int, int, int, str)
            self.liststoreCurrent = Gtk.ListStore(int, str, int, int, int, str)

            Gtk.Grid.__init__(self)
            self.set_column_homogeneous(True)
            self.set_row_spacing(5)
            self.set_column_spacing(5)

            label = widgets.AlignedLabel("<b>%s</b>" % (category))
            label.set_use_markup(True)
            self.attach(label, 0, 0, 1, 1)

            self.labelCount = Gtk.Label()
            self.labelCount.set_alignment(1, 0.5)
            self.attach(self.labelCount, 1, 0, 1, 1)

            target = Gtk.TargetEntry.new("MY_TREE_MODEL_ROW", Gtk.TargetFlags.SAME_APP, 0)

            targets = [("MY_TREE_MODEL_ROW", Gtk.TargetFlags.SAME_APP, 0),
                       ("text/plain", 0, 1),
                       ("TEXT", 0, 2),
                       ("STRING", 0, 3),
                      ]

            cellrenderertext = Gtk.CellRendererText()

            scrolledwindow = Gtk.ScrolledWindow()
            scrolledwindow.set_vexpand(True)
            scrolledwindow.set_hexpand(True)
            self.attach(scrolledwindow, 0, 1, 1, 1)

            self.treeviewAvailable = Gtk.TreeView()
            self.treeviewAvailable.set_model(self.liststoreAvailable)
            self.treeviewAvailable.set_enable_search(False)
            self.treeviewAvailable.set_search_column(-1)
            self.treeviewAvailable.enable_model_drag_source(Gdk.ModifierType.BUTTON1_MASK, targets, Gdk.DragAction.MOVE)
            self.treeviewAvailable.drag_source_set(Gdk.ModifierType.BUTTON1_MASK, [(target)], Gdk.DragAction.MOVE)
            self.treeselection = self.treeviewAvailable.get_selection()
            scrolledwindow.add(self.treeviewAvailable)
            treeviewcolumn = widgets.TreeViewColumn(title="Name", column=1)
            treeviewcolumn.set_expand(True)
            self.treeviewAvailable.append_column(treeviewcolumn)
            treeviewcolumn = widgets.TreeViewColumn(title="Quantity", column=2)
            self.treeviewAvailable.append_column(treeviewcolumn)
            treeviewcolumn = widgets.TreeViewColumn(title="Period", column=3)
            self.treeviewAvailable.append_column(treeviewcolumn)
            treeviewcolumn = widgets.TreeViewColumn(title="Cost", column=5)
            self.treeviewAvailable.append_column(treeviewcolumn)

            scrolledwindow = Gtk.ScrolledWindow()
            scrolledwindow.set_vexpand(True)
            scrolledwindow.set_hexpand(True)
            self.attach(scrolledwindow, 1, 1, 1, 1)

            self.treeviewCurrent = Gtk.TreeView()
            self.treeviewCurrent.set_model(self.liststoreCurrent)
            self.treeviewCurrent.set_enable_search(False)
            self.treeviewCurrent.set_search_column(-1)
            self.treeviewCurrent.enable_model_drag_dest(targets, Gdk.DragAction.MOVE)
            scrolledwindow.add(self.treeviewCurrent)
            treeselection = self.treeviewCurrent.get_selection()
            treeselection.set_mode(Gtk.SelectionMode.NONE)
            treeviewcolumn = widgets.TreeViewColumn(title="Name", column=1)
            treeviewcolumn.set_expand(True)
            self.treeviewCurrent.append_column(treeviewcolumn)
            treeviewcolumn = widgets.TreeViewColumn(title="Quantity", column=2)
            self.treeviewCurrent.append_column(treeviewcolumn)
            treeviewcolumn = widgets.TreeViewColumn(title="Period", column=3)
            self.treeviewCurrent.append_column(treeviewcolumn)

        def advertising_add(self, index):
            model, treeiter = self.treeselection.get_selected()

            advertid = model[treeiter][0]

            if index == 0:
                game.clubs[game.teamid].hoardings.move(advertid)
            elif index == 1:
                game.clubs[game.teamid].programmes.move(advertid)

        def on_drag_data_get(self, treeview, context, selection, info, time, index):
            model, treeiter = self.treeselection.get_selected()

            advertid = "%i/%s" % (index, str(model[treeiter][0]))
            data = bytes(advertid, "utf-8")

            selection.set(selection.get_target(), 8, data)

        def on_drag_data_received(self, treeview, context, x, y, selection, info, time, index):
            data = selection.get_data().decode("utf-8")
            data = data.split("/")

            drop_info = treeview.get_dest_row_at_pos(x, y)

            advertid = int(data[1])

            if int(data[0]) == index:
                if index == 0:
                    game.clubs[game.teamid].hoardings.move(advertid)
                elif index == 1:
                    game.clubs[game.teamid].programmes.move(advertid)

                if context.get_actions() == Gdk.DragAction.MOVE:
                    context.finish(True, True, time)

            return

    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_row_spacing(5)

        self.hoardings = self.Display("Hoardings")
        self.hoardings.treeviewAvailable.connect("row-activated", self.advertising_add, 0)
        self.hoardings.treeviewAvailable.connect("drag-data-get", self.hoardings.on_drag_data_get, 0)
        self.hoardings.treeviewCurrent.connect("drag-data-received", self.advertising_dnd, 0)
        self.attach(self.hoardings, 0, 0, 2, 1)

        self.programmes = self.Display("Programmes")
        self.programmes.treeviewAvailable.connect("row-activated", self.advertising_add, 1)
        self.programmes.treeviewAvailable.connect("drag-data-get", self.programmes.on_drag_data_get, 1)
        self.programmes.treeviewCurrent.connect("drag-data-received", self.advertising_dnd, 1)
        self.attach(self.programmes, 0, 1, 2, 1)

        buttonbox = Gtk.ButtonBox()
        buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
        self.attach(buttonbox, 0, 2, 2, 1)

        buttonAuto = Gtk.ToggleButton("_Assistant")
        buttonAuto.set_use_underline(True)
        buttonAuto.set_tooltip_text("Advertising handled by assistant manager")
        buttonAuto.connect("toggled", self.assistant_handler)
        buttonbox.add(buttonAuto)

    def assistant_handler(self, togglebutton):
        game.advertising_assistant = togglebutton.get_active()

    def advertising_add(self, treeview, treepath, treeviewcolumn, index):
        if index == 0:
            self.hoardings.advertising_add(index)
        elif index == 1:
            self.programmes.advertising_add(index)

        self.populate_data()

    def advertising_dnd(self, treeview, context, x, y, selection, info, time, index):
        if index == 0:
            self.hoardings.on_drag_data_received(treeview, context, x, y, selection, info, time, index)
        elif index == 1:
            self.programmes.on_drag_data_received(treeview, context, x, y, selection, info, time, index)

        self.populate_data()

    def update_totals(self):
        club = game.clubs[game.teamid]

        quantity = club.hoardings.get_advert_count()
        self.hoardings.labelCount.set_label("Used %i of %i hoarding spaces" % (quantity, club.hoardings.maximum))

        quantity = club.programmes.get_advert_count()
        self.programmes.labelCount.set_label("Used %i of %i programme spaces" % (quantity, club.programmes.maximum))

    def populate_data(self):
        self.hoardings.liststoreAvailable.clear()
        self.programmes.liststoreAvailable.clear()
        self.hoardings.liststoreCurrent.clear()
        self.programmes.liststoreCurrent.clear()

        club = game.clubs[game.teamid]

        for advertid, advert in club.hoardings.available.items():
            item = advert.get_details()
            item.insert(0, advertid)
            self.hoardings.liststoreAvailable.append(item)

        for advertid, advert in club.programmes.available.items():
            item = advert.get_details()
            item.insert(0, advertid)
            self.programmes.liststoreAvailable.append(item)

        for advert in club.hoardings.current.values():
            item = advert.get_details()
            item.insert(0, advertid)
            self.hoardings.liststoreCurrent.append(item)

        for advert in club.programmes.current.values():
            item = advert.get_details()
            item.insert(0, advertid)
            self.programmes.liststoreCurrent.append(item)

        self.update_totals()

    def run(self):
        self.populate_data()

        self.show_all()


class Merchandise(Gtk.Grid):
    __name__ = "merchandise"

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

        for index in range(0, 12):
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
        club = game.clubs[game.teamid]

        club.merchandise.percentages[index] = spinbutton.get_value()

        cost = constants.merchandise[index][1]
        profit = (self.spins[index].get_value() * 0.01) * cost + cost
        profit = display.currency(profit, mode=1)
        self.display[index][2].set_label("%s" % (profit))

    def run(self):
        club = game.clubs[game.teamid]

        for count, item in enumerate(constants.merchandise):
            self.display[count][0].set_label(item[0])
            cost = display.currency(item[1], mode=1)
            self.display[count][1].set_label("%s" % (cost))

            value = game.clubs[game.teamid].merchandise.percentages[count]
            self.spins[count].set_value(value)

            profit = (self.spins[count].get_value() * 0.01) * item[1] + item[1]
            profit = display.currency(profit, mode=1)
            self.display[count][2].set_label("%s" % (profit))

            if len(club.merchandise.sales) > 0:
                sales = "%i" % (club.merchandise.sales[count][0])
                revenue = club.merchandise.sales[count][1]
                cost = club.merchandise.sales[count][2]
                profit = revenue - cost

                revenue = display.currency(revenue)
                self.display[count][4].set_label(revenue)

                profit = display.currency(profit)
                self.display[count][5].set_label(profit)
            else:
                sales = "No Sales"

            self.display[count][3].set_label(sales)

        self.show_all()


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
        game.clubs[game.teamid].catering.percentages[index] = spinbutton.get_value()

        cost = constants.catering[index][1]

        profit = (self.spins[index].get_value() * 0.01) * cost + cost
        profit = display.currency(profit, mode=1)
        self.display[index][2].set_label("%s" % (profit))

    def run(self):
        club = game.clubs[game.teamid]

        for count, item in enumerate(constants.catering):
            self.display[count][0].set_label(item[0])
            cost = display.currency(item[1], mode=1)
            self.display[count][1].set_label("%s" % (cost))

            value = game.clubs[game.teamid].catering.percentages[count]
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
