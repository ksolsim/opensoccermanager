#!/usr/bin/env python3

from gi.repository import Gtk
from gi.repository import Gdk
import random

import constants
import display
import game
import money
import widgets


targets = [('MY_TREE_MODEL_ROW', Gtk.TargetFlags.SAME_APP, 0),
           ('text/plain', 0, 1),
           ('TEXT', 0, 2),
           ('STRING', 0, 3),
           ]


class Tickets(Gtk.Grid):
    def __init__(self):
        self.scales = []

        Gtk.Grid.__init__(self)
        self.set_vexpand(True)
        self.set_hexpand(True)
        self.set_border_width(5)
        self.set_row_spacing(5)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        self.attach(grid, 0, 0, 1, 1)

        label = widgets.AlignedLabel("<b>Ticket Prices</b>")
        label.set_use_markup(True)
        grid.attach(label, 0, 0, 1, 1)

        label = Gtk.Label("<b>League</b>")
        label.set_use_markup(True)
        grid.attach(label, 1, 1, 2, 1)
        label = Gtk.Label("<b>Cup</b>")
        label.set_use_markup(True)
        grid.attach(label, 3, 1, 2, 1)
        label = Gtk.Label("<b>Season</b>")
        label.set_use_markup(True)
        grid.attach(label, 5, 1, 2, 1)

        label = widgets.AlignedLabel("Standing")
        grid.attach(label, 0, 2, 1, 1)
        label = widgets.AlignedLabel("Covered Standing")
        grid.attach(label, 0, 3, 1, 1)
        label = widgets.AlignedLabel("Seating")
        grid.attach(label, 0, 4, 1, 1)
        label = widgets.AlignedLabel("Covered Seating")
        grid.attach(label, 0, 5, 1, 1)
        label = widgets.AlignedLabel("Corporate Box")
        grid.attach(label, 0, 6, 1, 1)

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
                scale.connect("format-value", self.format_value, count)
                grid.attach(scale, column * 2, row + 1, 1, 1)
                self.scales.append(scale)

                count += 1

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        self.attach(grid, 0, 1, 1, 1)

        label = widgets.AlignedLabel("<b>School Tickets</b>")
        label.set_use_markup(True)
        grid.attach(label, 0, 0, 1, 1)

        label = widgets.AlignedLabel("Free School Tickets")
        grid.attach(label, 0, 1, 1, 1)
        self.spinbuttonSchoolTickets = Gtk.SpinButton()
        self.spinbuttonSchoolTickets.set_snap_to_ticks(True)
        self.spinbuttonSchoolTickets.connect("value-changed", self.school_tickets)
        grid.attach(self.spinbuttonSchoolTickets, 1, 1, 1, 1)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        self.attach(grid, 0, 2, 1, 1)

        label = widgets.AlignedLabel("<b>Season Tickets</b>")
        label.set_use_markup(True)
        grid.attach(label, 0, 0, 1, 1)

        label = widgets.AlignedLabel("Season Ticket Allocation Percentage")
        grid.attach(label, 0, 1, 1, 1)
        self.spinbuttonSeasonTickets = Gtk.SpinButton.new_with_range(0, 100, 1)
        self.spinbuttonSeasonTickets.connect("value-changed", self.season_tickets)
        grid.attach(self.spinbuttonSeasonTickets, 1, 1, 1, 1)
        self.labelStatus = widgets.AlignedLabel()
        grid.attach(self.labelStatus, 0, 2, 2, 1)

    def value_changed(self, scale, index):
        game.clubs[game.teamid].tickets[index] = int(scale.get_value())

    def format_value(self, scale, value, index):
        value = display.currency(value)

        return value

    def school_tickets(self, scale):
         game.clubs[game.teamid].school_tickets = scale.get_value_as_int()

    def season_tickets(self, scale):
        game.clubs[game.teamid].season_tickets = scale.get_value_as_int()

    def run(self):
        stadiumid = game.clubs[game.teamid].stadium
        stadium = game.stadiums[stadiumid]

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
                price = game.clubs[game.teamid].tickets[count]
                self.scales[count].set_range(0, price * 2)
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
        self.spinbuttonSchoolTickets.set_value(game.clubs[game.teamid].school_tickets)

        self.spinbuttonSeasonTickets.set_value(game.clubs[game.teamid].season_tickets)

        if game.season_tickets_status == 0:
            status = "Season tickets are currently on sale."
        else:
            status = "Season tickets can not be purchased at this time."
            self.spinbuttonSeasonTickets.set_sensitive(False)

        self.labelStatus.set_label(status)

        self.show_all()


class Advertising(Gtk.Grid):
    def __init__(self):
        self.active = None
        self.model = None

        def on_drag_data_get(treeview, context, selection, info, time, index):
            treeselection = treeview.get_selection()
            model, treeiter = treeselection.get_selected()
            data = '%i/%s/%s/%s/%s' % (index, model[treeiter][0], model[treeiter][1], model[treeiter][2], model[treeiter][3])
            data = bytes(data, "utf-8")
            selection.set(selection.get_target(), 8, data)

            self.active = treeiter
            self.model = model

        def on_drag_data_received(treeview, context, x, y, selection, info, time, index):
            model = treeview.get_model()
            data = selection.get_data().decode("utf-8")
            drop_info = treeview.get_dest_row_at_pos(x, y)

            advertid = data.split("/")[0]

            if index == int(advertid):
                name = data.split("/")[1]
                period = int(data.split("/")[2])
                quantity = int(data.split("/")[3])
                amount = int(data.split("/")[4])
                data = [name, period, quantity, amount]

                treeiter = model.append(data)
                path = model.get_path(treeiter)

                state = self.advertising_add_dnd(model, path, index)

                if state:
                    if context.get_actions() == Gdk.DragAction.MOVE:
                        context.finish(True, True, time)

            return

        Gtk.Grid.__init__(self)
        self.set_vexpand(True)
        self.set_hexpand(True)
        self.set_border_width(5)
        self.set_row_spacing(5)

        self.liststoreHoardingsAvailable = Gtk.ListStore(str, int, int, int, str)
        self.liststoreProgrammesAvailable = Gtk.ListStore(str, int, int, int, str)
        self.liststoreHoardingsCurrent = Gtk.ListStore(str, int, int, int)
        self.liststoreProgrammesCurrent = Gtk.ListStore(str, int, int, int)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        grid.set_column_homogeneous(True)
        self.attach(grid, 0, 0, 1, 1)

        label = widgets.AlignedLabel("<b>Hoardings</b>")
        label.set_use_markup(True)
        grid.attach(label, 0, 0, 1, 1)

        self.labelHoardingsCount = Gtk.Label()
        self.labelHoardingsCount.set_alignment(1, 0.5)
        grid.attach(self.labelHoardingsCount, 1, 0, 1, 1)

        cellrenderertext = Gtk.CellRendererText()

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_vexpand(True)
        scrolledwindow.set_hexpand(True)
        grid.attach(scrolledwindow, 0, 1, 1, 1)

        target = Gtk.TargetEntry.new("MY_TREE_MODEL_ROW", Gtk.TargetFlags.SAME_APP, 0)

        treeviewHoardings1 = Gtk.TreeView()
        treeviewHoardings1.set_model(self.liststoreHoardingsAvailable)
        treeviewHoardings1.set_enable_search(False)
        treeviewHoardings1.set_search_column(-1)
        treeviewHoardings1.enable_model_drag_source(Gdk.ModifierType.BUTTON1_MASK, targets, Gdk.DragAction.MOVE)
        treeviewHoardings1.drag_source_set(Gdk.ModifierType.BUTTON1_MASK, [(target)], Gdk.DragAction.MOVE)
        treeviewHoardings1.connect("row-activated", self.advertising_add, 0)
        treeviewHoardings1.connect("drag-data-get", on_drag_data_get, 0)
        scrolledwindow.add(treeviewHoardings1)
        treeviewcolumn = Gtk.TreeViewColumn("Name", cellrenderertext, text=0)
        treeviewcolumn.set_expand(True)
        treeviewHoardings1.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Quantity", cellrenderertext, text=1)
        treeviewHoardings1.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Period", cellrenderertext, text=2)
        treeviewHoardings1.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Cost", cellrenderertext, text=4)
        treeviewHoardings1.append_column(treeviewcolumn)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_vexpand(True)
        scrolledwindow.set_hexpand(True)
        grid.attach(scrolledwindow, 1, 1, 1, 1)

        treeviewHoardings2 = Gtk.TreeView()
        treeviewHoardings2.set_model(self.liststoreHoardingsCurrent)
        treeviewHoardings2.set_enable_search(False)
        treeviewHoardings2.set_search_column(-1)
        treeviewHoardings2.enable_model_drag_dest(targets, Gdk.DragAction.MOVE)
        treeviewHoardings2.connect("drag-data-received", on_drag_data_received, 0)
        scrolledwindow.add(treeviewHoardings2)
        treeselection = treeviewHoardings2.get_selection()
        treeselection.set_mode(Gtk.SelectionMode.NONE)
        treeviewcolumn = Gtk.TreeViewColumn("Name", cellrenderertext, text=0)
        treeviewcolumn.set_expand(True)
        treeviewHoardings2.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Quantity", cellrenderertext, text=1)
        treeviewHoardings2.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Period", cellrenderertext, text=2)
        treeviewHoardings2.append_column(treeviewcolumn)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        grid.set_column_homogeneous(True)
        self.attach(grid, 0, 1, 1, 1)

        label = widgets.AlignedLabel("<b>Programmes</b>")
        label.set_use_markup(True)
        grid.attach(label, 0, 0, 1, 1)

        self.labelProgrammesCount = Gtk.Label()
        self.labelProgrammesCount.set_alignment(1, 0.5)
        grid.attach(self.labelProgrammesCount, 1, 0, 1, 1)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_vexpand(True)
        scrolledwindow.set_hexpand(True)
        grid.attach(scrolledwindow, 0, 1, 1, 1)

        treeviewProgrammes1 = Gtk.TreeView()
        treeviewProgrammes1.set_model(self.liststoreProgrammesAvailable)
        treeviewProgrammes1.set_enable_search(False)
        treeviewProgrammes1.set_search_column(-1)
        treeviewProgrammes1.enable_model_drag_source(Gdk.ModifierType.BUTTON1_MASK, targets, Gdk.DragAction.MOVE)
        treeviewProgrammes1.drag_source_set(Gdk.ModifierType.BUTTON1_MASK, [(target)], Gdk.DragAction.MOVE)
        treeviewProgrammes1.connect("row-activated", self.advertising_add, 1)
        treeviewProgrammes1.connect("drag-data-get", on_drag_data_get, 1)
        scrolledwindow.add(treeviewProgrammes1)
        treeviewcolumn = Gtk.TreeViewColumn("Name", cellrenderertext, text=0)
        treeviewcolumn.set_expand(True)
        treeviewProgrammes1.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Quantity", cellrenderertext, text=1)
        treeviewProgrammes1.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Period", cellrenderertext, text=2)
        treeviewProgrammes1.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Cost", cellrenderertext, text=4)
        treeviewProgrammes1.append_column(treeviewcolumn)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_vexpand(True)
        scrolledwindow.set_hexpand(True)
        grid.attach(scrolledwindow, 1, 1, 1, 1)

        treeviewProgrammes2 = Gtk.TreeView()
        treeviewProgrammes2.set_model(self.liststoreProgrammesCurrent)
        treeviewProgrammes2.set_enable_search(False)
        treeviewProgrammes2.set_search_column(-1)
        treeviewProgrammes2.enable_model_drag_dest(targets, Gdk.DragAction.MOVE)
        treeviewProgrammes2.connect("drag-data-received", on_drag_data_received, 1)
        scrolledwindow.add(treeviewProgrammes2)
        treeselection = treeviewProgrammes2.get_selection()
        treeselection.set_mode(Gtk.SelectionMode.NONE)
        treeviewcolumn = Gtk.TreeViewColumn("Name", cellrenderertext, text=0)
        treeviewcolumn.set_expand(True)
        treeviewProgrammes2.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Quantity", cellrenderertext, text=1)
        treeviewProgrammes2.append_column(treeviewcolumn)
        treeviewcolumn = Gtk.TreeViewColumn("Period", cellrenderertext, text=2)
        treeviewProgrammes2.append_column(treeviewcolumn)

        buttonbox = Gtk.ButtonBox()
        buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
        self.attach(buttonbox, 0, 2, 1, 1)

        buttonAuto = Gtk.ToggleButton("_Assistant")
        buttonAuto.set_use_underline(True)
        buttonAuto.set_tooltip_text("Advertising handled by assistant manager")
        buttonAuto.connect("toggled", self.assistant_handler)
        buttonbox.add(buttonAuto)

    def assistant_handler(self, togglebutton):
        game.advertising_assistant = togglebutton.get_active()

    def advertising_add(self, treeview, path, treeviewcolumn, index):
        selection = treeview.get_selection()
        model, treeiter = selection.get_selected()
        item = model[treeiter]

        if index == 0:
            if game.clubs[game.teamid].hoardings[2] - (self.hoardings_quantity + item[1]) >= 0:
                game.clubs[game.teamid].hoardings[1].append(item[0:4])
                self.liststoreHoardingsCurrent.append(item[0:4])

                amount = item[3]
                self.hoardings_quantity += item[1]
                self.update_totals()

                model.remove(treeiter)

                game.clubs[game.teamid].hoardings[0] = []

                for item in model:
                    game.clubs[game.teamid].hoardings[0].append(item[0:])

                money.deposit(amount, 2)
        elif index == 1:
            if game.clubs[game.teamid].programmes[2] - (self.programmes_quantity + item[1]) >= 0:
                game.clubs[game.teamid].programmes[1].append(item[0:4])
                self.liststoreProgrammesCurrent.append(item[0:4])

                amount = item[3]
                self.programmes_quantity += item[1]
                self.update_totals()

                model.remove(treeiter)

                game.clubs[game.teamid].programmes[0] = []

                for item in model:
                    game.clubs[game.teamid].programmes[0].append(item[0:])

                money.deposit(amount, 2)

        if game.advertising_timeout == 0:
            game.advertising_timeout = random.randint(8, 12)

    def advertising_add_dnd(self, model, treepath, index):
        treeiter = model.get_iter(treepath)
        item = model[treeiter]

        state = False

        quantity = item[1]

        club = game.clubs[game.teamid]

        if index == 0:
            if quantity + self.hoardings_quantity <= club.hoardings[2]:
                club.hoardings[1].append(item[0:4])

                amount = item[3]
                money.deposit(amount, 2)

                self.model.remove(self.active)

                self.hoardings_quantity += quantity

                club.hoardings[0] = []

                for item in self.liststoreHoardingsAvailable:
                    club.hoardings[0].append(item[0:])

                self.update_totals()

                state = True
        else:
            if quantity + self.programmes_quantity <= club.programmes[2]:
                club.programmes[1].append(item[0:4])

                amount = item[3]
                money.deposit(amount, 2)

                self.model.remove(self.active)

                self.programmes_quantity += item[1]

                club.programmes[0] = []

                for item in self.liststoreProgrammesAvailable:
                    club.programmes[0].append(item[0:])

                self.update_totals()

                state = True

        if game.advertising_timeout == 0:
            game.advertising_timeout = random.randint(8, 12)

        return state

    def update_totals(self):
        club = game.clubs[game.teamid]

        self.labelHoardingsCount.set_label("Used %i of %i hoarding spaces" % (self.hoardings_quantity, club.hoardings[2]))
        self.labelProgrammesCount.set_label("Used %i of %i programme spaces" % (self.programmes_quantity, club.programmes[2]))

    def populate_data(self):
        self.liststoreHoardingsAvailable.clear()
        self.liststoreProgrammesAvailable.clear()
        self.liststoreHoardingsCurrent.clear()
        self.liststoreProgrammesCurrent.clear()

        club = game.clubs[game.teamid]

        for item in club.hoardings[0]:
            amount = display.currency(item[3])
            self.liststoreHoardingsAvailable.append([item[0], item[1], item[2], item[3], amount])

        for item in club.programmes[0]:
            amount = display.currency(item[3])
            self.liststoreProgrammesAvailable.append([item[0], item[1], item[2], item[3], amount])

        for item in club.hoardings[1]:
            self.liststoreHoardingsCurrent.append(item)

        for item in club.programmes[1]:
            self.liststoreProgrammesCurrent.append(item)

        self.hoardings_quantity = 0
        self.programmes_quantity = 0

        for item in club.hoardings[1]:
            self.hoardings_quantity += item[1]

        for item in club.programmes[1]:
            self.programmes_quantity += item[1]

        self.update_totals()

    def run(self):
        self.populate_data()

        self.show_all()


class Merchandise(Gtk.Grid):
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

        club.merchandise[index] = spinbutton.get_value()

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

            value = game.clubs[game.teamid].merchandise[count]
            self.spins[count].set_value(value)

            profit = (self.spins[count].get_value() * 0.01) * item[1] + item[1]
            profit = display.currency(profit, mode=1)
            self.display[count][2].set_label("%s" % (profit))

            if len(club.sales[0]) > 0:
                sales = "%i" % (club.sales[0][count][0])
                revenue = club.sales[0][count][1]
                cost = club.sales[0][count][2]
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
        game.clubs[game.teamid].catering[index] = spinbutton.get_value()

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

            value = game.clubs[game.teamid].catering[count]
            self.spins[count].set_value(value)

            profit = (self.spins[count].get_value() * 0.01) * item[1] + item[1]
            profit = display.currency(profit, mode=1)
            self.display[count][2].set_label("%s" % (profit))

            if len(club.sales[1]) > 0:
                sales = "%i" % (club.sales[1][count][0])

                revenue = club.sales[1][count][1]
                cost = club.sales[1][count][2]
                profit = revenue - cost

                revenue = display.currency(revenue)
                self.display[count][4].set_label(revenue)

                profit = display.currency(profit)
                self.display[count][5].set_label(profit)
            else:
                sales = "No Sales"

            self.display[count][3].set_label(sales)

        self.show_all()
