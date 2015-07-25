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

import game
import stadiums
import user
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

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        commonframe.insert(grid)

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
                scale.connect("format-value", self.format_value_tickets)
                grid.attach(scale, column * 2, row + 1, 1, 1)
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
        club = user.get_user_club()
        club.tickets.tickets[index] = int(scale.get_value())

    def format_value_tickets(self, scale, value):
        value = display.currency(value)

        return value

    def format_value_season(self, scale):
        value = "%i%%" % (scale.get_value_as_int())
        scale.set_text(value)

        return True

    def school_tickets(self, spinbutton):
        club = user.get_user_club()
        club.tickets.school_tickets = spinbutton.get_value_as_int()

    def season_tickets(self, spinbutton):
        club = user.get_user_club()
        club.tickets.season_tickets = spinbutton.get_value_as_int()

    def populate_data(self):
        club = user.get_user_club()

        stadium = stadiums.stadiumitem.stadiums[club.stadium]

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
                price = club.tickets.tickets[count]

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

        self.spinbuttonSchoolTickets.set_range(0, stadium.get_capacity())
        self.spinbuttonSchoolTickets.set_increments(100, 1000)
        self.spinbuttonSchoolTickets.set_value(club.tickets.school_tickets)

        self.spinbuttonSeasonTickets.set_value(club.tickets.season_tickets)

        if club.tickets.season_tickets_available:
            status = "Season tickets are currently on sale."
        else:
            status = "Season tickets can not be purchased at this time."

        self.spinbuttonSeasonTickets.set_sensitive(club.tickets.season_tickets_available)

        self.labelStatus.set_label(status)

    def run(self):
        self.populate_data()

        self.show_all()
