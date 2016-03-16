any#!/usr/bin/env python3

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
import uigtk.widgets


class Tickets(uigtk.widgets.Grid):
    __name__ = "tickets"

    club = None

    def __init__(self):
        uigtk.widgets.Grid.__init__(self)

        frame = uigtk.widgets.CommonFrame("Tickets")
        self.attach(frame, 0, 0, 1, 1)

        label = uigtk.widgets.Label("League")
        frame.grid.attach(label, 1, 0, 1, 1)
        label = uigtk.widgets.Label("Cup")
        frame.grid.attach(label, 2, 0, 1, 1)
        label = uigtk.widgets.Label("Season")
        frame.grid.attach(label, 3, 0, 1, 1)

        label = uigtk.widgets.Label("Standing Uncovered", leftalign=True)
        frame.grid.attach(label, 0, 1, 1, 1)
        label = uigtk.widgets.Label("Standing Covered", leftalign=True)
        frame.grid.attach(label, 0, 2, 1, 1)
        label = uigtk.widgets.Label("Seating Uncovered", leftalign=True)
        frame.grid.attach(label, 0, 3, 1, 1)
        label = uigtk.widgets.Label("Seating Covered", leftalign=True)
        frame.grid.attach(label, 0, 4, 1, 1)
        label = uigtk.widgets.Label("Executive Box", leftalign=True)
        frame.grid.attach(label, 0, 5, 1, 1)

        self.tickets = []

        for vcount in range(1, 6):
            self.tickets.append([])

            for hcount in range(1, 4):
                scale = Gtk.Scale()
                scale.index = (vcount - 1, hcount - 1)
                scale.set_hexpand(True)
                scale.set_value_pos(Gtk.PositionType.BOTTOM)
                scale.set_digits(0)

                if hcount == 3:
                    scale.set_range(0, 999)
                else:
                    scale.set_range(0, 99)

                scale.set_increments(1, 10)
                scale.connect("value-changed", self.on_ticket_changed)
                scale.connect("format-value", self.format_ticket_amount)
                frame.grid.attach(scale, hcount, vcount, 1, 1)
                self.tickets[vcount - 1].append(scale)

        buttonbox = uigtk.widgets.ButtonBox()
        buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
        self.attach(buttonbox, 0, 1, 4, 1)

        buttonAssistant = uigtk.widgets.Button("Assistant")
        buttonAssistant.set_tooltip_text("Have assistant manager reset to recommended ticket price.")
        buttonAssistant.connect("clicked", self.on_assistant_clicked)
        buttonbox.add(buttonAssistant)

        self.season_tickets = SeasonTickets()
        self.attach(self.season_tickets, 0, 2, 1, 1)

        self.school_tickets = SchoolTickets()
        self.attach(self.school_tickets, 0, 3, 1, 1)

    def on_assistant_clicked(self, *args):
        '''
        Set ticket prices to those recommended by assistant manager.
        '''
        Tickets.club.tickets.set_initial_prices()

        self.populate_data()

    def on_ticket_changed(self, scale):
        '''
        Update data model when cost of ticket is changed.
        '''
        self.club.tickets.tickets.set_ticket_price(scale.index[0],
                                                   scale.index[1],
                                                   scale.get_value())

    def format_ticket_amount(self, scale, value):
        '''
        Format ticket value for display on scale.
        '''
        return data.currency.get_currency(value, integer=True)

    def update_interface(self):
        '''
        Update whether ticket item interface elements are sensitive.
        '''
        for stand in self.tickets[0]:
            stand.set_sensitive(self.club.stadium.get_standing_uncovered())

        for stand in self.tickets[1]:
            stand.set_sensitive(self.club.stadium.get_standing_covered())

        for stand in self.tickets[2]:
            stand.set_sensitive(self.club.stadium.get_seating_uncovered())

        for stand in self.tickets[3]:
            stand.set_sensitive(self.club.stadium.get_seating_covered())

        for stand in self.tickets[4]:
            stand.set_sensitive(self.club.stadium.get_executive_box())

    def populate_data(self):
        for count, category in enumerate(self.club.tickets.get_ticket_prices()):
            self.tickets[count][0].set_value(category.prices[0])
            self.tickets[count][1].set_value(category.prices[1])
            self.tickets[count][2].set_value(category.prices[2])

    def run(self):
        Tickets.club = data.clubs.get_club_by_id(data.user.team)

        self.update_interface()

        self.show_all()

        self.populate_data()
        self.season_tickets.populate_data()
        self.school_tickets.populate_data()


class SeasonTickets(uigtk.widgets.CommonFrame):
    def __init__(self):
        uigtk.widgets.CommonFrame.__init__(self, "Season Tickets")

        label = uigtk.widgets.Label("Capacity _Percentage Allocated For Season Tickets")
        self.grid.attach(label, 0, 0, 1, 1)

        self.spinbuttonSeasonTickets = Gtk.SpinButton.new_with_range(0, 100, 1)
        self.spinbuttonSeasonTickets.set_numeric(False)
        self.spinbuttonSeasonTickets.set_tooltip_text("Specify the percentage of season tickets available.")
        self.spinbuttonSeasonTickets.connect("output", self.format_ticket_output)
        self.spinbuttonSeasonTickets.connect("value-changed", self.on_season_tickets_changed)
        label.set_mnemonic_widget(self.spinbuttonSeasonTickets)
        self.grid.attach(self.spinbuttonSeasonTickets, 1, 0, 1, 1)

        self.labelStatus = uigtk.widgets.Label("Season tickets are not currently on sale.", leftalign=True)
        self.grid.attach(self.labelStatus, 0, 1, 2, 1)

    def on_season_tickets_changed(self, spinbutton):
        '''
        Store season ticket value when changed.
        '''
        Tickets.club.tickets.season_tickets = spinbutton.get_value_as_int()

    def format_ticket_output(self, spinbutton):
        '''
        Format percentage sign into season ticket spinbutton output.
        '''
        spinbutton.set_text("%i%%" % (spinbutton.get_value_as_int()))

        return True

    def populate_data(self):
        self.spinbuttonSeasonTickets.set_value(Tickets.club.tickets.season_tickets)

        if not Tickets.club.tickets.season_tickets_available:
            self.spinbuttonSeasonTickets.set_sensitive(False)
            self.labelStatus.set_visible(True)
        else:
            self.labelStatus.set_visible(False)


class SchoolTickets(uigtk.widgets.CommonFrame):
    def __init__(self):
        uigtk.widgets.CommonFrame.__init__(self, "School Tickets")

        label = uigtk.widgets.Label("Capacity Allocated For _Free School Ticket Programme")
        self.grid.attach(label, 0, 0, 1, 1)

        self.spinbuttonSchoolTickets = Gtk.SpinButton.new_with_range(0, 74000, 100)
        self.spinbuttonSchoolTickets.set_increments(100, 1000)
        self.spinbuttonSchoolTickets.set_snap_to_ticks(True)
        self.spinbuttonSchoolTickets.set_numeric(True)
        self.spinbuttonSchoolTickets.set_tooltip_text("Specify in 100 blocks the number of free school tickets.")
        self.spinbuttonSchoolTickets.connect("value-changed", self.on_school_tickets_changed)
        label.set_mnemonic_widget(self.spinbuttonSchoolTickets)
        self.grid.attach(self.spinbuttonSchoolTickets, 1, 0, 1, 1)

    def on_school_tickets_changed(self, spinbutton):
        '''
        Store school tickets value when changed.
        '''
        Tickets.club.tickets.school_tickets = spinbutton.get_value_as_int()

    def populate_data(self):
        self.spinbuttonSchoolTickets.set_value(Tickets.club.tickets.school_tickets)
